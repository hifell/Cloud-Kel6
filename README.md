
End-to-end Azure Lakehouse untuk klasifikasi valuasi properti Indonesia.
Berbasis Medallion Architecture (Bronze → Silver → Gold).

## Setup Awal

```bash
# Install dependencies
poetry install

# Setup environment
cp .env.example .env
# Edit .env dengan kredensial yang diperlukan

# Download dataset dari Kaggle
poetry run python scripts/download_jakarta_house_price.py

# Upload ke bronze
poetry run python scripts/ingest_to_bronze.py
```

## Struktur Folder

```
Project/
├── pyproject.toml
├── .env.example
├── scripts/
│   ├── download_jakarta_house_price.py
│   ├── ingest_to_bronze.py
│   ├── transform_silver.py
│   └── aggregate_gold.py
├── notebooks/
└── tests/
```

## Biaya & Cost Control

- Synapse Spark Pool: Auto-pause setelah 15 menit idle
- Budget Alert: $50 dan $75 dari $100 student credit
- Monitoring: Azure Cost Management Dashboard
