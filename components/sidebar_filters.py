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
                label="State",
                placeholder="state...",
                id="state-regex"
            ),
            dmc.Select(
                label="340B Status",
                id="340b-status-dropdown",
                placeholder="Select 340B status...",
                data=[
                    {"value": '1', "label": "Eligible"},
                    {"value": '0', "label": "Ineligible"},
                ],
                clearable=True
            ),
            dmc.TextInput(
                label="Description Keyword",
                placeholder="Enter description keyword...",
                id="description-regex"
            ),

            dmc.Select(
                label="Setting status",
                id="setting-status-dropdown",
                placeholder="Select setting status...",
                data=[
                    {"value": 'inpatient', "label": "Inpatient"},
                    {"value": 'outpatient', "label": "Outpatient"},
                    {"value": 'both', "label": "Both"},
                ],
                clearable=True
            ),
                dmc.TextInput(
                label="Payer Name",
                placeholder="Enter payer name...",
                id="payer-regex"
            ),
                dmc.TextInput(
                label="Plan Name",
                placeholder="Enter plan name...",
                id="plan-regex"
            ),
                dmc.TextInput(
                label="Plan Mapped Name",
                placeholder="Enter plan mapped name...",
                id="plan-mapped-regex"
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

