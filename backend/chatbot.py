import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.schema import Document
from retriever import get_pinecone_retriever  # your retriever wrapper
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        # Initialize OpenAI Chat model
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")

        # ChatOpenAI supports GPT-4 or GPT-3.5-turbo
        self.llm = ChatOpenAI(
            model="gpt-4",  # or "gpt-3.5-turbo"
            temperature=0.2,
            openai_api_key=openai_api_key,
            max_tokens=1024,
            streaming=False,
        )

        # Initialize Retriever for Pinecone vector DB
        self.retriever = get_pinecone_retriever()

        # Load or define prompt template for symptom triage
        self.prompt_template = PromptTemplate(
            input_variables=["question", "context"],
            template=(
                "You are a veterinary AI assistant helping pet owners. "
                "Use the following context extracted from trusted veterinary guides and symptom data to answer the question.\n\n"
                "Context:\n{context}\n\n"
                "Question: {question}\n"
                "Answer carefully with clear and helpful advice."
            ),
        )

        # Setup RetrievalQA chain combining retriever + LLM + prompt template
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",  # 'stuff' combines context docs into prompt
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": self.prompt_template},
        )

    def ask(self, user_question: str) -> str:
        """
        Answer the user's question by retrieving relevant vet docs and
        generating a response via OpenAI LLM.

        Args:
            user_question (str): The user's input question about pet health

        Returns:
            str: Chatbot's answer string
        """
        if not user_question.strip():
            return "Please ask a valid question about your pet's symptoms or health."

        try:
            # Run the RAG chain: retrieve relevant docs + generate answer
            response = self.qa_chain.run(user_question)
            return response.strip()
        except Exception as e:
            # Log error, but do not expose raw error to user
            print(f"[Chatbot] Error during response generation: {e}")
            return "Sorry, I encountered an error while trying to answer. Please try again later."
