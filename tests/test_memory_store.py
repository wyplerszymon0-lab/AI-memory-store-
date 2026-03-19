import pytest
from pathlib import Path
from memory_store import MemoryStore


@pytest.fixture
def store(tmp_path):
    return MemoryStore(path=tmp_path / "test_memories.json")


def test_add_memory(store):
    m = store.add("My name is Szymon", "user", "session-1")
    assert m.content == "My name is Szymon"
    assert m.role == "user"
    assert m.session_id == "session-1"
    assert len(store.all()) == 1


def test_add_memory_with_tags(store):
    m = store.add("I like Python", "user", "session-1", tags=["python", "preference"])
    assert "python" in m.tags


def test_search_by_content(store):
    store.add("I love hiking", "user", "s1")
    store.add("Python is great", "user", "s1")
    results = store.search("hiking")
    assert len(results) == 1
    assert "hiking" in results[0].content


def test_search_by_tag(store):
    store.add("I like Go", "user", "s1", tags=["go", "programming"])
    results = store.search("go")
    assert any("Go" in m.content for m in results)


def test_search_returns_most_relevant_first(store):
    store.add("Python Python Python", "user", "s1")
    store.add("Python once", "user", "s1")
    results = store.search("Python")
    assert results[0].content == "Python Python Python"


def test_get_session_filters_correctly(store):
    store.add("Message A", "user", "session-a")
    store.add("Message B", "user", "session-b")
    results = store.get_session("session-a")
    assert len(results) == 1
    assert results[0].content == "Message A"


def test_get_by_tag(store):
    store.add("Important note", "user", "s1", tags=["important"])
    store.add("Other note", "user", "s1", tags=["misc"])
    results = store.get_by_tag("important")
    assert len(results) == 1
    assert results[0].content == "Important note"


def test_delete_memory(store):
    m = store.add("To delete", "user", "s1")
    result = store.delete(m.id)
    assert result is True
    assert len(store.all()) == 0


def test_delete_nonexistent_returns_false(store):
    result = store.delete("nonexistent-id")
    assert result is False


def test_clear_session(store):
    store.add("A", "user", "session-1")
    store.add("B", "user", "session-1")
    store.add("C", "user", "session-2")
    removed = store.clear_session("session-1")
    assert removed == 2
    assert len(store.all()) == 1


def test_persistence(tmp_path):
    path = tmp_path / "memories.json"
    store1 = MemoryStore(path=path)
    store1.add("Persisted memory", "user", "s1")

    store2 = MemoryStore(path=path)
    assert len(store2.all()) == 1
    assert store2.all()[0].content == "Persisted memory"


def test_search_empty_store_returns_empty(store):
    results = store.search("anything")
    assert results == []


def test_search_limit_respected(store):
    for i in range(10):
        store.add(f"memory {i}", "user", "s1")
    results = store.search("memory", limit=3)
    assert len(results) <= 3
```

---

**`requirements.txt`**
```
openai==1.30.0
pytest==8.2.0
