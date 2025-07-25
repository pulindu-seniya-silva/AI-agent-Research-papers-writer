from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from langchain.output_parsers import PydanticOutputParser
from tools import search_tool, wiki_tool

# Load environment variable
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define output structure
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

# Parser setup
parser = PydanticOutputParser(pydantic_object=ResearchResponse)
format_instructions = parser.get_format_instructions()

# User input
query = input("🔎 What can I help you research? ")

# Prompt
prompt = f"""
You are a research assistant that helps write research papers.
Wrap the output in the following format and provide no other text:
{format_instructions}

Research Topic: {query}
"""

# Call Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)
raw_output = response.text

# Parse output
try:
    structured_response = parser.parse(raw_output)
    print("✅ Structured Response:\n", structured_response)

    # Ask user if they want to save it
    save_input = input("💾 Do you want to save this to a file? (yes/no): ").strip().lower()
    if "yes" in save_input or "save" in save_input:
        def save_to_file(data: ResearchResponse):
            filename = f"{data.topic.replace(' ', '_')}_research.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(f"📘 Topic: {data.topic}\n\n")
                f.write(f"📄 Summary:\n{data.summary}\n\n")
                f.write(f"📚 Sources:\n" + "\n".join(data.sources) + "\n\n")
                f.write(f"🛠 Tools Used:\n" + ", ".join(data.tools_used))
            print(f"✅ Saved to file: {filename}")

        save_to_file(structured_response)

except Exception as e:
    print("❌ Error parsing response:", e)
    print("Raw output:\n", raw_output)
