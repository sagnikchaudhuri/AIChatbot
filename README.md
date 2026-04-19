# AI Business Chatbot (Groq Powered)

## Setup

1. Install dependencies
pip install -r requirements.txt

2. Set API Key
export GROQ_API_KEY=your_key

3. Run server
python backend/app.py

4. Open frontend/index.html

## Features
- FAQ handling
- AI responses (Groq)
- Lead capture (SQLite)

## Usage
Send:
- Normal questions → bot replies
- "I want to join" → lead capture triggered
- "Name, Phone" → saved in DB