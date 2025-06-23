
```markdown
# 🐾 ChatVet — AI-Powered Veterinary Assistant

ChatVet is an intelligent SaaS-style veterinary assistant built with GPT-4, LangChain, and RAG (Retrieval-Augmented Generation). It provides pet owners with instant, personalized health triage and care guidance using a secure, subscription-ready interface.

![ChatVet UI](docs/demo_screenshot.png) <!-- Optional: add a demo screenshot -->

---

## 🚀 Features

- 🧠 **GPT-4 Powered**: Leverages OpenAI's GPT-4 for natural language understanding and veterinary reasoning.
- 🔍 **RAG Pipeline**: Combines LLM reasoning with real vet knowledge via Pinecone and LangChain.
- 📚 **Custom Knowledge Base**: Ingested CSVs + web-scraped PDFs containing pet care protocols and symptom data.
- 💾 **Persistent Chat Memory**: Stores user sessions to simulate continuity in conversation.
- 💳 **SaaS Prototype**: Includes mocked user login and Stripe billing for a subscription-like experience.
- 🌐 **Streamlit Interface**: Clean, reactive frontend built with Streamlit for rapid deployment.

---

## 🧱 Tech Stack

| Layer        | Tech                                                   |
|--------------|--------------------------------------------------------|
| Language     | Python 3.10                                            |
| LLM API      | OpenAI GPT-4                                           |
| Framework    | Streamlit + LangChain                                  |
| Vector DB    | Pinecone                                               |
| Embeddings   | OpenAI Embeddings (can be replaced with local models)  |
| Auth / Billing | Streamlit Auth + Mock Stripe API                    |
| Packaging    | Docker, dotenv, modular Python packages                |

---

## 📁 Repository Structure

```

chatvet/
├── app/                  # Streamlit UI and routing
├── backend/              # RAG logic, LLM interaction, data loaders
├── data/                 # Raw PDFs, cleaned data, vet knowledge base
├── embeddings/           # Pinecone indexing, OpenAI embedding logic
├── auth/                 # Login flow, mock billing
├── configs/              # Prompt templates and UI settings
├── tests/                # Unit tests for RAG + LLM integration
├── notebooks/            # Optional data exploration or demos
├── requirements.txt
├── README.md
├── .env                  # API keys (not included in repo)

````

---

## 🛠 Setup Instructions

1. **Clone the repository**
```bash
git clone https://github.com/yaldakasravi/chatvet.git && cd chatvet
````

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Configure environment**
   Create a `.env` file:

```
OPENAI_API_KEY=your_openai_key
PINECONE_API_KEY=your_pinecone_key
PINECONE_ENV=your_pinecone_env
```

4. **Run the app**

```bash
streamlit run app/main.py
```

---

## 🧪 Demo Commands

* `search <symptom>`: Retrieves relevant care articles using vector search
* `ask "What should I do if my cat is sneezing?"`: Triggers GPT-4 response with retrieved context
* Simulate Stripe billing: Toggle user access based on subscription flag in mock

---

## 📈 Future Enhancements

* Replace OpenAI with local LLM (Mistral, LLaMA) for offline deployment
* Integrate Vet24 APIs or online vet triage systems
* Add chatbot memory persistence via Redis or Firestore
* Add voice chat via Whisper API for accessibility

---

## 👩‍⚕️ Use Cases

* Triage for pet symptoms and care guidance
* Education and vet advice retrieval
* Accessible AI vet assistant for pet owners in underserved areas

---
