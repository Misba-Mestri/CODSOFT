"""
╔══════════════════════════════════════════════════════════════╗
║         CODSOFT AI INTERNSHIP — TASK 1                       ║
║         Rule-Based Chatbot                                   ║
║         Author: Your Name | CodSoft AI Intern               ║
╚══════════════════════════════════════════════════════════════╝

WHAT IT DOES:
  A smart rule-based chatbot that uses pattern matching (regex)
  to understand user queries and provide relevant responses.
  Topics: greetings, name, time, weather, jokes, math, farewell.
"""

import re
import random
from datetime import datetime

# ─────────────────────────────────────────────
#  KNOWLEDGE BASE  (pattern → list of replies)
# ─────────────────────────────────────────────
RULES = [
    # Greetings
    (r"hi|hello|hey|howdy|hiya",
     ["Hello! 👋 How can I help you today?",
      "Hey there! What's on your mind?",
      "Hi! Great to see you. Ask me anything!"]),

    # How are you
    (r"how are you|how('s| is) it going|you good",
     ["I'm doing fantastic, thanks for asking! 😊",
      "Running on pure logic — couldn't be better!",
      "Great! I'm always happy to chat."]),

    # Name
    (r"what('s| is) your name|who are you|tell me about yourself",
     ["I'm **CodBot** 🤖 — your AI assistant built for the CodSoft internship!",
      "They call me CodBot. I'm a rule-based AI with big dreams!"]),

    # Time
    (r"what('s| is) the time|current time|time now",
     [f"The current time is ⏰ {datetime.now().strftime('%H:%M:%S')}"]),

    # Date
    (r"what('s| is) (the |today's )?date|today",
     [f"Today is 📅 {datetime.now().strftime('%A, %B %d, %Y')}"]),

    # Weather (mock — no API needed)
    (r"weather|temperature|forecast",
     ["I don't have live weather data, but it's always sunny inside a chatbot! ☀️",
      "Check weather.com for live updates, but I hear it's lovely outside!"]),

    # Jokes
    (r"tell me a joke|joke|make me laugh|funny",
     ["Why don't scientists trust atoms? Because they make up everything! 😄",
      "I told my computer I needed a break. Now it won't stop sending me Kit-Kat ads. 🍫",
      "Why do programmers prefer dark mode? Because light attracts bugs! 🐛"]),

    # Math
    (r"what is (\d+)\s*[\+plus]\s*(\d+)",
     ["MATH"]),  # handled specially below
    (r"what is (\d+)\s*[\-minus]\s*(\d+)",
     ["MATH_SUB"]),

    # Age of AI / interesting facts
    (r"what is ai|define ai|artificial intelligence",
     ["AI (Artificial Intelligence) is the simulation of human intelligence by machines. "
      "It includes machine learning, NLP, computer vision, and much more! 🧠"]),

    # Thanks
    (r"thank(s| you)|thx|ty",
     ["You're welcome! 😊", "Happy to help!", "Anytime! That's what I'm here for."]),

    # Bye
    (r"bye|goodbye|see you|exit|quit",
     ["Goodbye! 👋 Keep coding and learning!", "See you next time! 🚀", "Bye! Stay awesome!"]),

    # Help
    (r"help|what can you do|your features",
     ["I can help with:\n"
      "  💬 Greetings & small talk\n"
      "  ⏰ Current time & date\n"
      "  😄 Jokes\n"
      "  🔢 Simple math (e.g., 'what is 5 + 3')\n"
      "  🧠 AI facts\n"
      "  Just type anything and I'll try my best!"]),
]

# ─────────────────────────────────────────────
#  RESPONSE ENGINE
# ─────────────────────────────────────────────
def get_response(user_input: str) -> str:
    text = user_input.lower().strip()

    for pattern, responses in RULES:
        match = re.search(pattern, text)
        if match:
            # Special: math addition
            if responses == ["MATH"]:
                m = re.search(r"(\d+)\s*[\+plus]\s*(\d+)", text)
                if m:
                    result = int(m.group(1)) + int(m.group(2))
                    return f"🔢 {m.group(1)} + {m.group(2)} = **{result}**"

            # Special: math subtraction
            if responses == ["MATH_SUB"]:
                m = re.search(r"(\d+)\s*[\-minus]\s*(\d+)", text)
                if m:
                    result = int(m.group(1)) - int(m.group(2))
                    return f"🔢 {m.group(1)} - {m.group(2)} = **{result}**"

            return random.choice(responses)

    # Default fallback
    fallback = [
        "Hmm, I'm not sure about that. Try asking something else! 🤔",
        "Interesting question! I'm still learning. Type 'help' to see what I can do.",
        "I didn't quite catch that. Could you rephrase?"
    ]
    return random.choice(fallback)

# ─────────────────────────────────────────────
#  MAIN CHAT LOOP
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("   🤖  CodBot — Rule-Based AI Chatbot")
    print("   CodSoft AI Internship | Task 1")
    print("=" * 60)
    print("   Type 'help' to see what I can do.")
    print("   Type 'bye' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue

            response = get_response(user_input)
            print(f"CodBot: {response}\n")

            # Exit gracefully on bye
            if re.search(r"bye|goodbye|exit|quit", user_input.lower()):
                break

        except KeyboardInterrupt:
            print("\nCodBot: Goodbye! 👋")
            break

if __name__ == "__main__":
    main()
