import marimo

__generated_with = "0.9.20"
app = marimo.App()


@app.cell
def cell_1():
    import marimo as mo
    import numpy as np
    from mowidget.viewer.array_viewer import ArrayViewer
    return ArrayViewer, mo, np


@app.cell
def cell_2(np):
    # Generate base data with normal distribution
    np.random.seed(42)  # For reproducibility
    rows = 20
    cols = 30
    base_data = np.random.normal(loc=0, scale=1, size=(rows, cols))

    # Add some outliers
    num_outliers = 10
    outlier_positions = np.random.choice(rows * cols, num_outliers, replace=False)
    outlier_values = np.random.choice([-10, -8, 8, 10], num_outliers)

    # Add some special values (inf/nan)
    base_data[0, 0] = np.inf
    base_data[0, 1] = -np.inf
    base_data[0, 2] = np.nan

    for pos, val in zip(outlier_positions, outlier_values):
        i, j = pos // cols, pos % cols
        base_data[i, j] = val
    return (
        base_data,
        cols,
        i,
        j,
        num_outliers,
        outlier_positions,
        outlier_values,
        pos,
        rows,
        val,
    )


@app.cell
def cell_4(ArrayViewer, array_viewer_controller, base_data, mo):
    # Create custom row labels
    row_labels = [f"Row {i+1}" for i in range(len(base_data))]

    # Create the widget
    widget = mo.ui.anywidget(
        ArrayViewer(data=base_data, **array_viewer_controller.value)
    )
    return row_labels, widget


@app.cell
def __(ArrayViewer):
    array_viewer_controller = ArrayViewer.controller()
    return (array_viewer_controller,)


@app.cell
def cell_6(widget):
    widget
    return


@app.cell
def __(array_viewer_controller):
    array_viewer_controller.vstack()
    return


@app.cell
def cell_8(widget):
    # Display selected cells
    widget.selected_cells
    return


@app.cell
def __(mo):
    mo.md(r"""test custom outlier detection""")
    return


@app.cell
def __(np):
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
def __(
    ArrayViewer,
    array_viewer_controller,
    base_data,
    custom_outlier_detection,
    mo,
):
    mo.ui.anywidget(
        ArrayViewer(
            data=base_data,
            outlier_detection=custom_outlier_detection,
            **array_viewer_controller.value,
        )
    )
    return


@app.cell
def __(array_viewer_controller):
    array_viewer_controller.vstack()
    return


if __name__ == "__main__":
    app.run()
