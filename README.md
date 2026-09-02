# Marketplace Data Mesh Airflow Demo

This is a portfolio and demo project that implements a multi-marketplace data ingestion pipeline orchestrated with Apache Airflow, following a Data Mesh style SOR, SOT, SPEC layering pattern I use professionally.

Disclaimer: all data used in this project is synthetically generated, see src/marketplace_data_generator.py. No real marketplace, seller, or order data is used anywhere in this repository. This is a simplified sample meant to illustrate architecture and coding practices, not a production system.

## Architecture

SOR, System of Record: each fictitious marketplace's raw order events are written as is, preserving each marketplace's own field naming and schema quirks, for auditability.

SOT, System of Truth: all marketplaces' SOR data is conformed into a single unified schema, resolving field naming differences, applying data quality checks, and deduplicating by order id.

SPEC, Data Product: the SOT layer is aggregated into a business-ready per-marketplace order funnel, with counts by status and total revenue, ready to be consumed by BI tools or downstream teams.

An Airflow DAG, in dags/marketplace_ingestion_dag.py, orchestrates the full SOR to SOT to SPEC flow across all synthetic marketplaces.

## Project structure

src/config.py: environment based configuration with no hardcoded secrets.

src/marketplace_data_generator.py: synthetic multi-marketplace order generator.

src/sor_layer.py: System of Record ingestion logic.

src/sot_layer.py: System of Truth conformance and data quality logic.

src/spec_layer.py: Data Product, funnel aggregation logic.

dags/marketplace_ingestion_dag.py: Airflow DAG orchestrating the full pipeline.

tests: unit tests for the SOR and SOT layers.

SECURITY.md: security practices applied in this demo.

## Running locally

Create a virtual environment and install dependencies from requirements.txt.

Copy .env.example to .env and adjust values if needed.

The DAG can be placed in a local Airflow dags folder and triggered from the Airflow UI or CLI, or the underlying src functions can be called directly, for example from a Python shell, for a quick end to end run without Airflow.

## Tech stack

Python, Apache Airflow, pandas, pyarrow, pytest, python-dotenv.

## About this repository

This project is part of my professional portfolio and demonstrates the kind of Data Mesh, multi-source ingestion, and Airflow orchestration work described in my LinkedIn profile and resume. It is a self-contained sample built specifically for this purpose using synthetic data, not an export of proprietary employer code.
