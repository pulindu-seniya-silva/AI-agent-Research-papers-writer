from dotenv import load_dotenv
import os
import google.generativeai as genai
from pydantic import BaseModel
from typing import List
from langchain.output_parsers import PydanticOutputParser

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Define output format using Pydantic
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

# Set up parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Format instructions
format_instructions = parser.get_format_instructions()

# Create prompt
prompt = f"""
You are a research assistant that helps write research papers.
Wrap the output in the following format and provide no other text:
{format_instructions}

What is the meaning of life?
"""

# Call Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content(prompt)

# Get actual text response from Gemini
raw_output = response.text

# Try parsing the response
try:
    structured_response = parser.parse(raw_output)
    print("Structured Response:\n", structured_response)
except Exception as e:
    print("Error parsing response:", e, "\nRaw response:\n", raw_output)
