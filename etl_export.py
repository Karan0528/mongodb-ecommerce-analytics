"""
etl_export.py
-------------
PHASE 3 — ETL: MongoDB → CSV → Tableau-ready files

Reads data directly from your local JSON files (no MongoDB connection needed
for this step — the aggregation logic mirrors the MongoDB pipelines exactly).

Output files go to ../exports/:
  - revenue_by_category.csv     → Tableau bar chart
  - monthly_revenue_trend.csv   → Tableau line chart
  - top_products.csv            → Tableau packed bubbles / bar
  - return_rates.csv            → Tableau highlight table
  - geo_revenue.csv             → Tableau map (state-level)
  - orders_flat.csv             → Master flat table for any ad-hoc viz

PORTFOLIO TIP:
  Connect Tableau Desktop/Public to each CSV and build one sheet per file.
  Use a Dashboard layout to combine all 5 views with a Date filter.
"""

import json
import csv
from pathlib import Path
from collections import defaultdict
from datetime import datetime

DATA_DIR = Path(r"C:\Users\Karan\OneDrive\Desktop\db project\mongodb_ecommerce_project\mongodb_ecommerce\data")
EXPORTS_DIR = Path(__file__).parent.parent / "exports"
EXPORTS_DIR.mkdir(exist_ok=True)


def load(name):
    with open(DATA_DIR / f"{name}.json") as f:
        return json.load(f)


def write_csv(filename, rows, fieldnames):
    path = EXPORTS_DIR / filename
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"  ✅  {filename:<35}  {len(rows):>5,} rows  →  {path.name}")
    return path


# ─── Load raw data ─────────────────────────────────────────────────────────────
print("\n📂  Loading JSON data...")
products  = {p["product_id"]: p for p in load("products")}
customers = {c["customer_id"]: c for c in load("customers")}
orders    = load("orders")
print(f"  Products: {len(products):,}  |  Customers: {len(customers):,}  |  Orders: {len(orders):,}\n")

print("📊  Building aggregations...\n")

# ─── 1. Revenue by category ────────────────────────────────────────────────────
cat_stats = defaultdict(lambda: {"revenue": 0, "units": 0, "order_count": 0})
for o in orders:
    if o["order_status"] == "delivered":
        for item in o["items"]:
            cat_stats[item["category"]]["revenue"]     += item["line_total"]
            cat_stats[item["category"]]["units"]       += item["quantity"]
            cat_stats[item["category"]]["order_count"] += 1

total_rev = sum(v["revenue"] for v in cat_stats.values())
cat_rows  = sorted([
    {
        "category":       cat,
        "revenue_inr":    round(v["revenue"]),
        "revenue_share_pct": round(v["revenue"] / total_rev * 100, 1),
        "units_sold":     v["units"],
        "order_count":    v["order_count"],
        "avg_order_value": round(v["revenue"] / v["order_count"]) if v["order_count"] else 0,
    }
    for cat, v in cat_stats.items()
], key=lambda x: -x["revenue_inr"])

write_csv("revenue_by_category.csv", cat_rows,
          ["category", "revenue_inr", "revenue_share_pct", "units_sold", "order_count", "avg_order_value"])

# ─── 2. Monthly revenue trend ──────────────────────────────────────────────────
monthly = defaultdict(lambda: {"revenue": 0, "order_count": 0})
for o in orders:
    if o["order_status"] == "delivered":
        dt  = datetime.fromisoformat(o["order_date"])
        key = (dt.year, dt.month)
        monthly[key]["revenue"]     += o["total_amount"]
        monthly[key]["order_count"] += 1

month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_rows = sorted([
    {
        "year":        k[0],
        "month_num":   k[1],
        "month_name":  month_names[k[1]-1],
        "period":      f"{month_names[k[1]-1]} {k[0]}",
        "date_label":  f"{k[0]}-{k[1]:02d}-01",
        "revenue_inr": round(v["revenue"]),
        "order_count": v["order_count"],
        "avg_order_value": round(v["revenue"] / v["order_count"]) if v["order_count"] else 0,
    }
    for k, v in monthly.items()
], key=lambda x: (x["year"], x["month_num"]))

write_csv("monthly_revenue_trend.csv", monthly_rows,
          ["year","month_num","month_name","period","date_label","revenue_inr","order_count","avg_order_value"])

# ─── 3. Top products ───────────────────────────────────────────────────────────
prod_stats = defaultdict(lambda: {"category":"","brand":"","revenue":0,"qty":0})
for o in orders:
    if o["order_status"] == "delivered":
        for item in o["items"]:
            prod_stats[item["product_name"]]["category"] = item["category"]
            prod_stats[item["product_name"]]["brand"]    = item["brand"]
            prod_stats[item["product_name"]]["revenue"] += item["line_total"]
            prod_stats[item["product_name"]]["qty"]     += item["quantity"]

