import dash_mantine_components as dmc
from dash import Dash, Input, Output, State, callback,no_update, callback_context
from dash.exceptions import PreventUpdate
from UI.index import layout
from helpers.helpers import get_product_list, get_hcpcs_desc_list,no_price_table, get_hcpcs_code_from_desc,filter_payment_info, create_html_table
from ag_grid.helpers import get_grid_data
from figure.fig_schema import schema_for_fig_data
import polars as pl
from polars import col as c
from figure.price_dist_plot import create_price_distribution_plot
from figure.map_plot import create_map_plot
from tables.tables import HOSPITAL_TABLE
from components.render_tranparency_table import render_transparency_table

app = Dash()

app.layout = dmc.MantineProvider(layout)

@callback(
    Output("switch-text", "children"), 
    Input("switch-toggle", "checked")
)
def update_switch_text(checked):
    """Update the switch description text"""
    return f"Search by {'HCPCS' if checked else 'Product'}"

@callback(
    Output("appshell", "navbar"),
    Input("burger", "opened"),
    State("appshell", "navbar"),
)
def toggle_navbar(opened, navbar):
    navbar["collapsed"] = {"mobile": not opened}
    return navbar

@callback(
    [Output('selection-dropdown', 'data'),
     Output('selection-dropdown', 'value')],
    Input('switch-toggle', 'checked')
)
def update_dropdown_options(is_hcpcs):
    """Update dropdown options based on toggle selection"""
    try:
        if is_hcpcs:
            options = get_hcpcs_desc_list()
        else:
            options = get_product_list()
        
        return options, options[0] if options else None
    except Exception as e:
        print(f"Error updating dropdown options: {e}")
        return [], None

@callback(
    [Output('grid', 'rowData'),
     Output('price-info', 'children')],
    [Input('selection-dropdown', 'value'),
     Input('switch-toggle', 'checked')]
)
def update_data_and_prices(selected_value, is_hcpcs):
    """Update grid data and price information"""
    if not selected_value:
        return [], no_price_table()
    
    try:
        # Use existing ag_grid helpers function
        filtered_data = get_grid_data(is_hcpcs, selected_value).collect(engine='streaming').to_dicts()
        transparency_table = render_transparency_table(is_hcpcs, selected_value)

        return filtered_data, transparency_table

    except Exception as e:
        print(f"Error updating data: {e}")
        return [], no_price_table()

@callback(
    [Output('map', 'figure'),
     Output('price-distribution', 'figure')],
    [Input('grid', 'virtualRowData'),
     Input('grid', 'rowData')]
)
def update_visualizations(virtual_row_data, row_data):
    """Update map and price distribution charts"""
    # Use virtualRowData if available (when filtering/scrolling), otherwise use rowData
    data_to_use = virtual_row_data if virtual_row_data else row_data
    
    if not data_to_use:
        # Return empty figures
        return {}, {}
    
    try:
        data = pl.DataFrame(data_to_use, schema=schema_for_fig_data(), strict=False).lazy()
        map_fig = create_map_plot(data)
        dist_fig = create_price_distribution_plot(data)
        return map_fig.to_dict(), dist_fig.to_dict()
    except Exception as e:
        print(f"Error updating visualizations: {e}")
        return {}, {}

@callback(
    [Output("price-collapse", "opened"),
     Output('hidden-text-price', 'style')],
    Input("price-collapse-btn", "n_clicks")
)
def toggle_price_section(n_clicks):
    """Toggle price section visibility"""
    if not n_clicks:
        return True, {'display': 'none'}
    
    is_open = n_clicks % 2 == 1
    text_style = {'display': 'block' if is_open else 'none'}
    
    return not is_open, text_style

@callback(
    [Output("collapse-grid", "opened"),
     Output('hidden-grid-text', 'style')],
    Input("collapse-btn", "n_clicks")
)
def toggle_grid_section(n_clicks):
    """Toggle grid section visibility"""
    if not n_clicks:
        return True, {'display': 'none'}
    
    is_open = n_clicks % 2 == 1
    text_style = {'display': 'block' if is_open else 'none'}
    
    return not is_open, text_style

@callback(
    Output("grid", "exportDataAsCsv"),
    Input("csv-button", "n_clicks"),
    prevent_initial_call=True
)
def export_csv(n_clicks):
    """Export grid data to CSV"""
    return True if n_clicks else False

