import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    from mowidget.design.color_picker import ColorPicker

    color_picker = mo.ui.anywidget(ColorPicker())
    color_picker
    return ColorPicker, color_picker


@app.cell
def __(color_picker):
    color_picker.selected_color
    return


@app.cell
def __(color_picker, mo):
    mo.md(f"Selected color: {color_picker.selected_color}")

    # Generate palette
    color_picker.generate_palette(color_picker.selected_color, "analogous", 5)
    return


if __name__ == "__main__":
    app.run()
