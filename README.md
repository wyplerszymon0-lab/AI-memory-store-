# ai-memory-store

A persistent memory layer for AI agents. Stores conversation history across sessions, supports keyword search and tag-based retrieval — giving your agent long-term memory without a vector database.

## How It Works
```
User message
     ↓
Search relevant memories
     ↓
Inject into system prompt
     ↓
OpenAI API call
     ↓
Save user + assistant turn to memory
```

## Features

- Persistent JSON storage — memories survive restarts
- Keyword search with relevance scoring
- Tag-based memory organization
- Session isolation — retrieve only relevant context
- No external vector DB required

## Run
```bash
pip install -r requirements.txt
export OPENAI_API_KEY=your_key
python agent.py
```

## Test
```bash
pytest tests/ -v
```

## Project Structure
```
ai-memory-store/
├── memory_store.py       # Core MemoryStore class
├── agent.py              # Chat agent using memory
├── requirements.txt
├── README.md
└── tests/
    └── test_memory_store.py
```

## Author

**Szymon Wypler** — [@wyplerszymon0-lab](https://github.com/wyplerszymon0-lab)

## License

MIT
