from dash import html
import dash_mantine_components as dmc
def no_price_table():
    return dmc.Box(
            html.Table(
                [html.Tr([
                    html.Td("No pricing information available.", colSpan=3, className="no-prices-row")
                ])]
            ),
            className="price-table-section"
        )