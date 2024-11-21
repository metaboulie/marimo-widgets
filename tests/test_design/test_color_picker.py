import marimo

__generated_with = "0.9.20"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(color_picker, mo):
    mo.md(f"Selected color: {color_picker.selected_color}")
    return


@app.cell
def __(mo):
    from mowidget.design.color_picker import ColorPicker

    color_picker = mo.ui.anywidget(ColorPicker())
    color_picker
    return ColorPicker, color_picker


@app.cell
def __(ColorMatrix, color_picker, generated_palette):
    color_matrix = ColorMatrix(
        color_data=generated_palette,
        row_labels=color_picker.available_palette_types,
        font_size=8,
        cell_height=30,
        cell_width=30,
    )
    color_matrix
    return (color_matrix,)


@app.cell
def __():
    from mowidget.design.color_matrix import ColorMatrix
    return (ColorMatrix,)


@app.cell
def __(mo):
    palette_size = mo.ui.slider(
        start=3, step=1, stop=30, value=16, show_value=True, label="Palette Size: "
    )
    palette_size
    return (palette_size,)


@app.cell
def __(color_picker, palette_size):
    generated_palette = [
        color_picker.generate_palette(
            palette_type=palette_type, palette_size=palette_size.value
        )
        for palette_type in color_picker.available_palette_types
    ]
    return (generated_palette,)


if __name__ == "__main__":
    app.run()
