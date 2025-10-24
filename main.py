#!/usr/bin/env python3
import os
import sys
import readchar
import datetime

# colors
BRIGHT_GREEN   = "\033[92m"
BRIGHT_BLUE    = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
RESET          = "\033[0m"
RED            = "\033[31m"

# main menu
main_menu = [
    ("         Gmail (Menu)", "Gmail"),
    ("         Crypto (Menu)", "Crypto"),
    ("         Exit", "Exit")
]

# crypto submenu (top)
crypto_menu = [
    ("         Generate Wallet", "GenerateWallet"),
    ("         Batch Sender", "BatchSender"),
    ("         Batch Burn", "BatchBurn"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

# generate-wallet menu (list chains)
generate_wallet_menu = [
    ("         EVM", "EVM"),
    ("         TON", "TON"),
    ("         SOL", "SOL"),
    ("         SUI", "SUI"),
    ("         APTOS", "APTOS"),
    ("         BITCOIN", "BITCOIN"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

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
        # Back and Exit are red per request
        color = RED if key in ["Exit", "Back"] else BRIGHT_GREEN
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

            # Exit always quits
            if choice == "Exit":
                clear()
                print("\nExiting script...\n")
                sys.exit(0)

            # Back returns to caller
            if choice == "Back":
                return

            # If an action exists, call it
            if actions and choice in actions:
                try:
                    actions[choice]()
                except Exception as e:
                    clear()
                    print(center_text("An error occurred while running action:"))
                    print(center_text(str(e)))
                    input(center_text("Press [ENTER] to return"))
                # after action returns, loop continues
            else:
                clear()
                print(center_text(f"Selected: {choice}"))
                input(center_text("Press [ENTER] to return"))

# ---------- Load Gmail actions (placeholders if missing) ----------
def load_gmail_actions():
    actions = {}
    try:
        from Gmail import dottrick, captrick
        actions["DotTrick"] = dottrick.dottrick_flow
        actions["CapitalTrick"] = captrick.capitaltrick_flow
    except Exception:
        actions["DotTrick"] = lambda: input(center_text("DotTrick module missing. Press [ENTER] to return"))
        actions["CapitalTrick"] = lambda: input(center_text("CapitalTrick module missing. Press [ENTER] to return"))
    actions["Back"] = lambda: None
    actions["Exit"] = lambda: None
    return actions

def gmail_menu_loop():
    gmail_menu = [
        ("         DotTrick", "DotTrick"),
        ("         CapitalTrick (Telegram)", "CapitalTrick"),
        ("         Back", "Back"),
        ("         Exit", "Exit")
    ]
    actions = load_gmail_actions()
    while True:
        menu_loop(gmail_menu, "=== Gmail Menu ===", actions)
        return  # back to main

# ---------- Load Crypto actions ----------
def load_crypto_actions():
    actions = {}
    try:
        from Crypto import EVM_generator
        actions["GenerateWallet"] = lambda: generate_wallet_menu_loop()
    except Exception:
        # ensure GenerateWallet still routes to our submenu even if module missing
        actions["GenerateWallet"] = lambda: generate_wallet_menu_loop()
    # placeholders for other crypto top-level items
    actions["BatchSender"] = lambda: input(center_text("Batch Sender placeholder. Press [ENTER] to return"))
    actions["BatchBurn"] = lambda: input(center_text("Batch Burn placeholder. Press [ENTER] to return"))
    actions["Back"] = lambda: None
    actions["Exit"] = lambda: None
    return actions

def crypto_menu_loop():
    actions = load_crypto_actions()
    while True:
        menu_loop(crypto_menu, "=== Crypto Menu ===", actions)
        return

# ---------- Generate Wallet submenu loop ----------
def generate_wallet_menu_loop():
    # load chain actions - EVM implemented, others placeholder that can be replaced by real modules
    chain_actions = {}
    try:
        from Crypto import EVM_generator
        chain_actions["EVM"] = EVM_generator.generate_wallet_evm_flow
    except Exception:
        chain_actions["EVM"] = lambda: input(center_text("EVM_generator module missing. Press [ENTER] to return"))

    # placeholders for non-implemented chains (can be replaced with real modules the same way)
    chain_actions["TON"] = lambda: input(center_text("TON generator placeholder. Press [ENTER] to return"))
    chain_actions["SOL"] = lambda: input(center_text("SOL generator placeholder. Press [ENTER] to return"))
    chain_actions["SUI"] = lambda: input(center_text("SUI generator placeholder. Press [ENTER] to return"))
    chain_actions["APTOS"] = lambda: input(center_text("APTOS generator placeholder. Press [ENTER] to return"))
    chain_actions["BITCOIN"] = lambda: input(center_text("BITCOIN generator placeholder. Press [ENTER] to return"))
    chain_actions["Back"] = lambda: None
    chain_actions["Exit"] = lambda: None

    # call the menu loop for generate_wallet_menu
    menu_loop(generate_wallet_menu, "=== Generate Wallet ===", chain_actions)
    # when Back is chosen, menu_loop returns here and we go back to Crypto menu

# ---------- Main ----------
def main():
    actions = {
        "Gmail": gmail_menu_loop,
        "Crypto": crypto_menu_loop,
        "Exit": lambda: sys.exit(0)
    }
    menu_loop(main_menu, "=== Main Menu ===", actions)

if __name__ == "__main__":
    main()
