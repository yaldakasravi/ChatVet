from langchain.prompts import PromptTemplate

# Basic symptom triage prompt template:
# Takes 'question' (user input) and 'context' (retrieved vet info) as inputs.
symptom_triage_template = """
You are a veterinary AI assistant helping pet owners by providing clear, compassionate, and informative advice.
Use the information provided in the context below to answer the user's question.

Context:
{context}

Question:
{question}

Instructions:
- Use only the context information to answer.
- If the context does not contain enough information, politely say so.
- Avoid giving any emergency or medical diagnosis; always recommend consulting a qualified veterinarian if serious symptoms are present.
- Provide advice in simple, friendly language suitable for pet owners.
- If appropriate, suggest general next steps like monitoring symptoms, ensuring hydration, or visiting a vet.

Answer:
"""

symptom_triage_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=symptom_triage_template.strip(),
)

# You can add more prompt variants here for different styles or tasks if needed.
# For example, a prompt focused on preventative care advice:

preventative_care_template = """
You are a knowledgeable veterinary assistant.

Based on the following veterinary information, provide friendly advice about how pet owners can prevent common illnesses and keep their pets healthy.

Information:
{context}

Question:
{question}

Answer:
"""

preventative_care_prompt = PromptTemplate(
    input_variables=["question", "context"],
    template=preventative_care_template.strip(),
)
