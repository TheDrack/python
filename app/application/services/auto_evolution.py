import os
from typing import Dict, Optional
from app.application.services.capability_registry import CapabilityRegistry


ALLOWED_AUTO_EVOLUTION_CHAPTERS = [
    "CHAPTER_1_IMMEDIATE_FOUNDATION",
    "CHAPTER_2_FUNCTIONAL_SELF_AWARENESS",
    "CHAPTER_3_CONTEXTUAL_UNDERSTANDING",
    "CHAPTER_4_STRATEGIC_REASONING",
]


class AutoEvolutionService:
    def __init__(self):
        self.capabilities = CapabilityRegistry()

    def find_next_capability(self) -> Optional[Dict]:
        return self.capabilities.get_next_unfulfilled(
            allowed_chapters=ALLOWED_AUTO_EVOLUTION_CHAPTERS
        )

    def mark_capability_completed(
        self,
        capability_id: int,
        implementation_logic: str,
        requirements: list[str] | None = None
    ) -> bool:
        commit_hash = os.popen("git rev-parse HEAD").read().strip()
        return self.capabilities.mark_completed(
            capability_id=capability_id,
            implementation_logic=implementation_logic,
            requirements=requirements,
            commit_hash=commit_hash
        )