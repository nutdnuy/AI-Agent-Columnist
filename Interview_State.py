

#### Interview_State

# Interview_State.py

from typing import List, Optional, Dict, Any

from typing_extensions import TypedDict, Annotated

# สมมติว่า Editor อยู่ในไฟล์ Gen_Perspectives.py
# แก้ไขให้ตรงกับโปรเจกต์ของคุณ
try:
    from Gen_Perspectives import Editor
except ImportError:
    # ถ้าไม่เจอหรือไม่ตรง ให้กำหนด fallback หรือเอาออก
    # หรือคอมเมนต์โค้ดนี้ออกหากคุณมี Editor ที่อื่น
    class Editor:
        """
        Fallback stub for Editor. 
        Replace or remove if you have a real Editor model from pydantic or others.
        """
        pass

from langchain_core.messages import AnyMessage

# กรณีคุณใช้ langgraph สำหรับ StateGraph, START, END
try:
    from langgraph.graph import END, StateGraph, START
except ImportError:
    # ถ้าไม่ได้ใช้จริง ให้คอมเมนต์หรือเอาออก
    pass
# ========= Helper functions =========
#
def add_messages(left, right):
    if not isinstance(left, list):
        left = [left]
    if not isinstance(right, list):
        right = [right]
    return left + right


def update_references(references, new_references):
    if not references:
        references = {}
    references.update(new_references)
    return references


def update_editor(editor, new_editor):
    # Can only set at the outset
    if not editor:
        return new_editor
    return editor


#
# ========= InterviewState Definition =========
#
class InterviewState(TypedDict):
    """A TypedDict for storing interview-related state."""
    messages: Annotated[
        List[AnyMessage],
        add_messages
    ]
    references: Annotated[
        Optional[Dict[str, Any]],
        update_references
    ]
    editor: Annotated[
        Optional[Editor],
        update_editor
    ]





