# Shopify Assessment

## Requirements
- python3
- Flask 1.0.2

## Installation
- `pip3 install -r requirements.txt`

## Running the code
- `python3 app.py

## API Documentation

All the requests should hit http://localhost:5000

### GET /products?available_inventory=<true|false>
- Returns all the products in the database. If `available_inventory=true` then all the products
with inventory `>0` are also displayed and vice versa
- **Sample Response** 
```{"products": [{"id": 1, "title": "iphone", "price": 800, "inventory_count": 1}, {"id": 2, "title": "laptop", "price": 1000, "inventory_count": 5}, {"id": 3, "title": "Apple", "price": 5, "inventory_count": 15}, {"id": 4, "title": "Mango", "price": 3, "inventory_count": 0}]}```

### GET /product/<id>
- Returns a product with the specific ID
- **Sample Response**
```{"id": 1, "title": "iphone", "price": 800, "inventory_count": 1}```

### POST /purchase

- **Request Body**: 
Takes an input as list of objects in a shopping cart
```{
"shopping_cart":[
    {
        "id": 2,
        "count": 1,
        "price": 1000
    }
]
```

- **Sample Response**
```angular2
{"status": [{"id": 2, "purchase_status": "Successful"}]}
```


### POST /create_cart
- **Request Body**: 
Takes an input as list of objects to add to cart with their id and count
```angular2
[
  {
    "id": 2,
    "count": 1
  }
]
```

- **Sample Response**:
```angular2
{"shopping_cart": [{"id": 2, "count": 1, "price": 1000}]}
```
