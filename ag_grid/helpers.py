import polars as pl
from helpers.helpers import filter_payment_info
from tables.tables import HOSPITAL_TABLE

def get_grid_data(is_hcpcs: bool, value: str) -> pl.LazyFrame:
    selection_type = 'hcpcs' if is_hcpcs else 'ndc'
    # Get filtered data
    filtered_data = (
        filter_payment_info(selection_type, value)
        .join(HOSPITAL_TABLE, left_on='hospital_id', right_on='id') # type: ignore
        
    )
    return filtered_data