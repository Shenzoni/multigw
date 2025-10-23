#!/usr/bin/env python3
import os
import sys
import readchar
import datetime

# colors
BRIGHT_GREEN = "\033[92m"
BRIGHT_BLUE  = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
RESET = "\033[0m"
RED = "\033[31m"

# Main menu
main_menu = [
    ("         Gmail (Menu)", "Gmail"),
    ("         Crypto (Menu)", "Crypto"),
    ("         Exit", "Exit")
]

# Placeholder menus (spasi tetap)
gmail_menu = [
    ("         DotTrick", "DotTrick"),
    ("         CapitalTrick (Telegram)", "CapitalTrick"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

crypto_menu = [
    ("         Generate Wallet", "GenerateWallet"),
    ("         Batch Sender", "BatchSender"),
    ("         Batch Burn", "BatchBurn"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

# ----- Helpers -----
def clear():
    os.system("clear")

def center_text(text):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    return text.center(width)

def print_datetime_header():
    now = datetime.datetime.now()
    time_str = now.strftime("%I:%M %p")
    date_str = now.strftime("%A, %d %B %Y")
    print(center_text(time_str))
    print(center_text(date_str))
    print(center_text(f"{BRIGHT_MAGENTA}      🚨This script is free for use🚨{RESET}"))
    print(center_text(f"{BRIGHT_BLUE}             ▶ Telegram support{RESET} {BRIGHT_GREEN}: t.me/mnebdusk{RESET}"))
    print(center_text(" ▶ ©Copyright by ShenzoID ◀"))
    print("\n")

def print_menu(menu, selected, header):
    clear()
    print("\n")
    print_datetime_header()
    print(center_text(header))
    for i, (label, key) in enumerate(menu):
        color = BRIGHT_GREEN if key not in ["Exit"] else RED
        pointer = " ◀" if i == selected else ""
        print(center_text(f"{color}{label}{RESET}{pointer}"))
    print("\n")

def menu_loop(menu, header, actions=None):
    """
    menu: list of tuples (label, key)
    actions: dict {key: function}
    """
    selected = 0
    while True:
        print_menu(menu, selected, header)
        key = readchar.readkey()
        if key == readchar.key.UP:
            selected = (selected - 1) % len(menu)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(menu)
        elif key == readchar.key.ENTER:
            choice = menu[selected][1]
            if choice == "Exit":
                sys.exit()
            if actions and choice in actions:
                actions[choice]()
            else:
                print(center_text(f"Selected: {choice}"))
                input(center_text("Press [ENTER] to return"))

# ----- Gmail Actions -----
def load_gmail_actions():
    actions = {}
    try:
        from Gmail import dottrick
        from Gmail import captrick
        actions["DotTrick"] = dottrick.dottrick_flow
        actions["CapitalTrick"] = captrick.capitaltrick_flow
    except Exception as e:
        print("Gmail module missing:", e)
        actions["DotTrick"] = lambda: input("DotTrick placeholder [ENTER]")
        actions["CapitalTrick"] = lambda: input("CapitalTrick placeholder [ENTER]")
    actions["Back"] = lambda: None
    actions["Exit"] = sys.exit
    return actions

def gmail_menu_loop():
    actions = load_gmail_actions()
    menu_loop(gmail_menu, "=== Gmail Menu ===", actions)

# ----- Crypto Actions -----
def load_crypto_actions():
    actions = {}
    try:
        from Crypto import EVM_generator
        actions["GenerateWallet"] = EVM_generator.generate_wallet_evm_flow
    except Exception as e:
        print("Crypto module missing:", e)
        actions["GenerateWallet"] = lambda: input("GenerateWallet placeholder [ENTER]")
    actions["BatchSender"] = lambda: input("BatchSender placeholder [ENTER]")
    actions["BatchBurn"] = lambda: input("BatchBurn placeholder [ENTER]")
    actions["Back"] = lambda: None
    actions["Exit"] = sys.exit
    return actions

def crypto_menu_loop():
    actions = load_crypto_actions()
    menu_loop(crypto_menu, "=== Crypto Menu ===", actions)

# ----- Main Actions -----
def main_menu_actions():
    return {
        "Gmail": gmail_menu_loop,
        "Crypto": crypto_menu_loop,
        "Exit": sys.exit
    }

# ----- Main -----
def main():
    actions = main_menu_actions()
    menu_loop(main_menu, "=== Main Menu ===", actions)

if __name__ == "__main__":
    main()
