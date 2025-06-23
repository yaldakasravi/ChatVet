# embeddings/embed.py

import os
from dotenv import load_dotenv
from openai import OpenAIError
from openai.embeddings_utils import get_embedding
from preprocessing import preprocess_pdf_folder, preprocess_csv_file
from pinecone_utils import upsert_embeddings
import time

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-ada-002"

if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

def generate_embeddings_from_texts(texts, model=EMBEDDING_MODEL, max_retries=3):
    """
    Generate OpenAI embeddings for a list of texts.

    Args:
        texts: List of strings to embed.
        model: Embedding model name.
        max_retries: How many times to retry on failure.

    Returns:
        List of embeddings.
    """
    embeddings = []
    for i, text in enumerate(texts):
        attempt = 0
        success = False
        while attempt < max_retries and not success:
            try:
                embedding = get_embedding(text, engine=model)
                embeddings.append(embedding)
                success = True
                time.sleep(0.5)  # Rate limit safety
            except OpenAIError as e:
                attempt += 1
                print(f"[Retry {attempt}] Failed to embed text {i}: {e}")
                time.sleep(1)
        if not success:
            raise Exception(f"Failed to embed text after {max_retries} attempts.")
    return embeddings

def run_embedding_pipeline():
    """
    Full pipeline:
    1. Preprocess PDFs + CSVs
    2. Generate embeddings
    3. Upload to Pinecone
    """
    print("Step 1: Preprocessing data...")
    pdf_chunks = preprocess_pdf_folder("data/pdf_guides")
    csv_chunks = preprocess_csv_file("data/vet_guides.csv")

    all_chunks = pdf_chunks + csv_chunks
    print(f"Total chunks: {len(all_chunks)}")

    print("Step 2: Generating OpenAI embeddings...")
    embeddings = generate_embeddings_from_texts(all_chunks)

    print("Step 3: Uploading embeddings to Pinecone...")
    upsert_embeddings(embeddings, all_chunks)

    print("✅ Embedding pipeline completed.")

if __name__ == "__main__":
    run_embedding_pipeline()
