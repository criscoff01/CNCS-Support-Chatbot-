#References: 
# Learn 12 Basic SQL Concepts in 15 Minutes - https://youtu.be/_vxobA36UN4?si=40cYFnC97-M1a-1n
# How to create a simple flask app in just 5 minutes - https://youtu.be/6M3LzGmIAso?si=5zfwenQXwDlwVBTM 
# Connect to SQLite Databae. GET Data -https://youtu.be/Ym6LsUO9gQo?si=L8iUu6fVK7v-Ovl1
# How to render HTML page using Flask - https://youtu.be/TH-S2shHKw0?si=sq6ODRDjvaM3RAG-
# Learn Flask for Python Full Tutorial - https://youtu.be/Z1RJmh_OqeA?si=qKWot2_jgLas9dFW
# jsonify python flask - https://youtu.be/wEla4oQ9TqI?si=KyUmo8cAy26lzgr4

# Import needed web component framework
from flask import Flask, render_template, request, jsonify

# Import needed DB framework
import sqlite3

# Configuration Constants
DebuggerOn =        True
NameOfChatBotDB =   'cncs_chatbot.db'
RouteToHostPage =   '/'
NameOfHostPage =    'index.html'
RouteToChatBotAPI = '/api/chat'

UserID = 1          # No user login developed for this app (assumed to pre-exist), so default to this user for Track Order use case demo

# Chatbot Intents - interpretations of user intent to drive chatbot responses
GreetingIntent =    "greeting"  # Initial / Main Menu intent
FallbackIntent =    "fallback"  # Default when user intent cannot be determined
FindContactIntent = "poc"       # Use case 1
FindProductIntent = "product"   # Use case 2
TrackOrderIntent =  "order"     # Use case 3
LookupFAQsIntent =  "faq"       # Use case 4

# Chatbot menu button labels
MainMenuLabel = "Main Menu"
ContactLabel =  "Contact CNCS"
ProductLabel =  "Find a Product"
OrderLabel =    "Check Order Status"
FAQsLabel =     "Explore FAQs"

DepartmentsLabel =  "Back to Departments"
CategoriesLabel =   "Back to Categories"
OrderDetailsLabel = "View Order Details"
AnotherOrderLabel = "Check Another Order"
FAQsBackLabel =     "Back to FAQs"

# Chatbot menu buttons for user interaction
MainMenuButton =    {"text": MainMenuLabel, "value": GreetingIntent}
FindContactButton = {"text": ContactLabel, "value": FindContactIntent}
FindProductButton = {"text": ProductLabel, "value": FindProductIntent}
TrackOrderButton =  {"text": OrderLabel, "value": TrackOrderIntent}
LookupFAQsButton =  {"text": FAQsLabel, "value": LookupFAQsIntent}

DepartmentsBackButton = {"text": DepartmentsLabel, "value": FindContactIntent}
CategoriesBackButton =  {"text": CategoriesLabel, "value": FindProductIntent}
TryAnotherOrderButton = {"text": AnotherOrderLabel, "value": TrackOrderIntent}
FAQsBackButton =        {"text": FAQsBackLabel, "value": LookupFAQsIntent}

PrimaryMenu = [FindContactButton, FindProductButton, TrackOrderButton, LookupFAQsButton]

# Static chatbot responses
InitialGreeting =       "Hello! I'm Suppo, the CNCS support chatbot. How can I help you?"
UnknownRequest =        "I cannot help with that, but I am working on it. Try again later."
FindPOCResponse =       "Choose a department:"
FindProductResponse =   "Choose a product category:"
TrackOrderResponse =    "Please enter your order number below to check the status:"
LookupFAQsResponse =    "Frequently Asked Questions:\n\n"

# Initialize the chatbot application
app = Flask(__name__)

# For root URL visits, launch the host web page - which contains the chatbot
@app.route(RouteToHostPage)                     # Config route to host web page
def index():
    return render_template(NameOfHostPage)

# Receive and process customer chat requests
@app.route(RouteToChatBotAPI, methods=['POST'])         # Config route for chatbot API requests
def chat():
    userRequestData = request.json                      # Extract customer input data from user request
    userIntent = getUserIntent(userRequestData)
    userText = getUserTypedText(userRequestData)
    chatResults = processUserIntent(userIntent, userText)         # Send to the proper user intent handler
    return jsonify(chatResults)  # 'chatResults' is a dictionary with a response and menu buttons to display

