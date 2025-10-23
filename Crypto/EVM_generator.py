#!/usr/bin/env python3
import os
import sys
import time
import subprocess

# Colors
BRIGHT_GREEN = "\033[92m"
BRIGHT_MAGENTA = "\033[95m"
RESET = "\033[0m"

def clear():
    os.system("clear")

def center_text(text):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    return text.center(width)

def ensure_libraries():
    """Ensure mnemonic and bip-utils are installed"""
    try:
        import mnemonic
        import bip_utils
        return True
    except ImportError:
        print("\nInstalling required libraries 'mnemonic' and 'bip-utils' ...")
        subprocess.run([sys.executable, "-m", "pip", "install", "mnemonic", "bip-utils"], check=False)
    try:
        import mnemonic
        import bip_utils
        print("Libraries installed successfully!")
        time.sleep(1)
        return True
    except ImportError:
        print("Failed to import libraries. Check your environment.")
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
    print(center_text("=== EVM Wallet Generator (BIP39 + Keys) ===\n"))

    if not ensure_libraries():
        input("\nPress [ENTER] to return...")
        return

    from mnemonic import Mnemonic
    from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

    mnemo = Mnemonic("english")

    count = ask_positive_int("How many wallets to generate: ")
    interval = ask_interval("Interval between each wallet (min 0.5s): ", 0.5)

    clear()
    print(center_text("Generating wallets... ⏳⏳⏳"))
    time.sleep(2)
    print("\n")

    for i in range(count):
        # Generate 12-word seed
        seed_phrase = mnemo.generate(strength=128)

        # Derive private/public key
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        bip44_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM).DeriveDefaultPath()
        private_key = bip44_wallet.PrivateKey().Raw().ToHex()
        public_key  = bip44_wallet.PublicKey().RawCompressed().ToHex()

        # Print with colors
        print(f"{BRIGHT_GREEN}Seed{i+1}: {seed_phrase}{RESET}")
        print(f"{BRIGHT_GREEN}Private Key: {private_key}{RESET}")
        print(f"{BRIGHT_MAGENTA}Public Key:  {public_key}{RESET}\n")

        if i < count - 1:
            time.sleep(interval)

    print("\nAll wallets generated! Press [ENTER] to return")
    input()

if __name__ == "__main__":
    generate_wallet_evm_flow()
