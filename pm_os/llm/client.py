from pm_os.config import settings
from pm_os.llm.demo_mode import demo_complete_json

class LLMClient:
    def complete_json(self, *, system: str, user: str, schema_name: str) -> dict:
        if settings.demo_mode:
            return demo_complete_json(system=system, user=user, schema_name=schema_name)
        raise RuntimeError("LLM not configured. Set DEMO_MODE=1 or implement provider.")

