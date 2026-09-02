"""
Synthetic multi-marketplace order data generator.

Generates fake order events for several fictitious marketplaces, used
only to demonstrate a Data Mesh style ingestion pipeline. No real
marketplace, seller, or order data is used anywhere in this project.
"""
from __future__ import annotations

import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List

_FAKE_MARKETPLACES = ["marketplace_a", "marketplace_b", "marketplace_c", "marketplace_d"]
_FAKE_PRODUCTS = [
    ("SKU-2001", "Backpack", 129.90),
    ("SKU-2002", "Water Bottle", 39.90),
    ("SKU-2003", "Desk Lamp", 89.50),
    ("SKU-2004", "Office Chair", 599.00),
]
_VALID_STATUSES = ["created", "paid", "shipped", "delivered", "cancelled"]


def generate_fake_marketplace_orders(
    marketplace: str,
    num_orders: int = 200,
    seed: int = 42,
) -> List[Dict[str, Any]]:
    """Generate fake raw order events for a single marketplace.

    Args:
        marketplace: name of the fictitious marketplace to simulate.
        num_orders: number of synthetic orders to generate.
        seed: random seed for reproducibility.

    Returns:
        A list of dictionaries representing raw (SOR-layer) order events,
        with a marketplace-specific field naming quirk to simulate the
        kind of schema drift seen across real marketplaces.
    """
    rng = random.Random(f"{marketplace}-{seed}")
    orders: List[Dict[str, Any]] = []
    base_time = datetime(2026, 6, 1)

    for _ in range(num_orders):
        sku, name, price = rng.choice(_FAKE_PRODUCTS)
        quantity = rng.randint(1, 4)
        order_id = str(uuid.uuid4())
        created_at = (base_time + timedelta(minutes=rng.randint(0, 60 * 24 * 60))).isoformat()
        status = rng.choice(_VALID_STATUSES)

        if marketplace == "marketplace_a":
            record = {
                "order_id": order_id,
                "sku": sku,
                "product_name": name,
                "unit_price": price,
                "qty": quantity,
                "status": status,
                "created_at": created_at,
            }
        else:
            record = {
                "orderId": order_id,
                "itemSku": sku,
                "itemName": name,
                "price": price,
                "quantity": quantity,
                "orderStatus": status,
                "createdAt": created_at,
            }

        orders.append(record)

    return orders
