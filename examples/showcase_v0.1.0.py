# /// script
# requires-python = ">=3.9"
# dependencies = [
#     "marimo",
#     "numpy",
#     "mowidget",
# ]
# ///


import marimo

__generated_with = "0.9.23"
app = marimo.App()


@app.cell
def title(mo):
    mo.md(r"""# MoWidget v0.1.0 showcase""")
    return


@app.cell
def string_form_intro(mo):
    mo.md(
        r"""
        ## String Form

        A simple extensible form with string-only data

        - form data will only update with __Save Changes__
        """
    )
    return


@app.cell
def create_string_form(StringForm, mo):
    string_form = mo.ui.anywidget(StringForm(default_keys=["name", "email"]))
    string_form
    return (string_form,)


@app.cell
def access_form_data(mo):
    mo.md("""access form data with `form_data`""")
    return


@app.cell
def string_form_data(string_form):
    string_form.form_data
    return


@app.cell
def notebook_header_intro(mo):
    mo.md(
        r"""
        ## Notebook Header

        A simple header for your notebook

        - use your own banner and control its height
        """
    )
    return


@app.cell
def create_notebook_header(NotebookHeader, datetime):
    NotebookHeader(
        metadata={
            "Title": "MoWidget Showcase v0.1.0",
            "Description": "Interactive demonstration of MoWidget components",
            "Author": '<a href="https://github.com/metaboulie/marimo-widgets">Eugene</a>',
            "Last Updated": datetime.now().strftime("%B %d, %Y"),
            "Components": "ColorPicker, ColorMatrix, ArrayViewer, PomodoroTimer, NotebookHeader, StringForm",
        },
        banner="https://raw.githubusercontent.com/Haleshot/marimo-tutorials/main/community-tutorials-banner.png",
        banner_height=150,
    )
    return


@app.cell
def mixture_intro(mo):
    mo.md(r"""### A mixture of notebook header and string form""")
    return


@app.cell
def string_form_data(string_form):
    string_form
    return


@app.cell
def create_notebook_header_from_string_form(NotebookHeader, string_form):
    NotebookHeader(
        metadata=string_form.form_data,
        banner="https://raw.githubusercontent.com/Haleshot/marimo-tutorials/main/community-tutorials-banner.png",
        banner_height=150,
    )
    return


@app.cell
def pomodoro_timer_intro(mo):
    mo.md(
        r"""
        ## Pomodoro Timer

        Start a focused work session with customizable durations

        - access the controller with `pomodoro_control = PomodoroTimer.controller()`, then control the ui conveniently through this interactive and reactive controller
        """
    )
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


@app.cell
def color_picker_intro(mo):
    mo.md(
        r"""
        ## Color Picker & Color Matrix

        Select a base color to generate palettes and visualizations
        """
    )
    return


@app.cell
def section_color_tools(ColorPicker, mo):
    color_picker = mo.ui.anywidget(ColorPicker())
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
def array_viewer_w_color_picker(array_viewer_w_color_picker):
    array_viewer_w_color_picker
    return


@app.cell
def create_array_viewer_w_color_picker(
    ArrayViewer,
    color_picker,
    data,
    mo,
):
    array_viewer_w_color_picker = mo.ui.anywidget(
        ArrayViewer(
            data=data,
            outlier_detection=None,
            color_mode="single_color",
            base_color=color_picker.selected_color,
            cell_size=int(1 / data.size * 10000),
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


if __name__ == "__main__":
    app.run()
