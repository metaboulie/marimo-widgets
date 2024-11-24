import marimo

__generated_with = "0.9.20"
app = marimo.App(layout_file="layouts/showcase_v0.1.0.grid.json")


@app.cell(hide_code=True)
def create_header(NotebookHeader, datetime, mo):
    """Create showcase header."""

    header = mo.ui.anywidget(
        NotebookHeader(
            metadata={
                "Title": "MoWidget Showcase v0.1.0",
                "Description": "Interactive demonstration of MoWidget components",
                "Author": '<a href="https://github.com/metaboulie/marimo-widgets">Eugene</a>',
                "Last Updated": datetime.now().strftime("%B %d, %Y"),
                "Components": "ColorPicker, ColorMatrix, ArrayViewer, PomodoroTimer, NotebookHeader",
            },
            banner="https://raw.githubusercontent.com/Haleshot/marimo-tutorials/main/community-tutorials-banner.png",
            banner_height=150,
        )
    )
    header
    return (header,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""__Pomodoro Timer__: Start a focused work session with customizable durations.""")
    return


@app.cell
def __(mo):
    pomodoro_control = mo.ui.dictionary(
        {
            "work_duration": mo.ui.number(
                start=0.1, value=25.0, label="work duration"
            ),
            "short_break": mo.ui.number(start=0.1, value=5.0, label="short break"),
            "long_break": mo.ui.number(start=0.1, value=15.0, label="long break"),
            "sessions_before_long_break": mo.ui.number(
                start=1, step=1, value=4, label="sessions before long break"
            ),
            "num_cycles": mo.ui.number(
                start=1, step=1, value=3, label="number of cycles"
            ),
        }
    )
    return (pomodoro_control,)


@app.cell
def section_pomodoro(PomodoroTimer, mo, pomodoro_control):
    pomodoro = mo.ui.anywidget(PomodoroTimer(**pomodoro_control.value))
    mo.vstack([pomodoro, pomodoro_control.vstack()], gap=2)
    return (pomodoro,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 2. Design Tools

        ### ColorPicker

        Select a base color to generate palettes and visualizations:
        """
    )
    return


@app.cell
def section_color_tools(ColorPicker, mo):
    color_picker = mo.ui.anywidget(ColorPicker())
    color_picker
    return (color_picker,)


@app.cell
def palette_controls(mo):
    palette_size = mo.ui.slider(
        start=3,
        stop=20,
        step=1,
        value=8,
        label="Palette Size",
        show_value=True,
    )

    palette_size
    return (palette_size,)


@app.cell
def __(mo):
    mo.md(
        r"""
        ### ColorMatrix

        Visualize different color palettes based on the selected color:
        """
    )
    return


@app.cell
def create_color_matrix(ColorMatrix, color_picker, palette_size):
    generated_palettes = [
        color_picker.generate_palette(
            palette_type=palette_type, palette_size=palette_size.value
        )
        for palette_type in color_picker.available_palette_types
    ]

    palette_matrix = ColorMatrix(
        color_data=generated_palettes,
        row_labels=color_picker.available_palette_types,
        tooltips=[[f"{color}" for color in row] for row in generated_palettes],
        cell_width=40,
        cell_height=30,
        font_size=10,
    )

    palette_matrix
    return generated_palettes, palette_matrix


@app.cell
def __(mo):
    mo.md(
        r"""
        ## 3. Data Visualization

        ### ArrayViewer

        Visualize numerical arrays with outlier detection:
        """
    )
    return


@app.cell
def section_array_viewer(mo):
    array_controls = mo.ui.dictionary(
        {
            "rows": mo.ui.slider(start=5, stop=30, step=1, value=15, label="Rows"),
            "cols": mo.ui.slider(
                start=5, stop=30, step=1, value=20, label="Columns"
            ),
            "outliers": mo.ui.slider(
                start=0, stop=20, step=1, value=8, label="Number of Outliers"
            ),
            "outlier_strength": mo.ui.slider(
                start=2, stop=5, step=0.5, value=3, label="Outlier Strength"
            ),
        }
    )

    array_controls.vstack()
    return (array_controls,)


@app.cell
def generate_array_data(array_controls, np):
    np.random.seed(42)

    rows = array_controls["rows"].value
    cols = array_controls["cols"].value
    data = np.random.normal(loc=0, scale=1, size=(rows, cols))

    # Add outliers
    num_outliers = array_controls["outliers"].value
    strength = array_controls["outlier_strength"].value
    outlier_positions = np.random.choice(rows * cols, num_outliers, replace=False)
    outlier_values = np.random.choice([-strength, strength], num_outliers)

    # Add special values
    data[0, 0] = np.inf
    data[0, 1] = np.nan

    # Add outliers
    for pos, val in zip(outlier_positions, outlier_values):
        i, j = pos // cols, pos % cols
        data[i, j] = val * np.std(data)
    return (
        cols,
        data,
        i,
        j,
        num_outliers,
        outlier_positions,
        outlier_values,
        pos,
        rows,
        strength,
        val,
    )


@app.cell
def create_array_viewer(ArrayViewer, color_picker, data, margin_size, mo):
    array_viewer = mo.ui.anywidget(
        ArrayViewer(
            data=data,
            color_mode="single_color",
            base_color=color_picker.selected_color,
            outlier_detection="std",
            outlier_threshold=2.0,
            cell_size=25,
            margin_size=margin_size.value,
            font_size=10,
        )
    )

    array_viewer
    return (array_viewer,)


@app.cell
def __(mo):
    margin_size = mo.ui.slider(0, 10, 1, 2, label="Margin Size")
    return (margin_size,)


@app.cell
def __(mo):
    mo.md(r"""Selected Cells:""")
    return


@app.cell
def show_selected_cells(array_viewer):
    array_viewer.selected_cells
    return


@app.cell
def add_footer(mo):
    """Add footer with additional information."""

    mo.md("""
    ---
    ### Additional Information

    - All widgets are fully interactive and customizable
    - Color selections affect both the ColorMatrix and ArrayViewer
    - The PomodoroTimer can help maintain focus while exploring the visualizations
    - Try selecting cells in the ArrayViewer to see their values

    For more information, visit our [documentation](https://github.com/marimo-team/mowidget).
    """)
    return


@app.cell
def __():
    from datetime import datetime

    import marimo as mo
    import numpy as np
    return datetime, mo, np


@app.cell
def import_widgets():
    """Import all widgets from mowidget."""

    from mowidget.design.color_matrix import ColorMatrix
    from mowidget.design.color_picker import ColorPicker
    from mowidget.layout.header import NotebookHeader
    from mowidget.productivity.pomodoro_timer import PomodoroTimer
    from mowidget.viewer.array_viewer import ArrayViewer
    return (
        ArrayViewer,
        ColorMatrix,
        ColorPicker,
        NotebookHeader,
        PomodoroTimer,
    )


@app.cell
def __(
    array_controls,
    array_viewer,
    color_picker,
    margin_size,
    mo,
    palette_matrix,
    palette_size,
):
    mo.vstack(
        [
            mo.hstack([color_picker, palette_matrix], justify="space-around"),
            array_viewer,
            array_viewer.selected_cells,
            palette_size,
            array_controls.vstack(),
            margin_size,
        ],
        align="center",
    )
    return


@app.cell
def __(array_controls, mo, palette_size):
    mo.vstack([palette_size, array_controls.vstack()])
    return


if __name__ == "__main__":
    app.run()
