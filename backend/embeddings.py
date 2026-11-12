from functools import lru_cache
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

@lru_cache(maxsize=1)
def get_embedding_model():
    return SentenceTransformer(MODEL_NAME)

def embed_texts(texts):
    model = get_embedding_model()
    return model.encode(texts, normalize_embeddings=True).tolist()

def embed_query(query):
    model = get_embedding_model()
    return model.encode([query], normalize_embeddings=True).tolist()[0]
