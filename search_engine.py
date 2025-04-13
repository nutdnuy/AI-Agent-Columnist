# ==== LangChain Core ====
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnableLambda, RunnableConfig
from langchain_core.runnables import chain as as_runnable
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage, AnyMessage
from langchain_core.documents import Document
from langchain_core.tools import tool

# ==== LangChain Community ====
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.retrievers import WikipediaRetriever
from langchain_community.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import ArxivLoader
#from langchain_community.tools import TavilySearchResults



from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper


# DDG
search_engine = DuckDuckGoSearchAPIWrapper()

@tool
async def search_engine(query: str):
    """Search engine to the internet."""
    results = DuckDuckGoSearchAPIWrapper()._ddgs_text(query)
    return [{"content": r["body"], "url": r["href"]} for r in results]
'''

# Tavily is typically a better search engine, but your free queries are limited
search_engine = TavilySearchResults(max_results=4)
tavily_search =  TavilySearchResults(
    max_results=20,
    include_answer=True,
    include_raw_content=True,
    include_images=True,
    # search_depth="advanced",
    # include_domains = []
    # exclude_domains = []
)
@tool
async def search_engine(query: str):
    """Search engine to the internet."""
    results = tavily_search.invoke(query)
    return [{"content": r["content"], "url": r["url"]} for r in results]
'''