from anthropic import BaseModel
from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent

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

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use neccessary tools. 
            Wrap the output in this format and provide no other text\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())


# Make a call
response = model.generate_content("What is the meaning of life?")
print(response.text)
