"""
Centralized configuration for the marketplace Data Mesh demo.

Security note:
    All configuration values are loaded from environment variables
    (optionally via a local .env file for development). No credentials
    or secrets are ever hardcoded in source code. See .env.example for
    the list of supported variables.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()  # loads a local .env file if present; safe no-op otherwise


@dataclass(frozen=True)
class Settings:
    data_lake_root: str
    environment: str
    log_level: str

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            data_lake_root=os.getenv("DATA_LAKE_ROOT", "./data"),
            environment=os.getenv("ENVIRONMENT", "local"),
            log_level=os.getenv("LOG_LEVEL", "INFO"),
        )


settings = Settings.from_env()
