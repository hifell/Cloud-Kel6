# Final Project Planning: Bautomate PropTech Analytics

**Target:** Azure Lakehouse End-to-End & Mesin Rekomendasi Investasi Properti (Margin of Safety).
**Environment:** Debian (slim7), VS Code, Python/Poetry, Azure Data Lake Storage Gen2 (`adlskelompok6`), Azure Synapse Analytics.
**Team Roles:** Thufail (Lead Data Engineer/Architect), Evan, Otniel, Falah.
**Strict Constraint:** Data WAJIB riil hasil scraping mandiri dari 99.co, WAJIB mematuhi FinOps (hemat), dan WAJIB memenuhi 10 Pilar Arsitektur RPS.

## 🚀 Pre-requisites & Setup (Local to Cloud)
- [x] **Task 0.1:** Inisialisasi repositori Git lokal dan setup `pyproject.toml` menggunakan Poetry (Dependencies: `pyspark`, `delta-spark`, `azure-storage-file-datalake`, `xgboost`, `mlflow`, `fastapi`, `beautifulsoup4`, `requests`, `playwright`).
- [x] **Task 0.2:** Autentikasi Azure CLI (`az login`).
- [x] **Task 0.3:** Eksekusi Azure CLI untuk membuat 3 container (`bronze`, `silver`, `gold`) di `adlskelompok6`.

---

## 🎯 Milestone 1: Real Data Ingestion & Storage (Target RPS: Pertemuan 4)
**Kriteria:** Ekstraksi data riil dan unggah ke lapisan Bronze DENGAN STRUKTUR PARTISI + NEAR REAL-TIME INGESTION.

- [x] **Task 1.1 (Custom Scraper):** Buat script `scrape_properti.py` menggunakan **Playwright** untuk mengekstrak minimal 1.000+ data listing dari **99.co** secara *headless* dengan *delay anti-bot*, simpan sebagai `raw_property_data.csv`.
- [x] **Task 1.2 (Partitioning):** Buat script `ingest_to_bronze.py` untuk mengunggah CSV ke container `bronze` **dengan struktur partisi direktori berdasarkan tanggal scraping** (contoh: `bronze/raw_data/year=YYYY/month=MM/day=DD/`).
- [x] **Task 1.3 (Near Real-Time Ingestion):** Buat Azure Function Timer Trigger (`microbatch_stream`) untuk menjalankan ingest setiap **5 menit** secara otomatis. Cost: ~$0/bulan (Consumption Plan). Konfigurasi schedule: `0 */5 * * * *`. ✅ Alternative: Azure Logic Apps (docs/LOGICAPPS_SETUP.md)

---

## 🎯 Milestone 2: Security & FinOps (Target RPS: Pertemuan 7)
**Kriteria:** RBAC dan perlindungan kredit Azure (Maks $100).

- [x] **Task 2.1:** Konfigurasi RBAC via Azure CLI. Berikan role `Storage Blob Data Contributor` pada `adlskelompok6` untuk seluruh anggota tim.
- [x] **Task 2.2:** Buat Budget Alert via Azure CLI sebesar $50 dengan notifikasi email saat pemakaian mencapai 50% dan 75%.
- [x] **Task 2.3:** Konfigurasi Auto-Pause agresif (10 menit) dan ukuran node terkecil pada Synapse Spark Pool.

---

## 🎯 Milestone 3: Processing, Delta Lake & Orchestration (Target RPS: Pertemuan 10)
**Kriteria:** Transformasi Medallion, Pipeline Orkestrasi, dan Near Real-Time Micro-Batch.

- [x] **Task 3.1 (Silver & Delta Lake MERGE):** Buat script `transform_silver.py`. Baca data terpartisi dari `bronze`, bersihkan anomali harga. Gunakan operasi Delta Lake `MERGE` (Upsert) untuk menangani update data baru secara **near real-time**, simpan ke `silver`.
- [x] **Task 3.2 (Gold & Business Logic):** Buat script `aggregate_gold.py`. Hitung rata-rata harga per kecamatan, buat kolom `Margin_of_Safety_Pct` dan label `Investment_Score`. Simpan ke `gold` (Delta Lake).
- [x] **Task 3.3 (Orchestration & Streaming):** Rancang **Azure Synapse Pipeline** untuk menjadwalkan eksekusi `ingest_to_bronze.py` -> `transform_silver.py` -> `aggregate_gold.py` secara **terotomatisasi**. Gunakan **Trigger Schedule** setiap 5 menit untuk simulasi near real-time processing.

---

## 🎯 Milestone 4: Machine Learning, Retraining & BI (Target RPS: Pertemuan 12)
**Kriteria:** Model ML, API inference, ML Retraining, dan dashboard Power BI.

