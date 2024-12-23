# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "numpy==2.1.3",
#     "mowidget==0.1.3",
#     "plotly==5.24.1",
# ]
# ///

import marimo

__generated_with = "0.9.34"
app = marimo.App()


@app.cell(hide_code=True)
def __(NotebookHeader, datetime):
    NotebookHeader(
        metadata={
            "Title": "MoWidget Showcase v0.1",
            "Description": "Interactive demonstration of widgets in marimo",
            "Author": '<a href="https://github.com/metaboulie/marimo-widgets">Eugene</a>',
            "Last Updated": datetime.now().strftime("%B %d, %Y"),
            "Components": "ColorPicker, ColorMatrix, ArrayViewer, PomodoroTimer, NotebookHeader, StringForm",
        },
        banner="https://raw.githubusercontent.com/Haleshot/marimo-tutorials/main/community-tutorials-banner.png",
        banner_height=150,
    )
    return


@app.cell(hide_code=True)
def string_form_intro(mo):
    mo.md(r"""Use the minimalistic string form for convenient configuration""")
    return


@app.cell
def create_string_form(StringForm, mo):
    string_form = mo.ui.anywidget(StringForm(default_keys=["title", "name"]))
    string_form.center()
    return (string_form,)


@app.cell
def __(NotebookHeader, header_height, string_form):
    NotebookHeader(
        metadata=string_form.form_data,
        banner="https://raw.githubusercontent.com/Haleshot/marimo-tutorials/main/community-tutorials-banner.png",
        banner_height=header_height.value,
    )
    return


@app.cell
def __(header_height):
    header_height
    return


@app.cell
def __(mo):
    header_height = mo.ui.slider(
        100, 300, 1, 150, show_value=True, label="height of the header"
    )
    return (header_height,)


@app.cell(hide_code=True)
def access_form_data(mo):
    mo.md("""access form data """)
    return


@app.cell
def string_form_data(string_form):
    string_form.form_data
    return


@app.cell(hide_code=True)
def pomodoro_timer_intro(mo):
    mo.md(r"""Use pomodoro timer to control your time in marimo""")
    return


@app.cell
def section_pomodoro(PomodoroTimer, mo, pomodoro_control):
    pomodoro = mo.ui.anywidget(PomodoroTimer(**pomodoro_control.value))
    mo.vstack([pomodoro, pomodoro_control.vstack()], gap=2)
    return (pomodoro,)


@app.cell
def pomodoro_timer_controls(PomodoroTimer):
    pomodoro_control = PomodoroTimer.controller()
    return (pomodoro_control,)


@app.cell(hide_code=True)
def color_picker_intro(mo):
    mo.md(
        r"""
        Freely choose color for plots

        Use color picker to select the base color, use the generated palette to choose other colors
        """
    )
    return


@app.cell
def section_color_tools(ColorPicker, mo):
    color_picker = mo.ui.anywidget(ColorPicker())
    return (color_picker,)


@app.cell
def __(color_picker):
    color_picker
    return


@app.cell
def __(palette_matrix):
    palette_matrix
    return


@app.cell
def __(mo):
    configure_palette_matrix = mo.ui.switch(label="configure palette")
    return (configure_palette_matrix,)


@app.cell
def __(
    color_matrix_controller,
    configure_palette_matrix,
    mo,
    palette_size,
):
    (
        mo.vstack(
            [
                configure_palette_matrix,
                palette_size,
                color_matrix_controller.vstack(),
            ]
        )
        if configure_palette_matrix.value
        else configure_palette_matrix
    )
    return


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
    return (palette_size,)


@app.cell
def create_color_matrix(
    ColorMatrix,
    color_matrix_controller,
    color_picker,
    mo,
    palette_size,
):
    generated_palettes = [
        color_picker.generate_palette(
            palette_type=palette_type, palette_size=palette_size.value
        )
        for palette_type in color_picker.available_palette_types
    ]

    palette_matrix = mo.ui.anywidget(
        ColorMatrix(
            color_data=generated_palettes,
            row_labels=color_picker.available_palette_types,
            tooltips=[[f"{color}" for color in row] for row in generated_palettes],
            **color_matrix_controller.value,
        )
    )
    return generated_palettes, palette_matrix


@app.cell
def get_color_matrix_controller(mo):
    mo.md(r"""get the controller of Color Matrix""")
    return


@app.cell
def color_matrix_controller(ColorMatrix):
    color_matrix_controller = ColorMatrix.controller()
    return (color_matrix_controller,)


@app.cell
def color_matrix_controls(
    color_matrix_controller,
    color_picker,
    mo,
    palette_matrix,
    palette_size,
):
    mo.vstack(
        [
            color_picker,
            palette_matrix,
            palette_size,
            color_matrix_controller.vstack(),
        ],
        gap=2,
    )
    return


@app.cell
def select_cells_in_color_matrix(mo):
    mo.md(r"""you can select cells in the Color Matrix ( try to click a cell in the color matrix )""")
    return


@app.cell
def selected_cells(palette_matrix):
    palette_matrix.selected_cells
    return


@app.cell
def array_viewer_intro(mo):
    mo.md(
        r"""
        ## ArrayViewer

        Visualize numerical arrays with outlier detection

        - you can change row labels with `row_labels`
        """
    )
    return


