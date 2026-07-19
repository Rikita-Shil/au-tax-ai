# 🇦🇺 Australian Tax AI Assistant

An AI-powered assistant that answers Australian Capital Gains Tax (CGT) questions using **Google ADK**, **Gemini**, **Supabase pgvector**, and **Retrieval-Augmented Generation (RAG)** over official Australian Taxation Office (ATO) documentation.

Instead of relying solely on an LLM's knowledge, the assistant retrieves relevant sections from official ATO guides and generates grounded responses with source references.

---

## 🚀 Features

- 🤖 Google ADK AI Agent
- 🔍 Semantic search using Supabase pgvector
- 📄 Retrieval-Augmented Generation (RAG)
- 🇦🇺 Answers based on official ATO documentation
- 📚 Grounded responses with source references
- ⚡ Gemini 2.5 Flash for answer generation
- 🐍 Built with Python

---

# Project Architecture

```
User Question
      │
      ▼
Google ADK Agent
      │
      ▼
Search Tool
      │
      ▼
Retrieval Service
      │
      ▼
Gemini Embeddings
      │
      ▼
Supabase pgvector
      │
      ▼
Relevant ATO Document Chunks
      │
      ▼
Gemini Answer Generation
      │
      ▼
Grounded Answer
```

---

# Installation

## 1. Clone the repository

```bash
git clone https://github.com/Rikita-Shil/au-tax-ai.git
cd au-tax-ai
```

---

## 2. Create a virtual environment

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create a `.env` file

Create a `.env` file in the project root and add your credentials.

```env
GEMINI_API_KEY=your_gemini_api_key

SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key

EMBEDDING_MODEL=gemini-embedding-001
EMBEDDING_DIMENSION=768
```

---

## 5. Run the application

Start the Google ADK web interface:

```bash
adk web
```

Then open the local URL shown in your terminal (typically `http://localhost:8000`) and start asking tax questions.

---

# Example Questions

The assistant is designed to answer Australian Capital Gains Tax (CGT) questions based on official ATO guidance.

### Shares

- Can I claim the 50% CGT discount?
- How long do I need to hold shares to qualify for the CGT discount?
- Do I pay tax when selling US shares?
- How is the cost base calculated?
- Can brokerage fees be included in the cost base?
- What happens if I sell shares at a loss?
- Can I offset capital losses against salary income?

### Property

- What is the main residence exemption?
- How does the six-year absence rule work?
- Do I pay CGT when selling an investment property?

### Foreign Investments

- How are foreign shares taxed?
- How do I convert foreign currency for CGT purposes?
- Are overseas capital gains taxable in Australia?

### General Tax Questions

- What records should I keep for CGT?
- How do capital losses work?
- When is a CGT event triggered?
- How do I calculate a capital gain?

---

# Technologies

- Python
- Google ADK
- Google Gemini
- Supabase
- PostgreSQL
- pgvector
- Retrieval-Augmented Generation (RAG)
- PyMuPDF

---

# Disclaimer

This project is intended for educational and demonstration purposes.

Responses are generated using official ATO documentation but should not be considered financial or legal advice. Always refer to the latest Australian Taxation Office (ATO) guidance or consult a qualified tax professional for advice specific to your circumstances.
