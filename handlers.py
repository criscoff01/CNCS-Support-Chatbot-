"""
CNCS Chatbot - Intent Handlers
Responsible only for handling each user intent and producing a response.
All database access goes through database.py; all response construction
goes through response_builder.py; AI calls go through ai_service.py.
"""

from config import Intent, Label, Message, Query
from database import query_db
from ai_service import query_ollama
from response_builder import (
    make_button, make_response, create_buttons,
    MAIN_MENU_BUTTON, ASK_BUTTON, DEPARTMENTS_BACK, CATEGORIES_BACK,
    ANOTHER_ORDER_BUTTON, FAQ_BACK, PRIMARY_MENU
)

# =============================================================================
# Greeting / Fallback
# =============================================================================

def handle_greeting():
    """Return the welcome message with the primary menu."""
    return make_response(Message.GREETING, PRIMARY_MENU)


def handle_fallback():
    """Return a generic fallback message."""
    return make_response(Message.UNKNOWN, [MAIN_MENU_BUTTON])

# =============================================================================
# Contact Handler
# =============================================================================

def handle_contact(intent):
    """Show department list, or contact details for a specific department."""
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

# =============================================================================
# Product Handler
# =============================================================================

def handle_product(intent):
    """Show category list, or products for a specific category."""
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

# =============================================================================
# Order Handler
# =============================================================================

def handle_order(intent, user_text):
    """Prompt for an order number, look up status, or show full order details."""
    prefix = f"{Intent.ORDER}_"

    if intent == Intent.ORDER:
        order_num = int(user_text) if (user_text and user_text.isdigit()) else None
        if order_num:
            return _lookup_order(order_num, prefix)
        return make_response(Message.ORDER, [MAIN_MENU_BUTTON], enable_input=True)

    order_num = int(intent.replace(prefix, ''))
    return _lookup_order_details(order_num)


def _lookup_order(order_num, prefix):
    """Look up and display order status."""
    orders = query_db(Query.ORDER, order_num)

    if not orders:
        return make_response(
            f"I'm sorry, I cannot find order #{order_num} in our system. Please try another order number.",
            [ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON]
        )

    response     = _format_order(order_num, orders)
    view_details = make_button(Label.VIEW_DETAILS, f"{prefix}{order_num}")
    return make_response(response, [view_details, ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON])


def _lookup_order_details(order_num):
    """Look up and display full order with line items."""
    orders = query_db(Query.ORDER, order_num)

    if not orders:
        return make_response(
            f"I'm sorry, I cannot find order #{order_num} in our system.",
            [ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON]
        )

    items    = query_db(Query.ORDER_ITEMS, order_num)
    response = _format_order(order_num, orders) + _format_items(items)
    return make_response(response, [ANOTHER_ORDER_BUTTON, MAIN_MENU_BUTTON])


def _format_order(order_num, orders):
    """Format basic order information into a string."""
    response = f"Order #{order_num}:\n"
    for order in orders:
        response += f"\nStatus: {order['Status']}\n"
        response += f"Order Date: {order['OrderDate']}\n"
        response += f"Total Amount: ${order['TotalAmount']:.2f}\n"
    return response


def _format_items(items):
    """Format order line items into a string."""
    if not items:
        return "No items found for this order."

    response = "\nItems in this order:\n"
    for item in items:
        response += f"\n- {item['ProductName']} (Qty: {item['Quantity']}): ${item['Subtotal']:.2f}\n"
    return response

# =============================================================================
# FAQ Handler
# =============================================================================

def handle_faq(intent):
    """Show FAQ list, or the answer to a specific FAQ."""
    prefix = f"{Intent.FAQ}_"

    if intent == Intent.FAQ:
        faqs     = query_db(Query.FAQS)
        response = Message.FAQ
        for faq in faqs:
            response += f"{faq['FAQID']}. {faq['Question']}\n"
        response += "\nChoose an FAQ answer below:"

        buttons = create_buttons(faqs, 'FAQID', "#", prefix)
        buttons.append(MAIN_MENU_BUTTON)
        return make_response(response, buttons)

    faq_id  = intent.replace(prefix, '')
    answers = query_db(Query.FAQ_ANSWER, faq_id)

    if answers:
        response = f"FAQ #{faq_id}:\n\n"
        for answer in answers:
            response += f"{answer['Question']}\n\nAnswer: {answer['Answer']}\n"
    else:
        response = f"I could not find an answer for FAQ #{faq_id}."

    return make_response(response, [FAQ_BACK, MAIN_MENU_BUTTON])

# =============================================================================
# Free-Text (AI) Handler
# =============================================================================

def handle_freetext(intent, user_text, session_id):
    """Prompt for a question, or forward a typed question to the AI service."""
    if intent == Intent.FREETEXT and not user_text:
        return make_response(Message.ASK, [MAIN_MENU_BUTTON], enable_input=True)

    if user_text and user_text.strip():
        ai_response = query_ollama(user_text, session_id)
        return make_response(ai_response, [ASK_BUTTON, MAIN_MENU_BUTTON], enable_input=True)

    return make_response("Please type a question.", [ASK_BUTTON, MAIN_MENU_BUTTON])

# =============================================================================
# Intent Router
# =============================================================================

def process_intent(intent, user_text, session_id):
    """Route an incoming intent to the appropriate handler."""
    handlers = {
        Intent.GREETING:  lambda: handle_greeting(),
        Intent.CONTACT:   lambda: handle_contact(intent),
        Intent.PRODUCT:   lambda: handle_product(intent),
        Intent.ORDER:     lambda: handle_order(intent, user_text),
        Intent.FAQ:       lambda: handle_faq(intent),
        Intent.FREETEXT:  lambda: handle_freetext(intent, user_text, session_id),
    }

    for key, handler in handlers.items():
        if intent.startswith(key):
            return handler()

    return handle_fallback()
