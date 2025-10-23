#!/usr/bin/env python3
import os
import sys
import readchar
import time
import datetime

# colors
BRIGHT_GREEN = "\033[92m"
BRIGHT_BLUE  = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
RESET = "\033[0m"
RED = "\033[31m"

# Main menu (spasi tetap dipertahankan)
main_menu = [
    ("         Gmail (Menu)", "Gmail"),
    ("         Crypto (Menu)", "Crypto"),
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
    time_str = now.strftime("%I:%M %p")  # 12-hour format + AM/PM
    date_str = now.strftime("%A, %d %B %Y")  # Day, DD Month YYYY
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

def menu_loop(menu, header):
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
            # Placeholder action
            print(center_text(f"Selected: {choice}"))
            input(center_text("Press [ENTER] to return"))

def main():
    menu_loop(main_menu, "=== Main Menu ===")                                                                                                           

if __name__ == "__main__":
    main()
