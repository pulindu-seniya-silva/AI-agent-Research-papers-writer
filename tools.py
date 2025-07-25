from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool

# Search tool
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for information"
)

# Wikipedia tool
wiki = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
wiki_tool = Tool(
    name="wikipedia",
    func=wiki.run,
    description="Fetch information from Wikipedia"
)
