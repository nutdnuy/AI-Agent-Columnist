# Expand_Topics.py

from typing import List
from pydantic import BaseModel, Field

try:
    from Promt_Quant import Expand_Topics_Promt
except ImportError:
    Expand_Topics_Promt = (
        "System: Please expand the given topic into related subjects."
    )

try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    raise ImportError("Please install or provide `langchain_core.prompts`.")

# ===== Pydantic Model =====
class RelatedSubjects(BaseModel):
    topics: List[str] = Field(
        description=Expand_Topics_Promt,
    )

# ===== Prompt Template =====
gen_related_topics_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", Expand_Topics_Promt),
        ("user", "{topic}"),
    ]
)

# ===== Build Chain Function =====
def build_expand_chain(fast_llm):
    """
    สร้าง LangChain ที่พร้อม structured output สำหรับ RelatedSubjects
    """
    return gen_related_topics_prompt | fast_llm.with_structured_output(RelatedSubjects)


# ===== Main async function =====
async def expand_topics(_input: str, fast_llm):
    """
    :param _input: หัวข้อ (topic) ที่ต้องการขยาย
    :param fast_llm: instance ของ LLM ที่รองรับ structured_output + ainvoke()
    :return: Tuple of (related_subjects, expand_chain)
    """
    expand_chain = build_expand_chain(fast_llm)
    related_subjects = await expand_chain.ainvoke({"topic": _input})
    return related_subjects, expand_chain

# ===== For standalone test =====
if __name__ == "__main__":
    import asyncio

    class MockLLM:
        def with_structured_output(self, schema):
            self.schema = schema
            return self
        async def ainvoke(self, prompt):
            return RelatedSubjects(topics=["AI Ethics", "Deep Learning", "ML in Education"])

    async def test():
        _input = "Generative AI in Education"
        mock_llm = MockLLM()
        related_subjects, expand_chain = await expand_topics(_input, mock_llm)

        print("=== Related Subjects ===")
        print(related_subjects.model_dump())
        print("\n=== Chain Object ===")
        print(expand_chain)

    asyncio.run(test())

