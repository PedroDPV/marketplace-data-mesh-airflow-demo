"""
SOT (System of Truth) layer.

Conforms each marketplace's SOR records into a single, unified schema,
resolving the field naming differences between marketplaces (for
example order_id vs orderId). This mirrors the SOR/SOT/SPEC Data Mesh
pattern I use professionally to structure multi-source pipelines.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List

import pandas as pd

from src.sor_layer import read_sor

SOT_DIR = "sot"
_MARKETPLACES = ["marketplace_a", "marketplace_b", "marketplace_c", "marketplace_d"]

_VALID_STATUSES = {"created", "paid", "shipped", "delivered", "cancelled"}


def _normalize_record(marketplace: str, record: Dict[str, Any]) -> Dict[str, Any]:
    """Map a marketplace-specific raw record into the unified SOT schema."""
    if marketplace == "marketplace_a":
        return {
            "order_id": record["order_id"],
            "marketplace": marketplace,
            "sku": record["sku"],
            "product_name": record["product_name"],
            "unit_price": record["unit_price"],
            "quantity": record["qty"],
            "order_status": record["status"],
            "created_at": record["created_at"],
        }
    return {
        "order_id": record["orderId"],
        "marketplace": marketplace,
        "sku": record["itemSku"],
        "product_name": record["itemName"],
        "unit_price": record["price"],
        "quantity": record["quantity"],
        "order_status": record["orderStatus"],
        "created_at": record["createdAt"],
    }


def build_sot(data_lake_root: str, marketplaces: List[str] = None) -> pd.DataFrame:
    """Build the unified SOT dataset from all marketplaces' SOR data.

    Args:
        data_lake_root: root path of the local/demo data lake.
        marketplaces: optional list of marketplaces to include; defaults
            to all known synthetic marketplaces.

    Returns:
        A single, schema-conformed DataFrame with one row per valid order.
    """
    marketplaces = marketplaces or _MARKETPLACES
    normalized: List[Dict[str, Any]] = []

    for marketplace in marketplaces:
        raw_records = read_sor(marketplace, data_lake_root)
        for record in raw_records:
            normalized.append(_normalize_record(marketplace, record))

    df = pd.DataFrame.from_records(normalized)
    df = df[df["order_status"].isin(_VALID_STATUSES)]
    df = df[(df["quantity"] > 0) & (df["unit_price"] > 0)]
    df = df.drop_duplicates(subset=["order_id"])

    output_dir = os.path.join(data_lake_root, SOT_DIR)
    os.makedirs(output_dir, exist_ok=True)
    df.to_parquet(os.path.join(output_dir, "orders.parquet"), index=False)

    return df
