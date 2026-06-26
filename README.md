# MongoDB E-Commerce Analytics Pipeline

> **End-to-end data analytics project** — NoSQL ingestion → aggregation pipelines → ETL → Tableau dashboard

[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://python.org)
[![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-green?logo=mongodb)](https://mongodb.com/atlas)
[![Tableau](https://img.shields.io/badge/Tableau-Public-orange?logo=tableau)](https://public.tableau.com)

---
⭐ Features

✔ MongoDB Atlas
✔ 5 Aggregation Pipelines
✔ ETL Pipeline
✔ Tableau Dashboard
✔ Interactive Filters
✔ Business Insights

## Business Problem

An e-commerce company needs to understand:
- Which product categories drive the most revenue?
- Is the business growing month-over-month?
- Which states have the highest customer value?
- Which categories are losing revenue to returns?

This pipeline answers all four questions using real aggregation logic on a MongoDB NoSQL store, then exports Tableau-ready CSVs for stakeholder dashboards.

---

## Architecture

```
JSON Dataset           MongoDB Atlas          Python ETL           Tableau Public
─────────────          ─────────────          ──────────           ──────────────
products.json    ──►   ecommerce_analytics    aggregate()    ──►   5 Dashboard Views
customers.json   ──►   ├── products           $group                ├── Revenue by Category
orders.json      ──►   ├── customers          $unwind               ├── Monthly Trend
                       └── orders             $lookup               ├── Top Products
                                              $match                ├── Return Rates
                                                      └──► CSVs    └── State Map
```

---

## Dataset

Synthetic Indian e-commerce dataset generated with realistic distributions:

| Collection | Records | Key Fields |
|------------|---------|------------|
| `products` | 180 | product_id, category, brand, price, rating |
| `customers` | 500 | customer_id, city, state, age_group, is_premium |
| `orders` | 3,000 | order_id, items[], total_amount, order_status, payment_method |

Orders contain **embedded line items** (nested array) — demonstrating MongoDB's document model advantage over relational joins.

---

## MongoDB Aggregation Pipelines

Five business-driven pipelines using `$match`, `$unwind`, `$group`, `$sort`, `$addFields`, `$project`, `$lookup`:

| # | Pipeline | MongoDB Operators Used |
|---|----------|----------------------|
| 1 | Revenue by category | `$match` → `$unwind` → `$group` → `$sort` → `$project` |
| 2 | Monthly revenue trend | `$addFields` + `$dateFromString` → `$group` → `$sort` |
| 3 | Top 10 products | `$unwind` → `$group` → `$sort` → `$limit` |
| 4 | Return rate by category | `$match` → `$group` with `$cond` → `$addFields` |
| 5 | State-level revenue | `$group` with `$addToSet` → `$size` for unique customers |

---

## Project Structure

```
mongodb_ecommerce/
├── data/
│   ├── products.json          # 180 products across 6 categories
│   ├── customers.json         # 500 customers across 20 Indian cities
│   └── orders.json            # 3,000 orders with embedded line items
├── scripts/
│   ├── generate_data.py       # Generates synthetic dataset
│   ├── mongo_pipelines.py     # MongoDB aggregation pipelines (Phase 2)
│   └── etl_export.py          # ETL: data → Tableau CSVs (Phase 3)
├── exports/
│   ├── revenue_by_category.csv
│   ├── monthly_revenue_trend.csv
│   ├── top_products.csv
│   ├── return_rates.csv
│   ├── geo_revenue.csv
│   └── orders_flat.csv        # 9,014 rows master flat table
├── docs/
│   └── schema_diagram.png     # MongoDB schema design
├── requirements.txt
└── README.md
```

---

## Setup & Run

### Option A — MongoDB Atlas (recommended for portfolio)

1. Create a free cluster at [cloud.mongodb.com](https://cloud.mongodb.com)
2. Create a database user and whitelist your IP
3. Copy your connection string
4. Update `MONGO_URI` in `scripts/mongo_pipelines.py`

### Option B — Local MongoDB

Install [MongoDB Community](https://www.mongodb.com/try/download/community) and run `mongod` locally.

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run the pipeline

```bash
# Step 1 — Generate dataset
python scripts/generate_data.py

# Step 2 — Import to MongoDB + run aggregation pipelines
python scripts/mongo_pipelines.py

# Step 3 — Export Tableau-ready CSVs
python scripts/etl_export.py
```

---

## Key Findings (sample output)

| Category | Revenue (₹) | Share | Avg Order Value |
|----------|-------------|-------|-----------------|
| Electronics | ~₹45,00,000 | ~35% | ₹4,200 |
| Home & Kitchen | ~₹28,00,000 | ~22% | ₹2,800 |
| Clothing | ~₹18,00,000 | ~14% | ₹1,100 |

**Business recommendations:**
- Electronics drives 35% of revenue but has the highest return risk — prioritise product description accuracy
- Maharashtra and Gujarat account for ~30% of revenue combined — invest in regional marketing here
- October and November show consistent revenue spikes (Diwali effect) — plan inventory 6 weeks ahead

---

## Tableau Dashboard

**[View Live Dashboard →](#)** *(https://public.tableau.com/views/e-commercesales_17824636602990/Dashboard1?:language=en-GB&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)*

5 views on one dashboard:
- Revenue by Category (bar chart)
- Monthly Revenue Trend (line chart with YoY overlay)
- Top 20 Products (horizontal bar)
- Return Rate Heatmap (highlight table)
- State Revenue Map (filled map)

---

## Skills Demonstrated

- **MongoDB** — Atlas cluster setup, collection design, 5 aggregation pipelines
- **Python** — PyMongo, data generation with realistic distributions, ETL scripting
- **Data Modeling** — Embedded document design (orders with nested items array)
- **ETL** — Mongo → Python → CSV pipeline with business transformations
- **Tableau** — Dashboard design with filters and cross-sheet actions
- **Business Thinking** — Framing queries around real business questions, not just data output

---

## Author

**Karan bhatt**  
[www.linkedin.com/in/
karan-bhatt-3332b9249] 
