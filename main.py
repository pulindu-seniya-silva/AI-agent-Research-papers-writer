from dotenv import load_dotenv
import os
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from langchain.agents import create_tool_calling_agent, AgentExecutor
from pydantic import BaseModel
from typing import List

# Load API key from .env file
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# Configure Gemini with API key
genai.configure(api_key=api_key)

# Define the output format
class ResearchResponse(BaseModel):
    topic: str
    summary: str
    sources: List[str]
    tools_used: List[str]

# Use Gemini model
llm = genai.GenerativeModel("gemini-1.5-flash")

# LangChain output parser
parser = PydanticOutputParser(pydantic_object=ResearchResponse)

# Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            You are a research assistant that will help generate a research paper.
            Answer the user query and use necessary tools. 
            Wrap the output in this format and provide no other text:\n{format_instructions}
            """,
        ),
        ("placeholder", "{chat_history}"),
        ("human", "{query}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
).partial(format_instructions=parser.get_format_instructions())

# Build the agent
agent = create_tool_calling_agent(
    llm=llm,
    prompt=prompt,
    tools=[],
)

# Create executor
agent_executor = AgentExecutor(agent=agent, tools=[], verbose=True)

# Run the agent
response = agent_executor.invoke({
    "query": "What is the meaning of life?"
})

# Print final response
print("Response:", response)
