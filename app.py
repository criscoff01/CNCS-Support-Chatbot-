"""
CNCS Support Chatbot - Flask Application
Responsible only for wiring up routes and delegating to handlers.
"""

from flask import Flask, render_template, request, jsonify
from config import DEBUG_MODE, Intent
from handlers import process_intent

app = Flask(__name__)

# =============================================================================
# Routes
# =============================================================================

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')


@app.route('/api/chat', methods=['POST'])
def chat():
    """Receive a chat request and return a handler response."""
    data = request.json

    intent    = data.get('userIntent',    Intent.GREETING)
    user_text = data.get('userTypedText', '')
    session_id = data.get('sessionId',   '')

    print(f"\n=== SESSION: {session_id} ===")
    print(f"Intent:  {intent}")
    print(f"Text:    {user_text}")

    result = process_intent(intent, user_text, session_id)
    return jsonify(result)

# =============================================================================
# Entry Point
# =============================================================================

if __name__ == '__main__':
    app.run(debug=DEBUG_MODE)
