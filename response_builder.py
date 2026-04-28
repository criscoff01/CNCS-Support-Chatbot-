"""
CNCS Chatbot - Response Builder
Responsible only for constructing button and response dictionaries,
and defining the shared button/menu constants used across handlers.
"""

from config import Intent, Label

# =============================================================================
# Factory Functions
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
    """Generate a list of buttons from database rows."""
    return [
        make_button(f"{prefix}{item[attribute]}", f"{intent_prefix}{item[attribute]}")
        for item in items
    ]

# =============================================================================
# Shared Button Constants
# =============================================================================

MAIN_MENU_BUTTON     = make_button(Label.MAIN_MENU,        Intent.GREETING)
CONTACT_BUTTON       = make_button(Label.CONTACT,          Intent.CONTACT)
PRODUCT_BUTTON       = make_button(Label.PRODUCT,          Intent.PRODUCT)
ORDER_BUTTON         = make_button(Label.ORDER,            Intent.ORDER)
FAQ_BUTTON           = make_button(Label.FAQ,              Intent.FAQ)
ASK_BUTTON           = make_button(Label.ASK,              Intent.FREETEXT)
DEPARTMENTS_BACK     = make_button(Label.BACK_DEPARTMENTS, Intent.CONTACT)
CATEGORIES_BACK      = make_button(Label.BACK_CATEGORIES,  Intent.PRODUCT)
ANOTHER_ORDER_BUTTON = make_button(Label.ANOTHER_ORDER,    Intent.ORDER)
FAQ_BACK             = make_button(Label.BACK_FAQ,         Intent.FAQ)

PRIMARY_MENU = [CONTACT_BUTTON, PRODUCT_BUTTON, ORDER_BUTTON, FAQ_BUTTON, ASK_BUTTON]
