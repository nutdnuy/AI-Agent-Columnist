# ==== Standard Library ====
from typing import List, Optional, Annotated
from typing_extensions import TypedDict
import json
import getpass
import os
from IPython.core.display import display, HTML

# ==== Third-party Libraries ====
from pydantic import BaseModel, Field, field_validator

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

# ==== LangChain OpenAI ====
from langchain_openai import OpenAIEmbeddings

# ==== LangGraph ====
from langgraph.graph import START, END, StateGraph
from langgraph.pregel import RetryPolicy

# ==== Local Modules ====
from Gen_Initial_Outline import *
from Expand_Topics import * 
from Gen_Perspectives import *
from Interview_State import InterviewState
from Dialog_Roles import *

from Setup import *

class Queries(BaseModel):
    queries: List[str] = Field(
        description="Comprehensive list of search engine queries to answer the user's questions.",
    )

    
class AnswerWithCitations(BaseModel):
    answer: str = Field(
        description="Comprehensive answer to the user's question with citations.",
    )
    cited_urls: List[str] = Field(
        description="List of urls cited in the answer.",
    )

    @property
    def as_str(self) -> str:
        return f"{self.answer}\n\nCitations:\n\n" + "\n".join(
            f"[{i+1}]: {url}" for i, url in enumerate(self.cited_urls)
        )

def route_messages(state: InterviewState, name: str = "Subject_Matter_Expert"):
    messages = state["messages"]
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )
    if num_responses >= max_num_turns:
        return END
    last_question = messages[-2]
    if last_question.content.endswith("Thank you so much for your help!"):
        return END
    return "ask_question"


class SubSection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    content: str = Field(
        ...,
        title="Full content of the subsection. Include [#] citations to the cited sources where relevant.",
    )

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.content}".strip()


class WikiSection(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    content: str = Field(..., title="Full content of the section")
    subsections: Optional[List[Subsection]] = Field(
        default=None,
        title="Titles and descriptions for each subsection of the Wikipedia page.",
    )
    citations: List[str] = Field(default_factory=list)

    @property
    def as_str(self) -> str:
        subsections = "\n\n".join(
            subsection.as_str for subsection in self.subsections or []
        )
        citations = "\n".join([f" [{i}] {cit}" for i, cit in enumerate(self.citations)])
        return (
            f"## {self.section_title}\n\n{self.content}\n\n{subsections}".strip()
            + f"\n\n{citations}".strip()
        )




