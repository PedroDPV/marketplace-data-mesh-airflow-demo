"""Unit tests for the SOR and SOT layers."""
import tempfile

from src.marketplace_data_generator import generate_fake_marketplace_orders
from src.sor_layer import write_sor
from src.sot_layer import build_sot

_MARKETPLACES = ["marketplace_a", "marketplace_b"]


def _seed_sor(data_lake_root: str) -> None:
    for marketplace in _MARKETPLACES:
        records = generate_fake_marketplace_orders(marketplace=marketplace, num_orders=50, seed=1)
        write_sor(marketplace, records, data_lake_root)


def test_build_sot_unifies_schema_across_marketplaces():
    with tempfile.TemporaryDirectory() as tmp_dir:
        _seed_sor(tmp_dir)
        df = build_sot(tmp_dir, marketplaces=_MARKETPLACES)

        expected_columns = {
            "order_id",
            "marketplace",
            "sku",
            "product_name",
            "unit_price",
            "quantity",
            "order_status",
            "created_at",
        }
        assert expected_columns.issubset(set(df.columns))
        assert set(df["marketplace"].unique()).issubset(set(_MARKETPLACES))


def test_build_sot_drops_invalid_rows():
    with tempfile.TemporaryDirectory() as tmp_dir:
        _seed_sor(tmp_dir)
        df = build_sot(tmp_dir, marketplaces=_MARKETPLACES)

        assert (df["quantity"] > 0).all()
        assert (df["unit_price"] > 0).all()


def test_build_sot_deduplicates_by_order_id():
    with tempfile.TemporaryDirectory() as tmp_dir:
        _seed_sor(tmp_dir)
        df = build_sot(tmp_dir, marketplaces=_MARKETPLACES)

        assert df["order_id"].is_unique
