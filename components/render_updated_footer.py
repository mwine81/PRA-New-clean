from dash import html
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def render_updated_footer():
    """Create updated footer component inspired by Ohio Hospital Price Finder"""
    return html.Footer(
        dmc.Box([
            # Top row: Logo, Links, Social Icons
            dmc.Group([
                # Left - Logo
                dmc.Anchor(
                    dmc.Image(
                        src='/assets/pra_logo.png',
                        h=40,
                        className="updated-footer-logo",
                        alt="Patient Rights Advocate Logo"
                    ),
                    href="https://www.patientrightsadvocate.org/",
                    target="_blank"
                ),
                
                # Center - Links
                dmc.Group([
                    dmc.Anchor(
                        "OUR MISSION",
                        href="https://www.patientrightsadvocate.org/our-mission",
                        target="_blank",
                        className="updated-footer-link",
                        underline="never"
                    ),
                    dmc.Anchor(
                        "TERMS OF SERVICE",
                        href="https://www.patientrightsadvocate.org/termsofservice",
                        target="_blank",
                        className="updated-footer-link",
                        underline="never"
                    ),
                    dmc.Anchor(
                        "CONTACT US",
                        href="https://www.patientrightsadvocate.org/contact",
                        target="_blank",
                        className="updated-footer-link",
                        underline="never"
                    ),
                ], gap="lg"),
                
                # Right - Social media icons
                dmc.Group([
                    dmc.Anchor(
                        DashIconify(icon="ri:twitter-x-fill", width=24),
                        href="https://x.com/PtRightsAdvoc",
                        target="_blank",
                        className="updated-footer-social-icon"
                    ),
                    dmc.Anchor(
                        DashIconify(icon="ri:facebook-fill", width=24),
                        href="https://www.facebook.com/thepatientrightsadvocate",
                        target="_blank",
                        className="updated-footer-social-icon"
                    ),
                    dmc.Anchor(
                        DashIconify(icon="ri:instagram-fill", width=24),
                        href="https://www.instagram.com/patientrightsadvocate/",
                        target="_blank",
                        className="updated-footer-social-icon"
                    ),
                    dmc.Anchor(
                        DashIconify(icon="ri:youtube-fill", width=24),
                        href="https://www.youtube.com/channel/UCN7j6idxar-akDLDzVWD46Q",
                        target="_blank",
                        className="updated-footer-social-icon"
                    ),
                ], gap="md"),
                
            ], justify="space-between", align="center", className="updated-footer-top-row"),
            
            # Bottom row: Copyright and developer info
            dmc.Group([
                dmc.Text(
                    "© 2026 Patient Rights Advocate",
                    size="sm",
                    className="updated-footer-copyright-text"
                ),
                dmc.Anchor(
                    "Developed by 3AxisAdvisors",
                    href="https://www.3axisadvisors.com/",
                    target="_blank",
                    size="sm",
                    className="updated-footer-dev-link",
                    underline="hover"
                ),
            ], justify="center", gap="md", className="updated-footer-bottom-row"),
            
        ], className="updated-footer-container")
    )
