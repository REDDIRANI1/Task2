import csv
import requests
import json

HEADERS = {
    "auth_key": "c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477",
    "device_id": "ac03a11a-eb12-4b29-972c-3d7127e2c157",
    "lat": "12.986211",
    "lon": "77.711654",
    "app_client": "consumer_web",
    "app_version": "1010101010",
    "platform": "desktop_web",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
    "referer": "https://blinkit.com/cn/munchies/nachos/cid/1237/316",
    "origin": "https://blinkit.com",
}

def fetch_products(l0_cat, l1_cat):
    url = f"https://blinkit.com/v1/layout/listing_widgets?l0_cat={l0_cat}&l1_cat={l1_cat}"
    try:
        res = requests.post(url, headers=HEADERS, json={})
        if res.status_code != 200:
            print(f"Non-200 response: {res.status_code}")
            return []
        data = res.json()
        items = []
        for widget in data.get("widgets", []):
            for product in widget.get("products", []):
                items.append({
                    "Latitude": HEADERS["lat"],
                    "Longitude": HEADERS["lon"],
                    "CategoryID": l0_cat,
                    "SubCategoryID": l1_cat,
                    "ProductName": product.get("display_name", ""),
                    "Price": product.get("price", ""),
                    "MRP": product.get("mrp", ""),
                    "Discount": product.get("discount", ""),
                    "Rating": product.get("rating", ""),
                })
        return items
    except Exception as e:
        print(f"Error: {e}")
        return []

# Example usage
products = fetch_products("1237", "316")
with open("products.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Latitude", "Longitude", "CategoryID", "SubCategoryID", "ProductName", "Price", "MRP", "Discount", "Rating"
    ])
    writer.writeheader()
    writer.writerows(products)

print(f"Wrote {len(products)} products to products.csv")
