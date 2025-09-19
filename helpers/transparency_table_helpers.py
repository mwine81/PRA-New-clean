import polars as pl
from polars import col as c
import polars.selectors as cs
from tables.tables import BENCHMARK_TABLE, HCPCS_DESC_TABLE, NDC_NAME_TABLE

##Transparency Table Logic
def format_usd(col_to_format, alias) -> pl.Expr:
    return col_to_format.map_elements(lambda x: f"${x:,.2f}", return_dtype=pl.String).alias(alias)

def base_transparency_table(value, is_hcpcs):
    return (
        BENCHMARK_TABLE
        .pipe(lambda df: df.filter(c.hcpcs == value) if is_hcpcs else df.filter(c.ndc.is_in(value)))
    )

def ndc_summary(value, is_hcpcs):
    return (
        base_transparency_table(value, is_hcpcs)
        .join(NDC_NAME_TABLE, on='ndc')
        .rename({'product':'description'})
        .drop(['hcpcs','ndc'])
        .group_by(c.description)
    .agg(cs.numeric().mean())
    )

def hcpcs_summary(value, is_hcpcs):
    return (
        base_transparency_table(value, is_hcpcs)
        .join(HCPCS_DESC_TABLE, on='hcpcs')
        .rename({'hcpcs_desc':'description'})
    .drop(['hcpcs','ndc'])
    .group_by(c.description.str.split('[').list.first().str.strip_chars())
    .agg(cs.numeric().mean())
)

def transparency_table(value, is_hcpcs) -> pl.LazyFrame:
    return (
    pl.concat([ndc_summary(value, is_hcpcs), hcpcs_summary(value, is_hcpcs)])
    .rename({'asp':'ASP','nadac':'NADAC', 'tx_unit_price':'TX Unit Price','tx_340b':'TX 340B'})
    .unpivot(index='description')
    .filter(c.value.is_not_null())
    .with_columns(format_usd(c.value, "value"))
    .sort(c.description, c.variable)
)

