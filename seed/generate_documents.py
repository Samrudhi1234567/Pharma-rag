import os
import random
import pandas as pd

OUTPUT_DIR = "data/raw/pharma_docs"

os.makedirs(OUTPUT_DIR, exist_ok=True)

random.seed(42)

# ---------------------------------------------------------
# Load product information
# ---------------------------------------------------------

products_path = "data/raw/products.csv"

products_df = pd.read_csv(products_path)

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------

TENANTS = [
    "pharma-a",
    "pharma-b",
]

ROLES = [
    "sales_manager",
    "analyst",
]

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

CLASSIFICATION = "internal"

YEAR = 2026


# ---------------------------------------------------------
# Helper function
# ---------------------------------------------------------

def write_document(filename, content):

    path = os.path.join(
        OUTPUT_DIR,
        filename
    )

    with open(
        path,
        "w",
        encoding="utf-8"
    ) as file:

        file.write(content)

    print(f"Created: {filename}")


# =========================================================
# 1. PRODUCT SHEETS
# =========================================================

product_documents = products_df.head(10)

for _, product in product_documents.iterrows():

    product_id = product["product_id"]
    product_name = product["product_name"]
    therapeutic_area = product["therapeutic_area"]
    indication = product["synthetic_indication"]
    dosage_form = product["dosage_form"]

    tenant = "pharma-a"

    role = "analyst"

    quarter = random.choice(
        ["Q1", "Q2", "Q3", "Q4"]
    )

    region = random.choice(REGIONS)

    content = f"""Tenant: {tenant}
Allowed Roles: {role}
Product: {product_id}
Region: {region}
Year: {YEAR}
Quarter: {quarter}
Classification: {CLASSIFICATION}

Product ID: {product_id}
Product Name: {product_name}
Therapeutic Area: {therapeutic_area}
Synthetic Indication: {indication}
Dosage Form: {dosage_form}

{product_name} demonstrated strong synthetic commercial performance
during {quarter} {YEAR}.

The product showed significant demand across the {region} region.
Sales performance remained consistent with the synthetic business
targets for the reporting period.

This document contains synthetic pharmaceutical product information
created for the Pharma RAG evaluation system.
"""

    filename = f"Product_{product_id}_Sheet.txt"

    write_document(
        filename,
        content
    )


# =========================================================
# 2. REGIONAL REPORTS
# =========================================================

regional_reports = [
    (
        "Q1_North_Report.txt",
        "pharma-a",
        "Q1",
        "North",
        "P007",
        "Delhi"
    ),
    (
        "Q2_South_Report.txt",
        "pharma-a",
        "Q2",
        "South",
        "P001",
        "Karnataka"
    ),
    (
        "Q3_East_Report.txt",
        "pharma-b",
        "Q3",
        "East",
        "P003",
        "West Bengal"
    ),
    (
        "Q4_West_Report.txt",
        "pharma-b",
        "Q4",
        "West",
        "P009",
        "Maharashtra"
    ),
]

for (
    filename,
    tenant,
    quarter,
    region,
    product_id,
    top_state
) in regional_reports:

    content = f"""Tenant: {tenant}
Allowed Roles: sales_manager, analyst
Product: {product_id}
Region: {region}
Year: {YEAR}
Quarter: {quarter}
Classification: {CLASSIFICATION}

Regional Sales Report
=====================

Region: {region}
Quarter: {quarter}
Year: {YEAR}

Product {product_id} achieved the highest synthetic revenue
performance in the {region} region during {quarter}.

The strongest state-level contribution came from {top_state}.

Sales performance exceeded the synthetic quarterly target
during the reporting period.

This report contains synthetic sales information created
for the Pharma RAG evaluation system.
"""

    write_document(
        filename,
        content
    )


# =========================================================
# 3. STATE REPORTS
# =========================================================

state_reports = [
    (
        "Karnataka_Sales_Report.txt",
        "pharma-a",
        "Karnataka",
        "P001",
        "Q2"
    ),
    (
        "Maharashtra_Sales_Report.txt",
        "pharma-a",
        "Maharashtra",
        "P004",
        "Q2"
    ),
    (
        "Delhi_Sales_Report.txt",
        "pharma-b",
        "Delhi",
        "P007",
        "Q1"
    ),
    (
        "Gujarat_Sales_Report.txt",
        "pharma-b",
        "Gujarat",
        "P009",
        "Q4"
    ),
]

