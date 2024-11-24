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


    # Example custom outlier detection function
    def custom_outlier_detection(
        data: np.ndarray,
    ) -> tuple[np.ndarray, np.ndarray]:
        """Custom outlier detection using percentiles."""
        finite_data = data[np.isfinite(data)]
        high_threshold = np.percentile(finite_data, 95)
        low_threshold = np.percentile(finite_data, 5)

        outliers_high = (data > high_threshold) & np.isfinite(data)
        outliers_low = (data < low_threshold) & np.isfinite(data)

        return outliers_high, outliers_low
    return (
        base_data,
        cols,
        custom_outlier_detection,
        i,
        j,
        num_outliers,
        outlier_positions,
        outlier_values,
        pos,
        rows,
        val,
    )


@app.cell(hide_code=True)
def cell_3(mo):
    # UI controls for widget configuration
    controls = mo.ui.dictionary(
        {
            "color_mode": mo.ui.dropdown(
                options=["grayscale", "single_color"],
                value="grayscale",
                label="Color Mode",
            ),
            "base_color": mo.ui.text(
                value="#1f77b4",
                label="Base Color (hex)",
            ),
            "cell_size": mo.ui.slider(
                start=10,
                stop=50,
                step=1,
                value=20,
                label="Cell Size",
            ),
            "outlier_threshold": mo.ui.slider(
                start=0.5, stop=3.0, step=0.1, value=1.0, label="Outlier Threshold"
            ),
            "outlier_detection": mo.ui.dropdown(
                options=["std", "custom"], value="std", label="Outlier Detection"
            ),
            "margin_size": mo.ui.slider(
                start=0,
                stop=10,
                step=1,
                value=2,
                label="Margin Size",
            ),
            "font_size": mo.ui.slider(
                start=8,
                stop=16,
                step=1,
                value=12,
                label="Font Size",
            ),
        }
    )
    return (controls,)


@app.cell
def cell_4(ArrayViewer, base_data, controls, custom_outlier_detection, mo):
    # Create custom row labels
    row_labels = [f"Row {i+1}" for i in range(len(base_data))]

    # Determine outlier detection method
    outlier_method = (
        custom_outlier_detection
        if controls["outlier_detection"].value == "custom"
        else controls["outlier_detection"].value
    )

    # Create the widget
    widget = mo.ui.anywidget(
        ArrayViewer(
            data=base_data,
            color_mode=controls["color_mode"].value,
            base_color=controls["base_color"].value,
            outlier_detection=outlier_method,
            outlier_threshold=controls["outlier_threshold"].value,
            row_labels=row_labels,
            cell_size=controls["cell_size"].value,
            margin_size=controls["margin_size"].value,
            font_size=controls["font_size"].value,
        )
    )
    return outlier_method, row_labels, widget


@app.cell
def cell_5(controls):
    controls.vstack()
    return


@app.cell
def cell_6(widget):
    # Display the widget
    widget
    return


@app.cell
def cell_8(widget):
    # Display selected cells
    widget.selected_cells
    return


if __name__ == "__main__":
    app.run()
