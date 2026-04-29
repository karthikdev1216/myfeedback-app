# Student Feedback Application

A full-stack web application for collecting student feedback with real-time Telegram notifications.

## Features
- **Modern UI**: Beautiful, glassmorphic design with responsive layout.
- **Star Rating**: Interactive 1-5 star rating system.
- **Telegram Integration**: Instant alerts when a new submission is received.
- **Database**: SQLite for local storage, ready for PostgreSQL in production.
- **Validation**: Frontend and Backend input validation.
- **Anti-Spam**: Submission debouncing on the frontend.

## Prerequisites
- Python 3.x
- A Telegram Bot (optional, but recommended for notifications)

## Setup Instructions

1. **Clone the project**
2. **Setup Backend**
   ```bash
   cd backend
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**
   - Create a `.env` file in the root directory (or in `backend/`).
   - Copy contents from `.env.example`.
   - Add your `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`.

4. **Run the Backend**
   ```bash
   python app.py
   ```
   The backend will run at `http://localhost:5000`.

5. **Run the Frontend**
   - Simply open `frontend/index.html` in your browser.
   - Alternatively, use a live server (like VS Code Live Server).

## Deployment

### Backend (Render / Railway)
- Use the `backend` folder.
- Set the start command to `gunicorn app:app`.
- Add your environment variables in the platform's dashboard.

### Frontend (Vercel / Netlify)
- Deploy the `frontend` folder as a static site.
- Update `API_URL` in `script.js` to point to your deployed backend.

## Telegram Bot Setup
1. Message `@BotFather` on Telegram to create a bot and get the `TOKEN`.
2. Message `@userinfobot` to get your `CHAT_ID`.
3. Add these to your `.env` file.
