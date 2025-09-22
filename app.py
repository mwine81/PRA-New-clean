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
    [Output('hospital-regex', 'value'),
     Output('description-regex', 'value'),
     Output('state-regex', 'value'),
     Output('payer-regex', 'value'),
     Output('340b-status-dropdown', 'value'),
     Output('setting-status-dropdown', 'value'),
     Output('plan-regex', 'value'),
     Output('plan-mapped-regex', 'value'),
        Output('lob-mapped-regex', 'value'),
        Output('drug-measurement-regex', 'value'),
     # Make sure output is last
     Output('apply-filters-btn', 'n_clicks')
     ],
    Input('clear-filters-btn', 'n_clicks'),
    State('apply-filters-btn', 'n_clicks'),
    prevent_initial_call=True
)
def clear_all_filters(clear_clicks, current_apply_clicks):
    """Clear all filter inputs and trigger apply filters automatically"""
    print(f"Clear filters button clicked! n_clicks: {clear_clicks}")
    # Increment the apply button clicks to trigger the main callback
    return "", "", "", "", None, None,'','','','', (current_apply_clicks or 0) + 1

@callback(
    [Output('grid', 'rowData'),
     Output('price-info', 'children'),
     Output('map', 'figure'),
     Output('price-distribution', 'figure')],
    [Input('selection-dropdown', 'value'),
    Input('switch-toggle', 'checked'),
    Input('apply-filters-btn', 'n_clicks')],
    [State('hospital-regex', 'value'),
     State('description-regex', 'value'),
     State('state-regex', 'value'),
     State('payer-regex', 'value'),
     State('340b-status-dropdown', 'value'),
     State('setting-status-dropdown', 'value'),
    State('plan-regex', 'value'),
    State('plan-mapped-regex', 'value'),
    State('lob-mapped-regex', 'value'),
    State('drug-measurement-regex', 'value')
     ]
)
def update_data_prices_and_visualizations(
    selected_value, 
    is_hcpcs,
    n_clicks, 
    hospital_regex, 
    description_regex, 
    state_regex, 
    payer_regex, 
    status_340b, 
    setting_status, 
    plan_regex,
    plan_mapped_regex,
    lob_mapped_regex,
    drug_measurement_regex
):
    """Update grid data, price information, and visualizations in a single callback"""
    if not selected_value:
        return [], no_price_table(), {}, {}
    
    try:
        # Get filtered data once
        filtered_data_lazy = get_grid_data(is_hcpcs, selected_value)
        
        # Apply filters when they have meaningful values
        if hospital_regex and hospital_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.name.str.contains(f'(?i){hospital_regex}'))

        if description_regex and description_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.description.str.contains(f'(?i){description_regex}'))
        
        if state_regex and state_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.state.str.contains(f'(?i){state_regex}'))

        if payer_regex and payer_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.payer_name.str.contains(f'(?i){payer_regex}'))

        if status_340b in ['Eligible', 'Ineligible']:
            is_340b = True if status_340b == 'Eligible' else False
            filtered_data_lazy = filtered_data_lazy.filter(c.is_340b == is_340b)
        
        if setting_status is not None and setting_status != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.setting == setting_status)

        if plan_regex and plan_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.plan_name.str.contains(f'(?i){plan_regex}'))

        if plan_mapped_regex and plan_mapped_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.mapped_plan_name.str.contains(f'(?i){plan_mapped_regex}'))

        if lob_mapped_regex and lob_mapped_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.mapped_lob_name.str.contains(f'(?i){lob_mapped_regex}'))

        if drug_measurement_regex and drug_measurement_regex.strip() != '':
            filtered_data_lazy = filtered_data_lazy.filter(c.drug_type_of_measurement.str.contains(f'(?i){drug_measurement_regex}'))

        # Convert to dicts for grid
        filtered_data_dicts = filtered_data_lazy.collect(engine='streaming').to_dicts()
        
        # Generate transparency table
        transparency_table = render_transparency_table(is_hcpcs, selected_value)
        
        # Prepare data for plotting with the figure schema
        plot_data = filtered_data_lazy.select([
            c for c in filtered_data_lazy.collect_schema().names()
            if c in schema_for_fig_data().keys()
        ])
        
        # Create visualizations
        map_fig = create_map_plot(plot_data)
        dist_fig = create_price_distribution_plot(plot_data)
        
        return filtered_data_dicts, transparency_table, map_fig.to_dict(), dist_fig.to_dict()

    except Exception as e:
        print(f"Error updating data and visualizations: {e}")
        return [], no_price_table(), {}, {}



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
    [State('selection-dropdown', 'value'),
     State('switch-toggle', 'checked')],
    prevent_initial_call=True,
)
def toggle_map_modal(n_clicks, opened, selected_value, is_hcpcs):
    """Toggle map modal visibility"""
    if not selected_value:
        raise PreventUpdate

    if not n_clicks:
        return no_update, no_update
        
    try:
        # Use the same data filtering logic as update_data_and_prices
        filtered_data_lazy = get_grid_data(is_hcpcs, selected_value)
        
        # Convert to DataFrame for plotting with the figure schema
        data = filtered_data_lazy.select([
            c for c in filtered_data_lazy.columns 
            if c in schema_for_fig_data().keys()
        ])
        
        map_fig = create_map_plot(data)
        return not opened, map_fig.to_dict()
    except Exception as e:
        print(f"Error updating map modal: {e}")
        return not opened, {}

@callback(
    Output("distribution-modal", "opened"),
    Output("distribution-modal-graph", "figure"),
    Input("expand-distribution-btn", "n_clicks"),
    State("distribution-modal", "opened"),
    [State('selection-dropdown', 'value'),
     State('switch-toggle', 'checked')],
    prevent_initial_call=True,
)
def toggle_distribution_modal(n_clicks, opened, selected_value, is_hcpcs):
    """Toggle distribution modal visibility"""
    if not selected_value:
        raise PreventUpdate

    if not n_clicks:
        return no_update, no_update
        
    try:
        # Use the same data filtering logic as update_data_and_prices
        filtered_data_lazy = get_grid_data(is_hcpcs, selected_value)
        
        # Convert to DataFrame for plotting with the figure schema
        data = filtered_data_lazy.select([
            c for c in filtered_data_lazy.columns 
            if c in schema_for_fig_data().keys()
        ])
        
        dist_fig = create_price_distribution_plot(data)
        return not opened, dist_fig.to_dict()
    except Exception as e:
        print(f"Error updating distribution modal: {e}")
        return not opened, {}

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