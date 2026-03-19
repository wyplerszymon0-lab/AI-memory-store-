import os
from openai import OpenAI
from memory_store import MemoryStore

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])


def build_context(memories, query):
    if not memories:
        return ""
    lines = ["Relevant memories from past conversations:"]
    for m in memories:
        lines.append(f"- [{m.role}] {m.content}")
    return "\n".join(lines)


def chat(store: MemoryStore, session_id: str, user_message: str) -> str:
    memories = store.search(user_message, limit=4)
    context = build_context(memories, user_message)

    system_prompt = "You are a helpful assistant with memory of past conversations."
    if context:
        system_prompt += f"\n\n{context}"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message},
        ],
        max_tokens=500,
    )

    reply = response.choices[0].message.content

    store.add(user_message, "user", session_id)
    store.add(reply, "assistant", session_id)

    return reply


if __name__ == "__main__":
    import uuid

    session_id = str(uuid.uuid4())
    store = MemoryStore(path="data/memories.json")

    print("AI Memory Chat — type 'exit' to quit, 'history' to see session memories\n")

    while True:
        user_input = input("You: ").strip()
        if not user_input:
            continue
        if user_input == "exit":
            break
        if user_input == "history":
            for m in store.get_session(session_id):
                print(f"  [{m.role}] {m.content}")
            continue

        reply = chat(store, session_id, user_input)
        print(f"AI:  {reply}\n")
