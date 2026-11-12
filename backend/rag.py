from backend.config import TOP_K
from backend.llm import generate_answer
from backend.vector_store import search

def answer_question(question: str):
    results = search(question, top_k=TOP_K)

    context_parts = []
    sources = []

    for item in results:
        context_parts.append(
            f"Source: {item['source']}\n{item['text']}"
        )
        sources.append(item["source"])

    context = "\n\n---\n\n".join(context_parts)

    answer = generate_answer(question, context)

    return {
        "answer": answer,
        "sources": list(dict.fromkeys(sources)),
    }