# Interpret user intent - in this menu-driven chatbot, userIntent is simply determined by the button pressed
# If using typed text instead of menu buttons is desired, this is where AI/NLP support would be added
# Of note, AI/NLP use (eg, Amazon Lex) would require a table of training 'utterances' that map to the 'intents'
def getUserIntent(userData):
    userIntent = userData.get('userIntent', GreetingIntent)   # Get userIntent from user, default to GreetingIntent
    return userIntent

# Extract any user text from the text input field that was presented to the user
def getUserTypedText(userData):
    userTypedText = userData.get('userTypedText')
    return userTypedText

# Process the user intent by routing to an appropriate intent handler - as use cases are implemented I will add user intent handlers here
def processUserIntent(userIntent, userText):
    if userIntent == GreetingIntent:
        return handleGreetingIntent()
    elif userIntent.startswith(FindContactIntent):
        return handleFindContactIntent(userIntent)
    elif userIntent.startswith(FindProductIntent):  
        return handleFindProductIntent(userIntent)
    elif userIntent.startswith(TrackOrderIntent):
        return handleTrackOrderIntent(userIntent, userText)
    elif userIntent.startswith(LookupFAQsIntent):
        return handleLookupFAQsIntent(userIntent)
    else:    # FallbackIntent
        return handleFallbackIntent()

# Ensure proper format for every chatbot message sent back to the user
def chatBotMessage(response, buttons, enableTextInput):
    return {"response": response, "buttons": buttons, "enableTextInput": enableTextInput}

# Ensure proper format for every chatbot message sent back to the user
def makeButton(label, userIntent):
    return {"text": label, "value": userIntent}
    
# ===== DEFAULT INTENT HANDLERS =====

# Process the chatbot opening interaction
def handleGreetingIntent():
    return chatBotMessage(InitialGreeting, PrimaryMenu, False)

# Process an unknown chat request
def handleFallbackIntent():
    return chatBotMessage(UnknownRequest, [MainMenuButton], False)

# ===== DB ACCESS SUPPORT FOR THE CHATBOT'S USER INTENT HANDLERS =====

# SQL Queries
ListOfDepartments = "SELECT DISTINCT Department FROM Contacts"
ContactRecord =     "SELECT * FROM Contacts WHERE Department = ?"

ListOfCategories =  "SELECT DISTINCT Category FROM Products"
ProductRecord =     "SELECT * FROM Products WHERE Category = ?" 
OrderRecord =       f"SELECT * FROM Orders WHERE OrderID = ? and UserID = {UserID}"
ItemsRecord =       f"""
                    SELECT OrderDetails.OrderDetailID, OrderDetails.Quantity, OrderDetails.Subtotal, Products.ProductName
                    FROM OrderDetails
                    JOIN Products ON OrderDetails.ProductID = Products.ProductID
                    JOIN Orders ON OrderDetails.OrderID = Orders.OrderID
                    WHERE OrderDetails.OrderID = ? and Orders.UserID = {UserID}
                    """
ListOfFAQs =        "SELECT * FROM FAQs"
AnswerRecord =      "SELECT * FROM FAQs WHERE FAQID = ?"
# Open and configure a DB connection 
def getDB():
    db = sqlite3.connect(NameOfChatBotDB) # Open DB 
    db.row_factory = sqlite3.Row          # Config row access
    return db

# Pull data from the chatbot DB 
def pullDataFromDB(sqlQuery, value = ""):
    db = getDB()
    cursor = db.cursor()
    if value == "":
        cursor.execute(sqlQuery) 
    else:
        cursor.execute(sqlQuery, (value,))
    data = cursor.fetchall()
    db.close()
    return data

# ===== USER INTENT HANDLERS =====

# Utility function - Create a menu button for each item in the list
def createButtons(list, attribute, namePrefix, intentPrefix):
    menu = []
    for item in list:
        itemName = item[attribute]
        buttonName = f"{namePrefix}{itemName}"
        userIntent = f"{intentPrefix}{itemName}"
        menu.append(makeButton(buttonName, userIntent))
    return menu

# Phase 1


