"""
From these related subjects, we can select representative Wikipedia editors as
'subject matter experts' with distinct backgrounds and affiliations. These will help
distribute the search process to encourage a more well-rounded final report.
"""

from typing import List
from pydantic import BaseModel, Field, field_validator
from langchain_core.runnables import RunnableLambda
# import  model
'''
from Model import *
selector = LLMSelector(
        fast_model_name="gpt-4o",
        long_context_model_name="gpt-4.5-preview-2025-02-27"
    )

fast_llm, long_context_llm = selector.get_llms()
'''
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.retrievers import WikipediaRetriever



# ====== 1. PROMPT ======
try:
    from Promt_Quant import perspectives_prompt
except ImportError:
    perspectives_prompt = (
        "You are helping generate editorial perspectives for a topic. "
        "Given examples and a topic, return a list of editor personas."
    )


# ====== 2. MODEL STRUCTURE ======
class Editor(BaseModel):
    affiliation: str = Field(description="Primary affiliation of the editor.")
    name: str = Field(description="Name of the editor.", pattern=r"^[a-zA-Z0-9_-]{1,64}$")
    role: str = Field(description="Role of the editor in the context of the topic.")
    description: str = Field(description="Description of the editor's focus, concerns, and motives.")

    @field_validator("name", mode="before")
    def sanitize_name(cls, value: str) -> str:
        return value.replace(" ", "").replace(".", "")

    @property
    def persona(self) -> str:
        return (
            f"Name: {self.name}\nRole: {self.role}\n"
            f"Affiliation: {self.affiliation}\nDescription: {self.description}\n"
        )


class Perspectives(BaseModel):
    editors: List[Editor] = Field(
        description="Comprehensive list of editors with their roles and affiliations."
    )
'''
gen_perspectives_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", perspectives_prompt),
            ("user", "Topic of interest: {topic}"),
        ]
    )

gen_perspectives_chain = gen_perspectives_prompt | fast_llm.with_structured_output(
    Perspectives, method="function_calling"
)
'''
# ====== 3. BUILD CHAIN ======
def build_gen_perspectives_chain(fast_llm):
    gen_perspectives_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", perspectives_prompt),
            ("user", "Topic of interest: {topic}"),
        ]
    )
    return gen_perspectives_prompt | fast_llm.with_structured_output(
        Perspectives, method="function_calling"
    )


# ====== 4. FORMATTER ======
def format_doc(doc, max_length=1000):
    related = "- ".join(doc.metadata.get("categories", []))
    return f"### {doc.metadata.get('title')}\n\nSummary: {doc.page_content}\n\nRelated\n{related}"[:max_length]


def format_docs(docs):
    return "\n\n".join(format_doc(doc) for doc in docs)


# ====== 5. MAIN CLASS ======

class GenPerspectives:
    def __init__(self, fast_llm, expand_chain):
        self.fast_llm = fast_llm
        self.expand_chain = expand_chain
        self.wikipedia_retriever = WikipediaRetriever(load_all_available_meta=True, top_k_results=1)
        self.gen_perspectives_chain = build_gen_perspectives_chain(fast_llm)

    # ✅ เอา @as_runnable ออก
    async def survey_subjects(self, topic: str):
        related_subjects = await self.expand_chain.ainvoke({"topic": topic})

        retrieved_docs = await self.wikipedia_retriever.abatch(
            related_subjects.topics, return_exceptions=True
        )

        all_docs = []
        for docs in retrieved_docs:
            if isinstance(docs, BaseException):
                continue
            all_docs.extend(docs)

        formatted = format_docs(all_docs)
        perspectives = await self.gen_perspectives_chain.ainvoke(
            {"examples": formatted, "topic": topic}
        )

        return perspectives


# ====== 6. TEST CASE (สำหรับรันตรงไฟล์) ======
if __name__ == "__main__":
    import asyncio

    # Mock LLM
    class MockLLM:
        def with_structured_output(self, schema, method="function_calling"):
            return self
        async def ainvoke(self, data):
            return Perspectives(editors=[
                Editor(name="Alice", role="Economist", affiliation="MIT", description="Analyzes financial risk."),
                Editor(name="Bob", role="AI Researcher", affiliation="Google", description="Focuses on ethics in AI."),
            ])

    # Mock expand_chain
    class MockExpand:
        async def ainvoke(self, data):
            class Dummy:
                topics = ["Artificial Intelligence", "Machine Learning"]
            return Dummy()

    async def test():
        gen = GenPerspectives(fast_llm=MockLLM(), expand_chain=MockExpand())
        result = await gen.survey_subjects("AI in Finance")
        print(result.model_dump())

    asyncio.run(test())


