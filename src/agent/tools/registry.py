from __future__ import annotations

from agent.tools.base import Tool


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, tool: Tool) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")
        self._tools[tool.name] = tool

    def get(self, name: str) -> Tool | None:
        return self._tools.get(name)

    def descriptions(self) -> list[dict[str, object]]:
        return [{"name": tool.name, "description": tool.description, "input_schema": tool.schema()} for tool in self._tools.values()]

