import polars as pl

def schema_for_fig_data():
    """
    Define the schema for the DataFrame used in the visualization.
    
    Returns:
        dict: A dictionary defining the schema for the DataFrame.
    """
    return {
        'hospital_id': pl.String,
        'description': pl.String,   
        'ndc': pl.String,
        'hcpcs': pl.String,
        'setting': pl.String,
        'drug_unit_of_measurement': pl.Int64,
        'drug_type_of_measurement': pl.String,
        'payer_name': pl.String,
        'plan_name': pl.String,
        'standard_charge_gross': pl.Float64,
        'standard_charge_discounted_cash': pl.Float64,
        'standard_charge_negotiated_dollar': pl.Float64,
        'standard_charge_methodology': pl.String,
        'standard_charge_negotiated_percentage': pl.Float64,
        'calculated_negotiated_dollars': pl.Boolean,
        'hospital_unique_id': pl.String,
        'mapped_plan_name': pl.String,
        'mapped_lob_name': pl.String,
        'name': pl.String,
        'state': pl.String,
        'beds': pl.Int32,
        'lat': pl.Float64,
        'long': pl.Float64
    }