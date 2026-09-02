"""
Airflow DAG: multi-marketplace ingestion demo.

Orchestrates the SOR -> SOT -> SPEC flow for several synthetic
marketplaces. This DAG is a self-contained demo: it only ever reads and
writes synthetic data under a local data lake path, and does not connect
to any real marketplace API or cloud account.
"""
from __future__ import annotations

from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator

from src.config import settings
from src.marketplace_data_generator import generate_fake_marketplace_orders
from src.sor_layer import write_sor
from src.sot_layer import build_sot
from src.spec_layer import build_marketplace_funnel

_MARKETPLACES = ["marketplace_a", "marketplace_b", "marketplace_c", "marketplace_d"]

default_args = {
    "owner": "portfolio-demo",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def _ingest_marketplace(marketplace: str, **_context) -> None:
    records = generate_fake_marketplace_orders(marketplace=marketplace, num_orders=200)
    write_sor(marketplace, records, settings.data_lake_root)


def _build_sot(**_context) -> None:
    build_sot(settings.data_lake_root, marketplaces=_MARKETPLACES)


def _build_spec(**_context) -> None:
    build_marketplace_funnel(settings.data_lake_root)


with DAG(
    dag_id="marketplace_data_mesh_demo",
    description="Demo Data Mesh SOR/SOT/SPEC pipeline for synthetic marketplace orders",
    default_args=default_args,
    schedule="@daily",
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["demo", "data-mesh", "portfolio"],
) as dag:

    sor_tasks = []
    for marketplace_name in _MARKETPLACES:
        task = PythonOperator(
            task_id=f"ingest_sor_{marketplace_name}",
            python_callable=_ingest_marketplace,
            op_kwargs={"marketplace": marketplace_name},
        )
        sor_tasks.append(task)

    build_sot_task = PythonOperator(
        task_id="build_sot",
        python_callable=_build_sot,
    )

    build_spec_task = PythonOperator(
        task_id="build_spec_marketplace_funnel",
        python_callable=_build_spec,
    )

    sor_tasks >> build_sot_task >> build_spec_task
