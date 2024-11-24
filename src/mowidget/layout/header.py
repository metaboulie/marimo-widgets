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
    banner_height: int
        Optional. Height of the banner image in pixels. Default is 200.

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
    ...     banner_height=300,
    ... )

    """

    _esm = Path(__file__).parent / "header" / "notebook-header.js"
    _css = Path(__file__).parent / "header" / "notebook-header.css"

    metadata = traitlets.Dict({}).tag(sync=True)
    banner = traitlets.Unicode("").tag(sync=True)
    banner_height = traitlets.Int(200).tag(sync=True)

    def __init__(
        self,
        metadata: dict,
        banner: str | None = None,
        banner_height: int = 200,
    ) -> None:
        """
        Initialize the NotebookHeader widget.

        Parameters
        ----------
        metadata: dict
            A dictionary of metadata to display in the header.
        banner: str | None
            Optional. A URL to an image to display as the banner.
        banner_height: int
            Optional. Height of the banner image in pixels. Default is 200.

        """
        super().__init__()

        if not isinstance(metadata, dict):
            msg = "metadata must be a dictionary"
            raise TypeError(msg)

        self.metadata = metadata
        self.banner = banner or ""
        self.banner_height = banner_height
