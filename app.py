"""
CNCS Support Chatbot - Flask Backend
Handles chatbot logic and database operations
"""

from flask import Flask, render_template, request, jsonify
import sqlite3
import ollama

# =============================================================================
# Configuration
# =============================================================================

DEBUG_MODE = True
DATABASE_NAME = 'cncs_chatbot.db'
DEFAULT_USER_ID = 1  # Demo user (no auth implemented)
OLLAMA_MODEL = "llama3.2"

# =============================================================================
# Intent Constants
# =============================================================================

class Intent:
    GREETING = "greeting"
    FALLBACK = "fallback"
    CONTACT = "poc"
    PRODUCT = "product"
    ORDER = "order"
    FAQ = "faq"
    FREETEXT = "freetext"

# =============================================================================
# UI Labels
# =============================================================================

class Label:
    MAIN_MENU = "Main Menu"
    CONTACT = "Contact CNCS"
    PRODUCT = "Find a Product"
    ORDER = "Check Order Status"
    FAQ = "Explore FAQs"
    ASK = "Ask a Question"
    BACK_DEPARTMENTS = "Back to Departments"
    BACK_CATEGORIES = "Back to Categories"
    VIEW_DETAILS = "View Order Details"
    ANOTHER_ORDER = "Check Another Order"
    BACK_FAQ = "Back to FAQs"

# =============================================================================
# Response Messages
# =============================================================================

class Message:
    GREETING = "Hello! I'm Suppo, the CNCS support chatbot. How can I help you?"
    UNKNOWN = "I cannot help with that, but I am working on it. Try again later."
    CONTACT = "Choose a department:"
    PRODUCT = "Choose a product category:"
    ORDER = "Please enter your order number below to check the status:"
    FAQ = "Frequently Asked Questions:\n\n"
    ASK = "What would you like to know? Type your question below:"

# =============================================================================
# SQL Queries
# =============================================================================

class Query:
    DEPARTMENTS = "SELECT DISTINCT Department FROM Contacts"
    CONTACT = "SELECT * FROM Contacts WHERE Department = ?"
    CATEGORIES = "SELECT DISTINCT Category FROM Products"
    PRODUCTS = "SELECT * FROM Products WHERE Category = ?"
    ORDER = f"SELECT * FROM Orders WHERE OrderID = ? AND UserID = {DEFAULT_USER_ID}"
    ORDER_ITEMS = f"""
        SELECT od.OrderDetailID, od.Quantity, od.Subtotal, p.ProductName
        FROM OrderDetails od
        JOIN Products p ON od.ProductID = p.ProductID
        JOIN Orders o ON od.OrderID = o.OrderID
        WHERE od.OrderID = ? AND o.UserID = {DEFAULT_USER_ID}
    """
    FAQS = "SELECT * FROM FAQs"
    FAQ_ANSWER = "SELECT * FROM FAQs WHERE FAQID = ?"
    ALL_CONTACTS = "SELECT Department, Email, Phone FROM Contacts"
    ALL_PRODUCTS = "SELECT ProductName, Category, Price, StockQuantity FROM Products"
    ALL_FAQ_QA = "SELECT Question, Answer FROM FAQs"

# =============================================================================
# Application Setup
# =============================================================================

app = Flask(__name__)
conversation_sessions = {}

# Button definitions
MAIN_MENU_BUTTON = {"text": Label.MAIN_MENU, "value": Intent.GREETING}
CONTACT_BUTTON = {"text": Label.CONTACT, "value": Intent.CONTACT}
PRODUCT_BUTTON = {"text": Label.PRODUCT, "value": Intent.PRODUCT}
ORDER_BUTTON = {"text": Label.ORDER, "value": Intent.ORDER}
FAQ_BUTTON = {"text": Label.FAQ, "value": Intent.FAQ}
ASK_BUTTON = {"text": Label.ASK, "value": Intent.FREETEXT}
DEPARTMENTS_BACK = {"text": Label.BACK_DEPARTMENTS, "value": Intent.CONTACT}
CATEGORIES_BACK = {"text": Label.BACK_CATEGORIES, "value": Intent.PRODUCT}
ANOTHER_ORDER_BUTTON = {"text": Label.ANOTHER_ORDER, "value": Intent.ORDER}
FAQ_BACK = {"text": Label.BACK_FAQ, "value": Intent.FAQ}

PRIMARY_MENU = [CONTACT_BUTTON, PRODUCT_BUTTON, ORDER_BUTTON, FAQ_BUTTON, ASK_BUTTON]

