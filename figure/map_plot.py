import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from polars import col as c
import polars.selectors as cs
from tables.tables import HOSPITAL_TABLE

def create_empty_map():
    """Create an empty map when no data is available"""
    fig = px.scatter_geo(
        lat=[39.8], lon=[-98.5], 
        scope='usa',
        title='No Hospital Data Available',
        height=500
    )
    fig.update_traces(marker=dict(size=0))
    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor='rgb(248, 248, 248)',
            bgcolor='white'
        ),
        margin=dict(l=0, r=0, t=60, b=0)
    )
    return fig

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
        .collect(engine='streaming')
    )
    
    # Check if we have any data after filtering
    if map_data.height == 0:
        return create_empty_map()
    
    # Calculate min/max safely
    price_min = map_data.select(c.standard_charge_negotiated_dollar.min()).item()
    price_max = map_data.select(c.standard_charge_negotiated_dollar.max()).item()
    
    # Add marker size calculation with safe division
    if price_min is not None and price_max is not None and price_max != price_min:
        map_data = map_data.with_columns([
            ((c.standard_charge_negotiated_dollar - price_min) / 
             (price_max - price_min) * 26 + 4).alias('marker_size')
        ])
    else:
        # If all prices are the same or we have issues, use a default size
        map_data = map_data.with_columns([
            pl.lit(15.0).alias('marker_size')
        ])
    
    # Fill any remaining null sizes
    map_data = map_data.with_columns(c.marker_size.fill_nan(15.0))

    # calculate 5th and 95th percentile for color scale safely
    try:
        lower_bound = map_data.select(c.standard_charge_negotiated_dollar.quantile(0.05)).item()
        upper_bound = map_data.select(c.standard_charge_negotiated_dollar.quantile(0.95)).item()
        
        # If percentiles are None or the same, use min/max
        if lower_bound is None or upper_bound is None or lower_bound == upper_bound:
            lower_bound = price_min
            upper_bound = price_max
            
    except Exception:
        # Fallback to min/max if percentile calculation fails
        lower_bound = price_min
        upper_bound = price_max

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