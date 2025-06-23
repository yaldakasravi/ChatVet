import os
import fitz  # PyMuPDF
import pandas as pd
from typing import List
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS
import re

def clean_text(text: str) -> str:
    """
    Basic text cleaning: remove extra spaces, newlines, special chars.
    """
    text = text.replace('\n', ' ').replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)  # collapse multiple spaces
    text = text.strip()
    return text

def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract all text from a PDF file using PyMuPDF.
    """
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            page_text = page.get_text()
            text += page_text + "\n"
    return clean_text(text)

def load_csv_symptom_data(csv_path: str, text_columns: List[str] = None) -> List[str]:
    """
    Load and concatenate relevant text columns from CSV.
    Args:
        csv_path: Path to CSV file.
        text_columns: List of columns with text to extract. If None, uses all string columns.
    Returns:
        List of cleaned text entries (rows combined).
    """
    df = pd.read_csv(csv_path)
    if text_columns is None:
        # Use all string/object dtype columns
        text_columns = df.select_dtypes(include=["object"]).columns.tolist()

    texts = []
    for _, row in df.iterrows():
        combined = " ".join(str(row[col]) for col in text_columns if pd.notna(row[col]))
        cleaned = clean_text(combined)
        if cleaned:
            texts.append(cleaned)
    return texts

def chunk_text(text: str, max_chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """
    Split long text into smaller chunks with optional overlap.

    Args:
        text: Text to split.
        max_chunk_size: Maximum tokens/words per chunk.
        overlap: Number of tokens/words to overlap between chunks.

    Returns:
        List of text chunks.
    """
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + max_chunk_size
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words)
        chunks.append(chunk_text)
        start = end - overlap  # overlap for context continuity
        if start < 0:
            start = 0
    return chunks

def preprocess_pdf_folder(pdf_folder_path: str, max_chunk_size=500, overlap=50) -> List[str]:
    """
    Process all PDFs in a folder into cleaned, chunked text.

    Args:
        pdf_folder_path: Path to folder with PDFs.
        max_chunk_size: Chunk size in words.
        overlap: Overlap in words.

    Returns:
        List of text chunks from all PDFs.
    """
    all_chunks = []
    for filename in os.listdir(pdf_folder_path):
        if filename.lower().endswith(".pdf"):
            path = os.path.join(pdf_folder_path, filename)
            print(f"Processing PDF: {filename}")
            full_text = extract_text_from_pdf(path)
            chunks = chunk_text(full_text, max_chunk_size, overlap)
            all_chunks.extend(chunks)
    return all_chunks

def preprocess_csv_file(csv_path: str, max_chunk_size=500, overlap=50, text_columns=None) -> List[str]:
    """
    Process CSV symptom data into cleaned, chunked text.

    Args:
        csv_path: Path to CSV file.
        max_chunk_size: Chunk size in words.
        overlap: Overlap in words.
        text_columns: List of columns with text to extract.

    Returns:
        List of text chunks from CSV.
    """
    texts = load_csv_symptom_data(csv_path, text_columns)
    all_chunks = []
    for text in texts:
        chunks = chunk_text(text, max_chunk_size, overlap)
        all_chunks.extend(chunks)
    return all_chunks

if __name__ == "__main__":
    # Example usage
    pdf_folder = "data/pdf_guides"
    csv_file = "data/vet_guides.csv"

    pdf_chunks = preprocess_pdf_folder(pdf_folder)
    print(f"Extracted {len(pdf_chunks)} chunks from PDFs.")

    csv_chunks = preprocess_csv_file(csv_file)
    print(f"Extracted {len(csv_chunks)} chunks from CSV.")

    # Now, pdf_chunks + csv_chunks can be embedded and uploaded to Pinecone
