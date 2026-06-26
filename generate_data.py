"""
generate_data.py
----------------
Generates a realistic e-commerce dataset and saves it as JSON files.
Run this ONCE to create your data before importing into MongoDB.

Output files (in ../data/):
  - products.json      (~200 products)
  - customers.json     (~500 customers)
  - orders.json        (~3,000 orders)
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

random.seed(42)

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

# ─── Lookup tables ─────────────────────────────────────────────────────────────

CATEGORIES = {
    "Electronics":    ["Smartphone", "Laptop", "Headphones", "Smartwatch", "Tablet",
                       "Earbuds", "Camera", "Portable Speaker", "Gaming Console", "Monitor"],
    "Clothing":       ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Formal Shirt",
                       "Kurta", "Saree", "Ethnic Suit", "Sports Shorts", "Winter Coat"],
    "Home & Kitchen": ["Air Fryer", "Mixer Grinder", "Bedsheet Set", "Curtains",
                       "Wall Clock", "Coffee Maker", "Rice Cooker", "Vacuum Cleaner",
                       "Dinner Set", "Pressure Cooker"],
    "Books":          ["Self-Help Book", "Data Science Guide", "Novel", "Cookbook",
                       "Business Strategy", "Python Programming", "History Book",
                       "Children's Book", "Comic Collection", "Finance Guide"],
    "Beauty":         ["Face Serum", "Sunscreen SPF50", "Moisturizer", "Lip Balm",
                       "Hair Oil", "Shampoo", "Perfume", "Eyeliner", "Foundation", "Blush"],
    "Sports":         ["Yoga Mat", "Dumbbells Set", "Cricket Bat", "Football",
                       "Badminton Racket", "Cycling Helmet", "Running Shoes",
                       "Skipping Rope", "Resistance Bands", "Water Bottle"],
}

BRANDS = {
    "Electronics":    ["Samsung", "Apple", "OnePlus", "Sony", "Boat", "Realme", "LG", "Dell"],
    "Clothing":       ["Levi's", "H&M", "Zara", "Nike", "Puma", "W", "Manyavar", "Fabindia"],
    "Home & Kitchen": ["Prestige", "Philips", "Havells", "Usha", "Bajaj", "Bosch", "IFB", "Pigeon"],
    "Books":          ["Penguin", "Harper Collins", "Oxford", "Wiley", "Notion Press", "Westland"],
    "Beauty":         ["Lakme", "L'Oreal", "Mamaearth", "Plum", "Dot & Key", "Minimalist", "Biotique"],
    "Sports":         ["Decathlon", "Nike", "Adidas", "Cosco", "SG", "Nivia", "Boldfit", "Strauss"],
}

PRICE_RANGES = {
    "Electronics":    (499, 89999),
    "Clothing":       (199, 4999),
    "Home & Kitchen": (299, 12999),
    "Books":          (99, 999),
    "Beauty":         (99, 2999),
    "Sports":         (149, 7999),
}

CITIES = [
    "Mumbai", "Delhi", "Bengaluru", "Hyderabad", "Ahmedabad",
    "Chennai", "Kolkata", "Pune", "Jaipur", "Surat",
    "Lucknow", "Kanpur", "Nagpur", "Indore", "Bhopal",
    "Vadodara", "Coimbatore", "Visakhapatnam", "Patna", "Kochi",
]

STATES = {
    "Mumbai": "Maharashtra", "Delhi": "Delhi", "Bengaluru": "Karnataka",
    "Hyderabad": "Telangana", "Ahmedabad": "Gujarat", "Chennai": "Tamil Nadu",
    "Kolkata": "West Bengal", "Pune": "Maharashtra", "Jaipur": "Rajasthan",
    "Surat": "Gujarat", "Lucknow": "Uttar Pradesh", "Kanpur": "Uttar Pradesh",
    "Nagpur": "Maharashtra", "Indore": "Madhya Pradesh", "Bhopal": "Madhya Pradesh",
    "Vadodara": "Gujarat", "Coimbatore": "Tamil Nadu", "Visakhapatnam": "Andhra Pradesh",
    "Patna": "Bihar", "Kochi": "Kerala",
}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Net Banking", "Cash on Delivery", "EMI"]
ORDER_STATUSES  = ["delivered", "delivered", "delivered", "shipped", "processing", "cancelled", "returned"]
FIRST_NAMES     = ["Aarav", "Vivaan", "Aditya", "Rohit", "Priya", "Neha", "Anjali", "Pooja",
                   "Arjun", "Karan", "Rahul", "Vikram", "Meera", "Divya", "Sneha", "Riya",
                   "Amit", "Suresh", "Deepak", "Raj", "Ananya", "Kavya", "Ishaan", "Siddharth"]
LAST_NAMES      = ["Sharma", "Patel", "Verma", "Singh", "Gupta", "Kumar", "Joshi", "Mehta",
                   "Shah", "Rao", "Nair", "Pillai", "Reddy", "Iyer", "Agarwal", "Banerjee"]

def rand_date(start_year=2022, end_year=2024):
    start = datetime(start_year, 1, 1)
    end   = datetime(end_year, 12, 31)
    return start + timedelta(seconds=random.randint(0, int((end - start).total_seconds())))

def fmt(dt):
    return dt.strftime("%Y-%m-%dT%H:%M:%S")


# ─── Generate products ─────────────────────────────────────────────────────────

products = []
pid = 1
for category, items in CATEGORIES.items():
    for item in items:
        for _ in range(3):          # 3 variants per product name
            brand = random.choice(BRANDS[category])
            lo, hi = PRICE_RANGES[category]
            price  = round(random.uniform(lo, hi), -1)   # round to nearest 10
            products.append({
                "product_id":   f"PRD{pid:04d}",
                "name":         f"{brand} {item}",
                "category":     category,
                "brand":        brand,
                "price":        price,
                "rating":       round(random.uniform(3.0, 5.0), 1),
                "reviews_count": random.randint(10, 4000),
                "in_stock":     random.random() > 0.1,
                "created_at":   fmt(rand_date(2021, 2022)),
            })
            pid += 1

# ─── Generate customers ────────────────────────────────────────────────────────

customers = []
for cid in range(1, 501):
    city  = random.choice(CITIES)
    fname = random.choice(FIRST_NAMES)
    lname = random.choice(LAST_NAMES)
    reg   = rand_date(2020, 2023)
    customers.append({
        "customer_id":  f"CST{cid:04d}",
        "name":         f"{fname} {lname}",
        "email":        f"{fname.lower()}.{lname.lower()}{cid}@example.com",
        "city":         city,
        "state":        STATES[city],
        "age_group":    random.choice(["18-24", "25-34", "35-44", "45-54", "55+"]),
        "gender":       random.choice(["Male", "Female", "Prefer not to say"]),
        "registered_at": fmt(reg),
        "is_premium":   random.random() > 0.7,
    })

# ─── Generate orders ──────────────────────────────────────────────────────────

orders = []
for oid in range(1, 3001):
    customer  = random.choice(customers)
    n_items   = random.randint(1, 5)
    items     = []
    subtotal  = 0
    for _ in range(n_items):
        product  = random.choice(products)
        qty      = random.randint(1, 3)
        discount = round(random.choice([0, 0, 0, 5, 10, 15, 20]) / 100, 2)
        line_total = round(product["price"] * qty * (1 - discount), 2)
        subtotal  += line_total
        items.append({
            "product_id":   product["product_id"],
            "product_name": product["name"],
            "category":     product["category"],
            "brand":        product["brand"],
            "unit_price":   product["price"],
            "quantity":     qty,
            "discount_pct": int(discount * 100),
            "line_total":   line_total,
        })

    status      = random.choice(ORDER_STATUSES)
    order_date  = rand_date(2022, 2024)
    delivery_dt = order_date + timedelta(days=random.randint(1, 10)) if status == "delivered" else None
    shipping    = 0 if subtotal > 500 else 49
    orders.append({
        "order_id":       f"ORD{oid:05d}",
        "customer_id":    customer["customer_id"],
        "customer_city":  customer["city"],
        "customer_state": customer["state"],
        "order_date":     fmt(order_date),
        "delivery_date":  fmt(delivery_dt) if delivery_dt else None,
        "items":          items,
        "item_count":     n_items,
        "subtotal":       round(subtotal, 2),
        "shipping_fee":   shipping,
        "total_amount":   round(subtotal + shipping, 2),
        "payment_method": random.choice(PAYMENT_METHODS),
        "order_status":   status,
        "is_returned":    status == "returned",
    })

# ─── Save files ───────────────────────────────────────────────────────────────

for fname, data in [("products.json", products), ("customers.json", customers), ("orders.json", orders)]:
    path = DATA_DIR / fname
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    print(f"✅  {fname:20s}  →  {len(data):,} records  →  {path}")

print("\n📁 All data files saved to:", DATA_DIR)
