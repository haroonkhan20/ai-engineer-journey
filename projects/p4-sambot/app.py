from flask import Flask, render_template, request, jsonify
from groq import Groq
import os

API_KEY = os.environ.get("GROQ_API_KEY")

print(f"Key Loaded: {API_KEY[:10]}...")

app = Flask(__name__)
client = Groq(api_key=API_KEY)

conversation_history = []

SYSTEM_PROMPT = """You are SamBot, an intelligent AI assistant 
built by Mohammed Haroon Khan (HRK), an AI and Robotics Engineer.

Your personality:
- You are helpful, professional, and friendly
- You are knowledgeable about AI, robotics, Python, and engineering
- When asked who made you, say: "I was built by Mohammed Haroon Khan, an AI and Robotics Engineer"
- Never mention Samiteon or any company
- Never make up facts about your creator
- Keep responses clear and concise
- Answer general knowledge questions accurately and honestly"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")
    if not user_message:
        return jsonify({"reply": "Please say something!"})

    try:
        # Groq uses a cleaner message format
        conversation_history.append({
            "role": "user",
            "content": user_message
        })

        # Build messages list — system prompt + history
        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages += conversation_history

    
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   # free, fast, excellent
            messages=messages,
            max_tokens=1024
        )

        reply = response.choices[0].message.content.strip()

        conversation_history.append({
            "role": "assistant",
            "content": reply
        })

        return jsonify({"reply": reply})

    except Exception as e:
        print(f"ERROR: {e}")
        return jsonify({"reply": f"Error: {str(e)}"})

@app.route("/clear", methods=["POST"])
def clear():
    conversation_history.clear()
    return jsonify({"status": "Memory cleared!"})

if __name__ == "__main__":
    print("SamBot web server starting...")
    print("Open your browser at: http://localhost:5000")
    app.run(debug=True)