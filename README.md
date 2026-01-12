# CNCS Support Chatbot

> An intelligent customer support chatbot powered by Flask and Ollama AI, featuring natural language conversations and database-driven support capabilities.

## Key Features

### AI-Powered Conversations
Ask questions naturally and get intelligent responses powered by Ollama's language models. The chatbot understands context and provides helpful answers based on your company's knowledge base.

### Smart Database Integration
- **Contact Lookup** - Find department contacts instantly
- **Product Search** - Browse products by category with real-time pricing
- **Order Tracking** - Check order status and view detailed breakdowns
- **FAQ System** - Access frequently asked questions

### Multi-Turn Conversations
The chatbot maintains conversation context across multiple exchanges, allowing for natural follow-up questions and continuous dialogue.

---

## Demo

### Interactive Chatbot Experience
Watch Suppo in action - handling customer inquiries, looking up contact information, and providing AI-powered responses:

![Image](https://github.com/user-attachments/assets/078a040b-24ac-4a97-a468-c8e8ead42351)

### Responsive & Resizable Interface
Adaptable to your screen size and preference!

![Image](https://github.com/user-attachments/assets/6d9e6d95-6db7-479f-b7b6-7272e9f94f8e)

### Light & Dark Mode Toggle
Adjust to your personal preference!

![Image](https://github.com/user-attachments/assets/31ddc1bc-339e-49b7-a8d1-08169d377dfe)
---

## Quick Start

### Prerequisites
- Python 3.11+
- Ollama (for AI features)
- Flask
### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cncs-chatbot.git
cd cncs-chatbot

# Install dependencies
pip install flask

# Install Ollama and pull a model
ollama pull llama3.2

# Initialize the database
python create_database.py

# Run the application
python app.py
```

Visit `http://localhost:5000` to start chatting with Suppo!

---

## Architecture

```
┌─────────────────┐
│   Flask App     │  ← Main application server
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
┌───▼───┐ ┌──▼──────┐
│SQLite │ │ Ollama  │  ← AI processing
│  DB   │ │  LLM    │
└───────┘ └─────────┘
```

---

## New AI Features

### Natural Language Understanding
- Ask questions in your own words
- Get contextual responses based on your company data
- Conversation memory across multiple exchanges

### Intelligent Knowledge Base
The AI has access to:
- All department contacts and information
- Complete product catalog with pricing
- Full FAQ database
- Order tracking capabilities

### Session Management
Each user gets their own conversation session, ensuring personalized and contextual interactions.

---

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite3
- **AI Engine**: Ollama (LLaMA 3.2)
- **Frontend**: JavaScript
- **Styling**: Custom CSS with dark/light themes

---

## Usage Examples

**Finding Products:**
> "Show me your gaming laptops"
> "What monitors do you have under $500?"

**Order Tracking:**
> "What's the status of order #3?"
> "When will my order arrive?"

**General Questions:**
> "What's your return policy?"
> "How can I contact technical support?"

---

## Features

- ✅ Real-time AI responses
- ✅ Conversation context memory
- ✅ Dark/Light theme toggle
- ✅ Resizable chat window
- ✅ Mobile-responsive design
- ✅ Typing indicators
- ✅ Database-driven content
- ✅ Session-based conversations

---

## Project Structure

```
cncs-chatbot/
├── app.py                 # Main Flask application
├── create_database.py     # Database setup script
├── cncs_chatbot.db       # SQLite database
├── templates/
│   └── index.html        # Main webpage
└── static/
    ├── chatbot.css       # Chatbot styling
    └── chatbot.js        # Frontend logic
```

---

## Configuration

Edit `app.py` to customize:

```python
OLLAMA_MODEL = "llama3.2"  # Change AI model
DebuggerOn = True          # Toggle debug mode
UserID = 1                 # Default user for demo
```

---

## 📄 License

MIT License - Feel free to use and modify for your projects!

---


