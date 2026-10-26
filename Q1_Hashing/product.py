"""
Entity class representing a single product sold by the pharmacy.
"""


class Product:
    """A pharmacy product, e.g. a medicine."""

    def __init__(self, product_id, name, category, price, stock,
                 requires_prescription=False):
        self.product_id = product_id                    # int: unique key for the hash table
        self.name = name                                # str: e.g. "Paracetamol 500mg"
        self.category = category                        # str: e.g. "Painkiller"
        self.price = price                              # float: price in RM
        self.stock = stock                              # int: units in stock
        self.requires_prescription = requires_prescription  # bool: True / False

    def __str__(self):
        """Format the product as one readable line."""
        rx = "Yes" if self.requires_prescription else "No"
        return (f"ID: {self.product_id} | Name: {self.name} | "
                f"Category: {self.category} | Price: RM{self.price:.2f} | "
                f"Stock: {self.stock} | Prescription: {rx}")


if __name__ == "__main__":
    p = Product(1042, "Paracetamol 500mg", "Painkiller", 5.9, 120)
    print(p)