"""
CNCS Chatbot - Configuration
Constants, intent names, UI labels, messages, and SQL queries.
"""

# =============================================================================
# App Configuration
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
    FALLBACK  = "fallback"
    CONTACT   = "poc"
    PRODUCT   = "product"
    ORDER     = "order"
    FAQ       = "faq"
    FREETEXT  = "freetext"

# =============================================================================
# UI Labels
# =============================================================================

class Label:
    MAIN_MENU         = "Main Menu"
    CONTACT           = "Contact CNCS"
    PRODUCT           = "Find a Product"
    ORDER             = "Check Order Status"
    FAQ               = "Explore FAQs"
    ASK               = "Ask a Question"
    BACK_DEPARTMENTS  = "Back to Departments"
    BACK_CATEGORIES   = "Back to Categories"
    VIEW_DETAILS      = "View Order Details"
    ANOTHER_ORDER     = "Check Another Order"
    BACK_FAQ          = "Back to FAQs"

# =============================================================================
# Response Messages
# =============================================================================

class Message:
    GREETING = "Hello! I'm Suppo, the CNCS support chatbot. How can I help you?"
    UNKNOWN  = "I cannot help with that, but I am working on it. Try again later."
    CONTACT  = "Choose a department:"
    PRODUCT  = "Choose a product category:"
    ORDER    = "Please enter your order number below to check the status:"
    FAQ      = "Frequently Asked Questions:\n\n"
    ASK      = "What would you like to know? Type your question below:"

# =============================================================================
# SQL Queries
# =============================================================================

class Query:
    DEPARTMENTS  = "SELECT DISTINCT Department FROM Contacts"
    CONTACT      = "SELECT * FROM Contacts WHERE Department = ?"
    CATEGORIES   = "SELECT DISTINCT Category FROM Products"
    PRODUCTS     = "SELECT * FROM Products WHERE Category = ?"
    ORDER        = f"SELECT * FROM Orders WHERE OrderID = ? AND UserID = {DEFAULT_USER_ID}"
    ORDER_ITEMS  = f"""
        SELECT od.OrderDetailID, od.Quantity, od.Subtotal, p.ProductName
        FROM OrderDetails od
        JOIN Products p ON od.ProductID = p.ProductID
        JOIN Orders o ON od.OrderID = o.OrderID
        WHERE od.OrderID = ? AND o.UserID = {DEFAULT_USER_ID}
    """
    FAQS         = "SELECT * FROM FAQs"
    FAQ_ANSWER   = "SELECT * FROM FAQs WHERE FAQID = ?"
    ALL_CONTACTS = "SELECT Department, Email, Phone FROM Contacts"
    ALL_PRODUCTS = "SELECT ProductName, Category, Price, StockQuantity FROM Products"
    ALL_FAQ_QA   = "SELECT Question, Answer FROM FAQs"
