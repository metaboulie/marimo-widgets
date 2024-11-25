"""A simple string form."""

from __future__ import annotations

import pathlib

import anywidget
import traitlets


class StringForm(anywidget.AnyWidget):
    """
    A widget that creates a dynamic form for string inputs.

    This widget allows users to create a form with multiple string input
    fields. The fields are generated based on the provided default keys,
    where each key represents a form field label.

    Parameters
    ----------
    default_keys : list[str] | None, optional
        A list of strings that will be used as labels/keys for the form fields.
        If None, an empty form will be created. Default is None.

    Attributes
    ----------
    default_keys : traitlets.List
        The list of keys used to generate form fields, synced with frontend.
    form_data : traitlets.Dict
        A dictionary containing the form field values, where keys match
        default_keys and values are the user inputs, synced with frontend.

    """

    _esm = pathlib.Path(__file__).parent.parent / "frontend/js/string-form.js"
    _css = (
        pathlib.Path(__file__).parent.parent / "frontend/css/string-form.css"
    )

    # Input trait for default keys
    default_keys = traitlets.List(traitlets.Unicode()).tag(sync=True)

    # Output trait for form data
    form_data = traitlets.Dict().tag(sync=True)

    def __init__(self, default_keys: list[str] | None = None) -> None:
        super().__init__()
        self.default_keys = default_keys or []
        self.form_data = {key: "" for key in self.default_keys}
