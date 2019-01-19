import json
import sys


class Products:
    def __init__(self):
        try:
            with open("products.json", "r") as products_file:
                self.products = json.load(products_file)

        except FileNotFoundError:
            sys.exit(1)

