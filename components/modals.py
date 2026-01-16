import dash_mantine_components as dmc
from dash import dcc, html
from dash_iconify import DashIconify

data_dict_schema = [
        {"column": "description", "dtype": "str", "desc": "Description of the drug or service"},
        {"column": "ndc", "dtype": "str", "desc": "National Drug Code"},
        {"column": "hcpcs", "dtype": "str", "desc": "HCPCS code (Healthcare Common Procedure Coding)"},
        {"column": "setting", "dtype": "str", "desc": "Care setting (e.g., inpatient, outpatient)"},
        {"column": "drug_unit_of_measurement", "dtype": "int", "desc": "Drug unit of measurement"},
        {"column": "drug_type_of_measurement", "dtype": "str", "desc": "Type of drug measurement"},
        {"column": "payer_name", "dtype": "str", "desc": "Name of the payer"},
        {"column": "plan_name", "dtype": "str", "desc": "Name of the insurance plan"},
        {"column": "standard_charge_gross", "dtype": "float", "desc": "Gross standard charge"},
        {"column": "standard_charge_discounted_cash", "dtype": "float", "desc": "Discounted cash standard charge"},
        {"column": "standard_charge_negotiated_dollar", "dtype": "float", "desc": "Negotiated dollar standard charge"},
        {"column": "standard_charge_methodology", "dtype": "str", "desc": "Methodology for standard charge"},
        {"column": "standard_charge_negotiated_percentage", "dtype": "float", "desc": "Negotiated percentage standard charge"},
        {"column": "calculated_negotiated_dollars", "dtype": "bool", "desc": "Whether negotiated dollars are calculated"},
        {"column": "hospital_unique_id", "dtype": "str", "desc": "Unique hospital identifier"},
        {"column": "mapped_plan_name", "dtype": "str", "desc": "Mapped plan name"},
        {"column": "mapped_lob_name", "dtype": "str", "desc": "Mapped line of business name"},
        {"column": "name", "dtype": "str", "desc": "Hospital name"},
        {"column": "state", "dtype": "str", "desc": "State where hospital is located"},
        {"column": "beds", "dtype": "int", "desc": "Number of hospital beds"},
        {"column": "lat", "dtype": "float", "desc": "Latitude of hospital"},
        {"column": "long", "dtype": "float", "desc": "Longitude of hospital"},
    ]


def create_mantine_dictionary():
    """
    Create a Mantine-styled data dictionary component.

    Returns:
        dmc.Card: A Dash Mantine component containing the data dictionary
    """
    
    data = data_dict_schema
    
    table = dmc.Box([
        html.Table([
            # Header
            html.Thead(
                html.Tr([
                    html.Th("Column Name", className="dict-header"),
                    html.Th("Data Type", className="dict-header"),
                    html.Th("Description", className="dict-header")
                ])
            ),
            # Body
            html.Tbody([
                html.Tr([
                    html.Td(row["column"], className="dict-cell"),
                    html.Td(row["dtype"], className="dict-cell"),
                    html.Td(row["desc"], className="dict-cell")
                ]) for row in data
            ])
        ], className="dict-table")
    ], className="dict-container")

    return dmc.Box(
        children=[
            dmc.Text("Data Dictionary", className='section-title'),
            table
        ],

    )


def render_schema_modal():
    schema_modal = dmc.Modal(
        id="schema-modal",
        centered=True,
        size="xl",
        children=create_mantine_dictionary(),
        shadow='lg',
    )
    return schema_modal


def render_hospital_modal():
    return dmc.Modal(
        id="hospital-info-modal",
        centered=True,
        size="lg",
        children=[],
        opened=False,
        shadow='lg',
    )

def render_map_modal():
    return dmc.Modal(
        id="map-modal",
        centered=True,
        size="75%", # type: ignore
        children=[
        dcc.Graph(id='map-modal-graph')
    ],
    opened=False,
    shadow='lg',
)

# create modal with distribution plot
def render_distribution_modal():
    return dmc.Modal(
        id="distribution-modal",
        centered=True,
        size="75%", # type: ignore
        children=[
        dcc.Graph(id='distribution-modal-graph')
    ],
    opened=False,
    shadow='lg',
)

