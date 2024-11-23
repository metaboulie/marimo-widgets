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
    from mowidget.design.color_matrix import ColorMatrixWidget
    return (ColorMatrixWidget,)


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
    cell_width = mo.ui.slider(
        start=10,
        stop=50,
        step=5,
        value=20,
        label="width of each cell in the color matrix",
        show_value=True,
    )
    cell_height = mo.ui.slider(
        start=10,
        stop=50,
        step=5,
        value=20,
        label="height of each cell in the color matrix",
        show_value=True,
    )
    font_size = mo.ui.slider(
        start=7,
        stop=15,
        step=1,
        value=10,
        label="font size",
        show_value=True,
    )
    grid_gap = mo.ui.slider(
        start=0,
        stop=10,
        step=1,
        value=1,
        label="grid gap",
        show_value=True,
    )
    return cell_height, cell_width, font_size, grid_gap, num_cols, num_rows


@app.cell
def __(
    cell_height,
    cell_width,
    font_size,
    grid_gap,
    mo,
    num_cols,
    num_rows,
):
    mo.vstack([num_rows, num_cols, cell_width, cell_height, font_size, grid_gap])
    return


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
    ColorMatrixWidget,
    cell_height,
    cell_width,
    font_size,
    grid_gap,
    mo,
    np,
    num_cols,
    num_rows,
    random_color_format,
    row_labels,
):
    color_matrix = np.array(
        [
            [random_color_format() for _ in range(num_cols.value)]
            for _ in range(num_rows.value)
        ]
    )

    widget = mo.ui.anywidget(
        ColorMatrixWidget(
            color_data=color_matrix,
            cell_width=cell_width.value,
            cell_height=cell_height.value,
            font_size=font_size.value,
            grid_gap=grid_gap.value,
            row_labels=row_labels,
            tooltips=color_matrix,
        )
    )
    return color_matrix, widget


@app.cell
def __(widget):
    widget
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
