from tables.tables import BENCHMARK_TABLE, HCPCS_DESC_TABLE, NDC_NAME_TABLE
from polars import col as c
import dash_mantine_components as dmc
from helpers.helpers import get_hcpcs_code, get_ndc_codes
from helpers.transparency_table_helpers import transparency_table

def render_transparency_table(is_hcpcs, value):
    value = get_hcpcs_code(value) if is_hcpcs else get_ndc_codes(value)
    elements = transparency_table(value, is_hcpcs=is_hcpcs).collect(engine='streaming').to_dicts()

    rows = [
        dmc.TableTr(
            [
                dmc.TableTd(element["description"]),
                dmc.TableTd(element["variable"]),
                dmc.TableTd(element["value"]),
            ]
        )
        for element in elements
    ]

    head = dmc.TableThead(
        dmc.TableTr(
            [
                dmc.TableTh("Description"),
                dmc.TableTh("Benchmark"),
                dmc.TableTh("Price"),
            ]
        )
    )
    body = dmc.TableTbody(rows)
    #caption = dmc.TableCaption("Some elements from periodic table")
    table =dmc.Table([head, body])
    return table

