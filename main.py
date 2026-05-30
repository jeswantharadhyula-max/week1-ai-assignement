import json
import random
import datetime
import os

DATA_FILE = 'tips.json'
OUTPUT_FILE = 'output.txt'

def load_data():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        tips = data.get('tips', [])
        quotes = data.get('quotes', [])
    except Exception:
        tips = [
            "Break study sessions into 25-50 minute focused intervals.",
            "Teach the material to someone else.",
            "Use active recall and spaced repetition."
        ]
        quotes = [
            "Believe you can and you're halfway there. — Theodore Roosevelt",
            "Don't watch the clock; do what it does. Keep going. — Sam Levenson",
            "The future depends on what you do today. — Mahatma Gandhi"
        ]
    return tips, quotes


TIPS, QUOTES = load_data()


def save_output(category, text, name=None):
    ts = datetime.datetime.now().isoformat(sep=' ', timespec='seconds')
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
        header = f"[{ts}]"
        if name:
            header += f" {name}"
        header += f" | {category}\n"
        f.write(header)
        f.write(text + "\n\n")


def generate_tip():
    tip = random.choice(TIPS) if TIPS else "No tips available."
    print("\nStudy Tip:\n- " + tip + "\n")
    return tip


def generate_quote():
    quote = random.choice(QUOTES) if QUOTES else "No quotes available."
    print("\nMotivation Quote:\n- " + quote + "\n")
    return quote


def show_datetime():
    now = datetime.datetime.now()
    s = now.strftime("%Y-%m-%d %H:%M:%S")
    print("\nCurrent Date & Time:\n- " + s + "\n")
    return s


def main():
    name = input("What's your name? ").strip()
    if not name:
        name = "Student"
    print(f"\nHello, {name}! Welcome to Smart Student Assistant.\n")
    menu = (
        "1) Generate Study Tips\n"
        "2) Generate Motivation Quote\n"
        "3) Display Current Date & Time\n"
        "4) Exit\n"
    )
    while True:
        print("Menu:")
        print(menu)
        choice = input("Choose an option (1-4): ").strip()
        if choice == '1':
            result = generate_tip()
            save_output("Study Tip", result, name)
        elif choice == '2':
            result = generate_quote()
            save_output("Motivation Quote", result, name)
        elif choice == '3':
            result = show_datetime()
            save_output("DateTime", result, name)
        elif choice == '4' or choice.lower() == 'exit':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == '__main__':
    main()