@app.cell
def section_array_viewer(mo):
    array_controls = mo.ui.dictionary(
        {
            "rows": mo.ui.slider(
                start=5,
                stop=30,
                step=1,
                value=15,
                label="Rows",
                show_value=True,
            ),
            "cols": mo.ui.slider(
                start=5,
                stop=30,
                step=1,
                value=20,
                label="Columns",
                show_value=True,
            ),
            "outliers": mo.ui.slider(
                start=0,
                stop=20,
                step=1,
                value=8,
                label="Number of Outliers",
                show_value=True,
            ),
            "outlier_strength": mo.ui.slider(
                start=2,
                stop=5,
                step=0.5,
                value=3,
                label="Outlier Strength",
                show_value=True,
            ),
        }
    )
    return (array_controls,)


@app.cell
def array_viewer_controller(ArrayViewer):
    array_viewer_controller = ArrayViewer.controller()
    return (array_viewer_controller,)


@app.cell
def generate_array_data(array_controls, np):
    np.random.seed(42)

    rows = array_controls["rows"].value
    cols = array_controls["cols"].value
    array = np.random.normal(loc=0, scale=1, size=(rows, cols))

    # Add outliers
    num_outliers = array_controls["outliers"].value
    strength = array_controls["outlier_strength"].value
    outlier_positions = np.random.choice(rows * cols, num_outliers, replace=False)
    outlier_values = np.random.choice([-strength, strength], num_outliers)

    # Add special values
    array[0, 0] = np.inf
    array[0, 1] = np.nan

    # Add outliers
    for pos, val in zip(outlier_positions, outlier_values):
        i, j = pos // cols, pos % cols
        array[i, j] = val * np.std(array)
    return (
        array,
        cols,
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
def create_array_viewer(ArrayViewer, array_viewer_controller, data, mo):
    array_viewer = mo.ui.anywidget(
        ArrayViewer(
            data=data, outlier_detection="std", **array_viewer_controller.value
        )
    )
    return (array_viewer,)


@app.cell
def array_viewer_controls(
    array_controls,
    array_viewer,
    array_viewer_controller,
    mo,
):
    mo.vstack(
        [
            array_viewer,
            mo.hstack(
                [array_viewer_controller.vstack(), array_controls.vstack()],
                justify="space-around",
            ),
        ],
        gap=2,
    )
    return


@app.cell
def select_cells_in_array_viewer(mo):
    mo.md(r"""You can select cells in the Array Viewer""")
    return


@app.cell
def show_selected_cells(array_viewer):
    array_viewer.selected_cells
    return


@app.cell
def custom_outlier_detection_intro(mo):
    mo.md(r"""### Use custom outlier detection""")
    return


@app.cell
def custom_outlier_detection(np):
    def custom_outlier_detection(
        data: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Custom outlier detection using percentiles."""
        finite_data = data[np.isfinite(data)]
        high_threshold = np.percentile(finite_data, 90)
        low_threshold = np.percentile(finite_data, 10)

        outliers_high = (data > high_threshold) & np.isfinite(data)
        outliers_low = (data < low_threshold) & np.isfinite(data)

        return outliers_high, outliers_low
    return (custom_outlier_detection,)


@app.cell
def use_color_picker_to_select_base_color(mo):
    mo.md(r"""### Use color picker to select base color""")
    return


@app.cell
def color_picker(color_picker):
    color_picker
    return


@app.cell
def array_viewer_w_color_picker(
    array_viewer_w_color_picker,
    color_picker,
    mo,
):
    mo.hstack(
        [color_picker, array_viewer_w_color_picker],
        align="center",
        justify="space-around",
    )
    return


@app.cell
def create_array_viewer_w_color_picker(
    ArrayViewer,
    array,
    color_picker,
    data,
    mo,
):
    array_viewer_w_color_picker = mo.ui.anywidget(
        ArrayViewer(
            data=array,
            outlier_detection=None,
            color_mode="single_color",
            base_color=color_picker.selected_color,
            cell_size=int(1 / data.size * 8000),
            font_size=8,
            margin_size=0,
        )
    )
    return (array_viewer_w_color_picker,)


@app.cell
def __():
    from datetime import datetime

    import marimo as mo
    import numpy as np
    return datetime, mo, np


@app.cell
def import_widgets():
    from mowidget.base.string_form import StringForm
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
        StringForm,
    )


@app.cell
def __(mo):
    import plotly.io as pio

    pio.templates.default = (
        "plotly_dark" if mo.app_meta().theme == "dark" else "simple_white"
    )
    return (pio,)


@app.cell
def __():
    import pandas as pd
    return (pd,)


@app.cell
def __(mo, pd):
    data = pd.read_csv(mo.notebook_dir() / "parkinsons.csv")[
        ["RPDE", "HNR", "NHR", "status"]
    ]
    return (data,)


@app.cell
def __(color_picker, palette_matrix):
    another_color = (
        palette_matrix.selected_cells[0][-1][:-2]
        if palette_matrix.selected_cells
        else color_picker.selected_color
    )
    return (another_color,)


@app.cell
def __(another_color, color_picker, pd, px):
    def create_pairplot(data: pd.DataFrame, target="status"):
        data_copy = data.copy()
        data_copy[target] = data_copy[target].astype(str)
        return px.scatter_matrix(
            data_copy,
            dimensions=list(data_copy.columns[:-1]),
            color=target,
            symbol=target,
            symbol_sequence=["cross", "square"],
            opacity=0.5,
            color_discrete_sequence=[
                color_picker.selected_color,
                another_color,
            ],
        ).update_traces(
            marker_size=7,
        )
    return (create_pairplot,)


if __name__ == "__main__":
    app.run()
