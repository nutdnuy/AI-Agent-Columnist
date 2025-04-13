from langchain_openai import ChatOpenAI
# from langchain_fireworks import ChatFireworks  # Uncomment if needed
#from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.chat_models import ChatOllama



class LLMSelector:
    def __init__(self, fast_model_name: str, long_context_model_name: str):
        self.fast_llm = self._create_llm(fast_model_name)
        self.long_context_llm = self._create_llm(long_context_model_name)

    def _detect_provider(self, model_name: str) -> str:
        """Simple heuristic to guess provider from model name"""
        model_name = model_name.lower()
        if "gpt" in model_name:
            return "openai"
        elif "fireworks" in model_name:
            return "fireworks"
        elif "gemini" in model_name:
            return "gemini"
        elif "llama" in model_name or "mistral" in model_name:
            return "ollama"
        else:
            raise ValueError(f"Cannot detect provider from model name: {model_name}")

    def _create_llm(self, model_name: str):
        provider = self._detect_provider(model_name)
        if provider == "openai":
            return ChatOpenAI(model=model_name)
        elif provider == "fireworks":
            return ChatFireworks(model=model_name)
        elif provider == "gemini":
            return ChatGoogleGenerativeAI(model=model_name)
        elif provider == "ollama":
            return ChatOllama(model=model_name)
        else:
            raise ValueError(f"Unsupported provider: {provider}")

    def get_llms(self):
        return self.fast_llm, self.long_context_llm


# ---------------------------------------
# ✅ ตัวอย่างการใช้งาน (ใส่ชื่อโมเดลเข้าไป)
# ---------------------------------------
if __name__ == "__main__":
    # แค่ใส่ชื่อโมเดลเข้าไป
    selector = LLMSelector(
        fast_model_name="gpt-4o",
        long_context_model_name="gpt-4.5-preview-2025-02-27"
    )

    fast_llm, long_context_llm = selector.get_llms()

    # ทดลอง print ชื่อ class เพื่อดูว่าได้โมเดลอะไร
    print(f"Fast LLM: {type(fast_llm).__name__}")
    print(f"Long-context LLM: {type(long_context_llm).__name__}")
