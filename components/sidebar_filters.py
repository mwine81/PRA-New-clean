import dash_mantine_components as dmc
from dash_iconify import DashIconify

def create_filter_section():
    return dmc.Box([

        
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
                label=dmc.Tooltip("State", label="Enter state abbreviation(s), seperate with '|' for multiple state search (e.g., CA|NY|TX)"),
                placeholder="State Abbreviation e.g., CA|NY|TX",
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
        
    ],
    style={
        'backgroundColor': '#f8f9fa',
        'padding': '4px',
        'borderRadius': '8px',
        # 'border': '1px solid #e9ecef',
        'maxHeight': '80vh',
        'overflowY': 'auto'
    }
    )

