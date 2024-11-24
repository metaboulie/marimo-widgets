import marimo

__generated_with = "0.9.20"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __():
    import numpy as np
    return (np,)


@app.cell
def __():
    from mowidget.design.color_matrix import ColorMatrix
    return (ColorMatrix,)


@app.cell(hide_code=True)
def __(mo):
    num_rows = mo.ui.slider(
        start=1,
        stop=40,
        step=1,
        value=20,
        label="number of rows in the color matrix",
        show_value=True,
    )
    num_cols = mo.ui.slider(
        start=1,
        stop=40,
        step=1,
        value=20,
        label="number of columns in the color matrix",
        show_value=True,
    )
    return num_cols, num_rows


@app.cell
def __(ColorMatrix):
    color_matrix_controller = ColorMatrix.controller()
    return (color_matrix_controller,)


@app.cell
def __(num_rows):
    row_labels = [f"row {i+1}" for i in range(num_rows.value)]
    return (row_labels,)


@app.cell
def __(color_matrix):
    tooltips = color_matrix
    return (tooltips,)


@app.cell
def __(
    ColorMatrix,
    color_matrix_controller,
    mo,
    np,
    num_cols,
    num_rows,
    random_color_format,
):
    color_matrix = np.array(
        [
            [random_color_format() for _ in range(num_cols.value)]
            for _ in range(num_rows.value)
        ]
    )

    widget = mo.ui.anywidget(
        ColorMatrix(
            color_data=color_matrix,
            **color_matrix_controller.value,
        )
    )
    return color_matrix, widget


@app.cell
def __(widget):
    widget
    return


@app.cell
def __(color_matrix_controller, mo, num_cols, num_rows):
    mo.vstack([num_rows, num_cols, color_matrix_controller.vstack()])
    return


@app.cell
def __(widget):
    widget.selected_cells
    return


@app.cell
def __(random):
    def random_color_format():
        formats = [
            lambda: f"#{random.randint(0, 0xFFFFFF):06x}",  # Hex
            lambda: f"rgb({random.randint(0, 255)}, {random.randint(0, 255)}, {random.randint(0, 255)})",  # RGB array
            lambda: random.choice(
                [
                    "red",
                    "green",
                    "blue",
                    "yellow",
                    "magenta",
                    "cyan",
                    "white",
                    "black",
                ]
            ),  # Named colors
        ]
        return random.choice(formats)()
    return (random_color_format,)


@app.cell
def __():
    import random
    return (random,)


if __name__ == "__main__":
    app.run()
