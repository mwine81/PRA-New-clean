import plotly.express as px
import plotly.graph_objects as go
import polars as pl
from polars import col as c
import polars.selectors as cs

def create_empty_distribution_plot():
    """Create an empty distribution plot when no data is available"""
    fig = go.Figure()
    fig.add_annotation(
        text="No Price Distribution Data Available",
        xref="paper", yref="paper",
        x=0.5, y=0.5,
        showarrow=False,
        font=dict(size=16, color="gray")
    )
    fig.update_layout(
        title="No Price Distribution Data Available",
        height=400,
        xaxis=dict(showgrid=False, showticklabels=False),
        yaxis=dict(showgrid=False, showticklabels=False)
    )
    return fig


def create_price_distribution_plot(df: pl.LazyFrame):
    """
    Create a box plot showing price distribution by drug measurement type.
    
    Args:
        df: Polars DataFrame with columns 'drug_type_of_measurement' and 'price_per_unit'
    
    Returns:
        plotly.graph_objects.Figure
    """
    # Check if required columns exist
    try:
        schema = df.collect_schema()
        required_columns = ['drug_unit_of_measurement', 'drug_type_of_measurement', 'standard_charge_negotiated_dollar', 'name']
        missing_columns = [col for col in required_columns if col not in schema]
        
        if missing_columns:
            print(f"Missing columns for price distribution: {missing_columns}")
            return create_empty_distribution_plot()
            
    except Exception as e:
        print(f"Error checking schema: {e}")
        return create_empty_distribution_plot()
    
    # function to to create x label with hospital count
    def unique_hospital_count() -> pl.Expr:
        return c.name.n_unique().over('drug_type_of_measurement').alias('hospital_count')

    def drug_type_of_measurement_with_hospital_ct() -> pl.Expr:
        return pl.format('{}\n({})', c.drug_type_of_measurement, unique_hospital_count()).alias('drug_type_of_measurement')

    try:
        df = (
            df
            #if drug_unit_of_measurement is null or 0 set to 1.0
            .with_columns(c.drug_unit_of_measurement.fill_null(1.0))
            .with_columns(
                pl.when(c.drug_unit_of_measurement == 0)
                .then(1.0)
                .otherwise(c.drug_unit_of_measurement)
                .alias('drug_unit_of_measurement')
            )
            # calculate price per unit
            .group_by(c.name, c.drug_type_of_measurement)
            .agg([
                c.standard_charge_negotiated_dollar.mean().alias('avg_price'),
                c.drug_unit_of_measurement.mean().alias('avg_units')
            ])
            .with_columns([
                # Safe division - avoid division by zero
                pl.when(c.avg_units > 0)
                .then((c.avg_price / c.avg_units).round(2))
                .otherwise(c.avg_price.round(2))
                .alias('price_per_unit')
            ])
            .with_columns(drug_type_of_measurement_with_hospital_ct())
            .with_columns(c.drug_type_of_measurement.str.to_uppercase().alias('drug_type_of_measurement'))
        )

        # Collect the data and check if we have any
        collected_df = df.collect(engine="streaming")
        
        if collected_df.height == 0:
            return create_empty_distribution_plot()
            
    except Exception as e:
        print(f"Error processing price distribution data: {e}")
        return create_empty_distribution_plot()

    fig = px.box(
        collected_df,
        x='drug_type_of_measurement',
        y='price_per_unit',
        color='drug_type_of_measurement',
        points='all',
        title='Price Distribution by Drug Measurement Type',
        color_discrete_sequence=px.colors.qualitative.Dark2
    )

    # Configure y-axis
    fig.update_yaxes(
        type='log',
        title_text='Price per Unit (USD)',
        tickprefix="$",
        tickformat=",.2f",
        gridcolor='#E2E2E2',
        title_font=dict(size=16),
        tickfont=dict(size=14)
    )

    # Configure x-axis
    fig.update_xaxes(
        title_text='Drug Type of Measurement',
        gridcolor='#E2E2E2',
        title_font=dict(size=16),
        tickfont=dict(size=14),
        tickangle=0
    )

    # Update box and point styling
    fig.update_traces(
        marker=dict(
            size=6,
            opacity=0.7,
            line=dict(width=1, color='DarkSlateGrey')
        ),
        line=dict(width=1.5),
        boxmean=True,  # Show mean as a dashed line
        jitter=0.3,    # Spread out the points
        whiskerwidth=0.7,
        boxpoints=False  # Show only outlier points
    )    # Update layout
    fig.update_layout(
        template='plotly_white',
        font_family="Segoe UI, Arial, sans-serif",
        title=dict(
            text='Price Distribution by Drug Measurement Type<br><span style="font-size:14px;color:#666">Negotiated Prices per Unit</span>',
            x=0.5,  # Center the title
            xanchor='center',
            y=0.95,
            font=dict(size=20)
        ),
        showlegend=False,
        autosize=True,
        height=500,
        # Increased bottom margin
                    plot_bgcolor='white',
                    annotations=[
                            dict(
                                    text=      "1. The y-axis uses a logarithmic scale. Each box represents the interquartile range (25th–75th percentile); whiskers extend to 1.5× IQR.<br>"
                                                "2. The number in parentheses after each unit on the x-axis indicates the count of hospitals reporting prices in that unit.",
                                    showarrow=False,
                                    xref="paper",
                                    yref="paper",
                                    x=0,
                                    y=-0.26,  # Moved note further down
                font=dict(size=10, color="#666"),
                align="left"
            )
        ]
    )

    # Add thousands separators to hover text
    fig.update_traces(
        hovertemplate="<br>".join([
            "Drug Type: %{x}",
            "Price: $%{y:,.2f}",
            "Mean: $%{mean:,.2f}",
            "<extra></extra>"
        ])
    )
    
    return fig