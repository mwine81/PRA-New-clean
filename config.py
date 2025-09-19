from pathlib import Path

#DATABASE_DIR = Path(r'C:\Users\mwine\3 Axis Advisors Dropbox\Matthew matt@3axisadvisors.com\datalake\projects\SEPT_2025\PRA\data_sept_2025\app')
DATABASE_DIR = Path('data')
BENCHMARK_FILE = DATABASE_DIR / "benchmark_table.parquet"
HCPCS_DESC_FILE = DATABASE_DIR / "hcpcs_desc_table.parquet"
NDC_NAME_FILE = DATABASE_DIR / "ndc_name_table.parquet"
HOSPITAL_FILE = DATABASE_DIR / "hospital_table.parquet"
HOSPITAL_PRICE_FILE = DATABASE_DIR / "hospital_price_table.parquet"

UNIQUE_LOB_FILE = DATABASE_DIR / "unique_lob_names.parquet"
UNIQUE_PLAN_FILE = DATABASE_DIR / "unique_plan_names.parquet"