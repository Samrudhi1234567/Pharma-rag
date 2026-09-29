import os
import pandas as pd

OUTPUT_DIR = "data/raw"
os.makedirs(OUTPUT_DIR, exist_ok=True)

users = [
    ["alice", "pharma-a", "admin"],
    ["john", "pharma-a", "sales_manager"],
    ["sam", "pharma-a", "analyst"],
    ["raj", "pharma-a", "viewer"],
    ["bob", "pharma-b", "admin"],
    ["emma", "pharma-b", "sales_manager"],
    ["alex", "pharma-b", "analyst"],
    ["mike", "pharma-b", "viewer"],
]

df = pd.DataFrame(
    users,
    columns=["username", "tenant_id", "role"],
)

output_path = os.path.join(OUTPUT_DIR, "users.csv")
df.to_csv(output_path, index=False)

print(f"Created {output_path}")
print(f"Total users: {len(df)}")