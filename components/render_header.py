import dash_mantine_components as dmc
from dash_iconify import DashIconify

def render_header():
    return dmc.Box([
        dmc.Group([
            # Left side - Burger and Logo
            dmc.Group([
                dmc.Burger(id="burger", size="sm", hiddenFrom="sm", opened=False, className="header-burger"),
                    dmc.Anchor(
                        dmc.Image(src='./assets/pra_logo.png', h=45, className="header-logo"),
                        href="https://www.patientrightsadvocate.org/",
                        target="_blank"
                    ),
                ], gap="md"),
                
                # Center - Title and Subtitle
                dmc.Box([
                    dmc.Title("PRA Hospital Price Transparency", size="h2", className='header-main-title'),
                    dmc.Text("Empowering Patients Through Price Data", className='header-subtitle'),
                ], className="header-title-section"),
                
                # Right side - Action buttons
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
                ], gap="xs", visibleFrom="md"),
                
            ], justify="space-between", align="center", h="100%", px="lg"),        ], className="header-container")