@callback(
    Output("schema-modal", "opened"),
    Input("schema-btn", "n_clicks"),
    State("schema-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_schema_modal(n_clicks, opened):
    """Toggle schema modal visibility"""
    return not opened

@callback(
    Output("map-modal", "opened"),
    Output("map-modal-graph", "figure"),
    Input("expand-map-btn", "n_clicks"),
    State("map-modal", "opened"),
    [State("grid", "virtualRowData"),
     State("grid", "rowData")],
    prevent_initial_call=True,
)
def toggle_map_modal(n_clicks, opened, virtual_row_data, row_data):
    """Toggle map modal visibility"""
    # Use virtualRowData if available, otherwise use rowData
    data_to_use = virtual_row_data if virtual_row_data else row_data
    
    if not data_to_use:
        raise PreventUpdate

    if not n_clicks:
        return no_update, no_update
        
    data = pl.DataFrame(
        data_to_use,
        schema=schema_for_fig_data(),
        strict=False
    ).lazy()
    map_fig = create_map_plot(data)
    return not opened, map_fig.to_dict()

@callback(
    Output("distribution-modal", "opened"),
    Output("distribution-modal-graph", "figure"),
    Input("expand-distribution-btn", "n_clicks"),
    State("distribution-modal", "opened"),
    [State("grid", "virtualRowData"),
     State("grid", "rowData")],
    prevent_initial_call=True,
)
def toggle_distribution_modal(n_clicks, opened, virtual_row_data, row_data):
    """Toggle distribution modal visibility"""
    # Use virtualRowData if available, otherwise use rowData
    data_to_use = virtual_row_data if virtual_row_data else row_data
    
    if not data_to_use:
        raise PreventUpdate

    if not n_clicks:
        return no_update, no_update
        
    data = pl.DataFrame(
        data_to_use,
        schema=schema_for_fig_data(),
        strict=False
    ).lazy()
    dist_fig = create_price_distribution_plot(data)
    return not opened, dist_fig.to_dict()

@callback(
    Output("about-modal", "opened"),
    Input("about-btn", "n_clicks"),
    State("about-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_about_modal(n_clicks, opened):
    """Toggle about modal visibility"""
    return not opened

@callback(
    Output("help-modal", "opened"),
    Input("help-btn", "n_clicks"),
    State("help-modal", "opened"),
    prevent_initial_call=True,
)
def toggle_help_modal(n_clicks, opened):
    """Toggle help modal visibility"""
    return not opened

@callback(
    [Output('hospital-info-modal', 'children'),
     Output('hospital-info-modal', 'opened')],
    Input('map', 'clickData'),
    prevent_initial_call=True,
)
def show_hospital_info(click_data):
    """Display hospital information modal when map point is clicked"""
    if not click_data:
        return [], False
    
    try:
        hospital_id = click_data['points'][0]['customdata'][3]
        hospital_data = (
            HOSPITAL_TABLE
            .filter(c.id == hospital_id)
            .collect(engine='streaming')
            .to_dict(as_series=False)
        )
        
        if not hospital_data['name']:
            return [], False
        
        # Create hospital info card
        card = dmc.Card([
            dmc.Stack([
                dmc.Group([
                    dmc.Anchor(
                        dmc.Text(hospital_data['name'][0], className='hospital-title'),
                        href=hospital_data.get('hospital_url', ['#'])[0],
                        target="_blank"
                    ),
                    dmc.Badge("340B Participant", color="green") if hospital_data.get('is_340b', [False])[0] else None,
                ], justify="start"),
                
                dmc.Divider(),
                dmc.SimpleGrid([
                    dmc.Stack([
                        dmc.Text("State", size="sm", fw="bold"),
                        dmc.Text(hospital_data['state'][0])
                    ]),
                    dmc.Stack([
                        dmc.Text("Bed Count", size="sm", fw="bold"),
                        dmc.Text(str(hospital_data['beds'][0]))
                    ]),
                ], cols=2),
            ])
        ], shadow="sm", radius="md", p="lg", className='hospital-card')
        
        return card, True
        
    except Exception as e:
        print(f"Error displaying hospital info: {e}")
        return [], False

if __name__ == "__main__":
    app.run(debug=True)