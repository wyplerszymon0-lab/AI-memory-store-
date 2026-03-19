import json
import os
import time
import uuid
from dataclasses import dataclass, field, asdict
from pathlib import Path


@dataclass
class Memory:
    id: str
    content: str
    role: str
    tags: list[str]
    created_at: float
    session_id: str


@dataclass
class MemoryStore:
    path: Path
    _memories: list[Memory] = field(default_factory=list)

    def __post_init__(self):
        self.path = Path(self.path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if self.path.exists():
            self._load()

    def add(self, content: str, role: str, session_id: str, tags: list[str] | None = None) -> Memory:
        memory = Memory(
            id=str(uuid.uuid4()),
            content=content,
            role=role,
            tags=tags or [],
            created_at=time.time(),
            session_id=session_id,
        )
        self._memories.append(memory)
        self._save()
        return memory

    def search(self, query: str, limit: int = 5) -> list[Memory]:
        query_lower = query.lower()
        scored = []
        for memory in self._memories:
            score = 0
            for word in query_lower.split():
                if word in memory.content.lower():
                    score += 1
                if any(word in tag.lower() for tag in memory.tags):
                    score += 2
            if score > 0:
                scored.append((score, memory))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored[:limit]]

    def get_session(self, session_id: str) -> list[Memory]:
        return [m for m in self._memories if m.session_id == session_id]

    def get_by_tag(self, tag: str) -> list[Memory]:
        return [m for m in self._memories if tag in m.tags]

    def delete(self, memory_id: str) -> bool:
        before = len(self._memories)
        self._memories = [m for m in self._memories if m.id != memory_id]
        if len(self._memories) < before:
            self._save()
            return True
        return False

    def clear_session(self, session_id: str) -> int:
        before = len(self._memories)
        self._memories = [m for m in self._memories if m.session_id != session_id]
        removed = before - len(self._memories)
        if removed > 0:
            self._save()
        return removed

    def all(self) -> list[Memory]:
        return list(self._memories)

    def _save(self):
        data = [asdict(m) for m in self._memories]
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def _load(self):
        data = json.loads(self.path.read_text(encoding="utf-8"))
        self._memories = [Memory(**m) for m in data]
