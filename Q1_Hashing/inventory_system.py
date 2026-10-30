"""
Command-line Pharmacy Inventory System built on the generic HashTable.
"""
import time

import ui
from hash_table import HashTable
from product import Product

TABLE_CAPACITY = 101  # prime number spreads keys more evenly
LOW_STOCK = 20        # products below this stock level are flagged


def load_sample_products():
    """Return the pre-defined products the system starts with."""
    return [
        Product(1042, "Paracetamol 500mg", "Painkiller", 5.90, 120),
        Product(1143, "Ibuprofen 200mg", "Painkiller", 8.50, 80),
        Product(2001, "Amoxicillin 250mg", "Antibiotic", 15.00, 40, True),
        Product(2105, "Cetirizine 10mg", "Antihistamine", 12.80, 60),
        Product(3010, "Vitamin C 1000mg", "Supplement", 22.90, 150),
        Product(3500, "Omeprazole 20mg", "Antacid", 18.40, 15, True),
    ]


def linear_search(products, product_id):
    """Search a plain list one item at a time (used for comparison)."""
    for product in products:
        if product.product_id == product_id:
            return product
    return None


# ---------- input helpers ----------

def get_int(prompt):
    """Keep asking until the user enters a valid non-negative whole number."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        ui.error("Please enter a valid whole number.")


def get_float(prompt):
    """Keep asking until the user enters a valid non-negative number."""
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        ui.error("Please enter a valid number.")


# ---------- display helpers ----------

def show_menu():
    ui.section("MAIN MENU")
    print("  [1] Insert product        [5] View all products")
    print("  [2] Search product        [6] View hash table")
    print("  [3] Edit product          [7] Exit")
    print("  [4] Delete product")


def show_product(product):
    """Print one product as an easy-to-read card."""
    rx = "Required" if product.requires_prescription else "Not required"
    low = f"  {ui.YELLOW}(low stock){ui.RESET}" if product.stock < LOW_STOCK else ""
    print(f"  Product ID   : {product.product_id}")
    print(f"  Name         : {product.name}")
    print(f"  Category     : {product.category}")
    print(f"  Price        : RM {product.price:.2f}")
    print(f"  Stock        : {product.stock} units{low}")
    print(f"  Prescription : {rx}")


def probe_text(table, key, slot):
    """Describe how linear probing reached `slot`, e.g. '32 -> 33 (1 collision)'."""
    home = table.home_slot(key)
    steps = (slot - home) % table.capacity  # how many times we moved to the next slot
    if steps == 0:
        return f"{slot} (home slot, no collision)"
    path = " -> ".join(str((home + i) % table.capacity) for i in range(steps + 1))
    return f"{path} ({steps} collision(s), linear probing)"


# ---------- menu actions ----------

def insert_product(table, products):
    ui.section("INSERT PRODUCT")
    product_id = get_int("  Product ID     : ")
    if table.search(product_id) is not None:
        ui.error("A product with this ID already exists. Use Edit instead.")
        return

    name = input("  Name           : ").strip()
    category = input("  Category       : ").strip()
    price = get_float("  Price (RM)     : ")
    stock = get_int("  Stock quantity : ")
    needs_rx = input("  Prescription? (y/n): ").strip().lower() == "y"

    product = Product(product_id, name, category, price, stock, needs_rx)
    slot = table.insert(product_id, product)
    products.append(product)
    print()
    ui.success(f"Product inserted into slot [{slot}]")
    print(f"  Probe path   : {probe_text(table, product_id, slot)}")


def search_product(table, products):
    ui.section("SEARCH PRODUCT")
    product_id = get_int("  Product ID to search: ")

    start = time.perf_counter_ns()
    result = table.search(product_id)
    hash_time = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    linear_search(products, product_id)
    array_time = time.perf_counter_ns() - start

    print()
    if result is None:
        ui.error("Product not found.")
    else:
        slot = table.find_slot(product_id)
        ui.success(f"Product found in slot [{slot}]")
        show_product(result)
        print(f"  Probe path   : {probe_text(table, product_id, slot)}")
    print(f"  Search time  : Hash table {hash_time:,} ns | Array {array_time:,} ns")
    ui.info("  (Single measurement - see performance_test.py for the full experiment)")


def edit_product(table):
    ui.section("EDIT PRODUCT")
    product_id = get_int("  Product ID to edit: ")
    product = table.search(product_id)
    if product is None:
        ui.error("Product not found.")
        return

    print()
    show_product(product)
    ui.info("\n  Press Enter to keep the current value.")
    new_price = input(f"  New price (RM) [{product.price:.2f}]: ").strip()
    new_stock = input(f"  New stock      [{product.stock}]: ").strip()

    try:
        price = float(new_price) if new_price else product.price
        stock = int(new_stock) if new_stock else product.stock
    except ValueError:
        ui.error("Invalid number - no changes saved.")
        return
    if price < 0 or stock < 0:
        ui.error("Values cannot be negative - no changes saved.")
        return

    product.price = price   # the table and the list share the same object,
    product.stock = stock   # so both are updated at once
    print()
    ui.success("Product updated.")
    show_product(product)


def delete_product(table, products):
    ui.section("DELETE PRODUCT")
    product_id = get_int("  Product ID to delete: ")
    product = table.search(product_id)
    if product is None:
        ui.error("Product not found.")
        return

    print()
    show_product(product)
    confirm = input(f"\n  Delete this product? (y/n): ").strip().lower()
    if confirm != "y":
        ui.info("  Delete cancelled.")
        return

    slot = table.delete(product_id)
    products.remove(product)
    ui.success(f"Product deleted. Slot [{slot}] is now marked DELETED (tombstone).")


def view_all_products(table):
    ui.section("ALL PRODUCTS")
    products = [value for _, status, _, value in table.slots() if status == "OCCUPIED"]
    if not products:
        ui.info("  No products in the system.")
        return
    products.sort(key=lambda p: p.product_id)

    print(ui.BOLD + f"  {'ID':<6}{'Name':<22}{'Category':<15}{'Price':>9}{'Stock':>7}  Rx" + ui.RESET)
    ui.line()
    for p in products:
        price = f"RM{p.price:.2f}"
        rx = "Yes" if p.requires_prescription else "No"
        row = f"  {p.product_id:<6}{p.name[:21]:<22}{p.category[:14]:<15}{price:>9}{p.stock:>7}  {rx}"
        if p.stock < LOW_STOCK:
            row = ui.YELLOW + row + "  (low stock)" + ui.RESET
        print(row)
    ui.line()
    print(f"  {len(products)} product(s) | Low stock = below {LOW_STOCK} units")


def view_hash_table(table):
    ui.section("HASH TABLE VIEW")
    print(ui.BOLD + f"  {'Slot':>4} | {'Status':<8} | {'Home':>4} | Product" + ui.RESET)
    ui.line()
    for index, status, key, product in table.slots():
        if status == "EMPTY":
            continue
        if status == "DELETED":
            print(ui.DIM + f"  {index:>4} | {'DELETED':<8} | {'-':>4} | (tombstone)" + ui.RESET)
            continue
        home = table.home_slot(key)
        row = f"  {index:>4} | {status:<8} | {home:>4} | {product.product_id} {product.name}"
        if home != index:
            row += ui.YELLOW + "  <- collision, probed" + ui.RESET
        print(row)
    ui.line()
    print(f"  Stored: {len(table)} | Capacity: {table.capacity} | "
          f"Load factor: {table.load_factor():.2f}")
    ui.info("  Empty slots are hidden.")


# ---------- main program ----------

def main():
    table = HashTable(TABLE_CAPACITY)
    products = []  # same data in a plain list, for comparison

    for product in load_sample_products():
        table.insert(product.product_id, product)
        products.append(product)

    ui.banner("PHARMACY INVENTORY SYSTEM",
              "Hash Table | Open Addressing | Linear Probing")
    ui.info(f"Loaded {len(table)} sample products.")

    actions = {
        "1": lambda: insert_product(table, products),
        "2": lambda: search_product(table, products),
        "3": lambda: edit_product(table),
        "4": lambda: delete_product(table, products),
        "5": lambda: view_all_products(table),
        "6": lambda: view_hash_table(table),
    }

    while True:
        show_menu()
        choice = input("\n  Enter choice: ").strip()

        if choice == "7":
            ui.success("Exiting Inventory System. Goodbye!")
            break
        if choice in actions:
            actions[choice]()
            ui.pause()
        else:
            ui.error("Invalid choice, please enter 1-7.")


if __name__ == "__main__":
    main()