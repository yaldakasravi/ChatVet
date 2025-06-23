import os
import pinecone
from langchain.vectorstores import Pinecone
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv

load_dotenv()

def get_pinecone_retriever(top_k: int = 5):
    """
    Initialize Pinecone and return a LangChain retriever object.

    Args:
        top_k (int): Number of top documents to retrieve per query

    Returns:
        langchain.vectorstores.base.VectorStoreRetriever: Retriever for LangChain
    """

    # Load environment variables
    pinecone_api_key = os.getenv("PINECONE_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENVIRONMENT")
    pinecone_index_name = os.getenv("PINECONE_INDEX_NAME")
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not all([pinecone_api_key, pinecone_env, pinecone_index_name, openai_api_key]):
        raise ValueError("One or more environment variables for Pinecone/OpenAI are missing.")

    # Initialize Pinecone client
    pinecone.init(api_key=pinecone_api_key, environment=pinecone_env)

    # Connect to Pinecone index
    index = pinecone.Index(pinecone_index_name)

    # Create OpenAI embeddings instance
    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)

    # Create LangChain Pinecone vector store wrapper
    vectorstore = Pinecone(
        index=index,
        embedding_function=embeddings.embed_query,
        text_key="text",  # The metadata key where the original text is stored in Pinecone
    )

    # Return LangChain retriever interface (fetch top_k docs)
    retriever = vectorstore.as_retriever(search_type="similarity", search_kwargs={"k": top_k})

    return retriever