for (
    filename,
    tenant,
    state,
    product_id,
    quarter
) in state_reports:

    content = f"""Tenant: {tenant}
Allowed Roles: sales_manager, analyst
Product: {product_id}
Region: India
State: {state}
Year: {YEAR}
Quarter: {quarter}
Classification: {CLASSIFICATION}

State Sales Performance Report
==============================

State: {state}
Quarter: {quarter}
Year: {YEAR}

Product {product_id} recorded the strongest synthetic
sales performance in {state} during {quarter}.

The product demonstrated positive revenue growth and
performed above the synthetic sales target.

This document contains synthetic pharmaceutical sales
information created for the Pharma RAG evaluation system.
"""

    write_document(
        filename,
        content
    )


# =========================================================
# 4. QUARTERLY SUMMARY REPORTS
# =========================================================

quarterly_reports = [
    (
        "Q1_2026_Quarterly_Summary.txt",
        "pharma-a",
        "Q1",
        "P007"
    ),
    (
        "Q2_2026_Quarterly_Summary.txt",
        "pharma-a",
        "Q2",
        "P001"
    ),
    (
        "Q3_2026_Quarterly_Summary.txt",
        "pharma-b",
        "Q3",
        "P003"
    ),
    (
        "Q4_2026_Quarterly_Summary.txt",
        "pharma-b",
        "Q4",
        "P009"
    ),
]

for (
    filename,
    tenant,
    quarter,
    product_id
) in quarterly_reports:

    content = f"""Tenant: {tenant}
Allowed Roles: sales_manager, analyst
Product: {product_id}
Year: {YEAR}
Quarter: {quarter}
Classification: {CLASSIFICATION}

Quarterly Business Summary
==========================

Quarter: {quarter}
Year: {YEAR}

Product {product_id} delivered strong synthetic revenue
performance during {quarter}.

Revenue performance remained above the synthetic target
for the reporting period.

The product demonstrated stable demand across multiple
regions.

This document contains synthetic quarterly information
created for the Pharma RAG evaluation system.
"""

    write_document(
        filename,
        content
    )


# =========================================================
# 5. SOP DOCUMENTS
# =========================================================

sop_documents = [
    (
        "SOP_Sales_Data_Access.txt",
        "pharma-a",
        "admin"
    ),
    (
        "SOP_Product_Data_Access.txt",
        "pharma-a",
        "admin"
    ),
    (
        "SOP_Regional_Report_Access.txt",
        "pharma-b",
        "admin"
    ),
    (
        "SOP_RAG_Data_Usage.txt",
        "pharma-b",
        "admin"
    ),
    (
        "SOP_Tenant_Data_Isolation.txt",
        "pharma-a",
        "admin"
    ),
    (
        "SOP_Document_Authorization.txt",
        "pharma-b",
        "admin"
    ),
    (
        "SOP_Sensitive_Data_Handling.txt",
        "pharma-a",
        "admin"
    ),
    (
        "SOP_RAG_Access_Control.txt",
        "pharma-b",
        "admin"
    ),
]

for (
    filename,
    tenant,
    role
) in sop_documents:

    content = f"""Tenant: {tenant}
Allowed Roles: {role}
Year: {YEAR}
Classification: confidential

Standard Operating Procedure
============================

Document Access Policy

Only authenticated users belonging to the authorized
tenant may access this information.

Administrative documents are restricted to users with
the appropriate administrative role.

Tenant information must always be derived from the
authenticated identity.

Users must not be allowed to override tenant scope
through API request parameters.

All document access must respect tenant and role-based
authorization policies.

This SOP contains synthetic security information created
for the Pharma RAG evaluation system.
"""

    write_document(
        filename,
        content
    )


# =========================================================
# VALIDATION
# =========================================================

documents = [
    file
    for file in os.listdir(OUTPUT_DIR)
    if file.endswith(".txt")
]

print()
print("=" * 60)
print("DOCUMENT GENERATION COMPLETE")
print("=" * 60)
print(f"Total documents created: {len(documents)}")

if len(documents) == 30:
    print("PASS: Exactly 30 documents created.")
else:
    print(
        f"WARNING: Expected 30 documents but found {len(documents)}."
    )