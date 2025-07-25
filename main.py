from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from langchain.output_parsers import PydanticOutputParser
from tools import search_tool

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define output format
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

# Parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)
format_instructions = parser.get_format_instructions()

# 🔁 Get input from user FIRST
query = input("🔎 What can I help you research? ")

# Create dynamic prompt
prompt = f"""
You are a research assistant that helps write research papers.
Wrap the output in the following format and provide no other text:
{format_instructions}

Research Topic: {query}
"""

# Call Gemini
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Output
raw_output = response.text

try:
    structured_response = parser.parse(raw_output)
    print("✅ Structured Response:\n", structured_response)
except Exception as e:
    print("❌ Error parsing response:", e, "\nRaw response:\n", raw_output)
