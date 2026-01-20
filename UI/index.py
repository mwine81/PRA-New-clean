import dash_mantine_components as dmc
from components.render import RenderComponents
from components.modals import (
    render_schema_modal,
    render_hospital_modal,
    render_map_modal,
    render_distribution_modal,
    render_about_modal,
    render_help_modal
)


def create_price_section():
    """Create the pricing information section with modern header"""
    return dmc.Card([
        dmc.Text(
            "Price Transparency Data",
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
        dmc.Box(id='price-info', className='price-info')
    ], className='pricing-container', shadow='sm')

layout = dmc.AppShell(
    [
        dmc.AppShellHeader(
            RenderComponents.get_components()["header"]
        ),
        dmc.AppShellNavbar(
            id="navbar",
            children=RenderComponents.get_components()["sidebar"],
            p="md",
        ),
        dmc.AppShellMain([
            dmc.Stack([
                RenderComponents.get_components()["charts"],
                RenderComponents.get_components()["grid"],
                create_price_section(),
            ], gap='md'),
            render_about_modal(),
            render_help_modal(),
            render_schema_modal(),
            render_hospital_modal(),
            render_map_modal(),
            render_distribution_modal(),
        ]),
        dmc.AppShellFooter(
            RenderComponents.get_components()["footer"]
        ),
    ],
     **{
    "header": {"height": 60},
    "footer": {"height": 120},
    "padding": "md",
    "navbar": {
        "width": 380,
        "breakpoint": "sm",
        "collapsed": {"mobile": True},
    },
    "id": "appshell",
})

