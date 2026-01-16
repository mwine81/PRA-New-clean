import shutil
from pathlib import Path
import polars as pl
from polars import col as c
import polars.selectors as cs
to_copy = r"C:\Users\mwine\3 Axis Advisors Dropbox\Matthew matt@3axisadvisors.com\datalake\projects\SEPT_2025\PRA\data_sept_2025\app"
copy_dir = 'data'
# shutil.rmtree(copy_dir, ignore_errors=True)
# Path(copy_dir).mkdir(parents=True, exist_ok=True)
# copy every file from to copy to copy dir
# for file in Path(to_copy).iterdir():
#     if file.is_file():
#         shutil.copy(file, copy_dir)
# polars
# pandas
# dash
# dash-ag-grid
# dash-mantine-components
# plotly
# patito
# dash-iconify
# gunicorn
# rich