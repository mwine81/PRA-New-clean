import polars as pl
from polars import col as c
import polars.selectors as cs
from models.models import AGTable
from tables.tables import BENCHMARK_TABLE, HCPCS_DESC_TABLE, HOSPITAL_TABLE, NDC_NAME_TABLE, HOSPITAL_PRICE_TABLE
from rich import print
import dash_mantine_components as dmc
from dash import html
from pathlib import Path

def get_product_list() -> list:
    """
    Get a list of unique product names.
    
    Returns:
        list: A list of unique product names.
    """
    return NDC_NAME_TABLE.select(c("product")).unique().sort('product').collect().to_series().to_list()


def get_hcpcs_desc_list() -> list:
    """
    Get a list of unique HCPCS descriptions.
    
    Returns:
        list: A list of unique HCPCS descriptions.
    """
    return HCPCS_DESC_TABLE.select(c("hcpcs_desc")).unique().sort('hcpcs_desc').collect().to_series().to_list()


def get_hcpcs_code(hcpcs_desc: str) -> str:
    """
    Get the HCPCS code for a given description.
    
    Args:
        hcpcs_desc (str): The HCPCS description.
        
    Returns:
        str: The corresponding HCPCS code.
    """
    return HCPCS_DESC_TABLE.filter(c("hcpcs_desc") == hcpcs_desc).select(c("hcpcs")).collect(engine="streaming").item()

def get_ndc_codes(product: str) -> list:
    """
    Get the NDC codes for a given product.
    
    Args:
        product (str): The product name.
        
    Returns:
        list: The corresponding NDC codes.
    """
    return NDC_NAME_TABLE.filter(c("product") == product).select(c("ndc")).collect(engine="streaming").to_series().to_list()


def filter_payment_info(how: str, value: str, data: pl.LazyFrame = HOSPITAL_PRICE_TABLE) -> pl.LazyFrame | None:
    if how == "hcpcs":
        return data.filter(c("hcpcs") == get_hcpcs_code(value))
    if how == "ndc":
        return data.filter(c("ndc").is_in(get_ndc_codes(value)))
    # return an empty dataframe if no match
    return None

def get_hcpcs_code_from_desc(hcpcs_desc: str) -> str:
    """
    Extract HCPCS code from description string.
    
    Args:
        hcpcs_desc (str): The HCPCS description.
        
    Returns:
        str: The corresponding HCPCS code.
    """
    return HCPCS_DESC_TABLE.filter(c("hcpcs_desc") == hcpcs_desc).select(c("hcpcs")).collect(engine="streaming").item()



def create_html_table(data):
    """Create an HTML table from data dictionary"""
    if not data or not data.get('desc'):
        return no_price_table()
    
    # Create table rows
    rows = []
    for i in range(len(data['desc'])):
        rows.append(
            html.Tr([
                html.Td(data['desc'][i]),
                html.Td(data['price_type'][i]),
                html.Td(data['amount'][i])
            ])
        )
    
    return dmc.Box([
        html.Table([
            html.Thead([
                html.Tr([
                    html.Th("Description"),
                    html.Th("Price Type"),
                    html.Th("Amount")
                ])
            ]),
            html.Tbody(rows)
        ])
    ], className="price-table-section")

def no_price_table():
    """Create a no-price table placeholder"""
    return dmc.Box(
        html.Table([
            html.Tr([
                html.Td("No pricing information available.", colSpan=3, className="no-prices-row")
            ])
        ]),
        className="price-table-section"
    )