# =============================================================================
# Database Functions
# =============================================================================

def get_db():
    """Create database connection with row factory."""
    db = sqlite3.connect(DATABASE_NAME)
    db.row_factory = sqlite3.Row
    return db


def query_db(sql, params=""):
    """Execute SQL query and return results."""
    db = get_db()
    cursor = db.cursor()
    
    if params:
        cursor.execute(sql, (params,))
    else:
        cursor.execute(sql)
    
    data = cursor.fetchall()
    db.close()
    return data

# =============================================================================
# Helper Functions
# =============================================================================

def make_button(label, intent):
    """Create a button dictionary."""
    return {"text": label, "value": intent}


def make_response(text, buttons, enable_input=False):
    """Create a standardized response dictionary."""
    return {
        "response": text,
        "buttons": buttons,
        "enableTextInput": enable_input
    }


def create_buttons(items, attribute, prefix, intent_prefix):
    """Generate buttons from database items."""
    return [
        make_button(f"{prefix}{item[attribute]}", f"{intent_prefix}{item[attribute]}")
        for item in items
    ]

# =============================================================================
# Ollama Integration
# =============================================================================

def build_system_prompt():
    """Build Suppo's system prompt with database knowledge."""
    contacts = query_db(Query.ALL_CONTACTS)
    products = query_db(Query.ALL_PRODUCTS)
    faqs = query_db(Query.ALL_FAQ_QA)

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
"""


def query_ollama(question, session_id):
    """Query Ollama with conversation context."""
    global conversation_sessions

    try:
        if session_id not in conversation_sessions:
            conversation_sessions[session_id] = []

        system_prompt = build_system_prompt()
        conversation_sessions[session_id].append({'role': 'user', 'content': question})

        messages = [{'role': 'system', 'content': system_prompt}] + conversation_sessions[session_id]
        response = ollama.chat(model=OLLAMA_MODEL, messages=messages)
        
        assistant_response = response['message']['content']
        conversation_sessions[session_id].append({'role': 'assistant', 'content': assistant_response})

        return assistant_response

    except Exception as e:
        print(f"Ollama error: {e}")
        return "I'm having trouble processing your question. Please try using the menu options or try again later."

# =============================================================================
# Intent Handlers
# =============================================================================

def handle_greeting():
    """Handle initial greeting."""
    return make_response(Message.GREETING, PRIMARY_MENU)


def handle_fallback():
    """Handle unknown intents."""
    return make_response(Message.UNKNOWN, [MAIN_MENU_BUTTON])


def handle_contact(intent):
    """Handle contact lookup."""
    prefix = f"{Intent.CONTACT}_"
    
    if intent == Intent.CONTACT:
        departments = query_db(Query.DEPARTMENTS)
        buttons = create_buttons(departments, 'Department', "", prefix)
        buttons.append(MAIN_MENU_BUTTON)
        return make_response(Message.CONTACT, buttons)
    
    department = intent.replace(prefix, '')
    contacts = query_db(Query.CONTACT, department)
    
    if contacts:
        response = f"Here is the contact information for {department}:\n\n"
        for contact in contacts:
            response += f"Email: {contact['Email']}\nPhone: {contact['Phone']}\n"
    else:
        response = f"I could not find contact information for {department}."
    
    return make_response(response, [DEPARTMENTS_BACK, MAIN_MENU_BUTTON])


def handle_product(intent):
    """Handle product lookup."""
    prefix = f"{Intent.PRODUCT}_"
    
    if intent == Intent.PRODUCT:
        categories = query_db(Query.CATEGORIES)
        buttons = create_buttons(categories, 'Category', "", prefix)
        buttons.append(MAIN_MENU_BUTTON)
        return make_response(Message.PRODUCT, buttons)
    
    category = intent.replace(prefix, '')
    products = query_db(Query.PRODUCTS, category)
    
    if products:
        response = f"Here are our products in the {category} category:\n"
        for product in products:
            response += f"\n- {product['ProductName']}\n"
            response += f"  Price: ${product['Price']:.2f}\n"
            response += f"  Stock: {product['StockQuantity']} units\n"
    else:
        response = f"I could not find products in the {category} category."
    
    return make_response(response, [CATEGORIES_BACK, MAIN_MENU_BUTTON])


def handle_order(intent, user_text):
    """Handle order status lookup."""
    prefix = f"{Intent.ORDER}_"
    
    if intent == Intent.ORDER:
        order_num = None
        if user_text and user_text.isdigit():
            order_num = int(user_text)
        
        if order_num:
            return lookup_order(order_num, prefix)
        return make_response(Message.ORDER, [MAIN_MENU_BUTTON], enable_input=True)
    
    order_num = int(intent.replace(prefix, ''))
    return lookup_order_details(order_num)


def lookup_order(order_num, prefix):
    """Look up order status."""
    orders = query_db(Query.ORDER, order_num)
    
    if not orders:
        return make_response(
            f"I'm sorry, I cannot find order #{order_num} in our system. Please try another order number.",
            [ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON]
        )
    
    response = format_order_response(order_num, orders)
    view_details = make_button(Label.VIEW_DETAILS, f"{prefix}{order_num}")
    return make_response(response, [view_details, ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON])


def lookup_order_details(order_num):
    """Look up full order with items."""
    orders = query_db(Query.ORDER, order_num)
    
    if not orders:
        return make_response(
            f"I'm sorry, I cannot find order #{order_num} in our system.",
            [ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON]
        )
    
    items = query_db(Query.ORDER_ITEMS, order_num)
    response = format_order_response(order_num, orders)
    response += format_items_response(items)
    
    return make_response(response, [ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON])


def format_order_response(order_num, orders):
    """Format order information."""
    response = f"Order #{order_num}:\n"
    for order in orders:
        response += f"\nStatus: {order['Status']}\n"
        response += f"Order Date: {order['OrderDate']}\n"
        response += f"Total Amount: ${order['TotalAmount']:.2f}\n"
    return response


def format_items_response(items):
    """Format order items."""
    if not items:
        return "No items found for this order."
    
    response = "\nItems in this order:\n"
    for item in items:
        response += f"\n- {item['ProductName']} (Qty: {item['Quantity']}): ${item['Subtotal']:.2f}\n"
    return response


def handle_faq(intent):
    """Handle FAQ lookup."""
    prefix = f"{Intent.FAQ}_"
    
    if intent == Intent.FAQ:
        faqs = query_db(Query.FAQS)
        response = Message.FAQ
        for faq in faqs:
            response += f"{faq['FAQID']}. {faq['Question']}\n"
        response += "\nChoose an FAQ answer below:"
        
        buttons = create_buttons(faqs, 'FAQID', "#", prefix)
        buttons.append(MAIN_MENU_BUTTON)
        return make_response(response, buttons)
    
    faq_id = intent.replace(prefix, '')
    answers = query_db(Query.FAQ_ANSWER, faq_id)
    
    if answers:
        response = f"FAQ #{faq_id}:\n\n"
        for answer in answers:
            response += f"{answer['Question']}\n\nAnswer: {answer['Answer']}\n"
    else:
        response = f"I could not find an answer for FAQ #{faq_id}."
    
    return make_response(response, [FAQ_BACK, MAIN_MENU_BUTTON])


def handle_freetext(intent, user_text, session_id):
    """Handle free text questions using Ollama."""
    if intent == Intent.FREETEXT and not user_text:
        return make_response(Message.ASK, [MAIN_MENU_BUTTON], enable_input=True)
    
    if user_text and user_text.strip():
        ai_response = query_ollama(user_text, session_id)
        return make_response(ai_response, [ASK_BUTTON, MAIN_MENU_BUTTON], enable_input=True)
    
    return make_response("Please type a question.", [ASK_BUTTON, MAIN_MENU_BUTTON])

# =============================================================================
# Request Processing
# =============================================================================

def process_intent(intent, user_text, session_id):
    """Route request to appropriate handler."""
    handlers = {
        Intent.GREETING: lambda: handle_greeting(),
        Intent.CONTACT: lambda: handle_contact(intent),
        Intent.PRODUCT: lambda: handle_product(intent),
        Intent.ORDER: lambda: handle_order(intent, user_text),
        Intent.FAQ: lambda: handle_faq(intent),
        Intent.FREETEXT: lambda: handle_freetext(intent, user_text, session_id),
    }
    
    for key, handler in handlers.items():
        if intent.startswith(key):
            return handler()
    
    return handle_fallback()

# =============================================================================
# Routes
# =============================================================================

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Process chat requests."""
    data = request.json
    
    intent = data.get('userIntent', Intent.GREETING)
    user_text = data.get('userTypedText', '')
    session_id = data.get('sessionId', '')
    
    print(f"\n=== SESSION: {session_id} ===")
    print(f"Intent: {intent}")
    print(f"Text: {user_text}")
    
    result = process_intent(intent, user_text, session_id)
    return jsonify(result)

# =============================================================================
# Entry Point
# =============================================================================

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
