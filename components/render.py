from components.render_sidebar import render_sidebar
from components.render_charts import render_charts
from components.render_grid import render_grid
from components.render_footer import render_footer
from components.render_updated_footer import render_updated_footer
from components.render_header import render_header
from components.render_updated_header import render_updated_header
from components.sidebar_filters import create_filter_section

class RenderComponents:
    @staticmethod
    def get_components():
        return {
            "header": render_updated_header(),  # Swap with render_header() for original design
            "footer": render_updated_footer(),  # Swap with render_updated_footer() for new design
            "sidebar": render_sidebar(),
            "charts": render_charts(),
            "grid": render_grid(),
            "filters": create_filter_section(),
        }
