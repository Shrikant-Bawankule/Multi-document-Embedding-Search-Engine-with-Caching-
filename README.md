# Multi-Document Embedding Search Engine with Caching

A production-ready semantic search engine for text documents, built using **Sentence Transformers**, **FAISS**, **FastAPI**, and **Streamlit**. Implements efficient embedding generation, intelligent caching with SQLite, fast vector search, robust API, and ranking explanations.

***

## 🚀 Project Summary

This project fulfills the CodeAtRandom AI Engineer Intern assignment:

- Processes 200 text files (20 Newsgroups dataset)
- Cleans text and saves files with metadata and hash
- Generates and caches embeddings using `all-MiniLM-L6-v2` (sentence-transformers)
- Searches with FAISS or cosine similarity
- FastAPI retrieval API with result explanations
- (Bonus) Streamlit UI for interactive search

***

## 📂 Repository Structure

```
embedding-search-engine/
├── src/
│   ├── __init__.py
│   ├── preprocessor.py      # Data preprocessing, hashing
│   ├── cache_manager.py     # SQLite caching system
│   ├── embedder.py          # Embedding generation
│   ├── search_engine.py     # FAISS search + ranking
│   └── api.py               # FastAPI API server
├── app.py                   # Streamlit UI (bonus)
├── requirements.txt
├── .gitignore
├── README.md
└── data/
    └── docs/                # Cleaned docs + metadata (gitignored)
```

***

## 🛠️ Installation & Setup

**Prerequisites:**  
- Python 3.8+ (recommend using Conda/virtualenv)
- Git

**Steps:**

```bash
git clone https://github.com/Shrikant-Bawankule/Multi-document-Embedding-Search-Engine-with-Caching-
cd Multi-document-Embedding-Search-Engine-with-Caching-
pip install -r requirements.txt
```

***

## ⚙️ Usage

### 1. Preprocess & Clean Documents
```bash
python src/preprocessor.py
```

### 2. Generate Embeddings, Build Search Index & Test Search
```bash
python src/search_engine.py
```

### 3. Start FastAPI Server
```bash
uvicorn src.api:app --reload
```
Open http://localhost:8000/docs for API documentation.

### 4. Start Streamlit UI (optional bonus)
```bash
streamlit run app.py
```
Open `http://localhost:8501` in your browser.

***

## 🖥️ API Endpoints

### `POST /search`
Semantic search over your document index.
#### Example Request:
```json
{
  "query": "quantum physics book",
  "top_k": 5
}
```
#### Example Response:
```json
{
  "query": "quantum physics book",
  "results": [
    {
      "rank": 1,
      "doc_id": "doc_014",
      "score": 0.308,
      "preview": "Quantum theory is concerned with...",
      "category": "sci.space",
      "doc_length": 523,
      "explanation": {
        "matched_keywords": ["quantum", "physics"],
        "overlap_ratio": 0.4,
        "length_score": 1.0,
        "embedding_score": 0.308
      }
    }
  ],
  "processing_time_ms": 167.8,
  "total_documents": 200
}
```

### `GET /stats`
Get cache performance and index details.

***

## 🧠 How Caching Works

- Embeddings for each document are stored in a local SQLite database with a SHA-256 hash
- When the document’s hash matches, the embedding is loaded from cache (no recomputation)
- 100% cache hit rate after first run (all embeddings loaded instantly)

***

## 🧪 Ranking Explanation

Each result has:
- **Matched Keywords**: Intersection of query and document top words
- **Overlap Ratio**: How many query keywords matched (%)
- **Length Score**: Normalized for document length
- **Embedding Score**: FAISS similarity

***

## 🔬 Design Choices

- **Model:** `sentence-transformers/all-MiniLM-L6-v2` (fast, quality 384-dim embeddings)
- **Index:** FAISS `IndexFlatIP` (cosine similarity with normalized vectors)
- **Cache:** SQLite (ACID-compliant, zero external dependencies)
- **API:** FastAPI (type-safe, async server, auto docs)
- **UI:** Streamlit (bonus, interactive web search)
- **Dataset:** 20 Newsgroups via scikit-learn

***

## 📊 Performance Benchmarks

| Metric             | Value      |
|--------------------|------------|
| Documents          | 200        |
| Embedding Dim      | 384        |
| Cache Hit Rate     | 100%       |
| Typical Search     | ~160ms     |
| Index Size         | 200        |

***

## 📸 Demo

### Screenshots
- See `screenshots/` for example queries, performance, UI, and ranking explanations

### Demo Video (optional)
- [Link to demo video if created]

***

## 👤 Author

Shrikant Bawankule  
AI Engineer Intern Assignment – CodeAtRandom (OPC) Private Limited

***
