#!/usr/bin/env python3
import os
import sys
import time
import subprocess

# colors
BRIGHT_GREEN = "\033[92m"
RESET = "\033[0m"

def clear():
    os.system("clear")

def center_text(text):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    return text.center(width)

def ensure_mnemonic_installed():
    try:
        import mnemonic
        return True
    except ImportError:
        print("\nInstalling 'mnemonic' library...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mnemonic"], check=False)
    try:
        import mnemonic
        print("Library installed successfully!")
        time.sleep(1)
        return True
    except ImportError:
        print("Failed to import 'mnemonic'. Check environment.")
        return False

def ask_positive_int(prompt, min_value=1):
    while True:
        v = input(prompt).strip()
        if not v.isdigit() or int(v) < min_value:
            print(f"Please enter a positive integer >= {min_value}")
            continue
        return int(v)

def ask_interval(prompt, min_interval=0.5):
    while True:
        v = input(prompt).strip()
        try:
            f = float(v)
            if f < min_interval:
                print(f"Minimum interval is {min_interval} seconds")
                continue
            return f
        except ValueError:
            print("Please enter a valid number (e.g. 0.5)")

def generate_wallet_evm_flow():
    clear()
    print(center_text("=== EVM Wallet Generator (BIP39) ==="))
    print("\n")

    if not ensure_mnemonic_installed():
        input("\nPress [ENTER] to return...")
        return

    from mnemonic import Mnemonic
    m = Mnemonic("english")

    count = ask_positive_int("How many wallets to generate: ")
    interval = ask_interval("Interval between each wallet (min 0.5s): ", 0.5)

    clear()
    print(center_text("Generating wallets... ⏳⏳⏳"))
    time.sleep(2)
    print("\n")

    for i in range(count):
        seed_phrase = m.generate(strength=128)  # 12 words
        print(seed_phrase)
        if i < count - 1:
            time.sleep(interval)

    print("\nAll wallets generated! Press [ENTER] to return")
    input()

if __name__ == "__main__":
    generate_wallet_evm_flow()