top_products = sorted([
    {"product": k, "category": v["category"], "brand": v["brand"],
     "revenue_inr": round(v["revenue"]), "qty_sold": v["qty"]}
    for k, v in prod_stats.items()
], key=lambda x: -x["revenue_inr"])[:20]

write_csv("top_products.csv", top_products,
          ["product", "category", "brand", "revenue_inr", "qty_sold"])

# ─── 4. Return rates ───────────────────────────────────────────────────────────
ret_stats = defaultdict(lambda: {"total": 0, "returned": 0, "revenue_lost": 0})
for o in orders:
    if o["order_status"] in ("delivered", "returned"):
        for item in o["items"]:
            cat = item["category"]
            ret_stats[cat]["total"] += 1
            if o["order_status"] == "returned":
                ret_stats[cat]["returned"]     += 1
                ret_stats[cat]["revenue_lost"] += item["line_total"]

return_rows = sorted([
    {
        "category":        cat,
        "total_orders":    v["total"],
        "returned_orders": v["returned"],
        "return_rate_pct": round(v["returned"] / v["total"] * 100, 1) if v["total"] else 0,
        "revenue_lost_inr": round(v["revenue_lost"]),
        "high_risk_flag":  "Yes" if (v["returned"] / v["total"] * 100 if v["total"] else 0) > 10 else "No",
    }
    for cat, v in ret_stats.items()
], key=lambda x: -x["return_rate_pct"])

write_csv("return_rates.csv", return_rows,
          ["category","total_orders","returned_orders","return_rate_pct","revenue_lost_inr","high_risk_flag"])

# ─── 5. Geo revenue ────────────────────────────────────────────────────────────
state_stats = defaultdict(lambda: {"revenue": 0, "orders": 0, "customers": set()})
for o in orders:
    if o["order_status"] == "delivered":
        s = o["customer_state"]
        state_stats[s]["revenue"]   += o["total_amount"]
        state_stats[s]["orders"]    += 1
        state_stats[s]["customers"].add(o["customer_id"])

geo_rows = sorted([
    {
        "state":                s,
        "revenue_inr":          round(v["revenue"]),
        "order_count":          v["orders"],
        "unique_customers":     len(v["customers"]),
        "revenue_per_customer": round(v["revenue"] / len(v["customers"])) if v["customers"] else 0,
        "avg_order_value":      round(v["revenue"] / v["orders"]) if v["orders"] else 0,
    }
    for s, v in state_stats.items()
], key=lambda x: -x["revenue_inr"])

write_csv("geo_revenue.csv", geo_rows,
          ["state","revenue_inr","order_count","unique_customers","revenue_per_customer","avg_order_value"])

# ─── 6. Master flat table ─────────────────────────────────────────────────────
flat_rows = []
for o in orders:
    cust = customers.get(o["customer_id"], {})
    dt   = datetime.fromisoformat(o["order_date"])
    for item in o["items"]:
        flat_rows.append({
            "order_id":       o["order_id"],
            "order_date":     dt.strftime("%Y-%m-%d"),
            "year":           dt.year,
            "month":          dt.month,
            "quarter":        f"Q{(dt.month-1)//3+1}",
            "order_status":   o["order_status"],
            "payment_method": o["payment_method"],
            "customer_id":    o["customer_id"],
            "customer_city":  o.get("customer_city", ""),
            "customer_state": o.get("customer_state", ""),
            "customer_age_group": cust.get("age_group", ""),
            "customer_gender":    cust.get("gender", ""),
            "is_premium_customer": cust.get("is_premium", False),
            "product_name":   item["product_name"],
            "category":       item["category"],
            "brand":          item["brand"],
            "unit_price":     item["unit_price"],
            "quantity":       item["quantity"],
            "discount_pct":   item["discount_pct"],
            "line_total":     round(item["line_total"], 2),
            "shipping_fee":   o["shipping_fee"],
            "is_returned":    o["is_returned"],
        })

write_csv("orders_flat.csv", flat_rows, [
    "order_id","order_date","year","month","quarter","order_status","payment_method",
    "customer_id","customer_city","customer_state","customer_age_group","customer_gender","is_premium_customer",
    "product_name","category","brand","unit_price","quantity","discount_pct","line_total",
    "shipping_fee","is_returned"
])

print(f"\n🎉  ETL complete! All CSV files saved to: {EXPORTS_DIR}")
print(f"\n📊  Tableau Quick-Start:")
print(f"  1. Open Tableau Public (free) → Connect → Text File")
print(f"  2. Load orders_flat.csv as your master source")
print(f"  3. Build 5 sheets: Bar chart, Line chart, Bubble chart, Highlight table, Map")
print(f"  4. Combine into a Dashboard with a Date Range filter")
print(f"  5. Publish to Tableau Public → copy link for GitHub README")
