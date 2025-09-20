import dash_mantine_components as dmc
from dash_iconify import DashIconify

def side_bar_buttons():
        """Create control buttons"""
        return dmc.Stack([
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