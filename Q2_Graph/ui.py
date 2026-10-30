"""
Small helpers for a clean, consistent command-line interface.
"""
WIDTH = 70


def banner(title, subtitle=""):
    """Large title shown once when the program starts."""
    print("=" * WIDTH)
    print(title.center(WIDTH))
    if subtitle:
        print(subtitle.center(WIDTH))
    print("=" * WIDTH)


def section(title):
    """Heading line that starts each screen, e.g. ── SEARCH PRODUCT ──────."""
    print("\n")
    print(f"── {title} " + "─" * (WIDTH - len(title) - 4))


def line():
    print("  " + "-" * (WIDTH - 2))


def success(message):
    print("[OK] " + message)


def error(message):
    print("[ERROR] " + message)


def warning(message):
    print("[!] " + message)


def info(message):
    print(message)
