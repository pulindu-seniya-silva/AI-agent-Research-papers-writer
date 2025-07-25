from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import List

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

# Create prompt
format_instructions = """
Respond in JSON with the following format:
{
  "topic": "...",
  "summary": "...",
  "sources": ["...", "..."],
  "tools_used": ["..."]
}
"""

prompt = f"""
You are a research assistant that helps write research papers.
Wrap the output in the following format and provide no other text:
{format_instructions}

What is the meaning of life?
"""

model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

print("Response:\n", response.text)