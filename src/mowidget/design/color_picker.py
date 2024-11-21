"""A color picker widget."""

import colorsys
import pathlib
from typing import ClassVar, Literal

import anywidget
import traitlets

PALETTE_TYPE = Literal[
    "analogous",
    "complementary",
    "triadic",
    "tetradic",
    "split_complementary",
    "monochromatic",
]


class ColorPicker(anywidget.AnyWidget):
    """
    A minimal color picker widget.

    Attributes:
        selected_color: The currently selected color.
        available_palette_types: List of available palette types.

    Methods:
        generate_palette: Generate a color palette based on color theory.

    """

    _esm = pathlib.Path(__file__).parent / "color-picker" / "color-picker.js"
    _css = pathlib.Path(__file__).parent / "color-picker" / "color-picker.css"

    # Core color value
    selected_color = traitlets.Unicode("#FF0000").tag(sync=True)

    available_palette_types: ClassVar[tuple[PALETTE_TYPE, ...]] = (
        "analogous",
        "complementary",
        "triadic",
        "tetradic",
        "split_complementary",
        "monochromatic",
    )

    def generate_palette(
        self,
        palette_type: PALETTE_TYPE = "analogous",
        palette_size: int = 5,
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
                return self._generate_complementary_palette(
                    h, s, v, palette_size
                )
            case "triadic":
                return self._generate_triadic_palette(h, s, v, palette_size)
            case "tetradic":
                return self._generate_tetradic_palette(h, s, v, palette_size)
            case "split_complementary":
                return self._generate_split_complementary_palette(
                    h, s, v, palette_size
                )
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
        """
        Generate analogous colors with evenly spaced hues
        and varying opacity.
        """
        colors = []
        base_angle = 30
        # Calculate optimal section size based on palette_size
        section_size = min(
            max(3, palette_size // 2), 7
        )  # Between 3 and 7 colors per section

        for i in range(palette_size):
            # Distribute hues evenly within the analogous range
            section = i % section_size
            hue_range = base_angle * (section_size - 1) / 360
            new_h = (
                h + (section / (section_size - 1) * hue_range - hue_range / 2)
            ) % 1.0

            # Smoothly vary opacity and saturation based on cycles
            cycle = i // section_size
            cycle_factor = cycle / (max(1, palette_size // section_size))

            new_s = max(0.2, min(1.0, s * (1.0 - cycle_factor * 0.3)))
            opacity = max(0.2, min(1.0, 1.0 - cycle_factor * 0.6))

            r, g, b = colorsys.hsv_to_rgb(new_h, new_s, v)
            colors.append(
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}{int(opacity*255):02x}"
            )
        return colors

    @staticmethod
    def _generate_complementary_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """Generate complementary colors with variations."""
        colors = []
        for i in range(palette_size):
            # Alternate between original and complementary
            is_complement = i % 2
            base_h = (h + (0.5 * is_complement)) % 1.0

            # Add variations in saturation and value
            cycle = i // 2
            new_s = max(0.2, min(1.0, s * (0.7 + (cycle * 0.15))))
            new_v = max(0.3, min(1.0, v * (0.85 + (cycle * 0.1))))
            opacity = max(0.3, 1.0 - (cycle * 0.12))

            r, g, b = colorsys.hsv_to_rgb(base_h, new_s, new_v)
            colors.append(
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}{int(opacity*255):02x}"
            )
        return colors

    @staticmethod
    def _generate_triadic_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """Generate triadic colors with variations."""
        colors = []
        angles = [0, 120, 240]

        for i in range(palette_size):
            # Cycle through triadic colors
            base_angle = angles[i % 3]
            new_h = (h + base_angle / 360) % 1.0

            # Add variations
            cycle = i // 3
            new_s = max(0.2, min(1.0, s * (0.75 + (cycle * 0.12))))
            new_v = max(0.3, min(1.0, v * (0.9 + (cycle * 0.08))))
            opacity = max(0.3, 1.0 - (cycle * 0.1))

            r, g, b = colorsys.hsv_to_rgb(new_h, new_s, new_v)
            colors.append(
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}{int(opacity*255):02x}"
            )
        return colors

    @staticmethod
    def _generate_tetradic_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """Generate four-color rectangular arrangement with variations."""
        colors = []
        angles = [0, 90, 180, 270]

        for i in range(palette_size):
            # Cycle through tetradic colors
            base_angle = angles[i % 4]
            new_h = (h + base_angle / 360) % 1.0

            # Add variations
            cycle = i // 4
            new_s = max(0.2, min(1.0, s * (0.8 + (cycle * 0.1))))
            new_v = max(0.3, min(1.0, v * (0.9 + (cycle * 0.08))))
            opacity = max(0.3, 1.0 - (cycle * 0.12))

            r, g, b = colorsys.hsv_to_rgb(new_h, new_s, new_v)
            colors.append(
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}{int(opacity*255):02x}"
            )
        return colors

    @staticmethod
    def _generate_split_complementary_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """Generate split complementary colors with variations."""
        colors = []
        angles = [0, 150, 210]  # Base color and two colors 30° from complement

        for i in range(palette_size):
            # Cycle through split complementary colors
            base_angle = angles[i % 3]
            new_h = (h + base_angle / 360) % 1.0

            # Add variations
            cycle = i // 3
            new_s = max(0.2, min(1.0, s * (0.75 + (cycle * 0.15))))
            new_v = max(0.3, min(1.0, v * (0.85 + (cycle * 0.1))))
            opacity = max(0.3, 1.0 - (cycle * 0.13))

            r, g, b = colorsys.hsv_to_rgb(new_h, new_s, new_v)
            colors.append(
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}{int(opacity*255):02x}"
            )
        return colors

    @staticmethod
    def _generate_monochromatic_palette(
        h: float, s: float, v: float, palette_size: int
    ) -> list[str]:
        """Generate monochromatic variations with decreasing opacity."""
        colors = []
        for i in range(palette_size):
            # Linear opacity decrease from 1.0 to 0.0
            opacity = (
                1.0 - (i / (palette_size - 1)) if palette_size > 1 else 1.0
            )

            r, g, b = colorsys.hsv_to_rgb(h, s, v)
            colors.append(
                f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}{int(opacity*255):02x}"
            )
        return colors
