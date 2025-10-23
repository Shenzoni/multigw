#!/usr/bin/env python3
import os
import sys
import time

# colors
BRIGHT_GREEN   = "\033[92m"
BRIGHT_MAGENTA = "\033[95m"
RESET          = "\033[0m"
RED            = "\033[31m"

def clear():
    os.system("clear")

def center_text(text):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    return text.center(width)

def check_requirements_or_warn():
    """
    Do NOT auto-install. If required packages are missing,
    show message and return False.
    """
    try:
        import mnemonic
        import bip_utils
        return True
    except Exception:
        # show the required message (in red)
        clear()
        print("\n")
        print(center_text(f"   {RED}Being lazy to read makes you stupid!!!{RESET}"))
        print(center_text(". If requirements.txt is not installed, please install it first"))
        print("\n")
        input(center_text("Press [ENTER] to return"))
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
    print(center_text("=== EVM Wallet Generator (BIP39 + Keys) ==="))
    print("\n")
    # If requirements not met, warn and return (NO auto-install)
    if not check_requirements_or_warn():
        return

    # Now safe to import libs
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
        seed_phrase = mnemo.generate(strength=128)
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        bip44_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM).DeriveDefaultPath()
        private_key = bip44_wallet.PrivateKey().Raw().ToHex()
        public_key  = bip44_wallet.PublicKey().RawCompressed().ToHex()

        # Print with colors
        print(f"{BRIGHT_GREEN}{i+1}. Seed: {seed_phrase}{RESET}")
        print(f"{BRIGHT_GREEN}   Private Key: {private_key}{RESET}")
        print(f"{BRIGHT_MAGENTA}   Public Key:  {public_key}{RESET}\n")

        if i < count - 1:
            time.sleep(interval)

    print("\nAll wallets generated! Press [ENTER] to return")
    input()

# If script called directly
if __name__ == "__main__":
    generate_wallet_evm_flow()
