# CNCS Support Chatbot

A Flask-based customer support chatbot for CyberNet Computer Systems (CNCS) that provides automated assistance for common customer inquiries including contact information, product searches, order tracking, and FAQ management.

## Features

The chatbot supports four main use cases:

- **Contact Information**: Find department contacts and contact details
- **Product Search**: Browse products by category with pricing and stock information
- **Order Tracking**: Check order status and view detailed order information
- **FAQ Management**: Access frequently asked questions and answers

## Project Structure

```
cncs-chatbot/
├── app.py                 # Main Flask application with chatbot logic
├── create_database.py     # Database initialization script
├── templates/
│   └── index.html        # Main webpage with embedded chatbot
├── static/
│   ├── chatbot.css       # Chatbot styling
│   └── chatbot.js        # Frontend JavaScript functionality
└── cncs_chatbot.db       # SQLite database (created after running setup)
```

## Requirements

- Python 3.11+
- Flask
- SQLite3 (included with Python)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/criscoff01/CNCS-Support-Chatbot-.git
   cd cncs-chatbot
   ```

2. **Install dependencies**
   ```bash
   pip install flask
   ```

3. **Initialize the database**
   ```bash
   python create_database.py
   ```
   This creates `cncs_chatbot.db` with sample data for testing.

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Access the chatbot**
   Open your web browser and navigate to `http://localhost:5000`

## Usage

### Main Interface
- The chatbot appears as a floating widget in the bottom-right corner
- Click the chat icon to open the chatbot interface
- Use the menu buttons to navigate between different support options

### Supported Operations

#### 1. Contact Information
- Select "Contact CNCS" from the main menu
- Choose a department to view contact details
- Available departments: Sales, Technical Support, Customer Service, Returns, Billing, Shipping, Corporate, Marketing, HR

#### 2. Product Search
- Select "Find a Product" from the main menu
- Browse by categories: Laptops, Desktops, Accessories, Monitors, Audio, Storage, Components
- View product names, prices, and stock quantities

#### 3. Order Tracking
- Select "Check Order Status" from the main menu
- Enter your order number when prompted (sample order numbers range from 1-5) 
- View order status, date, and total amount
- Option to see detailed item breakdown

#### 4. FAQ Access
- Select "Explore FAQs" from the main menu
- Browse available questions
- Click on any FAQ number to view the detailed answer

## Database Schema

The application uses SQLite with the following tables:

- **Contacts**: Department contact information
- **Products**: Product catalog with categories, prices, and stock
- **Orders**: Customer order records
- **OrderDetails**: Individual items within orders
- **FAQs**: Frequently asked questions and answers

## Configuration

Key configuration variables in `app.py`:

```python
DebuggerOn = True                    # Enable/disable Flask debug mode
NameOfChatBotDB = 'cncs_chatbot.db' # Database filename
UserID = 1                           # Default user ID for demo purposes
```

## API Endpoints

- `GET /` - Serves the main webpage with embedded chatbot
- `POST /api/chat` - Processes chatbot requests and returns responses

### API Request Format
```json
{
    "userTypedText": "user input text",
    "userIntent": "intent_category"
}
```

### API Response Format
```json
{
    "response": "chatbot response text",
    "buttons": [{"text": "Button Label", "value": "intent_value"}],
    "enableTextInput": false
}
```

## Customization

### Adding New Departments
1. Insert new records into the `Contacts` table
2. No code changes required - the chatbot automatically displays all departments

### Adding New Product Categories
1. Insert new products with desired categories into the `Products` table
2. The system automatically creates category buttons

### Modifying Responses
Edit the response constants in `app.py`:
- `InitialGreeting`
- `FindPOCResponse`
- `FindProductResponse`
- `TrackOrderResponse`
- `LookupFAQsResponse`

## Development Notes

- The chatbot uses a menu-driven approach rather than natural language processing
- User intents are determined by button clicks rather than text analysis
- All styling is contained in `static/chatbot.css`
- Frontend JavaScript handles UI interactions in `static/chatbot.js`
- Database operations are centralized in the `pullDataFromDB()` function

## Testing Data

The `create_database.py` script includes sample data for testing:
- 9 departments with contact information
- 11 products across various categories
- 5 sample orders for UserID 1
- 9 frequently asked questions

## Browser Compatibility

The chatbot interface is compatible with modern web browsers that support:
- ES6 JavaScript features
- CSS Flexbox
- SVG graphics

## License

[Add your license information here]



**Note**: This is a demonstration application with hardcoded sample data. For production use, consider implementing user authentication, input validation, and security measures appropriate for your environment.
