import dash_mantine_components as dmc
from dash_iconify import DashIconify
from components.side_bar_buttons import side_bar_buttons
from components.sidebar_filters import create_filter_section

def filter_header():
            # Compact header
        return dmc.Group([
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
        ], justify="space-between")

def filter_actions():
    return dmc.Group([
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

def create_dropdown():
    """Create the product selection dropdown"""
    return dmc.Box([
        dmc.Select(
            id="selection-dropdown",
            searchable=True,
            placeholder="Search for a procedure or medication..."
        )
    ], className="dropdown-container")

def dropdown_tooltip():
    """Create the tooltip for the dropdown"""
    return dmc.Tooltip(
        label="Switch between HCPCS and NDC codes",
        children=DashIconify(icon="mdi:help-circle-outline", width=18, color="#1976d2"),
        position="right",
        withArrow=True,
        offset=4
    )

def toggle_switch():
    """Create toggle switch"""
    return dmc.Box([
        dmc.Group([
            dmc.Switch(id="switch-toggle", checked=True),
            dmc.Box("Search by HCPCS", id="switch-text"),
        ])
    ])


def render_sidebar():
    """Create the navigation panel with search, actions, and filters."""
    return dmc.Card([
        dmc.Stack([
            # Search Section
            dmc.Text(
                'Search & Filter',
                className='section-title-modern',
                style={
                    'fontSize': '1.05rem',
                    'fontWeight': 500,
                    'letterSpacing': '0.01em',
                    'marginBottom': '0.2rem',
                    'color': '#1976d2',
                }
            ),
            dmc.Divider(),
            dmc.Group([
                create_dropdown(),
                dropdown_tooltip()
            ], gap='xs', align='center'),
            dmc.Box(
                toggle_switch(),
                style={
                    'flexGrow': 0,
                    'display': 'flex',
                    'flexDirection': 'column',
                }
            ),
            
            # Filters section
            dmc.Divider(mb='xs', mt='md'),
            filter_header(),
            create_filter_section(),
            filter_actions(),
              
            # Actions section
            dmc.Divider(mb='xs'),
            dmc.Text("Actions", size="sm", style={'color': '#888', 'marginBottom': '0.2rem', 'marginTop': '0.2rem', 'fontWeight': 500}),
            side_bar_buttons(),
            
        ], gap='sm', style={
            'flexGrow': 1,
            'display': 'flex',
            'flexDirection': 'column',
            'height': '100%'
        }),
    ], shadow='md', p='md', radius='md', style={
        'background': 'linear-gradient(135deg, #f8fafc 80%, #e3f2fd 100%)',
        'border': '1px solid #e3e8ee',
        'minWidth': '300px',
        'maxWidth': '380px',
        'margin': '0 auto',
        'boxShadow': '0 2px 12px rgba(30, 64, 175, 0.07)',
        'height': 'calc(100vh - 120px)',
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'flex-start',
        'paddingBottom': '1.5rem',
        'overflowY': 'auto',  # Enable scrolling for the sidebar
    })

