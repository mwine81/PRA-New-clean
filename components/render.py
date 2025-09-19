from components.render_sidebar import render_sidebar
from components.render_charts import render_charts
from components.render_grid import render_grid
from components.render_footer import render_footer
from components.render_header import render_header

class RenderComponents:
    @staticmethod
    def get_components():
        return {
            "header": render_header(),
            "footer": render_footer(),
            "sidebar": render_sidebar(),
            "charts": render_charts(),
            "grid": render_grid(),
        }