# Use Case 1 : FindContactIntent - Lookup Points of Conctact (POCs) by Department
# ---The structure of userIntent is either "FindContactIntent" or "FindContactIntent_Department"
def handleFindContactIntent(userIntent):
    intentPrefix = f"{FindContactIntent}_"
    if userIntent == FindContactIntent:       # Primary level of detail needed
        return lookupDepartments(intentPrefix)
    else:                                     # Secondary level of detail needed 
        department = userIntent.replace(intentPrefix, '') #Remove intentPrefix
        return lookupContacts(department) 
    
# Respond to the user with a set of buttons representing the different departments
def lookupDepartments(intentPrefix):
    departments = pullDataFromDB(ListOfDepartments)
    response = FindPOCResponse
    buttons = createButtons(departments, 'Department', "", intentPrefix)
    buttons.append(MainMenuButton)
    return chatBotMessage(response, buttons, False)

# Respond to the user with all contact information for the user selected department
def lookupContacts(department):
    contacts = pullDataFromDB(ContactRecord, department)
    response = formatContactsResponse(department, contacts)
    buttons = [DepartmentsBackButton, MainMenuButton]
    return chatBotMessage(response, buttons, False)

# Format response that includes details for all contacts in the department
def formatContactsResponse(department, contacts):
    if contacts:        # if contacts were found, prep a response with contact info
        response = f"Here is the contact infromation for {department}:\n\n"
        for contact in contacts:
            response += f"Email: {contact['Email']}\n"
            response += f"Phone: {contact['Phone']}\n"
    else:           # if no contacts were found, prep a response stating so
        response = f"I could not find contact information for {department}."
    return response


# Phase 2 


# Use Case 2 : FindProductIntent - Lookup Products by Category

# The structure of userIntent is either "FindProductIntent" or "FindProductIntent_Category"
def handleFindProductIntent(userIntent):
    intentPrefix = f"{FindProductIntent}_"
    if userIntent == FindProductIntent:
        return lookupCategories(intentPrefix)
    else:
        category = userIntent.replace(intentPrefix, '')
        return lookupProducts(category)
    
# Respond to the user with a set of buttons representing the different product categories
def lookupCategories(intentPrefix):
    categories = pullDataFromDB(ListOfCategories) 
    response = FindProductResponse
    buttons = createButtons(categories, 'Category', "", intentPrefix)
    buttons.append(MainMenuButton)
    return chatBotMessage(response, buttons, False)

# Respond to the user with details for all products in the user selected 'category' 
def lookupProducts(category):
    products = pullDataFromDB(ProductRecord, category)
    response = formatProductsResponse(category, products)
    buttons = [CategoriesBackButton, MainMenuButton]
    return chatBotMessage(response, buttons, False)

# Format a respones that includes details for all products in a category
def formatProductsResponse(category, products):
    if products:
        response = f"Here are our products in the {category} category:\n"
        for product in products:
            #inlcude product name, price, and stock qunatity
            response += f"\n- {product['ProductName']}\n"
            response += f"  Price: ${product['Price']:.2f}\n"
            response += f"  Stock: {product['StockQuantity']} units \n"
    else:
        response = f"I could not find products in the {category} category."
    return response


# Phase 3


# Use Case 3 : TrackOrderIntent - Lookup a Customer's Order status and offer full order review

# ---The strucutre of userIntent is either "TrackOrderIntent" or "TrackOrderIntent_OrderNumber"
def handleTrackOrderIntent(userIntent, userText):
    intentPrefix = f"{TrackOrderIntent}_"
    if userIntent == TrackOrderIntent:       # Primary level of detail needed
        orderNumber = convertToOrderNumber(userText)
        if orderNumber:                      # Did the user provide an orderNumber?
            return lookupOrderNumber(orderNumber, intentPrefix)
        else:                                # If not, get one
            return requestOrderNumber()
    else:                                    # Secondary level of detail needed
        orderNumber = int(userIntent.replace(intentPrefix, ''))  # Remove intent Prefix
        return lookupFullOrder(orderNumber) 

# If the user provided aan order number, convert it to int
def convertToOrderNumber(userText):
    orderNumber = None
    if userText and userText.isdigit():
        orderNumber = int(userText)
    return orderNumber

# The customer requested order tracking but has not yet provided an order number, so ask for one
def requestOrderNumber():   # Opens a text input field, which is triggered by the True flag
    return chatBotMessage(TrackOrderResponse, [MainMenuButton], True)

