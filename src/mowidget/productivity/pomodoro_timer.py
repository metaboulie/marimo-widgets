"""Pomodoro Timer."""

import pathlib

import anywidget
import marimo as mo
import traitlets


class PomodoroTimer(anywidget.AnyWidget):
    """
    Pomodoro Timer.

    Parameters
    ----------
    work_duration: float
        The duration of a work session in minutes.
    short_break: float
        The duration of a short break in minutes.
    long_break: float
        The duration of a long break in minutes.
    sessions_before_long_break: int
        The number of sessions before a long break.
    num_cycles: int
        The total number of pomodoro cycles to complete.

    Attributes
    ----------
    current_session: int
        The current session number.

    Examples
    --------
    >>> PomodoroTimer(
    ...     work_duration=25.0,
    ...     short_break=5.0,
    ...     long_break=15.0,
    ...     sessions_before_long_break=4,
    ... )

    """

    _esm = (
        pathlib.Path(__file__).parent.parent / "frontend/js/pomodoro-timer.js"
    )
    _css = (
        pathlib.Path(__file__).parent.parent
        / "frontend/css/pomodoro-timer.css"
    )

    sessions_before_long_break = traitlets.Int(default_value=4).tag(sync=True)
    num_cycles = traitlets.Int(default_value=5).tag(sync=True)
    _current_cycle = traitlets.Int(default_value=1).tag(sync=True)
    _work_duration_seconds = traitlets.Int(default_value=1500).tag(sync=True)
    _short_break_seconds = traitlets.Int(default_value=300).tag(sync=True)
    _long_break_seconds = traitlets.Int(default_value=900).tag(sync=True)
    _current_session = traitlets.Int(default_value=0).tag(sync=True)
    _timer_state = traitlets.Unicode(default_value="stopped").tag(sync=True)
    _remaining_seconds = traitlets.Int(default_value=1500).tag(sync=True)
    _is_break = traitlets.Bool(default_value=False).tag(sync=True)

    def __init__(
        self,
        work_duration: float = 25.0,
        short_break: float = 5.0,
        long_break: float = 15.0,
        sessions_before_long_break: int = 4,
        num_cycles: int = 5,
    ) -> None:
        """
        Initialize the Pomodoro Timer.

        Parameters
        ----------
        work_duration: float
            The duration of a work session in minutes.
        short_break: float
            The duration of a short break in minutes.
        long_break: float
            The duration of a long break in minutes.
        sessions_before_long_break: int
            The number of sessions before a long break.
        num_cycles: int
            The total number of pomodoro cycles to complete.

        """
        super().__init__()
        self._validate_positive(work_duration, "work_duration")
        self._validate_positive(short_break, "short_break")
        self._validate_positive(long_break, "long_break")
        self._validate_positive(
            sessions_before_long_break, "sessions_before_long_break"
        )
        self._validate_positive(num_cycles, "num_cycles")

        self.work_duration = work_duration
        self.short_break = short_break
        self.long_break = long_break
        self.sessions_before_long_break = sessions_before_long_break
        self.num_cycles = num_cycles

        self._work_duration_seconds = int(work_duration * 60.0)
        self._short_break_seconds = int(short_break * 60.0)
        self._long_break_seconds = int(long_break * 60.0)
        self._current_cycle = 1

        self._current_session = 0
        self._timer_state = "stopped"
        self._remaining_seconds = int(work_duration * 60.0)
        self._is_break = False

    @property
    def current_session(self) -> int:
        """Get the current session number."""
        return self._current_session

    @staticmethod
    def _validate_positive(value: float, param_name: str) -> None:
        """
        Validate that a parameter value is positive.

        Parameters
        ----------
        value : float
            The value to validate
        param_name : str
            The name of the parameter (for error message)

        Raises
        ------
        ValueError
            If the value is not positive

        """
        if value <= 0:
            msg = f"{param_name} must be positive, got {value}"
            raise ValueError(msg)

    @classmethod
    def controller(cls: type["PomodoroTimer"]) -> mo.ui.dictionary:
        """Get the controller for the Pomodoro Timer."""
        return mo.ui.dictionary(
            {
                "work_duration": mo.ui.number(
                    start=0.1, value=25.0, label="work duration"
                ),
                "short_break": mo.ui.number(
                    start=0.1, value=5.0, label="short break"
                ),
                "long_break": mo.ui.number(
                    start=0.1, value=15.0, label="long break"
                ),
                "sessions_before_long_break": mo.ui.number(
                    start=1,
                    step=1,
                    value=4,
                    label="sessions before long break",
                ),
                "num_cycles": mo.ui.number(
                    start=1, step=1, value=3, label="number of cycles"
                ),
            }
        )
