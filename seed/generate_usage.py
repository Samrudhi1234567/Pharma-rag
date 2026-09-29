import os
import random
import pandas as pd

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

TENANTS = ["pharma-a", "pharma-b"]

PRODUCTS = [f"P{i:03d}" for i in range(1, 21)]

INDICATIONS = [
    "Fever and pain management",
    "Bacterial infections",
    "Type 2 diabetes",
    "Pain and inflammation",
    "Allergy management",
    "Cholesterol management",
    "Acid reflux management",
    "Hypertension management",
    "Diabetes management",
    "Cardiovascular protection",
    "Blood clot prevention",
    "Vitamin D supplementation",
    "Calcium supplementation",
    "Nutritional supplementation",
]

REGIONS = [
    "North",
    "South",
    "East",
    "West",
]

AGE_BANDS = [
    "18-30",
    "31-45",
    "46-60",
    "61+",
]

USAGE_CATEGORIES = [
    "Prescription",
    "Hospital",
    "Retail",
    "Chronic Care",
    "Acute Care",
]

rows = []

for _ in range(2000):

    tenant = random.choice(TENANTS)
    product = random.choice(PRODUCTS)
    indication = random.choice(INDICATIONS)
    region = random.choice(REGIONS)
    age_band = random.choice(AGE_BANDS)
    usage_category = random.choice(USAGE_CATEGORIES)

    volume = random.randint(100, 1000)

    rows.append(
        [
            tenant,
            product,
            indication,
            region,
            age_band,
            usage_category,
            volume,
        ]
    )


df = pd.DataFrame(
    rows,
    columns=[
        "tenant_id",
        "product_id",
        "synthetic_indication",
        "region",
        "age_band",
        "usage_category",
        "volume",
    ],
)

output_path = os.path.join(OUTPUT_DIR, "usage.csv")

df.to_csv(output_path, index=False)

print(f"Created {output_path}")
print(f"Total usage rows: {len(df)}")
print(f"Random seed: 42")