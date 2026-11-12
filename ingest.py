from backend.loader import load_documents
from backend.chunker import chunk_documents
from backend.vector_store import build_index
from backend.config import DATA_DIR

def main():
    print("Loading data...")
    documents = load_documents(DATA_DIR)

    if not documents:
        print("No .txt, .md, or .pdf files found in backend/data/")
        return

    print(f"Loaded {len(documents)} document sections.")

    chunks = chunk_documents(documents)
    print(f"Created {len(chunks)} chunks.")

    print("Creating embeddings and vector index...")
    build_index(chunks)

    print("Done. Vector index created successfully.")

if __name__ == "__main__":
    main()
