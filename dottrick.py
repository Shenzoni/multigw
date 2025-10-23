#!/usr/bin/env python3
import os
import time

# colors (optional)
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

def gen_dot_variants(local):
    """
    Generate dot-variations for the local part.
    Includes original (mask=0). Caps unique combinations at 512.
    """
    n = len(local)
    if n <= 1:
        yield local
        return

    total = 1 << (n - 1)  # 2^(n-1) combinations between characters
    cap = 512
    limit = min(total, cap)

    for mask in range(limit):
        parts = []
        for i, ch in enumerate(local):
            parts.append(ch)
            if i < n - 1 and ((mask >> i) & 1):
                parts.append('.')
        yield ''.join(parts)

def ask_generate_count():
    while True:
        v = input("How many variants to generate: ").strip()
        if not v.isdigit() or int(v) <= 0:
            print("Please enter a positive integer (e.g. 10).")
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

def dottrick_flow():
    clear()
    print(center_text("=== DotTrick ==="))
    print("\n")
    gmail_input = input("Enter your Gmail: ").strip()
    if '@' not in gmail_input:
        print("\nInvalid input. Example: example@gmail.com")
        input("\nPress [ENTER] to return...")
        return

    local, domain = gmail_input.split('@', 1)
    local = local.strip()
    domain = domain.strip()

    unique_variants = list(gen_dot_variants(local))
    count = ask_generate_count()

    clear()
    print(center_text("Generating... ⏳⏳⏳"))
    time.sleep(2)
    print("\n")

    # print results left-aligned
    output_with_count(unique_variants, domain, count, delay_per_item=0.5)

    print("\nPress [ENTER] to return")
    input()

if __name__ == "__main__":
    dottrick_flow()
