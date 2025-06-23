# backend/chatbot.py

import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from prompt_templates import symptom_triage_prompt
from retriever import get_pinecone_retriever
from symptom_checker import SymptomChecker
from dotenv import load_dotenv

load_dotenv()

class Chatbot:
    def __init__(self):
        # Initialize OpenAI Chat model
        openai_api_key = os.getenv("OPENAI_API_KEY")
        if not openai_api_key:
            raise ValueError("OPENAI_API_KEY is not set in environment variables")

        self.llm = ChatOpenAI(
            model="gpt-4",  # or "gpt-3.5-turbo"
            temperature=0.2,
            openai_api_key=openai_api_key,
            max_tokens=1024,
            streaming=False,
        )

        # Initialize Retriever for Pinecone vector DB
        self.retriever = get_pinecone_retriever()

        # Use the centralized prompt template from prompt_templates.py
        self.prompt_template = symptom_triage_prompt

        # Setup RetrievalQA chain combining retriever + LLM + prompt template
        self.qa_chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.retriever,
            return_source_documents=False,
            chain_type_kwargs={"prompt": self.prompt_template},
        )

        # Initialize symptom checker with your symptom-suggestion CSV
        self.symptom_checker = SymptomChecker("data/vet_guides.csv")

    def ask(self, user_question: str) -> str:
        """
        Answer the user's question by trying quick symptom matching first,
        then fallback to Retrieval-Augmented Generation (RAG) with LLM.

        Args:
            user_question (str): The user's input question about pet health

        Returns:
            str: Chatbot's answer string
        """
        if not user_question.strip():
            return "Please ask a valid question about your pet's symptoms or health."

        # 1. Try symptom checker with a similarity threshold
        suggestions = self.symptom_checker.get_suggestions(user_question, threshold=0.5)

        # If confident suggestions found, return them directly
        fallback_msg = "No close matches found. Please consult a veterinarian for specific advice."
        if suggestions and suggestions[0] != fallback_msg:
            reply = "Based on your symptoms, here is some advice:\n- " + "\n- ".join(suggestions)
            return reply

        # 2. Fallback to RAG + LLM for more complex or unmatched queries
        try:
            response = self.qa_chain.run(user_question)
            return response.strip()
        except Exception as e:
            print(f"[Chatbot] Error during response generation: {e}")
            return "Sorry, I encountered an error while trying to answer. Please try again later."
