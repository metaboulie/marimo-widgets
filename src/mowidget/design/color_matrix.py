"""
A widget for displaying and interacting with color matrices.

This module implements a custom widget based on anywidget that
renders a matrix of colors with interactive features like tooltips
and cell selection. It supports both numpy arrays
and nested lists as input data structures.
"""

from __future__ import annotations

import pathlib

import anywidget
import marimo as mo
import numpy as np
import traitlets


class ColorMatrix(anywidget.AnyWidget):
    """
    An interactive widget for displaying a matrix of colors.

    This widget creates a grid of colored cells with customizable dimensions,
    labels, and tooltips. It supports user interaction through cell selection
    and hovering.

    Args:
        color_data (np.ndarray | list[list]):
            2D array or nested list of color values to display in the matrix.
        tooltips (np.ndarray | list[list], optional):
            2D array or nested list of tooltip texts for each cell. If None,
            the color values will be used as tooltips.
        row_labels (list[str], optional):
            List of labels for each row.
            If None, no row labels will be displayed.
        cell_width (int, default=40):
            Width of each cell in pixels.
        cell_height (int, default=40):
            Height of each cell in pixels.
        grid_gap (int, default=2):
            Gap between cells in pixels.
        font_size (int, default=12):
            Font size for labels in pixels.
        cell_radius (int, default=0):
            Border radius of cells in pixels.
            Set to half of cell width/height for circular cells.

    Attributes:
        selected_cells (list):
            Currently selected cells in the format [row, col, value].

    Examples:
        >>> color_data = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        >>> tooltips = np.array(
        ...     [["A", "B", "C"], ["D", "E", "F"], ["G", "H", "I"]]
        ... )
        >>> row_labels = ["Row 1", "Row 2", "Row 3"]
        >>> color_matrix = ColorMatrix(color_data, tooltips, row_labels)
        >>> color_matrix.selected_cells

    Note:
        Use ColorMatrix.controller() to get a dictionary of traits that can
        be used to control the widget.

    """

    _esm = pathlib.Path(__file__).parent.parent / "frontend/js/color-matrix.js"
    _css = (
        pathlib.Path(__file__).parent.parent / "frontend/css/color-matrix.css"
    )

    # Core data
    colors = traitlets.List().tag(sync=True)  # List of lists for color values
    tooltips = traitlets.List().tag(
        sync=True
    )  # List of lists for tooltip text

    # Labels
    row_labels = traitlets.List(
        trait=traitlets.Unicode(), default_value=[]
    ).tag(sync=True)

    selected_cells = traitlets.List().tag(
        sync=True
    )  # List of [row, col, value]

    # Styling
    cell_width = traitlets.Int(default_value=40).tag(sync=True)
    cell_height = traitlets.Int(default_value=40).tag(sync=True)
    grid_gap = traitlets.Int(default_value=2).tag(sync=True)
    font_size = traitlets.Int(default_value=12).tag(sync=True)
    cell_radius = traitlets.Int(default_value=0).tag(sync=True)

    def __init__(  # noqa: PLR0913
        self,
        color_data: np.ndarray | list[list],
        tooltips: np.ndarray | list[list] | None = None,
        row_labels: list[str] | None = None,
        cell_width: int = 40,
        cell_height: int = 40,
        grid_gap: int = 2,
        font_size: int = 12,
        cell_radius: int = 0,
    ) -> None:
        super().__init__()

        # Convert numpy arrays to lists for JSON serialization
        self.colors = (
            color_data.tolist()
            if isinstance(color_data, np.ndarray)
            else color_data
        )

        # Handle tooltips
        if tooltips is None:
            tooltips = [[str(c) for c in row] for row in self.colors]
        self.tooltips = (
            tooltips.tolist() if isinstance(tooltips, np.ndarray) else tooltips
        )

        # Handle labels - only set if provided
        self.row_labels = row_labels if row_labels is not None else []

        self.selected_cells = []

        # Styling
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.grid_gap = grid_gap
        self.font_size = font_size
        self.cell_radius = cell_radius

    @classmethod
    def controller(cls: type[ColorMatrix]) -> mo.ui.dictionary:
        """Get the controller for the Color Matrix."""
        return mo.ui.dictionary(
            {
                "cell_width": mo.ui.number(
                    start=1, step=1, value=40, label="cell width"
                ),
                "cell_height": mo.ui.number(
                    start=1, step=1, value=40, label="cell height"
                ),
                "grid_gap": mo.ui.number(start=0, value=2, label="grid gap"),
                "font_size": mo.ui.number(
                    start=1, step=1, value=10, label="font size"
                ),
                "cell_radius": mo.ui.number(
                    start=0, step=1, value=0, label="cell radius"
                ),
            }
        )
