# Ready RAG Chatbot

A simple, deployable RAG chatbot with:

- Streamlit frontend
- Backend RAG pipeline
- TXT / Markdown / PDF ingestion
- Local embeddings using `all-MiniLM-L6-v2`
- Local JSON vector index
- Groq LLM API
- API key kept in backend `.env`
- No data-entry UI
- Chat-only frontend

## 1. Open in VS Code

Open this folder in VS Code.

## 2. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

## 3. Install packages

```powershell
pip install -r requirements.txt
```

## 4. Add your API key

Copy:

```text
.env.example
```

to:

```text
.env
```

Then put your Groq API key in:

```text
GROQ_API_KEY=your_key_here
```

The API key is not placed in the frontend code.

## 5. Add your data

Put your knowledge files inside:

```text
backend/data/
```

Supported:

- `.txt`
- `.md`
- `.pdf`

You can remove the example `knowledge.txt` and add your own files.

## 6. Build the RAG index

Run:

```powershell
python ingest.py
```

You should see:

```text
Done. Vector index created successfully.
```

## 7. Run the chatbot

```powershell
streamlit run app.py
```

The browser will open the chatbot.

## 8. When you change the data

Run again:

```powershell
python ingest.py
```

This rebuilds the vector index.

## Project structure

```text
rag_chatbot_ready/
│
├── app.py
├── ingest.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
└── backend/
    ├── __init__.py
    ├── config.py
    ├── loader.py
    ├── chunker.py
    ├── embeddings.py
    ├── vector_store.py
    ├── llm.py
    ├── rag.py
    │
    └── data/
        └── knowledge.txt
```

## Deployment

For Streamlit deployment, add your API key through the deployment platform's secret/environment-variable settings rather than committing `.env`.

The vector index can be generated during deployment or included as part of your deployment workflow.

## Important

Do not upload `.env` or expose your API key in frontend code or GitHub.
