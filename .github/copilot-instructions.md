# Copilot Instructions for AI Agents

## Project Overview
- This is a Dash-based data exploration and visualization app using Dash Mantine Components and Dash AG Grid.
- The main entry point is `app.py`, which wires up callbacks, layout, and data logic.
- UI layout is composed in `UI/index.py` using Mantine's AppShell, with custom components in `components/` and AG Grid integration in `ag_grid/`.
- Data is loaded from Parquet files in the `data/` directory, using Polars and Patito models defined in `models.py` and loaded in `tables.py`.

## Key Patterns & Conventions
- All UI elements are composed as Mantine components, often wrapped in helper functions (see `components/`).
- AG Grid is configured in `ag_grid/ag_grid_def.py` and instantiated in `ag_grid/ag_grid_component.py`.
- Data for dropdowns and grids is fetched via helper functions in `helpers.py`, which use Polars LazyFrames for efficient data handling.
- Callbacks are defined in `app.py` using the `@callback` decorator from Dash. Outputs must match the expected type (e.g., AG Grid expects a list of dicts for `rowData`).
- When returning Plotly figures in callbacks, always return `fig.to_dict()` or `fig.to_plotly_json()` (not the Figure object itself).
- The toggle switch and dropdown are linked: toggling updates both the dropdown options and the label next to the switch.
- Data joins (e.g., for grid data) are performed with Polars, joining price and hospital tables, and selecting columns as defined in `models.AGTable`.

## Developer Workflows
- Run the app with `uv run app.py` or `python app.py` from the project root.
- All dependencies are listed in `requirements.txt`.
- Data files must be present in the `data/` directory for the app to function.
- Debug output is printed to the console; errors in callbacks are caught and printed.

## Integration Points
- Uses Dash Mantine Components (`dash-mantine-components`) for UI.
- Uses Dash AG Grid (`dash-ag-grid`) for tabular data display.
- Uses Polars and Patito for data modeling and manipulation.
- Data is loaded from local Parquet files, not from a database or API.

## Examples
- To add a new dropdown, create a helper in `components/`, add it to the layout in `UI/index.py`, and wire up a callback in `app.py`.
- To add a new data column, update the relevant Patito model in `models.py`, update the grid definition, and ensure the data join in `helpers.py` includes the new column.

## File/Directory Reference
- `app.py`: Main app, callbacks, and entry point
- `UI/index.py`: Layout composition
- `components/`: Custom UI components
- `ag_grid/`: AG Grid config and components
- `helpers.py`: Data access and transformation
- `models.py`: Data models (Patito)
- `tables.py`: Loads data tables
- `data/`: Parquet data files

---

If you are unsure about a callback's output type, check the component's documentation or existing callback patterns in `app.py`.
