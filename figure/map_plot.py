import plotly.express as px
import polars as pl
from polars import col as c
import polars.selectors as cs
from tables.tables import HOSPITAL_TABLE

def create_map_plot(data: pl.LazyFrame):
    """
    Create a geographical visualization of hospital price distribution.

    Args:
        data: LazyFrame containing hospital data with required columns:
              hospital_unique_id, standard_charge_negotiated_dollar, lat, long, name, state

    Returns:
        plotly.graph_objects.Figure: The configured map visualization
    """
    # Aggregate the data and remove null values
    map_data = (
        data
        .group_by(['hospital_id'])
        .agg(c.standard_charge_negotiated_dollar.mean())
        .join(HOSPITAL_TABLE, left_on='hospital_id', right_on='id')
        .filter(c.standard_charge_negotiated_dollar.is_not_null())
        .with_columns([
            pl.min('standard_charge_negotiated_dollar').alias('price_min'),
            pl.max('standard_charge_negotiated_dollar').alias('price_max'),            ((pl.col('standard_charge_negotiated_dollar') - pl.min('standard_charge_negotiated_dollar')) / 
             (pl.max('standard_charge_negotiated_dollar') - pl.min('standard_charge_negotiated_dollar')) * 26 + 4)
            .alias('marker_size')
        ]
        )
        # set default marker size to 4.0 if null
        .with_columns(c.marker_size.fill_nan(4.0))  # Fill null sizes with a default value
        .collect(engine='streaming')
    )

    # calculate 5th and 95th percentile for color scale
    lower_bound = map_data.select(c.standard_charge_negotiated_dollar.quantile(0.05)).item()
    upper_bound = map_data.select(c.standard_charge_negotiated_dollar.quantile(0.95)).item()

    # Create map visualization
    fig = px.scatter_geo(
        data_frame=map_data,
        lat='lat',
        lon='long',
        size='marker_size',  # Use the scaled size column
        color='standard_charge_negotiated_dollar',
        scope='usa',
        custom_data=['name', 'state', 'standard_charge_negotiated_dollar', 'hospital_id'],
        title='Hospital Price Distribution Across USA',
        color_continuous_scale='Viridis',
        range_color=[lower_bound, upper_bound],  # Set color range based on percentiles
        height=500,
    )

    # Update hover template
    fig.update_traces(
        hovertemplate="<br>".join([
            "<b>%{customdata[0]}</b>",
            "State: %{customdata[1]}",
            "Average Price: $%{customdata[2]:,.2f}",
            "<extra></extra>"
        ]),

    )


    # Update layout
    fig.update_layout(
        title=dict(
            text='Hospital Price Distribution Across USA<br><span style="font-size:12px;">Circle size and color indicate average negotiated price</span>',
            x=0.5,
            font=dict(size=18, color='#2c3e50')
        ),
        paper_bgcolor='white',
        geo=dict(
            showland=True,
            showlakes=True,
            showcountries=True,
            showsubunits=True,
            landcolor='rgb(250, 250, 250)',
            subunitcolor='rgb(217, 217, 217)',
            countrycolor='rgb(217, 217, 217)',
            lakecolor='rgb(255, 255, 255)',
            bgcolor='white',
            projection_scale=1.1
        ),
        margin=dict(l=0, r=0, t=50, b=0),
        coloraxis_colorbar=dict(
            orientation='h',
            thickness=15,
            len=0.7,
            title=dict(
                text='Average Negotiated Price ($)',
                side='bottom',
                font=dict(size=12)
            ),
            y=-0.15,
            tickformat='$,.0f'
        )
    )
    
    return fig