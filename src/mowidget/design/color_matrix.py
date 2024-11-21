import pathlib
from typing import Optional, Union

import anywidget
import numpy as np
import traitlets

"""
todo
- auto scale cell size based on size of the matrix
"""


class ColorMatrixWidget(anywidget.AnyWidget):
    _esm = pathlib.Path(__file__).parent / "color-matrix" / "color-matrix.js"
    _css = pathlib.Path(__file__).parent / "color-matrix" / "color-matrix.css"

    # Core data
    colors = traitlets.List().tag(sync=True)  # List of lists for color values
    tooltips = traitlets.List().tag(
        sync=True
    )  # List of lists for tooltip text

    # Labels
    row_labels = traitlets.List(trait=traitlets.Unicode()).tag(sync=True)

    selected_cells = traitlets.List().tag(
        sync=True
    )  # List of [row, col, value]

    # Styling
    cell_width = traitlets.Int(default_value=40).tag(sync=True)
    cell_height = traitlets.Int(default_value=40).tag(sync=True)
    grid_gap = traitlets.Int(default_value=2).tag(sync=True)
    font_size = traitlets.Int(default_value=12).tag(sync=True)

    def __init__(
        self,
        color_data: Union[np.ndarray, list[list]],
        tooltips: Optional[Union[np.ndarray, list[list]]] = None,
        row_labels: Optional[list[str]] = None,
        cell_width: int = 40,
        cell_height: int = 40,
        grid_gap: int = 2,
        font_size: int = 12,
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

        # Handle labels
        n_rows = len(self.colors)
        self.row_labels = (
            row_labels
            if row_labels is not None
            else [str(i) for i in range(n_rows)]
        )

        self.selected_cells = []

        # Styling
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.grid_gap = grid_gap
        self.font_size = font_size
