"""
CNCS Chatbot - AI Service
Responsible only for building the system prompt, managing conversation
sessions, and communicating with the Ollama model.
"""

import ollama
from config import OLLAMA_MODEL, Query
from database import query_db

# In-memory store: { session_id: [{"role": ..., "content": ...}, ...] }
conversation_sessions = {}


def build_system_prompt():
    """Build Suppo's system prompt populated with live database knowledge."""
    contacts = query_db(Query.ALL_CONTACTS)
    products = query_db(Query.ALL_PRODUCTS)
    faqs     = query_db(Query.ALL_FAQ_QA)

    contacts_info = "DEPARTMENT CONTACTS:\n"
    for c in contacts:
        contacts_info += f"- {c['Department']}: Email: {c['Email']}, Phone: {c['Phone']}\n"

    products_info = "PRODUCTS:\n"
    for p in products:
        products_info += f"- {p['ProductName']} ({p['Category']}) - ${p['Price']:.2f} - {p['StockQuantity']} in stock\n"

    faqs_info = "FREQUENTLY ASKED QUESTIONS:\n"
    for f in faqs:
        faqs_info += f"Q: {f['Question']}\nA: {f['Answer']}\n\n"

    return f"""You are Suppo, the friendly customer service assistant for CyberNet Computer Systems (CNCS).

PERSONALITY:
- Warm, enthusiastic, and genuinely eager to help
- Conversational and friendly but professional
- Uses light humor when appropriate
- Patient and thorough in explanations
- Honest when you don't know something

YOUR KNOWLEDGE BASE:

{contacts_info}
{products_info}
{faqs_info}

GUIDELINES:
1. Answer using ONLY the information provided above
2. If asked about something not in your knowledge base, politely say you don't have that information and offer to help with other questions. That is it.
3. For order-specific questions, suggest using the "Check Order Status" button
4. Be concise but helpful
5. When discussing products, mention price and availability if relevant
6. Be accurate with prices and contact information - never make up details
7. Keep your responses concise and to the point. Don't add extra information that is not relevant to the question.
8. When asked about a product, only reference products from the category being discussed
"""


def query_ollama(question, session_id):
    """
    Send a question to Ollama, maintaining per-session conversation history.
    Returns the assistant's response text.
    """
    if session_id not in conversation_sessions:
        conversation_sessions[session_id] = []

    try:
        system_prompt = build_system_prompt()
        conversation_sessions[session_id].append({'role': 'user', 'content': question})

        messages  = [{'role': 'system', 'content': system_prompt}] + conversation_sessions[session_id]
        response  = ollama.chat(model=OLLAMA_MODEL, messages=messages)

        assistant_response = response['message']['content']
        conversation_sessions[session_id].append({'role': 'assistant', 'content': assistant_response})

        return assistant_response

    except Exception as e:
        print(f"Ollama error: {e}")
        return "I'm having trouble processing your question. Please try using the menu options or try again later."
