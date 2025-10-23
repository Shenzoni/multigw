#!/usr/bin/env python3
import os
import readchar
import time

# ---------- Colors ----------
BRIGHT_GREEN = "\033[92m"
RED          = "\033[31m"
PINK         = "\033[95m"
RESET        = "\033[0m"

# ---------- Menu Definitions ----------
main_menu = [
    ("         Gmail (Menu)", "Gmail"),
    ("         Crypto (Menu)", "Crypto"),
    ("         Exit", "Exit")
]

gmail_menu = [
    ("         DotTrick", "DotTrick"),
    ("         CapitalTrick (Telegram)", "CapitalTrick"),
    ("         Back", "Back"),
    ("         Exit", "Exit")
]

# ---------- Helpers ----------
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

# ---------- Gmail Helpers ----------
def gen_dot_variants(local):
    n = len(local)
    if n <= 1:
        yield local
        return
    total = 1 << (n - 1)
    cap = 512
    limit = min(total, cap)
    for mask in range(limit):
        parts = []
        for i, ch in enumerate(local):
            parts.append(ch)
            if i < n - 1 and ((mask >> i) & 1):
                parts.append('.')
        yield ''.join(parts)

def gen_capital_variants(local):
    n = len(local)
    if n == 0:
        yield local
        return
    total = 1 << n
    cap = 512
    limit = min(total, cap)
    for mask in range(limit):
        s = []
        for i, ch in enumerate(local):
            if ((mask >> i) & 1):
                s.append(ch.upper())
            else:
                s.append(ch.lower())
        yield ''.join(s)

def ask_generate_count():
    while True:
        v = input("Generate berapa : ").strip()
        if not v.isdigit() or int(v)<=0:
            print("Masukin angka bulat positif.")
            continue
        return int(v)

def output_with_count(variants_list, domain, requested_count, delay_per_item=0.5):
    printed = 0
    idx = 0
    total_variants = len(variants_list)
    if total_variants == 0:
        return
    while printed < requested_count:
        local_variant = variants_list[idx % total_variants]
        candidate = f"{local_variant}@{domain}"
        print(candidate)
        printed += 1
        idx += 1
        if printed < requested_count:
            time.sleep(delay_per_item)

# ---------- Gmail Flows ----------
def dottrick_flow():
    clear()
    print(center_text("=== DotTrick ==="))
    print("\n")
    gmail_input = input("Masukin Gmail lu : ").strip()
    if '@' not in gmail_input:
        print("\nInput gak valid. Contoh: contoh@gmail.com")
        input("\nTekan [ENTER] untuk kembali...")
        return

    local, domain = gmail_input.split('@', 1)
    local = local.strip()
    domain = domain.strip()

    unique_variants = list(gen_dot_variants(local))
    count = ask_generate_count()

    clear()
    print(center_text("Wait gua lagi generate ⏳⏳⏳"))
    time.sleep(2)
    print("\n")

    output_with_count(unique_variants, domain, count, delay_per_item=0.5)

    print("\nTekan [ENTER] untuk kembali")
    input()

def capitaltrick_flow():
    clear()
    print(center_text("=== CapitalTrick ==="))
    print("\n")
    gmail_input = input("Masukin Gmail lu : ").strip()
    if '@' not in gmail_input:
        print("\nInput gak valid. Contoh: contoh@gmail.com")
        input("\nTekan [ENTER] untuk kembali...")
        return

    local, domain = gmail_input.split('@', 1)
    local = local.strip()
    domain = domain.strip()

    unique_variants = list(gen_capital_variants(local))
    count = ask_generate_count()

    clear()
    print(center_text("Wait gua lagi generate ⏳⏳⏳"))
    time.sleep(2)
    print("\n")

    output_with_count(unique_variants, domain, count, delay_per_item=0.5)

    print("\nTekan [ENTER] untuk kembali")
    input()

# ---------- Menu Loops ----------
def gmail_menu_loop():
    selected = 0
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
                print("\nKeluar dari script...\n")
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
                clear()
                print(center_text("Crypto Menu placeholder"))
                input("\nTekan [ENTER] untuk kembali...")
            elif choice == "Exit":
                clear()
                print("\nKeluar dari script...\n")
                exit()

# ---------- Main ----------
if __name__ == "__main__":
    main_menu_loop()
