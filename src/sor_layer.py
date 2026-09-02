"""
SOR (System of Record) layer.

Persists each marketplace's raw order events exactly as received, in
their own marketplace-specific schema. This preserves an auditable,
unmodified copy of the source data, following the Data Mesh SOR/SOT/SPEC
layering pattern I use professionally.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List

SOR_DIR = "sor"


def write_sor(
    marketplace: str,
    records: List[Dict[str, Any]],
    data_lake_root: str,
) -> str:
    """Write raw marketplace records to the SOR layer as JSON lines.

    Args:
        marketplace: name of the marketplace the records belong to.
        records: raw order records, as produced by
            marketplace_data_generator.generate_fake_marketplace_orders.
        data_lake_root: root path of the local/demo data lake.

    Returns:
        The path to the written SOR file.
    """
    if not records:
        raise ValueError("records must not be empty")

    output_dir = os.path.join(data_lake_root, SOR_DIR, marketplace)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "orders.jsonl")

    with open(output_path, "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record) + "\n")

    return output_path


def read_sor(marketplace: str, data_lake_root: str) -> List[Dict[str, Any]]:
    """Read back the raw SOR records for a given marketplace."""
    input_path = os.path.join(data_lake_root, SOR_DIR, marketplace, "orders.jsonl")
    with open(input_path, "r", encoding="utf-8") as handle:
        return [json.loads(line) for line in handle if line.strip()]
