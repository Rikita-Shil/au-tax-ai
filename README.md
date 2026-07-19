# Australian Tax AI Assistant

An AI-powered assistant that answers Australian tax questions using Retrieval-Augmented Generation (RAG) over official ATO documentation.

## Features

- Google ADK Agent
- Gemini API
- Supabase pgvector
- Semantic search
- Grounded answers from ATO documents
- Retry handling for temporary API failures

## Tech Stack

- Python
- Google ADK
- Gemini
- Supabase
- pgvector
- PyMuPDF

## Architecture

User
↓
Google ADK Agent
↓
Search Tool
↓
Supabase Vector Search
↓
Relevant ATO Chunks
↓
Gemini
↓
Grounded Response
