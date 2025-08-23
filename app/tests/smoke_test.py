import os
import requests

url = os.getenv("url", "http://127.0.0.1:8000")
apiKey = os.getenv("apiKey","hello007")
header = {"onlinestore": apiKey, "Content-Type": "application/json"}

new_product = {
  "sku": "test2",
  "name": "test",
  "price": 10,
  "stock": 1
}
respPrdt = requests.post(f"{url}/products", json=new_product, headers=header)
print("Create product: ", respPrdt.status_code, respPrdt.json())

new_order = {
    "product_id": respPrdt.json()["id"],
    "quantity": 1,
    "status": "PENDING"
}
respOrder = requests.post(f"{url}/orders", json=new_order, headers=header)
print("Create order: ", respOrder.status_code, respOrder.json())