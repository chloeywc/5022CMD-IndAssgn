"""
Small helpers for a clean, consistent command-line interface.
Colours use standard ANSI codes, supported by PyCharm and most terminals.
"""
import os

os.system("")  # enables colour codes on Windows terminals; harmless on macOS

WIDTH = 70

BOLD = "\033[1m"
DIM = "\033[2m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"


def banner(title, subtitle=""):
    """Large title shown once when the program starts."""
    print(CYAN + "=" * WIDTH + RESET)
    print(BOLD + title.center(WIDTH) + RESET)
    if subtitle:
        print(DIM + subtitle.center(WIDTH) + RESET)
    print(CYAN + "=" * WIDTH + RESET)


def section(title):
    """Heading line that starts each screen, e.g. ── SEARCH PRODUCT ──────."""
    print()
    print(BOLD + CYAN + f"── {title} " + "─" * (WIDTH - len(title) - 4) + RESET)


def line():
    print("  " + "-" * (WIDTH - 2))


def success(message):
    print(GREEN + "✔ " + message + RESET)


def error(message):
    print(RED + "✘ " + message + RESET)


def warning(message):
    print(YELLOW + "! " + message + RESET)


def info(message):
    print(DIM + message + RESET)


def pause():
    """Wait so the user can read the result before the menu appears again."""
    input(DIM + "\nPress Enter to return to the menu..." + RESET)