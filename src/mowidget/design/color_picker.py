"""A color picker widget."""

import colorsys
import pathlib
from typing import Literal

import anywidget
import traitlets


class ColorPicker(anywidget.AnyWidget):
    """
    A minimal color picker widget.

    Attributes:
        selected_color: The currently selected color.

    Methods:
        generate_palette: Generate a color palette based on color theory.

    """

    _esm = pathlib.Path(__file__).parent / "color-picker" / "color-picker.js"
    _css = pathlib.Path(__file__).parent / "color-picker" / "color-picker.css"

    # Core color value
    selected_color = traitlets.Unicode("#FF0000").tag(sync=True)

    # Generated palette
    palette_size = traitlets.Int(5).tag(sync=True)
    palette_type = traitlets.Unicode("analogous").tag(sync=True)

    def generate_palette(
        self,
        palette_type: Literal[
            "analogous",
            "complementary",
            "triadic",
            "tetradic",
            "split_complementary",
            "monochromatic",
        ],
        palette_size: int,
    ) -> list[str]:
        """Generate a color palette based on color theory."""
        # Convert hex to HSV
        r, g, b = (
            int(self.selected_color[i : i + 2], 16) / 255 for i in (1, 3, 5)
        )
        h, s, v = colorsys.rgb_to_hsv(r, g, b)

        match palette_type:
            case "analogous":
                return self._generate_analogous_palette(h, s, v, palette_size)
            case "complementary":
                return self._generate_complementary_palette(h, s, v)
            case "triadic":
                return self._generate_triadic_palette(h, s, v)
            case "tetradic":
                return self._generate_tetradic_palette(h, s, v)
            case "split_complementary":
                return self._generate_split_complementary_palette(h, s, v)
            case "monochromatic":
                return self._generate_monochromatic_palette(
                    h, s, v, palette_size
                )
            case _:
                msg = f"Invalid palette type: {palette_type}"
                raise ValueError(msg)

    @staticmethod
    def _generate_analogous_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """Generate analogous colors with evenly spaced hues."""
        colors = []
        angle = 30
        for i in range(palette_size):
            new_h = (h + (i - palette_size // 2) * angle / 360) % 1.0
            r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
            colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return colors

    def _generate_complementary_palette(
        self, h: float, s: float, v: float
    ) -> list[str]:
        """Generate a complementary color pair."""
        colors = [self.selected_color]  # Original color
        comp_h = (h + 0.5) % 1.0
        r, g, b = colorsys.hsv_to_rgb(comp_h, s, v)
        colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return colors

    @staticmethod
    def _generate_triadic_palette(h: float, s: float, v: float) -> list[str]:
        """Generate three colors evenly spaced around the color wheel."""
        colors = []
        for angle in [0, 120, 240]:
            new_h = (h + angle / 360) % 1.0
            r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
            colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return colors

    @staticmethod
    def _generate_tetradic_palette(h: float, s: float, v: float) -> list[str]:
        """
        Generate four colors in a rectangular arrangement
        on the color wheel.
        """
        colors = []
        for angle in [0, 90, 180, 270]:
            new_h = (h + angle / 360) % 1.0
            r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
            colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return colors

    @staticmethod
    def _generate_split_complementary_palette(
        h: float, s: float, v: float
    ) -> list[str]:
        """Generate a color and two colors adjacent to its complement."""
        colors = []
        for angle in [
            0,
            150,
            210,
        ]:  # Base color and two colors 30° from complement
            new_h = (h + angle / 360) % 1.0
            r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
            colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return colors

    @staticmethod
    def _generate_monochromatic_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """
        Generate variations of the same color by
        adjusting saturation and value.
        """
        colors = []
        for i in range(palette_size):
            # Vary both saturation and value
            new_s = max(0.1, min(1.0, s + (i - palette_size // 2) * 0.2))
            new_v = max(0.1, min(1.0, v + (i - palette_size // 2) * 0.1))
            r, g, b = colorsys.hsv_to_rgb(h, new_s, new_v)
            colors.append(f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}")
        return colors
