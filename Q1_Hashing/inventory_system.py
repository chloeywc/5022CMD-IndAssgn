"""
Command-line Pharmacy Inventory System built on the generic HashTable.
"""
import time

from hash_table import HashTable
from product import Product

TABLE_CAPACITY = 101  # prime number spreads keys more evenly


def load_sample_products():
    """Return the pre-defined products the system starts with."""
    return [
        Product(1042, "Paracetamol 500mg", "Painkiller", 5.90, 120),
        Product(1143, "Ibuprofen 200mg", "Painkiller", 8.50, 80),
        Product(2001, "Amoxicillin 250mg", "Antibiotic", 15.00, 40, True),
        Product(2105, "Cetirizine 10mg", "Antihistamine", 12.80, 60),
        Product(3010, "Vitamin C 1000mg", "Supplement", 22.90, 150),
        Product(3500, "Omeprazole 20mg", "Antacid", 18.40, 35, True),
    ]


def linear_search(products, product_id):
    """Search a plain list one item at a time (used for comparison)."""
    for product in products:
        if product.product_id == product_id:
            return product
    return None


def get_int(prompt):
    """Keep asking until the user enters a valid non-negative whole number."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("  Please enter a valid whole number.")


def get_float(prompt):
    """Keep asking until the user enters a valid non-negative number."""
    while True:
        try:
            value = float(input(prompt))
            if value >= 0:
                return value
        except ValueError:
            pass
        print("  Please enter a valid number.")


def insert_product(table, products):
    """Ask for product details and insert the product into the hash table."""
    product_id = get_int("Enter Product ID: ")
    if table.search(product_id) is not None:
        print("  A product with this ID already exists.")
        return

    name = input("Enter Product Name: ").strip()
    category = input("Enter Category: ").strip()
    price = get_float("Enter Price (RM): ")
    stock = get_int("Enter Stock Quantity: ")
    needs_rx = input("Requires prescription? (y/n): ").strip().lower() == "y"

    product = Product(product_id, name, category, price, stock, needs_rx)
    slot = table.insert(product_id, product)
    products.append(product)
    print(f"Product inserted successfully into slot [{slot}]")


def search_product(table, products):
    """Search by ID in both the hash table and the list, and compare times."""
    product_id = get_int("Enter Product ID to search: ")

    start = time.perf_counter_ns()
    result = table.search(product_id)
    hash_time = time.perf_counter_ns() - start

    start = time.perf_counter_ns()
    linear_search(products, product_id)
    array_time = time.perf_counter_ns() - start

    if result is None:
        print("Product not found.")
    else:
        print("Product Found!")
        print(result)
    print(f"Search time - Hash Table: {hash_time:,} ns | Array: {array_time:,} ns")


def main():
    table = HashTable(TABLE_CAPACITY)
    products = []  # same data in a plain list, for comparison

    for product in load_sample_products():
        table.insert(product.product_id, product)
        products.append(product)
    print(f"Loaded {len(table)} sample products.")

    while True:
        print("\n==== Pharmacy Inventory System ====")
        print("1. Insert Product")
        print("2. Search Product")
        print("3. Exit")
        choice = input("Enter choice: ").strip()

        if choice == "1":
            insert_product(table, products)
        elif choice == "2":
            search_product(table, products)
        elif choice == "3":
            print("Exiting Inventory System. Goodbye!")
            break
        else:
            print("  Invalid choice, please enter 1-3.")


if __name__ == "__main__":
    main()