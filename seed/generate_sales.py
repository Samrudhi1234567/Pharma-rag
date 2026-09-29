import os
import random
import pandas as pd

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

TENANTS = ["pharma-a", "pharma-b"]

PRODUCTS = [f"P{i:03d}" for i in range(1, 21)]

REGIONS = [
    "North",
    "South",
    "East",
    "West",
]

STATES = [
    "Maharashtra",
    "Karnataka",
    "Delhi",
    "Tamil Nadu",
    "Gujarat",
]

CHANNELS = [
    "Hospital",
    "Retail",
    "Distributor",
    "Online",
]

MONTHS = list(range(1, 13))


def get_quarter(month):
    if month <= 3:
        return "Q1"
    elif month <= 6:
        return "Q2"
    elif month <= 9:
        return "Q3"
    return "Q4"


rows = []

for _ in range(5000):

    tenant = random.choice(TENANTS)
    product = random.choice(PRODUCTS)
    region = random.choice(REGIONS)
    state = random.choice(STATES)

    month = random.choice(MONTHS)
    quarter = get_quarter(month)

    units = random.randint(500, 10000)

    revenue_per_unit = random.randint(100, 1000)

    revenue = units * revenue_per_unit

    target = int(
        revenue * random.uniform(0.85, 1.15)
    )

    channel = random.choice(CHANNELS)

    rows.append(
        [
            tenant,
            product,
            region,
            state,
            month,
            quarter,
            units,
            revenue,
            target,
            channel,
        ]
    )


df = pd.DataFrame(
    rows,
    columns=[
        "tenant_id",
        "product_id",
        "region",
        "state",
        "month",
        "quarter",
        "units",
        "revenue",
        "target",
        "channel",
    ],
)

output_path = os.path.join(OUTPUT_DIR, "sales.csv")

df.to_csv(output_path, index=False)

print(f"Created {output_path}")
print(f"Total sales rows: {len(df)}")
print(f"Random seed: 42")