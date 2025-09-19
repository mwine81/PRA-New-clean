import dash_mantine_components as dmc
from dash_iconify import DashIconify

def side_bar_buttons():
        """Create control buttons"""
        return dmc.Stack([
            dmc.Button(
                "Toggle Price Comparison", 
                id="price-collapse-btn", 
                n_clicks=0, 
                variant='outline',
                leftSection=DashIconify(icon="mdi:table-eye", width=16),
                color='blue'
            ),
            dmc.Button(
                "Toggle Hospital Data", 
                id="collapse-btn", 
                n_clicks=0, 
                variant='outline',
                leftSection=DashIconify(icon="mdi:grid", width=16),
                color='blue'
            ),
            dmc.Button(
                "Export Data", 
                id="csv-button", 
                n_clicks=0, 
                variant='filled',
                leftSection=DashIconify(icon="mdi:download", width=16),
                color='green'
            ),
            dmc.Button(
                "Data Dictionary", 
                id="schema-btn", 
                n_clicks=0, 
                variant='outline',
                leftSection=DashIconify(icon="mdi:database-eye", width=16),
                color='violet'
            ),
        ], gap='sm')