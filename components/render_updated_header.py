import dash_mantine_components as dmc
from dash_iconify import DashIconify

def render_updated_header():
    """
    Simple header with logo on left and home link on right
    """
    return dmc.Box(
        dmc.Group([
            # Left - Logo and Burger
            dmc.Group([
                dmc.Burger(
                    id="burger", 
                    size="sm", 
                    hiddenFrom="sm", 
                    opened=False, 
                    className="updated-header-burger"
                ),
                dmc.Anchor(
                    dmc.Image(
                        src='/assets/pra_logo.png', 
                        h=45, 
                        className="updated-header-logo",
                        alt="Patient Rights Advocate Logo"
                    ),
                    href="https://www.patientrightsadvocate.org/",
                    target="_blank"
                ),
            ], gap="md"),
            
            # Right - Buttons and Home link
            dmc.Group([
                dmc.Button(
                    [DashIconify(icon="material-symbols:info-outline", width=16), "About"],
                    variant="subtle",
                    color="gray",
                    size="sm",
                    className="header-action-btn",
                    id='about-btn'
                ),
                dmc.Button(
                    [DashIconify(icon="material-symbols:help-outline", width=16), "Help"],
                    variant="subtle", 
                    color="gray",
                    size="sm",
                    className="header-action-btn",
                    id='help-btn'
                ),
                dmc.Anchor(
                    "HOME",
                    href="https://www.patientrightsadvocate.org/",
                    target="_blank",
                    className="updated-header-nav-link",
                    underline="never"
                ),
            ], gap="xs", visibleFrom="md"),
           
            
        ], justify="space-between", align="center", className="updated-header-nav-bar"),
        className="updated-header-container"
    )
