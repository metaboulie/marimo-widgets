import marimo

__generated_with = "0.9.17"
app = marimo.App()


@app.cell
def __():
    import marimo as mo
    return (mo,)


@app.cell
def __():
    from mowidget.productivity.pomodoro_timer import PomodoroTimer
    return (PomodoroTimer,)


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""test default timer""")
    return


@app.cell(hide_code=True)
def __(PomodoroTimer):
    PomodoroTimer()
    return


@app.cell(hide_code=True)
def __(mo):
    mo.md(r"""test fraction input""")
    return


@app.cell(hide_code=True)
def __(PomodoroTimer):
    PomodoroTimer(
        work_duration=1.1111111111111,
        short_break=0.111111,
        long_break=2.2222222,
        sessions_before_long_break=2,
        num_cycles=2,
    )
    return


if __name__ == "__main__":
    app.run()
