import dash_mantine_components as dmc
from dash_iconify import DashIconify
from dash import dcc


def _visualization_grid_col(viz_id, btn_id):
    """Reusable GridCol for visualization cards."""
    expand_icon = DashIconify(icon="mdi:fullscreen", width=22, height=22, style={"verticalAlign": "middle"})
    return dmc.GridCol(
        dmc.Card([
            dmc.Stack([
                dmc.Box([
                    dmc.Button(
                        expand_icon,
                        id=btn_id,
                        n_clicks=0,
                        variant='subtle',
                        size='lg',
                        className='expand-fab',
                        style={
                            'position': 'absolute',
                            'top': '12px',
                            'left': '12px',
                            'zIndex': 2,
                            'borderRadius': '50%',
                            'padding': '0.35rem',
                            'minWidth': '44px',
                            'minHeight': '44px',
                            'width': '44px',
                            'height': '44px',
                            'display': 'flex',
                            'alignItems': 'center',
                            'justifyContent': 'center',
                            'boxShadow': '0 2px 8px rgba(0,0,0,0.10)',
                            'background': 'rgba(255,255,255,0.95)',
                            'border': '1px solid #e3e8ee',
                            'transition': 'box-shadow 0.2s, background 0.2s',
                        }
                    ),
                ], style={'position': 'relative', 'width': '100%', 'height': '0'}),
                dcc.Loading(
                    dcc.Graph(id=viz_id),
                    type="circle"
                ),
            ], gap=0, style={'position': 'relative'}),
        ], shadow='sm', p="sm"),
        span={'base': 12, 'xl': 6}  # type: ignore
    )

def _visualization_container():
    """Create the visualization container"""
    return dmc.Grid([
        _visualization_grid_col('map', 'expand-map-btn'),
        _visualization_grid_col('price-distribution', 'expand-distribution-btn'),
    ])

def render_charts():
        """Create the charts section with professional, modern header"""
        return dmc.Card([
            dmc.Text(
                "Hospital Price Analysis",
                className='section-title-modern',
                style={
                    'textAlign': 'center',
                    'fontSize': '1.35rem',
                    'fontWeight': 600,
                    'letterSpacing': '0.01em',
                    'marginBottom': '0.5rem',
                    'color': '#1565c0',
                }
            ),
            _visualization_container(),
        ], shadow='sm')
