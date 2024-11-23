"""
A widget for visualizing and analyzing array data with color mapping and
interactive features.

This module implements a custom widget based on anywidget that renders
array data as a color matrix with advanced features like outlier detection,
custom thresholds, and interactive selection.
"""

from __future__ import annotations

import pathlib
from typing import TYPE_CHECKING, Callable, Literal

import anywidget
import numpy as np
import traitlets

if TYPE_CHECKING:
    from numpy.typing import ArrayLike


class ArrayViewer(anywidget.AnyWidget):
    """
    An interactive widget for visualizing array data with color mapping and
    analysis features.

    This widget creates a colored visualization of array data with support for:
    - Color mapping modes (grayscale, single color)
    - Outlier detection and highlighting with +/- indicators
    - Special indicators for nan/inf values
    - Interactive cell selection and hover information

    Parameters
    ----------
    data : ArrayLike
        2D array of numerical values to visualize
    color_mode : str, default="grayscale"
        Color mapping mode. One of: "grayscale", "single_color"
    base_color : str, default="#1f77b4"
        Base color for single_color mode (hex format)
    outlier_detection : str | Callable | None, default="std"
        Method for detecting outliers: "std", callable, or None.
        If callable, it should take the array data and return a tuple of
        (outliers_high, outliers_low) boolean masks
    outlier_threshold : float, default=2.0
        Threshold for outlier detection when using "std" method
    row_labels : list[str] | None, default=None
        Custom labels for rows
    cell_size : int, default=40
        Size of each cell in pixels
    margin_size : int, default=2
        Size of margin between cells in pixels
    font_size : int, default=12
        Font size for labels and tooltips in pixels

    """

    _esm = pathlib.Path(__file__).parent / "array-viewer" / "array-viewer.js"
    _css = pathlib.Path(__file__).parent / "array-viewer" / "array-viewer.css"

    # Core data
    data = traitlets.List().tag(sync=True)
    colors = traitlets.List().tag(sync=True)
    tooltips = traitlets.List().tag(sync=True)
    markers = traitlets.List().tag(sync=True)  # For +/- and special indicators

    # Display settings
    color_mode = traitlets.Unicode(default_value="grayscale").tag(sync=True)
    base_color = traitlets.Unicode(default_value="#1f77b4").tag(sync=True)

    # Labels
    row_labels = traitlets.List(trait=traitlets.Unicode()).tag(sync=True)

    # Interaction state
    selected_cells = traitlets.List().tag(sync=True)
    hover_info = traitlets.Dict().tag(sync=True)

    # Styling
    cell_size = traitlets.Int(default_value=40).tag(sync=True)
    grid_gap = traitlets.Int(default_value=2).tag(sync=True)
    font_size = traitlets.Int(default_value=12).tag(sync=True)

    def __init__(  # noqa: PLR0913
        self,
        data: ArrayLike,
        color_mode: Literal["grayscale", "single_color"] = "grayscale",
        base_color: str = "#1f77b4",
        outlier_detection: Literal["std"] | Callable | None = "std",
        outlier_threshold: float = 2.0,
        row_labels: list[str] | None = None,
        cell_size: int = 40,
        margin_size: int = 2,
        font_size: int = 12,
    ) -> None:
        """Initialize the ArrayViewer widget."""
        super().__init__()

        # Convert input data to numpy array and then to list
        self._array_data = np.asarray(data)
        if self._array_data.ndim != 2:  # noqa: PLR2004
            msg = "Input data must be 2-dimensional"
            raise ValueError(msg)

        self.data = self._array_data.tolist()

        # Set display parameters
        self.color_mode = color_mode
        self.base_color = base_color
        self.outlier_detection = outlier_detection
        self.outlier_threshold = outlier_threshold

        # Set styling
        self.cell_size = cell_size
        self.grid_gap = margin_size
        self.font_size = font_size

        # Initialize labels
        rows, _ = self._array_data.shape
        self.row_labels = (
            [str(i) for i in range(rows)] if row_labels is None else row_labels
        )

        # Initialize colors, markers and tooltips
        self._update_colors()
        self._update_markers()
        self._update_tooltips()

        # Initialize interaction state
        self.selected_cells = []
        self.hover_info = {}

    def _update_colors(self) -> None:
        """Update the color mapping based on current settings."""
        data = self._array_data
        normalized = self._normalize_data(data)

        if self.color_mode == "grayscale":
            self.colors = [
                [f"rgb({v*255},{v*255},{v*255})" for v in row]
                for row in normalized.tolist()
            ]
        else:  # single_color
            self.colors = [
                [f"{self.base_color}{int(v*255):02x}" for v in row]
                for row in normalized.tolist()
            ]

    def _normalize_data(self, data: np.ndarray) -> np.ndarray:
        """Normalize data to [0,1] range, handling inf/nan."""
        finite_mask = np.isfinite(data)
        if not np.any(finite_mask):
            return np.zeros_like(data)

        vmin = np.min(data[finite_mask])
        vmax = np.max(data[finite_mask])

        if vmin == vmax:
            return np.zeros_like(data)

        normalized = (data - vmin) / (vmax - vmin)
        normalized[~finite_mask] = 0  # Set inf/nan to 0
        return np.clip(normalized, 0, 1)

    def _update_markers(self) -> None:
        """Update cell markers for outliers and special values."""
        data = self._array_data
        markers = np.full_like(data, "", dtype=str)

        # Create masks for special values and outliers
        inf_mask = np.isinf(data)
        nan_mask = np.isnan(data)
        finite_mask = np.isfinite(data)

        # Initialize outlier masks
        outliers_high = np.zeros_like(data, dtype=bool)
        outliers_low = np.zeros_like(data, dtype=bool)

        # Handle outliers with vectorized operations
        if self.outlier_detection == "std":
            if np.any(finite_mask):
                mean = np.mean(data[finite_mask])
                std = np.std(data[finite_mask])
                threshold = self.outlier_threshold * std

                outliers_high = (data > mean + threshold) & finite_mask
                outliers_low = (data < mean - threshold) & finite_mask
        elif callable(self.outlier_detection):
            outliers_high, outliers_low = self.outlier_detection(data)

        # Apply markers using numpy where operations
        markers = np.where(inf_mask, "∞", markers)
        markers = np.where(nan_mask, "N", markers)
        markers = np.where(outliers_high, "+", markers)
        markers = np.where(outliers_low, "-", markers)

        self.markers = markers.tolist()

    def _update_tooltips(self) -> None:
        """Update tooltips with current data and outlier information."""
        self.tooltips = [[str(v) for v in row] for row in self.data]

        if self.outlier_detection == "std":
            finite_mask = np.isfinite(self._array_data)
            if np.any(finite_mask):
                mean = np.mean(self._array_data[finite_mask])
                std = np.std(self._array_data[finite_mask])
                threshold = self.outlier_threshold * std

                outliers = np.abs(self._array_data - mean) > threshold
                for i, row in enumerate(outliers):
                    for j, is_outlier in enumerate(row):
                        if is_outlier and np.isfinite(self._array_data[i, j]):
                            self.tooltips[i][j] += " (outlier)"

    def set_color_mode(self, mode: str) -> None:
        """Change the color mapping mode."""
        self.color_mode = mode
        self._update_colors()

    def set_outlier_detection(
        self, method: str | None, threshold: float | None = None
    ) -> None:
        """Update outlier detection settings."""
        self.outlier_detection = method
        if threshold is not None:
            self.outlier_threshold = threshold
        self._update_markers()
        self._update_tooltips()
