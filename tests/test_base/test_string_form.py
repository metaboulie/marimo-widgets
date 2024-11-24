import marimo

__generated_with = "0.9.20"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __(mo):
    from mowidget.base.string_form import StringForm

    form = mo.ui.anywidget(StringForm(default_keys=["name", "email"]))
    return StringForm, form


@app.cell
def __(form):
    form
    return


@app.cell
def __(form):
    form.form_data
    return


if __name__ == "__main__":
    app.run()
