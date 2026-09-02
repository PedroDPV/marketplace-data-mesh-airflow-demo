"""
SPEC (Data Product) layer.

Builds a business-ready, analytics-facing data product on top of the SOT
layer: a seller-style funnel summary per marketplace, ready to be
consumed by BI tools or downstream teams. This is the final stage of the
SOR/SOT/SPEC Data Mesh pattern I use professionally.
"""
from __future__ import annotations

import os

import pandas as pd

SPEC_DIR = "spec"


def build_marketplace_funnel(data_lake_root: str) -> pd.DataFrame:
    """Build a per-marketplace order funnel data product from the SOT layer.

    Args:
        data_lake_root: root path of the local/demo data lake.

    Returns:
        A DataFrame with one row per marketplace, summarizing order counts
        by status and total revenue from non-cancelled orders.
    """
    sot_path = os.path.join(data_lake_root, "sot", "orders.parquet")
    df = pd.read_parquet(sot_path)

    df["revenue"] = df["quantity"] * df["unit_price"]

    status_counts = (
        df.pivot_table(
            index="marketplace",
            columns="order_status",
            values="order_id",
            aggfunc="count",
            fill_value=0,
        )
        .reset_index()
    )

    revenue = (
        df[df["order_status"] != "cancelled"]
        .groupby("marketplace")["revenue"]
        .sum()
        .rename("total_revenue")
        .reset_index()
    )

    funnel = status_counts.merge(revenue, on="marketplace", how="left")
    funnel["total_revenue"] = funnel["total_revenue"].fillna(0)

    output_dir = os.path.join(data_lake_root, SPEC_DIR)
    os.makedirs(output_dir, exist_ok=True)
    funnel.to_csv(os.path.join(output_dir, "marketplace_funnel.csv"), index=False)

    return funnel
