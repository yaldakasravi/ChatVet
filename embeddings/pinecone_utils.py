# embeddings/pinecone_utils.py

import os
import pinecone
from typing import List, Dict
from uuid import uuid4
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT")
PINECONE_INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")

# Ensure values exist
if not all([PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME]):
    raise ValueError("Missing one or more Pinecone environment variables.")

# Initialize Pinecone
pinecone.init(api_key=PINECONE_API_KEY, environment=PINECONE_ENVIRONMENT)


def get_index():
    """Return Pinecone index object"""
    if PINECONE_INDEX_NAME not in pinecone.list_indexes():
        raise ValueError(f"Pinecone index '{PINECONE_INDEX_NAME}' does not exist.")
    return pinecone.Index(PINECONE_INDEX_NAME)


def upsert_embeddings(embeddings: List[List[float]], texts: List[str], batch_size: int = 100):
    """
    Upsert embedded vectors and original text into Pinecone.

    Args:
        embeddings: List of embedding vectors.
        texts: List of original text chunks (same order as embeddings).
        batch_size: Upsert in chunks to avoid memory overload.
    """
    if len(embeddings) != len(texts):
        raise ValueError("Number of embeddings and texts must match.")

    index = get_index()

    items = []
    for i in range(len(embeddings)):
        item_id = str(uuid4())
        vector = embeddings[i]
        metadata = {"text": texts[i]}
        items.append((item_id, vector, metadata))

    # Upload in batches
    for i in
