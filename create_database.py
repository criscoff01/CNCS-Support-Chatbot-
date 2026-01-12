"""
CNCS Chatbot Database Setup
Creates and populates the SQLite database with sample data
"""

import sqlite3

DATABASE_NAME = 'cncs_chatbot.db'


def create_database():
    """Create database and populate with sample data."""
    db = sqlite3.connect(DATABASE_NAME)
    cursor = db.cursor()

    # Clear existing data (for development/testing)
    clear_existing_tables(cursor)

    # Create tables
    create_contacts_table(cursor)
    create_products_table(cursor)
    create_orders_table(cursor)
    create_order_details_table(cursor)
    create_faqs_table(cursor)

    # Populate tables
    populate_contacts(cursor)
    populate_products(cursor)
    populate_orders(cursor)
    populate_order_details(cursor)
    populate_faqs(cursor)

    db.commit()
    db.close()
    print("Database created and populated successfully!")


def clear_existing_tables(cursor):
    """Remove existing data for clean setup."""
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    for table in tables:
        cursor.execute(f"DELETE FROM {table[0]};")


def create_contacts_table(cursor):
    """Create Contacts table."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Contacts (
            ContactID INTEGER PRIMARY KEY AUTOINCREMENT,
            Department TEXT NOT NULL,
            Email TEXT,
            Phone TEXT
        )
    ''')


def create_products_table(cursor):
    """Create Products table."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Products (
            ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
            ProductName TEXT NOT NULL,
            Category TEXT,
            Price REAL,
            StockQuantity INTEGER
        )
    ''')


def create_orders_table(cursor):
    """Create Orders table."""
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


def create_order_details_table(cursor):
    """Create OrderDetails table."""
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


def create_faqs_table(cursor):
    """Create FAQs table."""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS FAQs (
            FAQID INTEGER PRIMARY KEY AUTOINCREMENT,
            Question TEXT NOT NULL,
            Answer TEXT NOT NULL
        )
    ''')


def populate_contacts(cursor):
    """Insert sample contact data."""
    contacts = [
        ('Sales', 'sales@cybernet.com', '555-SALES-123'),
        ('Technical Support', 'support@cybernet.com', '555-TECH-123'),
        ('Customer Service', 'service@cybernet.com', '555-CUST-123'),
        ('Returns', 'returns@cybernet.com', '555-RETN-123'),
        ('Billing', 'billing@cybernet.com', '555-BILL-123'),
        ('Shipping', 'shipping@cybernet.com', '555-SHIP-123'),
        ('Corporate', 'corporate@cybernet.com', '555-CORP-123'),
        ('Marketing', 'marketing@cybernet.com', '555-MRKT-123'),
        ('HR', 'hr@cybernet.com', '555-HR12-123'),
    ]
    cursor.executemany(
        'INSERT INTO Contacts (Department, Email, Phone) VALUES (?, ?, ?)',
        contacts
    )


def populate_products(cursor):
    """Insert sample product data."""
    products = [
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
        ('HD Webcam', 'Accessories', 79.99, 18),
    ]
    cursor.executemany(
        'INSERT INTO Products (ProductName, Category, Price, StockQuantity) VALUES (?, ?, ?, ?)',
        products
    )


def populate_orders(cursor):
    """Insert sample order data."""
    orders = [
        (1, '2025-3-16 14:30:00', 1359.98, 'Delivered'),
        (1, '2025-3-17 09:15:00', 699.99, 'Shipped'),
        (1, '2025-3-18 16:45:00', 179.98, 'Processing'),
        (1, '2025-3-19 11:20:00', 2599.98, 'Delivered'),
        (1, '2025-3-20 08:10:00', 159.99, 'Pending'),
    ]
    cursor.executemany(
        'INSERT INTO Orders (UserID, OrderDate, TotalAmount, Status) VALUES (?, ?, ?, ?)',
        orders
    )


def populate_order_details(cursor):
    """Insert sample order details."""
    details = [
        (1, 1, 1, 1299.99),
        (1, 5, 1, 59.99),
        (2, 7, 1, 699.99),
        (3, 5, 1, 59.99),
        (3, 6, 1, 119.99),
        (4, 2, 1, 1899.99),
        (4, 7, 1, 699.99),
        (5, 9, 1, 159.99),
    ]
    cursor.executemany(
        'INSERT INTO OrderDetails (OrderID, ProductID, Quantity, Subtotal) VALUES (?, ?, ?, ?)',
        details
    )


def populate_faqs(cursor):
    """Insert sample FAQ data."""
    faqs = [
        ('What is your return policy?',
         'You can return any unopened product within 30 days of purchase for a full refund. '
         'Opened products may be eligible for exchange or store credit.'),
        ('How long does shipping take?',
         'Standard shipping takes 3-5 business days. Express shipping is 1-2 business days. '
         'International shipping may take 7-14 business days.'),
        ('Do you offer technical support?',
         'Yes, we offer technical support for all our products. '
         'You can reach our support team at support@cybernet.com or call 555-TECH-HELP.'),
        ('What payment methods do you accept?',
         'We accept Visa, Mastercard, American Express, PayPal, and Apple Pay.'),
        ('How do I track my order?',
         'You can track your order by selecting Track Order Status from the Main Menu '
         'and entering your order number, then I can help you locate the details!'),
        ('Do you offer warranties?',
         'Yes, all our products come with a standard 1-year manufacturer warranty. '
         'Extended warranties are available for purchase.'),
        ('Can I cancel my order?',
         'Orders can be canceled within 1 hour of placement. '
         'After that, please contact customer service for assistance.'),
        ('Do you ship internationally?',
         'Yes, we ship to most countries worldwide. '
         'International shipping costs and delivery times vary by location.'),
        ('How can I contact customer service?',
         'You can reach customer service at service@cybernet.com, '
         'via live chat on our website, or by calling 555-CUSTOMER.'),
    ]
    cursor.executemany(
        'INSERT INTO FAQs (Question, Answer) VALUES (?, ?)',
        faqs
    )


if __name__ == '__main__':
    create_database()
