from pathlib import Path
from pypdf import PdfReader

SUPPORTED = {".txt", ".md", ".pdf"}

def load_documents(data_dir: Path):
    documents = []

    for path in sorted(data_dir.rglob("*")):
        if not path.is_file() or path.suffix.lower() not in SUPPORTED:
            continue

        if path.suffix.lower() == ".pdf":
            reader = PdfReader(str(path))
            for page_number, page in enumerate(reader.pages, start=1):
                text = page.extract_text() or ""
                if text.strip():
                    documents.append({
                        "text": text,
                        "source": f"{path.name} - page {page_number}",
                    })
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if text.strip():
                documents.append({
                    "text": text,
                    "source": path.name,
                })

    return documents
