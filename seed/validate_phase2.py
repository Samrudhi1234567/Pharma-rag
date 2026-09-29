import os
import pandas as pd


RAW_DIR = "data/raw"
DOCS_DIR = os.path.join(RAW_DIR, "pharma_docs")


def check_csv(
    filename,
    expected_rows,
    expected_columns
):

    path = os.path.join(
        RAW_DIR,
        filename
    )

    if not os.path.exists(path):
        print(f"FAIL: {filename} does not exist")
        return False

    df = pd.read_csv(path)

    row_check = len(df) == expected_rows

    column_check = (
        list(df.columns) == expected_columns
    )

    if row_check and column_check:
        print(
            f"PASS: {filename} "
            f"({len(df)} rows)"
        )
        return True

    print(f"FAIL: {filename}")

    if not row_check:
        print(
            f"  Expected rows: {expected_rows}"
        )
        print(
            f"  Actual rows: {len(df)}"
        )

    if not column_check:
        print(
            f"  Expected columns: "
            f"{expected_columns}"
        )
        print(
            f"  Actual columns: "
            f"{list(df.columns)}"
        )

    return False


print("=" * 60)
print("PHASE 2 VALIDATION")
print("=" * 60)


results = []


# Products
results.append(
    check_csv(
        "products.csv",
        20,
        [
            "product_id",
            "product_name",
            "therapeutic_area",
            "synthetic_indication",
            "dosage_form",
        ],
    )
)


# Users
results.append(
    check_csv(
        "users.csv",
        8,
        [
            "username",
            "tenant_id",
            "role",
        ],
    )
)


# Sales
results.append(
    check_csv(
        "sales.csv",
        5000,
        [
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
)


# Usage
results.append(
    check_csv(
        "usage.csv",
        2000,
        [
            "tenant_id",
            "product_id",
            "synthetic_indication",
            "region",
            "age_band",
            "usage_category",
            "volume",
        ],
    )
)


# Documents
print()

if not os.path.exists(DOCS_DIR):

    print("FAIL: pharma_docs directory missing")

    results.append(False)

else:

    documents = [
        f
        for f in os.listdir(DOCS_DIR)
        if f.endswith(".txt")
    ]

    if len(documents) == 30:

        print(
            "PASS: pharma_docs "
            f"contains {len(documents)} documents"
        )

        results.append(True)

    else:

        print(
            "FAIL: Expected 30 documents, "
            f"found {len(documents)}"
        )

        results.append(False)


# Check empty documents

if os.path.exists(DOCS_DIR):

    empty_documents = []

    for filename in documents:

        path = os.path.join(
            DOCS_DIR,
            filename
        )

        if os.path.getsize(path) == 0:

            empty_documents.append(
                filename
            )

    if not empty_documents:

        print(
            "PASS: No empty documents"
        )

        results.append(True)

    else:

        print(
            "FAIL: Empty documents found:"
        )

        for document in empty_documents:

            print(
                f"  - {document}"
            )

        results.append(False)


# Final result

print()
print("=" * 60)

if all(results):

    print("PHASE 2 VALIDATION: PASS")
    print("Phase 2 is complete.")

else:

    print("PHASE 2 VALIDATION: FAIL")
    print("Fix the failed checks before Phase 3.")

print("=" * 60)