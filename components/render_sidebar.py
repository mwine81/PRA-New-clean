import dash_mantine_components as dmc
from dash_iconify import DashIconify
from components.side_bar_buttons import side_bar_buttons

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
    """Create the navigation panel with Actions section directly under the search dropdown."""
    return dmc.Card([
        dmc.Stack([
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
            dmc.Divider(mb='xs'),
            dmc.Group([
                create_dropdown(),
                dropdown_tooltip()
                
            ], gap='xs', align='center'),
            dmc.Space(h=2),
            dmc.Box(
                toggle_switch(),
                style={
                    'flexGrow': 0,
                    'display': 'flex',
                    'flexDirection': 'column',
                    #'minHeight': '90px',
                    'marginBottom': '0.5rem',
                }
            ),
            # Actions section moved directly under dropdown
            dmc.Divider(mb='xs'),
            dmc.Text("Actions", size="sm", style={'color': '#888', 'marginBottom': '0.2rem', 'marginTop': '0.2rem', 'fontWeight': 500}),
            side_bar_buttons(),
            # ...rest of sidebar content if any...
        ], gap='sm', style={
            'flexGrow': 1,
            'display': 'flex',
            'flexDirection': 'column',
            'height': '100%'
        }),
    ], shadow='md', p='md', radius='md', style={
        'background': 'linear-gradient(135deg, #f8fafc 80%, #e3f2fd 100%)',
        'border': '1px solid #e3e8ee',
        'minWidth': '270px',
        'maxWidth': '340px',
        'margin': '0 auto',
        'boxShadow': '0 2px 12px rgba(30, 64, 175, 0.07)',
        'height': 'calc(100vh - 48px)',  # 48px for header/footer or as needed
        'display': 'flex',
        'flexDirection': 'column',
        'justifyContent': 'flex-start',
        'paddingBottom': '1.5rem',  # leave some space at the bottom
    })

