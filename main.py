#!/usr/bin/env python3
import os
import sys
import readchar
import time

# ---------- Colors ----------
BRIGHT_GREEN = "\033[92m"
RED          = "\033[31m"
PINK         = "\033[95m"
RESET        = "\033[0m"

# ---------- Add repo folder to path ----------
sys.path.append(os.path.dirname(__file__))  # folder multigw harus sama dengan main.py

# ---------- Import modular scripts ----------
try:
    from dottrick import dottrick_flow
    from captrick import capitaltrick_flow
except ImportError:
    print("Failed to import Gmail modules. Make sure dottrick.py and captrick.py exist.")
    input("Press [ENTER] to exit...")
    sys.exit(1)

try:
    from EVM_generator import generate_wallet_evm_flow
    # Add other wallet modules later: SOLANA, TRON, TON, SUI, APTOS, BITCOIN
except ImportError:
    print("Failed to import wallet modules. Make sure EVM_generator.py exists.")
    input("Press [ENTER] to exit...")
    sys.exit(1)

# ---------- Menus ----------
main_menu = [
    ("         Gmail (Menu)", "Gmail"),
    ("         Crypto (Menu)", "Crypto"),
    ("         Exit", "Exit")
]

crypto_menu = [
    ("         Generate Wallet", "GenerateWallet"),
    ("         Batch Sender", "BatchSender"),
    ("         Batch Burn", "BatchBurn"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

generate_wallet_menu = [
    ("         EVM", "EVM"),
    ("         SOLANA", "SOLANA"),
    ("         TRON", "TRON"),
    ("         TON", "TON"),
    ("         SUI", "SUI"),
    ("         APTOS", "APTOS"),
    ("         BITCOIN", "BITCOIN"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

# ---------- Helper functions ----------
def clear():
    os.system("clear")

def center_text(text):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    return text.center(width)

def print_menu(menu, selected, header):
    clear()
    print("\n")
    print(center_text(header))
    print("\n")
    for i, (label, key) in enumerate(menu):
        color = BRIGHT_GREEN if key not in ["Exit", "Back"] else RED
        pointer = " ◀" if i == selected else ""
        print(center_text(f"{color}{label}{RESET}{pointer}"))
    print("\n")

# ---------- Menu Loops ----------
def generate_wallet_loop():
    selected = 0
    while True:
        print_menu(generate_wallet_menu, selected, "=== Generate Wallet ===")
        key = readchar.readkey()
        if key == readchar.key.UP:
            selected = (selected - 1) % len(generate_wallet_menu)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(generate_wallet_menu)
        elif key == readchar.key.ENTER:
            choice = generate_wallet_menu[selected][1]
            if choice == "EVM":
                generate_wallet_evm_flow()
            elif choice == "Back":
                return
            elif choice == "Exit":
                clear()
                print("\nExiting script...\n")
                exit()
            else:
                clear()
                print(center_text(f"{choice} selected - module not implemented yet"))
                input("\nPress [ENTER] to return")

def crypto_menu_loop():
    selected = 0
    while True:
        print_menu(crypto_menu, selected, "=== Crypto Menu ===")
        key = readchar.readkey()
        if key == readchar.key.UP:
            selected = (selected - 1) % len(crypto_menu)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(crypto_menu)
        elif key == readchar.key.ENTER:
            choice = crypto_menu[selected][1]
            if choice == "GenerateWallet":
                generate_wallet_loop()
            elif choice in ["BatchSender", "BatchBurn"]:
                clear()
                print(center_text(f"{choice} menu - module not implemented yet"))
                input("\nPress [ENTER] to return")
            elif choice == "Back":
                return
            elif choice == "Exit":
                clear()
                print("\nExiting script...\n")
                exit()

def gmail_menu_loop():
    selected = 0
    gmail_menu = [
        ("         DotTrick", "DotTrick"),
        ("         CapitalTrick (Telegram)", "CapitalTrick"),
        ("         Back", "Back"),
        ("         Exit", "Exit")
    ]
    while True:
        print_menu(gmail_menu, selected, "=== Gmail Menu ===")
        key = readchar.readkey()
        if key == readchar.key.UP:
            selected = (selected - 1) % len(gmail_menu)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(gmail_menu)
        elif key == readchar.key.ENTER:
            choice = gmail_menu[selected][1]
            if choice == "DotTrick":
                dottrick_flow()
            elif choice == "CapitalTrick":
                capitaltrick_flow()
            elif choice == "Back":
                return
            elif choice == "Exit":
                clear()
                print("\nExiting script...\n")
                exit()

def main_menu_loop():
    selected = 0
    while True:
        print_menu(main_menu, selected, "=== MAIN MENU ===")
        key = readchar.readkey()
        if key == readchar.key.UP:
            selected = (selected - 1) % len(main_menu)
        elif key == readchar.key.DOWN:
            selected = (selected + 1) % len(main_menu)
        elif key == readchar.key.ENTER:
            choice = main_menu[selected][1]
            if choice == "Gmail":
                gmail_menu_loop()
            elif choice == "Crypto":
                crypto_menu_loop()
            elif choice == "Exit":
                clear()
                print("\nExiting script...\n")
                exit()

# ---------- Main ----------
if __name__ == "__main__":
    main_menu_loop()
