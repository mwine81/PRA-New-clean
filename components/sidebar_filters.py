import dash_mantine_components as dmc
from dash_iconify import DashIconify

def create_filter_section():
    return dmc.Box([
        # Compact header
        dmc.Group([
            dmc.Text(
                "Data Filters",
                size="sm",
                style={'color': '#495057', 'fontWeight': '600'}
            ),
            dmc.ThemeIcon(
                DashIconify(icon="mdi:filter-variant", width=16),
                size="sm",
                color="blue",
                variant="light"
            )
        ], justify="space-between", mb="md"),
        
        # Compact filter layout
        dmc.Stack([
            # Basic filters in single column
            dmc.TextInput(
                label="Hospital Name",
                placeholder="Search hospitals...",
                id="hospital-regex",
                leftSection=DashIconify(icon="mdi:magnify", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            dmc.TextInput(
                label="State",
                placeholder="Enter state...",
                id="state-regex",
                leftSection=DashIconify(icon="mdi:map-marker", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            dmc.TextInput(
                label="Description",
                placeholder="Search descriptions...",
                id="description-regex",
                leftSection=DashIconify(icon="mdi:text-search", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            
            # Status dropdowns
            dmc.Select(
                label="340B Status",
                id="340b-status-dropdown",
                placeholder="Select status...",
                data=["Eligible", "Ineligible"],
                clearable=True,
                leftSection=DashIconify(icon="mdi:hospital", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            dmc.Select(
                label="Setting",
                id="setting-status-dropdown",
                placeholder="Select setting...",
                data=["inpatient", "outpatient", "both"],
                clearable=True,
                leftSection=DashIconify(icon="mdi:medical-bag", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            
            # Plan filters
            dmc.TextInput(
                label="Payer Name",
                placeholder="Search payers...",
                id="payer-regex",
                leftSection=DashIconify(icon="mdi:account-group", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            dmc.TextInput(
                label="Plan Name",
                placeholder="Search plans...",
                id="plan-regex",
                leftSection=DashIconify(icon="mdi:clipboard-text", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            dmc.TextInput(
                label="Plan Mapped",
                placeholder="Search mapped plans...",
                id="plan-mapped-regex",
                leftSection=DashIconify(icon="mdi:map", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            dmc.TextInput(
                label="LOB Mapped",
                placeholder="Search LOB mappings...",
                id="lob-mapped-regex",
                leftSection=DashIconify(icon="mdi:sitemap", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
            
            # Drug info
            dmc.TextInput(
                label="Drug Measurement",
                placeholder="Search measurements...",
                id="drug-measurement-regex",
                leftSection=DashIconify(icon="mdi:ruler", width=14),
                size="sm",
                styles={'input': {'fontSize': '13px'}}
            ),
        ], gap="xs"),
        
        # Compact action buttons
        dmc.Group([
            dmc.Button(
                "Apply", 
                id="apply-filters-btn", 
                n_clicks=0, 
                variant='filled',
                leftSection=DashIconify(icon="mdi:filter-check", width=16),
                size="sm",
                radius="md",
                color="blue",
                style={'flex': '1', 'fontSize': '12px'}
            ),
            dmc.Button(
                "Clear", 
                id="clear-filters-btn", 
                n_clicks=0, 
                variant='outline',
                leftSection=DashIconify(icon="mdi:filter-remove", width=16),
                color='red',
                size="sm",
                radius="md",
                style={'flex': '1', 'fontSize': '12px'}
            )
        ], gap='sm', grow=True, mt="sm")
    ],
    style={
        'backgroundColor': '#f8f9fa',
        'padding': '12px',
        'borderRadius': '8px',
        'border': '1px solid #e9ecef',
        'maxHeight': '60vh',
        'overflowY': 'auto'
    }
    )

