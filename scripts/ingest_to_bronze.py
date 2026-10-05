"""
Ingest data dari local ke Azure Data Lake Storage Gen2 - Bronze Layer.
Costhandler: Batch upload, tidak streaming untuk avoid unnecessary compute.
"""

import os
from pathlib import Path

# Enable Azure CLI auth mode for development
os.environ["AZURE_AUTH_MODE"] = "azure-cli"

from azure.storage.filedatalake import DataLakeServiceClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Config
STORAGE_ACCOUNT = os.getenv("STORAGE_ACCOUNT_NAME", "adlskelompok6")
CONTAINER_BRONZE = os.getenv("CONTAINER_BRONZE", "bronze")
RAW_DATA_DIR = Path(__file__).parent.parent / "data" / "raw"

def get_azure_credential():
    """Get Azure credential - uses Azure CLI login."""
    return AzureCliCredential()

def get_datalake_service_client():
    """Initialize Data Lake service client."""
    account_url = f"https://{STORAGE_ACCOUNT}.dfs.core.windows.net"
    credential = get_azure_credential()
    return DataLakeServiceClient(account_url, credential)

def upload_to_bronze(file_path: Path, partition_date: str = None):
    """Upload file ke bronze container dengan partition structure."""
    service_client = get_datalake_service_client()
    file_system_client = service_client.get_file_system_client(CONTAINER_BRONZE)

    # Partition path: /year=YYYY/month=MM/day=DD/filename.csv
    if partition_date:
        # Format: YYYY-MM-DD atau bisa pakai tanggal sekarang
        partition_path = f"jakarta_house_price/{partition_date}/{file_path.name}"
    else:
        from datetime import datetime
        today = datetime.now().strftime("%Y-%m-%d")
        partition_path = f"jakarta_house_price/ingestion_date={today}/{file_path.name}"

    print(f"Uploading {file_path.name} to: {partition_path}")

    file_client = file_system_client.get_file_client(partition_path)

    # Upload file
    with open(file_path, "rb") as f:
        file_client.upload_data(f, overwrite=True)

    print(f"✅ Uploaded: {partition_path}")

def ingest_all():
    """Ingest semua file dari raw directory."""
    if not RAW_DATA_DIR.exists():
        print(f"❌ Raw data directory not found: {RAW_DATA_DIR}")
        print("Run download_jakarta_house_price.py first")
        return

    csv_files = list(RAW_DATA_DIR.glob("*.csv"))

    if not csv_files:
        print(f"❌ No CSV files found in {RAW_DATA_DIR}")
        return

    print(f"Found {len(csv_files)} CSV files to ingest")

    service_client = get_datalake_service_client()
    file_system_client = service_client.get_file_system_client(CONTAINER_BRONZE)

    for csv_file in csv_files:
        upload_to_bronze(csv_file)

    print("\n✅ Ingestion complete!")
    print(f"Data location: https://{STORAGE_ACCOUNT}.dfs.core.windows.net/{CONTAINER_BRONZE}/jakarta_house_price/")

if __name__ == "__main__":
    ingest_all()
