from backend.config import CHUNK_SIZE, CHUNK_OVERLAP

def chunk_text(text: str):
    text = " ".join(text.split())

    if len(text) <= CHUNK_SIZE:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = min(start + CHUNK_SIZE, len(text))
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = max(0, end - CHUNK_OVERLAP)

    return chunks

def chunk_documents(documents):
    output = []

    for doc in documents:
        for chunk in chunk_text(doc["text"]):
            output.append({
                "text": chunk,
                "source": doc["source"],
            })

    return output
