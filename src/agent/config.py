from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True, slots=True)
class Settings:
    workspace: Path = Path(".")
    max_steps: int = 8
    tool_timeout_seconds: float = 10.0
    llm_provider: str = "mock"
    llm_model: str = "deterministic"
    temperature: float = 0.0
    rag_project_path: Path | None = None

    def __post_init__(self) -> None:
        if self.max_steps < 1 or self.tool_timeout_seconds <= 0:
            raise ValueError("max_steps and tool_timeout_seconds must be positive")
        if self.llm_provider not in {"mock", "openai_compatible"}:
            raise ValueError("llm_provider must be mock or openai_compatible")

    @classmethod
    def from_env(cls, env_file: str | Path | None = None) -> "Settings":
        load_dotenv(env_file)
        rag_path = os.getenv("AGENT_RAG_PROJECT_PATH", "").strip()
        return cls(
            workspace=Path(os.getenv("AGENT_WORKSPACE", ".")).resolve(),
            max_steps=int(os.getenv("AGENT_MAX_STEPS", "8")),
            tool_timeout_seconds=float(os.getenv("AGENT_TOOL_TIMEOUT_SECONDS", "10")),
            llm_provider=os.getenv("AGENT_LLM_PROVIDER", "mock"),
            llm_model=os.getenv("AGENT_LLM_MODEL", "deterministic"),
            temperature=float(os.getenv("AGENT_TEMPERATURE", "0")),
            rag_project_path=Path(rag_path).resolve() if rag_path else None,
        )

