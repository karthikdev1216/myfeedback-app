import os
import sqlite3
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from dotenv import load_dotenv

from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Load environment variables from .env file
env_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
CORS(app)

# Debug: Print if env vars are loaded (masking the token)
token = os.getenv('TELEGRAM_BOT_TOKEN')
print(f"DEBUG: TELEGRAM_BOT_TOKEN loaded: {'Yes' if token else 'No'}")
print(f"DEBUG: TELEGRAM_CHAT_ID loaded: {os.getenv('TELEGRAM_CHAT_ID')}")

# Rate Limiter Setup
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

# Database Setup
DB_PATH = os.getenv('DATABASE_URL', 'feedback.db')
if DB_PATH.startswith('sqlite:///'):
    DB_PATH = DB_PATH.replace('sqlite:///', '')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            rating INTEGER NOT NULL,
            experience TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# Telegram Integration
def send_telegram_message(name, email, rating, experience):
    bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    chat_id = os.getenv('TELEGRAM_CHAT_ID')
    
    if not bot_token or not chat_id:
        print("Telegram configuration missing. Skipping message.")
        return False

    message = (
        f"🌟 *New Feedback Received*\n\n"
        f"👤 *Name:* {name}\n"
        f"📧 *Email:* {email}\n"
        f"⭐ *Rating:* {rating}/5\n"
        f"📝 *Experience:* {experience}"
    )
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.ok:
            print("Telegram message sent successfully!")
            return True
        else:
            print(f"Telegram API Error: {response.status_code} - {response.text}")
            return False
    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False

@app.route('/submit-feedback', methods=['POST'])
@limiter.limit("5 per minute")
def submit_feedback():
    data = request.json
    
    # Validation
    name = data.get('name')
    email = data.get('email')
    rating = data.get('rating')
    experience = data.get('experience')

    if not all([name, email, rating, experience]):
        return jsonify({"error": "All fields are required"}), 400
    
    if not isinstance(rating, int) or not (1 <= rating <= 5):
        return jsonify({"error": "Rating must be between 1 and 5"}), 400

    # Store in Database
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO feedback (name, email, rating, experience) VALUES (?, ?, ?, ?)",
            (name, email, rating, experience)
        )
        conn.commit()
        conn.close()
    except Exception as e:
        return jsonify({"error": f"Database error: {str(e)}"}), 500

    # Send Telegram Notification
    send_telegram_message(name, email, rating, experience)

    return jsonify({"message": "Feedback submitted successfully! Thank you."}), 201

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=5000)
