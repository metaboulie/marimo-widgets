import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell(hide_code=True)
def __():
    import marimo as mo
    return (mo,)


@app.cell(hide_code=True)
def __():
    from mowidget.base.dummy import DummyWidget
    return (DummyWidget,)


@app.cell(hide_code=True)
def __(mo):
    message = mo.ui.text(value="hello marimo", label="message: ")
    particle_count = mo.ui.slider(
        10,
        1000,
        10,
        value=50,
        label="number of floating particles: ",
        show_value=True,
    )

    mo.vstack([message, particle_count])
    return message, particle_count


@app.cell(hide_code=True)
def __(DummyWidget, message, particle_count):
    DummyWidget(
        message=message.value,
        particle_count=particle_count.value,
    )
    return


if __name__ == "__main__":
    app.run()
