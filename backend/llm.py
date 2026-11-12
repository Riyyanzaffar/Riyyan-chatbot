from groq import Groq
from backend.config import GROQ_API_KEY, GROQ_MODEL

SYSTEM_PROMPT = """
You are a helpful RAG assistant.

Answer the user's question using the supplied context whenever possible.
Do not invent facts that are not supported by the context.
If the answer is not available in the knowledge base, clearly say that
the information is not available in the provided knowledge base.

Keep answers clear, useful, and concise.
"""

def generate_answer(question: str, context: str) -> str:
    if not GROQ_API_KEY:
        raise RuntimeError(
            "GROQ_API_KEY is missing. Add it to the backend .env file."
        )

    client = Groq(api_key=GROQ_API_KEY)

    user_prompt = f"""
Context:
{context}

User question:
{question}

Answer based on the context above.
"""

    response = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()
