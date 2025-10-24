#!/usr/bin/env python3
import os
import sys
import time

# colors
BRIGHT_MAGENTA = "\033[95m"   # for Seed & Private Key (ungu terang)
BRIGHT_GREEN   = "\033[92m"   # for Public Key (hijau terang)
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

def warn_requirements_and_return():
    clear()
    print("\n")
    print(center_text(f"{RED}Being lazy to read makes you stupid!!!{RESET}"))
    print(center_text("If requirements.txt is not installed, please install it first"))
    print("\n")
    input(center_text("Press [ENTER] to return"))
    return

def check_requirements():
    """
    Do NOT auto-install. If missing, return False.
    """
    try:
        import mnemonic
        import bip_utils
        return True
    except Exception:
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
                # custom insult per request
                print(f"\n{RED}Why you set below minimal interval? Are you stupid?{RESET}\n")
                continue
            return f
        except ValueError:
            print("Please enter a valid number (e.g. 0.5)")

def generate_wallet_evm_flow():
    clear()
    print(center_text("=== EVM Wallet Generator (BIP39 + Keys) ==="))
    print("\n")

    # check dependencies - DO NOT auto-install
    if not check_requirements():
        warn_requirements_and_return()
        return

    # imports only if present
    from mnemonic import Mnemonic
    from bip_utils import Bip39SeedGenerator, Bip44, Bip44Coins

    mnemo = Mnemonic("english")

    # ask how many
    count = ask_positive_int("How many wallets do you want to generate? : ")

    # ask interval
    interval = ask_interval("Set interval (min 0.5 seconds) : ")

    clear()
    print(center_text("Generating wallets... ⏳⏳⏳"))
    time.sleep(2)
    print("\n")

    for i in range(1, count + 1):
        # generate 12-word seed
        seed_phrase = mnemo.generate(strength=128)

        # derive keys (EVM / ETH derivation via bip-utils)
        seed_bytes = Bip39SeedGenerator(seed_phrase).Generate()
        bip44_wallet = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM).DeriveDefaultPath()
        private_key = bip44_wallet.PrivateKey().Raw().ToHex()
        public_key  = bip44_wallet.PublicKey().ToAddress()  # address string (eth address)

        # print colored output per request
        print(f"{BRIGHT_MAGENTA}{i}. Seed phrase: {seed_phrase}{RESET}")
        print(f"{BRIGHT_MAGENTA}   Private key: {private_key}{RESET}")
        print(f"{BRIGHT_GREEN}   Public key : {public_key}{RESET}\n")

        if i < count:
            time.sleep(interval)

    print("\nAll wallets generated! Press [ENTER] to return")
    input()

# allow running this module directly
if __name__ == "__main__":
    generate_wallet_evm_flow()
