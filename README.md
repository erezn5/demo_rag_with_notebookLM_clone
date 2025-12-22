# 2) Create venv
python3 -m venv venv --p=3.11

# 3) activate the venv
source venv/bin/activate

# 4) install requirements into the virtual environment
pip install -r requirements.txt

# 5) How to run the tests
pytest [name_of_the_test]

# NotebookLM-style RAG System

## Overview
A document-grounded question answering system inspired by Google NotebookLM.
Users upload documents into isolated notebooks and ask questions that are answered
strictly based on retrieved source content.

## Key Features
- Retrieval-Augmented Generation (RAG)
- Per-notebook document isolation
- Source-cited answers
- Clean FastAPI backend
- Minimal Streamlit UI for demo

## Architecture
- Ingestion: PDF/TXT loaders + chunking
- Storage: Vector database (per notebook)
- Retrieval: Similarity search (top-K)
- Generation: LLM answers grounded in retrieved chunks
- API: FastAPI
- UI: Streamlit

## Tech Stack
- Python 3.11
- FastAPI
- LangChain
- OpenAI (LLM + embeddings)
- Chroma (vector store)
- Streamlit

## Why RAG (and not fine-tuning)
- No model retraining
- Dynamic document updates
- Lower cost
- Stronger grounding and explainability

## Known Limitations
- PDF text extraction quality depends on source files
- No authentication (demo-focused)
- Basic ranking strategy

## Future Improvements
- Better PDF normalization / OCR
- Answer modes (summarize, compare)
- Auth + multi-user support