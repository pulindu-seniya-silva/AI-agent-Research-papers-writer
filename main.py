from anthropic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPrompttemplate
from langchain_core.output_parsers import PydanticOutputParser


# Load API key from .env
load_dotenv()

class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: list[str]
    tools_used: list[str]

api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini
genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Make a call
response = model.generate_content("What is the meaning of life?")
print(response.text)
