import plotly.express as px
import polars as pl
from polars import col as c
import polars.selectors as cs


def create_price_distribution_plot(df: pl.LazyFrame):
    """
    Create a box plot showing price distribution by drug measurement type.
    
    Args:
        df: Polars DataFrame with columns 'drug_type_of_measurement' and 'price_per_unit'
    
    Returns:
        plotly.graph_objects.Figure
    """
    # function to to create x label with hospital count
    def unique_hospital_count() -> pl.Expr:
        return c.name.n_unique().over('drug_type_of_measurement').alias('hospital_count')

    def drug_type_of_measurement_with_hospital_ct() -> pl.Expr:
        return pl.format('{}\n({})', c.drug_type_of_measurement, unique_hospital_count()).alias('drug_type_of_measurement')

    df = (
        df
        #if drug_unit_of_measurement is null or 0 set to 1.0
        .with_columns(c.drug_unit_of_measurement.fill_null(1.0))
        # calculate price per unit
        .group_by(c.name, c.drug_type_of_measurement)
        .agg(
            ((c.standard_charge_negotiated_dollar.mean() / c.drug_unit_of_measurement.mean())).round(2).alias('price_per_unit')
        )
        .with_columns(drug_type_of_measurement_with_hospital_ct())
    )


    fig = px.box(
        df.collect(engine="streaming"),
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