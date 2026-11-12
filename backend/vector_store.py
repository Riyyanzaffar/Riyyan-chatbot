
import json
import numpy as np

from backend.config import VECTOR_DIR
from backend.embeddings import embed_texts, embed_query

INDEX_FILE = VECTOR_DIR / "index.json"


def build_index(chunks):
    if not chunks:
        raise ValueError("No document chunks found.")

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    texts = [item["text"] for item in chunks]
    embeddings = np.asarray(
        embed_texts(texts),
        dtype=np.float32
    )

    if embeddings.ndim != 2 or embeddings.shape[0] != len(chunks):
        raise ValueError("Invalid embedding dimensions.")

    payload = {
        "chunks": chunks,
        "embeddings": embeddings.tolist(),
    }

    INDEX_FILE.write_text(
        json.dumps(payload, ensure_ascii=False),
        encoding="utf-8"
    )


def index_exists():
    return INDEX_FILE.exists()


def search(query: str, top_k: int = 4):
    if not index_exists():
        raise RuntimeError(
            "Vector index not found. Run: python ingest.py"
        )

    data = json.loads(
        INDEX_FILE.read_text(encoding="utf-8")
    )

    chunks = data["chunks"]
    embeddings = np.asarray(
        data["embeddings"],
        dtype=np.float32
    )

    query_embedding = np.asarray(
        embed_query(query),
        dtype=np.float32
    ).reshape(-1)

    if embeddings.ndim != 2:
        raise ValueError("Stored embeddings have an invalid shape.")

    if embeddings.shape[1] != query_embedding.shape[0]:
        raise ValueError(
            "Embedding dimensions do not match. Rebuild the index."
        )

    # Normalize document and query vectors for cosine similarity.
    document_norms = np.linalg.norm(
        embeddings, axis=1, keepdims=True
    )
    query_norm = np.linalg.norm(query_embedding)

    normalized_embeddings = embeddings / np.maximum(
        document_norms, 1e-12
    )
    normalized_query = query_embedding / max(
        float(query_norm), 1e-12
    )

    scores = normalized_embeddings @ normalized_query

    result_count = min(max(top_k, 0), len(chunks))
    best_indices = np.argsort(scores)[::-1][:result_count]

    results = []

    for idx in best_indices:
        item = chunks[int(idx)].copy()
        item["score"] = float(scores[idx])
        results.append(item)

    return results
