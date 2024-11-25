"""A fun dummy widget that says hello."""

import pathlib

import anywidget
import traitlets


class DummyWidget(anywidget.AnyWidget):
    """
    A playful widget that says hello with style.

    Parameters
    ----------
    message: str
        The message to display.
    particle_count: int
        The number of particles to display.

    Examples
    --------
    >>> DummyWidget(
    ...     message="hello marimo",
    ...     particle_count=50,
    ... )

    """

    _esm = pathlib.Path(__file__).parent.parent / "frontend/js/dummy.js"
    _css = pathlib.Path(__file__).parent.parent / "frontend/css/dummy.css"

    # Fun traits to control the widget
    message = traitlets.Unicode(default_value="hello marimo").tag(sync=True)
    particle_count = traitlets.Int(default_value=50).tag(sync=True)

    def __init__(
        self,
        message: str = "hello marimo",
        particle_count: int = 50,
    ) -> None:
        """
        Initialize the widget.

        Parameters
        ----------
        message: str
            The message to display.
        particle_count: int
            The number of particles to display.

        """
        super().__init__()

        self.message = message
        self.particle_count = particle_count
