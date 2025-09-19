from polars import col as c
import polars as pl
import polars.selectors as cs
import patito as pt
from pathlib import Path
from config import BENCHMARK_FILE, HCPCS_DESC_FILE, NDC_NAME_FILE, HOSPITAL_FILE, HOSPITAL_PRICE_FILE
from models.models import BenchmarkFile,  NDCNameTable, HospitalTable, HospitalPriceFile, HcpcsDescTable

def load_table(file_path: Path, df_model) -> pl.LazyFrame:
    """
    Load a table from a Parquet file and select the relevant columns based on the provided model.
    """
    return pl.scan_parquet(file_path).select(df_model.columns)

# Load the tables using the defined models

BENCHMARK_TABLE = load_table(BENCHMARK_FILE, BenchmarkFile)
HCPCS_DESC_TABLE = load_table(HCPCS_DESC_FILE, HcpcsDescTable)
NDC_NAME_TABLE = load_table(NDC_NAME_FILE, NDCNameTable)
HOSPITAL_TABLE = load_table(HOSPITAL_FILE, HospitalTable)
HOSPITAL_PRICE_TABLE = load_table(HOSPITAL_PRICE_FILE, HospitalPriceFile)