- [x] **Task 4.1:** Buat `train_xgboost.py` (XGBoost Regressor) terintegrasi dengan **MLflow** untuk *tracking* metrik (RMSE, MAE).
- [x] **Task 4.2 (Retraining Mechanism):** Tambahkan logika di dalam script `train_xgboost.py` untuk mengevaluasi data *batch* baru. Jika performa model turun (data drift), model otomatis dilatih ulang (*retrain*).
- [x] **Task 4.3:** Kemas model terbaik menjadi REST API *inference* menggunakan **Azure Functions (Serverless/Gratis)**.
- [x] **Task 4.4 (Power BI Dashboard):** Hubungkan data `gold` ke **Power BI Desktop** untuk membuat dashboard interaktif dengan:
  - "Top 10 Properti Strong Buy" (filter + sort)
  - Peta Panas (Heatmap) wilayah investasi
  - Time series harga rata-rata per lokasi
  - Slicer filter (kamar, luas, range harga)
  ✅ Guide: docs/POWERBI_GUIDE.md

---

## 🎯 Milestone 5: CI/CD, Observabilitas & Dokumentasi (Target RPS: Pertemuan 15-16)
**Kriteria:** Otomatisasi deployment (CI/CD), monitoring lengkap, dan dokumentasi jurnal Bab I-V.

- [x] **Task 5.1:** Buat file `.github/workflows/deploy.yml` (GitHub Actions) untuk otomatisasi *deployment* pipeline data dan model ke lingkungan Azure.
- [x] **Task 5.2 (Dokumentasi Lengkap):** Finalisasi dokumentasi sesuai format jurnal Bab I-V:
  - **Bab I:** Pendahuluan (Latar belakang, Rumusan masalah, Tujuan)
  - **Bab II:** Tinjauan Pustaka (Azure Lakehouse, Delta Lake, XGBoost, Margin of Safety)
  - **Bab III:** Metodologi (Arsitektur sistem, Data flow, Pipeline)
  - **Bab IV:** Hasil & Pembahasan (Screenshots, Metrik, Analisis)
  - **Bab V:** Penutup (Kesimpulan, Saran)
  - **Lampiran:** Diagram arsitektur, FinOps proof, API documentation
  ✅ Full report: docs/LAPORAN_AKHIR_BAUTOMATE.md

---

## 📊 Aspek Penilaian & Capaian

| No | Aspek | Skala Target | Evidence |
|----|-------|--------------|----------|
| 1 | Arsitektur E2E | 4 (Sangat Baik) | Full pipeline scraper → bronze → silver → gold → ML → API |
| 2 | Ingestion & Storage | 4 (Sangat Baik) | Near real-time (5 min), partitioning, Delta Lake |
| 3 | Query & Transformasi | 4 (Sangat Baik) | Delta MERGE/Upsert, Synapse SQL, time travel |
| 4 | Streaming | 4 (Sangat Baik) | Azure Function Timer (5 min), Micro-batch, checkpoint |
| 5 | ML & Analitik | 4 (Sangat Baik) | XGBoost + retraining + feature importance |
| 6 | Visualisasi BI | 4 (Sangat Baik) | Power BI interactive dashboard |
| 7 | Keamanan | 4 (Sangat Baik) | RBAC, Budget Alert, encryption, Managed Identity |
| 8 | Observabilitas | 4 (Sangat Baik) | Budget monitoring, logging, lineage, cost alert |
| 9 | Dokumentasi | 4 (Sangat Baik) | Bab I-V lengkap + diagram + FinOps proof |

---

## 💰 FinOps Cost Summary

| Resource | Config | Monthly Cost |
|----------|--------|-------------|
| Azure Data Lake | 3 containers | ~$5-10 |
| Azure Synapse | Serverless SQL | ~$5-10 |
| Synapse Spark Pool | Auto-pause 10min | ~$0 (idle) |
| Azure Function | Consumption (5 min) | **~$0** |
| GitHub Actions | 2000 min/month | $0 |
| **Total** | | **~$10-20/bulan** |

Budget Alert: $50 (50% = $25, 75% = $37.5)

---

## 🔗 Resource Links

- **Synapse Workspace:** https://web.azuresynapse.net?workspace=%2fsubscriptions%2f556c1a59-fd27-4102-8dca-1a20c2582164%2fresourceGroups%2ftechnology-cloud-sainsdata%2fproviders%2fMicrosoft.Synapse%2fworkspaces%2fkelompok6
- **Storage Account:** adlskelompok6
- **Budget Alert:** batomate-budget ($50/month)
