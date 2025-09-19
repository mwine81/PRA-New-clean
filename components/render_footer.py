from dash import html, get_asset_url
from dash_iconify import DashIconify
import dash_mantine_components as dmc


def render_footer():
    """Create the footer component"""
    return html.Footer(
        dmc.Box([
            dmc.Box([
                dmc.Text(
                    "Empowering Patients Through Price Transparency",
                    className='footer-text',
                    style={'fontStyle': 'italic', 'color': '#0074D9'}
                ),
                dmc.Anchor(
                    dmc.Image(src='./assets/pra_logo.png', className='footer-logo'),
                    href="https://www.patientrightsadvocate.org/",
                    target="_blank"
                ),
            ], className='footer-left'),

            dmc.Box([
                dmc.Box([
                    dmc.Text("© 2025 Patient Rights Advocate", className='copyright-text'),
                    dmc.Anchor(
                        dmc.Text("Developed by 3AxisAdvisors", className='rights-text'),
                        href="https://www.3axisadvisors.com/",
                        target="_blank"
                    )
                ], className='footer-text-stack'),

                dmc.Box([
                    dmc.Anchor(
                        DashIconify(icon='logos:linkedin-icon'),
                        href="https://www.linkedin.com/company/patient-rights-advocate/", className='social-icon', target="_blank"
                    ),
                    dmc.Anchor(
                        DashIconify(icon='logos:facebook'),
                        href="https://www.facebook.com/thepatientrightsadvocate", className='social-icon', target="_blank"
                    ),
                    dmc.Anchor(
                        DashIconify(icon='logos:x'),
                        href="https://x.com/PtRightsAdvoc", className='social-icon', target="_blank"
                    ),
                ], className='social-icons'),
            ], className='footer-right', visibleFrom='md'),
        ], className='footer-container')
    )