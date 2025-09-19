import dash_mantine_components as dmc
import dash_ag_grid as dag
from ag_grid.ag_grid_def import columnDefs, defaultColDef, dashGridOptions

def render_grid():
        """Create the data grid section with modern header"""
        return dmc.Card([
            dmc.Text(
                "Hospital Pricing Database",
                className='section-title-modern',
                style={
                    'fontSize': '1.15rem',
                    'fontWeight': 500,
                    'textAlign': 'center',
                    'letterSpacing': '0.01em',
                    'marginBottom': '0.3rem',
                    'color': '#1565c0',
                }
            ),
            dmc.Text(
                'Click the toggle to expand',
                size='sm', 
                id='hidden-grid-text', 
                className='hidden-text',
                style={'display': 'none'}
            ),
            dmc.Collapse(
                dag.AgGrid(
                    id='grid',
                    className='ag-theme-alpine',
                    columnDefs=columnDefs,
                    defaultColDef=defaultColDef,
                    dashGridOptions=dashGridOptions,
                    csvExportParams={"fileName": "hospital_data.csv"},
                    style={'height': '500px'}
                ),
                opened=True, 
                id='collapse-grid'
            )
        ], shadow='sm')