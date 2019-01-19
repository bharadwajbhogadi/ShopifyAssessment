import json

from flask import Flask, request, Response
from collections import defaultdict

from products import Products

app = Flask(__name__)

cart = defaultdict(list)


@app.route("/products", methods=["GET"])
def all_products():
    if request.method == "GET":
        available_inventory = request.args.get("available_inventory")
        products_list = Products().products

        if products_list.get("products") is None:
            return Response(status=404, content_type="application/json", response=json.dumps({"status": False}))

        if available_inventory.lower() == "true":
            inventory_list = defaultdict(list)

            for products in products_list["products"]:
                if int(products["inventory_count"]) > 0:
                    inventory_list["products"].append(products)

            return Response(status=200, content_type="application/json", response=json.dumps(inventory_list["products"]))
        elif available_inventory.lower() == "false":
            return Response(status=200, content_type="application/json", response=json.dumps(products_list["products"]))
        else:
            return Response(status=403)
    else:
        return Response(status=405)


@app.route("/product/<int:id>", methods=["GET"])
def get_single_product(id):
    if request.method == "GET":
        products_list = Products().products["products"]

        for product in products_list:
            if product.get("id") == id:
                return Response(status=200, content_type="application/json", response=json.dumps(product))

        return Response(status=404, content_type="application/json", response=json.dumps({"status": False}))
    else:
        return Response(status=405)


@app.route("/purchase", methods=["POST"])
def purchase_products():
    if request.method == "POST":

        shopping_cart = request.json

        products_list = Products().products

        purchase_status = defaultdict(list)

        for product in products_list["products"]:
            for item in shopping_cart["shopping_cart"]:

                if item.get("id") == product.get("id"):
                    if product.get("inventory_count") >= item.get("count"):
                        product["inventory_count"] -= item.get("count")
                        purchase_status["status"].append({
                            "id": item.get("id"),
                            "purchase_status": "Successful"
                        })
                    else:
                        purchase_status["status"].append({
                            "id": item.get("id"),
                            "purchase_status": "Not enough inventory. Available inventory is {}".format(product.get("inventory_count"))
                        })

        with open("products.json", "w") as products_file:
            json.dump(products_list, products_file)
        return Response(status=200, content_type="application/json", response=json.dumps(purchase_status))
    else:
        return Response(status=405)


@app.route("/create_cart", methods=["POST"])
def cart_create():
    cart.clear()
    if request.method == "POST":
        cart_items = request.json

        products_list = Products().products

        for product in products_list["products"]:
            for cart_item in cart_items:
                if product.get("id") == cart_item.get("id"):
                    if product.get("inventory_count") >= cart_item.get("count"):
                        cart["shopping_cart"].append({
                            "id": cart_item.get("id"),
                            "count": cart_item.get("count"),
                            "price": cart_item.get("count") * product.get("price")
                        })
        return Response(status=200, content_type="application/json", response=json.dumps(cart))
    else:
        return Response(status=405)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
