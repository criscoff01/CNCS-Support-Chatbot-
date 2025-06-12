#References: 
#How to Easily Create a SQLite Database - https://youtu.be/XSZE1iiKdSw?si=yxt0BRMoEaMnlxvX 
#SQLite 3 Python Tutorial in 5 minutes - https://youtu.be/XSZE1iiKdSw?si=yxt0BRMoEaMnlxvX

import sqlite3

# Create a connection to a new SQLite database file (or connect to an existing one)
db = sqlite3.connect('cncs_chatbot.db')
cursor = db.cursor()

# ----------- This section is for test and debug only - will be removed for final product submission

# Retrieve the list of all current tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

# Delete previous data from each table to ensure only the data initialized below is resident after each run
for table in tables:
    table_name = table[0]
    cursor.execute(f"DELETE FROM {table_name};")

# ----------- End of test and debug code section


# Phase I Data 


# Use Case 1 - Find Contacts

# Create Points of Contact table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Contacts (
    ContactID INTEGER PRIMARY KEY AUTOINCREMENT,
    Department TEXT NOT NULL,
    Email TEXT,
    Phone TEXT
)
''')

# Insert sample data for Points of Contact
cursor.execute('''
INSERT INTO Contacts (Department, Email, Phone)
VALUES
    ('Sales', 'sales@cybernet.com', '555-SALES-123'),
    ('Technical Support', 'support@cybernet.com', '555-TECH-123'),
    ('Customer Service', 'service@cybernet.com', '555-CUST-123'),
    ('Returns', 'returns@cybernet.com', '555-RETN-123'),
    ('Billing', 'billing@cybernet.com', '555-BILL-123'),
    ('Shipping', 'shipping@cybernet.com', '555-SHIP-123'),
    ('Corporate', 'corporate@cybernet.com', '555-CORP-123'),
    ('Marketing', 'marketing@cybernet.com', '555-MRKT-123'),
    ('HR', 'hr@cybernet.com', '555-HR12-123')
''')

# Phase II Data


# Use Case 2 - Find Products

# Create Products table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Products (
    ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
    ProductName TEXT NOT NULL,
    Category TEXT,
    Price REAL,
    StockQuantity INTEGER
)
''')

# Insert sample data for Products
cursor.execute('''
INSERT INTO Products (ProductName, Category, Price, StockQuantity)
VALUES
    ('Gaming Laptop', 'Laptops', 1299.99, 15),
    ('Gaming Desktop', 'Desktops', 1899.99, 7),
    ('Business Ultrabook', 'Laptops', 999.99, 23),
    ('Desktop Workstation', 'Desktops', 1499.99, 10),
    ('Ergonomic Mouse', 'Accessories', 59.99, 50),
    ('Mechanical Keyboard', 'Accessories', 119.99, 30),
    ('32-inch 4K Monitor', 'Monitors', 699.99, 8),
    ('Wireless Headset', 'Audio', 129.99, 25),
    ('External SSD 1TB', 'Storage', 159.99, 40),
    ('RTX 5090 Graphics Card', 'Components', 1999.99, 1),
    ('HD Webcam', 'Accessories', 79.99, 18)
''')

# Phase III Data

# Use Case 3 - Check Order Status

# Create Orders table
cursor.execute('''
CREATE TABLE IF NOT EXISTS Orders (
    OrderID INTEGER PRIMARY KEY AUTOINCREMENT,
    UserID INTEGER,
    OrderDate DATETIME DEFAULT CURRENT_TIMESTAMP,
    TotalAmount REAL,
    Status TEXT CHECK(Status IN ('Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled')),
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
)
''')

# Insert sample data for Orders
cursor.execute('''
INSERT INTO Orders (UserID, OrderDate, TotalAmount, Status)
VALUES
    (1, '2025-3-16 14:30:00', 1359.98, 'Delivered'),
    (1, '2025-3-17 09:15:00', 699.99, 'Shipped'),
    (1, '2025-3-18 16:45:00', 179.98, 'Processing'),
    (1, '2025-3-19 11:20:00', 2599.98, 'Delivered'),
    (1, '2025-3-20 08:10:00', 159.99, 'Pending')
''')

# Create Order Details table
cursor.execute('''
CREATE TABLE IF NOT EXISTS OrderDetails (
    OrderDetailID INTEGER PRIMARY KEY AUTOINCREMENT,
    OrderID INTEGER,
    ProductID INTEGER,
    Quantity INTEGER,
    Subtotal REAL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
)
''')

# Insert sample data for Order Details
cursor.execute('''
INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Subtotal)
VALUES
    (1, 1, 1, 1299.99),
    (1, 5, 1, 59.99),
    (2, 7, 1, 699.99),
    (3, 5, 1, 59.99),
    (3, 6, 1, 119.99),
    (4, 2, 1, 1899.99),
    (4, 7, 1, 699.99),
    (5, 9, 1, 159.99)
''')

# Use Case 4 - Explore FAQs

# Create FAQs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS FAQs (
    FAQID INTEGER PRIMARY KEY AUTOINCREMENT,
    Question TEXT NOT NULL,
    Answer TEXT NOT NULL
)
''')

# Insert sample data for FAQs
cursor.execute('''
INSERT INTO FAQs (Question, Answer)
VALUES
    ('What is your return policy?', 'You can return any unopened product within 30 days of purchase for a full refund. Opened products may be eligible for exchange or store credit.'),
    ('How long does shipping take?', 'Standard shipping takes 3-5 business days. Express shipping is 1-2 business days. International shipping may take 7-14 business days.'),
    ('Do you offer technical support?', 'Yes, we offer technical support for all our products. You can reach our support team at support@cybernet.com or call 555-TECH-HELP.'),
    ('What payment methods do you accept?', 'We accept Visa, Mastercard, American Express, PayPal, and Apple Pay.'),
    ('How do I track my order?', 'You can track your order by selecting Track Order Status from the Main Menu and entering your order number, then I can help you locate the details!'),
    ('Do you offer warranties?', 'Yes, all our products come with a standard 1-year manufacturer warranty. Extended warranties are available for purchase.'),
    ('Can I cancel my order?', 'Orders can be canceled within 1 hour of placement. After that, please contact customer service for assistance.'),
    ('Do you ship internationally?', 'Yes, we ship to most countries worldwide. International shipping costs and delivery times vary by location.'),
    ('How can I contact customer service?', 'You can reach customer service at service@cybernet.com, via live chat on our website, or by calling 555-CUSTOMER.')
''')


# Commit changes and close connection
db.commit()
print("Database created and populated successfully!")
db.close()