def render_about_modal():
    return dmc.Modal(
        id="about-modal",
        centered=True,
        size="lg",
        children=[
        dmc.Stack([
            dmc.Text("About PRA Hospital Price Transparency", size="xl", fw="bold", c="blue"),
            dmc.Divider(),
            dmc.Text([
                "Patient Rights Advocate (PRA) is dedicated to transforming healthcare through ",
                dmc.Text("price transparency", fw="bold", c="blue", span=True),
                ". We believe that transparent, competitive, and fair pricing leads to lower costs and better care quality for all Americans."
            ], size="md"),
            dmc.Space(h="md"),
            dmc.Text("Our Mission:", fw="bold", size="lg", c="blue"),
            dmc.List([
                dmc.ListItem("Empower patients with clear, accurate healthcare pricing information"),
                dmc.ListItem("Advocate for compliance with federal price transparency requirements"),
                dmc.ListItem("Support patients who have been overcharged due to lack of transparency"),
                dmc.ListItem("Transform healthcare into a transparent, competitive marketplace"),
            ], spacing="xs"),
            dmc.Space(h="md"),
            dmc.Group([
                dmc.Anchor(
                    dmc.Button(
                        "Visit PatientRightsAdvocate.org",
                        leftSection=DashIconify(icon="mdi:open-in-new"),
                        variant="filled",
                        color="blue"
                    ),
                    href="https://www.patientrightsadvocate.org/",
                    target="_blank"
                ),
                dmc.Anchor(
                    dmc.Button(
                        "Hospital Price Finder",
                        leftSection=DashIconify(icon="mdi:hospital-building"),
                        variant="outline",
                        color="blue"
                    ),
                    href="https://hospitalpricingfiles.org/",
                    target="_blank"
                ),
            ], justify="center"),
        ], gap="sm"),
    ],
    opened=False,
    shadow='lg',
)



def render_help_modal():
    return dmc.Modal(
        id="help-modal",
        centered=True,
        size="lg",
        children=[
            dmc.Stack([
                dmc.Text("How to Use This Hospital Price Transparency Tool", size="xl", fw="bold", c="blue"),
            dmc.Divider(),
            dmc.Text("This tool helps you explore hospital pricing data to make informed healthcare decisions.", size="md"),
            dmc.Space(h="sm"),
            
            dmc.Accordion([
                dmc.AccordionItem([
                    dmc.AccordionControl("Getting Started", icon=DashIconify(icon="mdi:play-circle")),
                    dmc.AccordionPanel([
                        dmc.List([
                            dmc.ListItem("Use the toggle switch to select between HCPCS codes or NDC drug codes"),
                            dmc.ListItem("Select a specific product or procedure from the dropdown menu"),
                            dmc.ListItem("View pricing data in the table and explore hospital locations on the map"),
                            dmc.ListItem("Use the expand buttons to view charts in full screen"),
                        ])
                    ]),
                ], value="getting-started"),
                
                dmc.AccordionItem([
                    dmc.AccordionControl("Understanding the Data", icon=DashIconify(icon="mdi:information")),
                    dmc.AccordionPanel([
                        dmc.List([
                            dmc.ListItem("Prices shown are what hospitals have disclosed in their transparency files"),
                            dmc.ListItem("340B hospitals participate in a federal drug discount program"),
                            dmc.ListItem("Click on map points to see detailed hospital information"),
                            dmc.ListItem("Use the data grid to sort and filter results"),
                            dmc.ListItem(
                                dmc.Anchor(
                                    "Learn more about our methods",
                                    href="https://019ae5fd-ef56-5599-dee6-bda5fb19b709.share.connect.posit.cloud/",
                                    target="_blank",
                                    style={"color": "#1976d2", "textDecoration": "underline"}
                                )
                            ),
                        ])
                    ]),
                ], value="understanding-data"),
                
                dmc.AccordionItem([
                    dmc.AccordionControl("Additional Resources", icon=DashIconify(icon="mdi:link")),
                    dmc.AccordionPanel([
                        dmc.Group([
                            dmc.Anchor(
                                dmc.Button(
                                    "PRA Price Finder",
                                    leftSection=DashIconify(icon="mdi:magnify"),
                                    size="sm",
                                    variant="outline"
                                ),
                                href="https://hospitalpricingfiles.org/",
                                target="_blank"
                            ),
                            dmc.Anchor(
                                dmc.Button(
                                    "How to Shop for Healthcare",
                                    leftSection=DashIconify(icon="mdi:cart"),
                                    size="sm",
                                    variant="outline"
                                ),
                                href="https://www.patientrightsadvocate.org/howtoshop",
                                target="_blank"
                            ),
                        ], gap="sm")
                    ]),
                ], value="resources"),
            ], value="getting-started"),
        ], gap="sm"),
    ],
    opened=False,
    shadow='lg',
)