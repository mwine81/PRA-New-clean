import dash_mantine_components as dmc
from dash_iconify import DashIconify

def create_filter_section():
    return dmc.Box(
        dmc.Card([
        dmc.SimpleGrid([
            dmc.TextInput(
                label="Hospital Name",
                placeholder="Enter hospital name...",
                id="hospital-regex"
            ),
            dmc.TextInput(
                label="Description Keyword",
                placeholder="Enter description keyword...",
                id="description-regex"
            ),
            dmc.TextInput(
                label="State",
                placeholder="state...",
                id="state-regex"
            ),
            dmc.TextInput(
                label="Payor Name",
                placeholder="Enter payor name...",
                id="payor-regex"
            ),
            dmc.Box()  # Empty box to fill the grid
        ], cols=3),
        dmc.Group([
            dmc.Button(
                "Apply Filters", 
                id="apply-filters-btn", 
                n_clicks=0, 
                variant='filled',
                leftSection=DashIconify(icon="mdi:filter", width=16),
                color='blue'
            ),
            dmc.Button(
                "Clear Filters", 
                id="clear-filters-btn", 
                n_clicks=0, 
                variant='outline',
                leftSection=DashIconify(icon="mdi:filter-remove", width=16),
                color='gray'
            )
        ], gap='sm', style={'marginTop': '1rem'})
    ], shadow='sm'), className='filter-section'
    )

