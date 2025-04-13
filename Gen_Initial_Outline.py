# Gen_Initial_Outline.py

from typing import List, Optional
from pydantic import BaseModel, Field


try:
    from Promt import Generate_Initial_Outline as Promtp_Generate_Initial_Outline
except ImportError:
    # fallback ถ้าไม่เจอ
    from  Promt_Quant import  *
    Promtp_Generate_Initial_Outline = "System Prompt: Please define how to generate an initial outline."


# dict ที่เก็บ title สำหรับ Field (ตัวอย่าง)
try:
    from config_outline import Outline_promt
except ImportError:
    # fallback
    Outline_promt = {
        "Section": "Description of the section",
        "page_title": "Title of the page"
    }

# ถ้าในโปรเจกต์คุณใช้ langchain_core.prompts
try:
    from langchain_core.prompts import ChatPromptTemplate
except ImportError:
    raise ImportError("Please install or provide `langchain_core.prompts`.")


#
# === Prompt Template สำหรับสั่งโมเดล ===
#
direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", Promtp_Generate_Initial_Outline),
        ("user", "{topic}"),
    ]
)

#
# === Pydantic Models สำหรับโครงสร้าง Outline ===
#
class Subsection(BaseModel):
    subsection_title: str = Field(..., title="Title of the subsection")
    description: str = Field(..., title="Content of the subsection")

    @property
    def as_str(self) -> str:
        return f"### {self.subsection_title}\n\n{self.description}".strip()


class Section(BaseModel):
    section_title: str = Field(..., title="Title of the section")
    description: str = Field(..., title="Content of the section")
    subsections: Optional[List[Subsection]] = Field(
        default=None,
        title=Outline_promt["Section"],
    )

    @property
    def as_str(self) -> str:
        subs_text = "\n\n".join(
            subsection.as_str for subsection in (self.subsections or [])
        )
        return f"## {self.section_title}\n\n{self.description}\n\n{subs_text}".strip()


class Outline(BaseModel):
    page_title: str = Field(..., title=Outline_promt["page_title"])
    sections: List[Section] = Field(default_factory=list, title=Outline_promt["Section"])

    @property
    def as_str(self) -> str:
        all_sections = "\n\n".join(section.as_str for section in self.sections)
        return f"# {self.page_title}\n\n{all_sections}".strip()


#
# === Class รับ fast_llm และ long_context_llm จากภายนอก ===
#
class GenInitialOutline:
    """
    ใช้สร้าง initial outline โดยยืดหยุ่นให้เราระบุ fast_llm หรือ long_context_llm
    ผ่าน constructor ตามต้องการ
    """
    def __init__(self, fast_llm, long_context_llm):
        """
        :param fast_llm: LLM ที่ตอบเร็ว (เช่น GPT-4o)
        :param long_context_llm: LLM ที่รองรับ context ยาว (เช่น Fireworks หรือ gpt-4.5-preview)
        """
        self.fast_llm = fast_llm
        self.long_context_llm = long_context_llm

    def generate_outline(self, example_topic: str, use_long_context: bool = False) -> Outline:
        """
        :param example_topic: หัวข้อที่จะให้ LLM สร้าง outline
        :param use_long_context: True ถ้าต้องการใช้ long_context_llm,
                                 False ถ้าต้องการใช้ fast_llm
        :return: Pydantic model Outline
        """
        chosen_llm = self.long_context_llm if use_long_context else self.fast_llm
        
        # ต่อ prompt กับ structured output โดยใช้ LLM ที่เลือก
        pipeline = direct_gen_outline_prompt | chosen_llm.with_structured_output(Outline)
        
        # เรียก invoke เพื่อให้ LLM สร้าง Outline
        initial_outline = pipeline.invoke({"topic": example_topic})
        return initial_outline


#
# === ตัวอย่างการใช้งานแบบง่าย (เมื่อลองรันไฟล์นี้ตรง ๆ) ===
#
if __name__ == "__main__":
    # สมมติว่าเรานิยาม fast_llm / long_context_llm ไว้แล้ว
    # (ให้แก้เป็น LLM จริง ๆ ของคุณ)
    class MockLLM:
        def with_structured_output(self, _model):
            return self
        def invoke(self, _prompt):
            # จำลองการส่งกลับโครงสร้าง Outline แบบ placeholder
            return Outline(page_title="Demo Page", sections=[
                Section(
                    section_title="Mock Section",
                    description="This is a mock section for demonstration.",
                    subsections=[
                        Subsection(subsection_title="Mock Subsection",
                                   description="Just a mock subsection.")
                    ]
                )
            ])
    fast_llm = MockLLM()
    long_context_llm = MockLLM()

    # สร้าง generator
    gen = GenInitialOutline(fast_llm=fast_llm, long_context_llm=long_context_llm)

    # ตัวอย่างใช้งาน: ไม่ใช้ long context
    outline_fast = gen.generate_outline("Introduction to Quant Finance", use_long_context=False)
    print("\n=== Outline (fast_llm) ===")
    print(outline_fast.as_str)

    # ตัวอย่างใช้งาน: ใช้ long context
    outline_long = gen.generate_outline("Introduction to Quant Finance", use_long_context=True)
    print("\n=== Outline (long_context_llm) ===")
    print(outline_long.as_str)
