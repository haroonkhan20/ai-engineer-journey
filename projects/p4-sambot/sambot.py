# sambot.py
# SamBot — AI Assistant
# Built by: Mohammed Haroon Khan
# Skills: Google Gemini API, conversation memory, file saving

from google import genai
from datetime import datetime

# ── CONFIG ────────────────────────────────────
API_KEY   = "your-api-key-here"
BOT_NAME  = "SamBot"
YOUR_NAME = "Haroon"

# ── SETUP ─────────────────────────────────────
client = genai.Client(api_key=API_KEY)

# This is the memory — a list of all messages so far
# Each message is a dictionary with "role" and "text"
conversation_history = []

# ── SYSTEM PROMPT — gives the bot its personality ──
SYSTEM_PROMPT = f"""You are {BOT_NAME}, an intelligent AI assistant 
built by {YOUR_NAME} to learn AI.
You are helpful, professional, and knowledgeable about:
- Robotics and embedded systems
- AI and machine learning  
- Python programming
- Engineering concepts
Keep responses clear and concise."""

# ── FUNCTION 1: Send message and get reply ────
def chat(user_message):
    # Add user message to history
    conversation_history.append({
        "role": "user",
        "text": user_message
    })

    # Build full context — system prompt + all history
    full_context = SYSTEM_PROMPT + "\n\n"
    for msg in conversation_history:
        if msg["role"] == "user":
            full_context += f"User: {msg['text']}\n"
        else:
            full_context += f"{BOT_NAME}: {msg['text']}\n"

    # Send to Gemini
    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=full_context
    )

    # Extract reply text
    reply = response.text.strip()

    # Add bot reply to history — this is the MEMORY
    conversation_history.append({
        "role": "bot",
        "text": reply
    })

    return reply

# ── FUNCTION 2: Save chat to file ─────────────
def save_chat():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename  = f"chat_{timestamp}.txt"

    with open(filename, "w", encoding="utf-8") as f:
        f.write(f"SamBot Chat — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
        f.write("=" * 50 + "\n\n")
        for msg in conversation_history:
            if msg["role"] == "user":
                f.write(f"You    : {msg['text']}\n")
            else:
                f.write(f"SamBot : {msg['text']}\n")
            f.write("\n")

    print(f"\nChat saved to {filename}")

# ── FUNCTION 3: Show commands ──────────────────
def show_help():
    print("""
Commands:
  'quit'    — exit SamBot
  'save'    — save chat to file
  'clear'   — clear conversation memory
  'help'    — show this menu
    """)

# ── MAIN — the conversation loop ──────────────
def main():
    print("=" * 50)
    print(f"  Welcome to {BOT_NAME}")
    print(f"  Built by {YOUR_NAME}")
    print(f"  Type 'help' for commands")
    print("=" * 50 + "\n")

    while True:
        # Get user input
        user_input = input(f"You: ").strip()

        # Skip empty input
        if not user_input:
            continue

        # Handle commands
        if user_input.lower() == "quit":
            print(f"\n{BOT_NAME}: Goodbye {YOUR_NAME}! Have a great day!")
            save_chat()
            break

        elif user_input.lower() == "save":
            save_chat()

        elif user_input.lower() == "clear":
            conversation_history.clear()
            print(f"{BOT_NAME}: Memory cleared! Fresh start.")

        elif user_input.lower() == "help":
            show_help()

        else:
            # Normal message — send to AI
            print(f"\n{BOT_NAME}: ", end="", flush=True)
            reply = chat(user_input)
            print(reply)
            print()

if __name__ == "__main__":
    main()


