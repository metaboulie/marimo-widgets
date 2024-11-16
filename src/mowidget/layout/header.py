"""
Responsive and interactive header widgets for Marimo notebooks with
dynamic content rendering and toggle functionality.
"""

from __future__ import annotations

from pathlib import Path

import anywidget
import traitlets


class NotebookHeader(anywidget.AnyWidget):
    """
    A responsive and interactive header widget for Marimo notebooks with
    dynamic content rendering and toggle functionality.

    Parameters
    ----------
    metadata: dict
        A dictionary of metadata to display in the header.
    banner: str
        Optional. A URL to an image to display as the banner.

    Examples
    --------
    >>> NotebookHeader(
    ...     metadata={
    ...         "Title": "Comprehensive E-Commerce Customer Behavior Analysis",
    ...         "Author": "<a href='https://github.com/Haleshot/marimo-tutorials'>"
    ...         "Dr. Jane Smith, PhD</a>",
    ...         "Last Updated": "November 3, 2024",
    ...     },
    ...     banner="https://example.com/banner.png",
    ... )

    """

    _esm = Path(__file__).parent / "header" / "notebook-header.js"
    _css = Path(__file__).parent / "header" / "notebook-header.css"

    metadata = traitlets.Dict({}).tag(sync=True)
    banner = traitlets.Unicode("").tag(sync=True)

    def __init__(self, metadata: dict, banner: str | None = None) -> None:
        """Initialize the NotebookHeader widget."""
        super().__init__()

        if not isinstance(metadata, dict):
            msg = "metadata must be a dictionary"
            raise TypeError(msg)

        self.metadata = metadata
        self.banner = banner or ""
