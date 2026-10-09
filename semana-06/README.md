#!/usr/bin/env python3
"""
RAG System for Banking and Finance Documents

The RAG_system.py script implements a complete Retrieval Augmented Generation (RAG) system:
1. Loads PDF documents from a local folder
2. Extracts and chunks text with overlap for context preservation
3. Generates embeddings using sentence transformers
4. Stores embeddings in a Chroma vector database with DuckDB persistence
5. Performs semantic search returning top-k most relevant fragments

Requirements:
    pip3 install pypdf chromadb sentence-transformers

Usage:
    python3 rag_system.py
"""