# Respond to the user with status for the 'orderNumber' provided
def lookupOrderNumber(orderNumber, intentPrefix):
    orders = pullDataFromDB(OrderRecord, orderNumber)
    if orders:             # Display the order status and provude a button to view full order details
        response = formatOrderResponse(orderNumber, orders)
        viewOrderDetailsbutton = makeButton(OrderDetailsLabel, f"{intentPrefix}{orderNumber}")
        buttons = [viewOrderDetailsbutton, TryAnotherOrderButton, MainMenuButton]
        return chatBotMessage(response, buttons, False)
    else:                  # Order not found
        return orderNotFoundMessage(orderNumber)

# Display the order status, including a list of all items in the order
def lookupFullOrder(orderNumber):
    orders = pullDataFromDB(OrderRecord, orderNumber)
    if orders:             # Display the order status and list all items purchased 
        items = pullDataFromDB(ItemsRecord, orderNumber)
        response = formatOrderResponse(orderNumber, orders)
        response += formatOrderItemsResponse(items)
        buttons = [TryAnotherOrderButton, MainMenuButton]
        return chatBotMessage(response, buttons, False)
    else:                   # Order not found
        return orderNotFoundMessage(orderNumber)

# Order not found, so let the user know and provide a button to try another order
def orderNotFoundMessage(orderNumber):
    response = f"I'm sorry, I cannot find order #{orderNumber} in our system. Please try another order number."
    buttons = [TryAnotherOrderButton, MainMenuButton]
    return chatBotMessage(response, buttons, False)

# format a response that includes all 'orders' associated with 'orderNumber'
def formatOrderResponse(orderNumber, orders):
    response = f"Order #{orderNumber}:\n"
    for order in orders:
        response += f"\nStatus: {order['Status']}\n"
        response += f"Order Date: {order['OrderDate']}\n"
        response += f"Total Amount: ${order['TotalAmount']:.2f}\n"
    return response

# Format a response that includes all items in an order
def formatOrderItemsResponse(items):
    if items:
        response = "\nItems in this order:\n"
        for item in items:
            response += f"\n- {item['ProductName']} (Qty: {item['Quantity']}): ${item['Subtotal']:.2f}\n"
    else:
        response = "No items found for this order."
    return response



# Use Case 4 :LookupFAQsIntent - Lookup all FAQs and allow the user to selectively review them

#---The strucute of userIntent is either "LookupFAQsIntent" or "LookupFAQsIntent_FaqNumber"
def handleLookupFAQsIntent(userIntent):
    intentPrefix = f"{LookupFAQsIntent}_"
    if userIntent == LookupFAQsIntent:
        return lookupFAQs(intentPrefix)
    else:
        faqNumber = userIntent.replace(intentPrefix, '')
        return lookupFAQanswers(faqNumber)

# Respond to the user with a list and set of buttons representing the different FAQs
def lookupFAQs(intentPrefix):
    faqs = pullDataFromDB(ListOfFAQs)
    response = formatLookupFAQsResponse(faqs)
    buttons = createButtons(faqs, 'FAQID', "#", intentPrefix)
    buttons.append(MainMenuButton)
    return chatBotMessage(response, buttons, False)

# Respond to the user with the FAQ and answer(s) indicated by 'faqNumber'
def lookupFAQanswers(faqNumber):
    answers =pullDataFromDB(AnswerRecord, faqNumber)
    response = formatLookupFAQanswersResponse(faqNumber, answers)
    buttons = [FAQsBackButton, MainMenuButton]
    return chatBotMessage(response, buttons, False)

# Forma a list of all FAQs available for the user to review
def formatLookupFAQsResponse(faqs):
    response = LookupFAQsResponse 
    for faq in faqs:
        response += f"{faq['FAQID']}. {faq['Question']}\n"
    response += "\nChoose an FAQ answer below:"
    return response

# Format a response that includes a specific FAQ and its answers
def formatLookupFAQanswersResponse(faqNumber, answers):
    if answers:      # if answers were found, prep a response
        response = f"FAQ #{faqNumber}:\n\n"
        for answer in answers:
            response += f"{answer['Question']}\n\n"
            response += f"Answer: {answer['Answer']}\n"
    else:            # if no answers were found, prep a response stating so
        response = f"I could not find an answer for FAQ #{faqNumber}."
    return response


# Run the Chatbot when this file is executed
if __name__ == '__main__':
    app.run(debug=DebuggerOn)   # Shows detailed error messages if DebuggerOn
