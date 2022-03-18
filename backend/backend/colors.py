import math
from pathlib import Path
from typing import cast
from typing import Sequence
from typing import TypeVar

from errors import CustomColorModelError
from paths import DATA_DIR
from PIL import Image


T = TypeVar("T")


# Source: https://github.com/d3/d3-scale-chromatic#cyclical
CYCLIC_COLOR_HUES_IMAGE = DATA_DIR / "rainbow.png"


def get_values_and_nearest_colors(
    values_with_target_colors: Sequence[tuple[T, "CustomColor"]],
    rest_values: Sequence[T],
    lightness: float = 0,
) -> list[tuple[T, "CustomColor"]]:
    colors = get_evenly_space_colors(
        len(values_with_target_colors) + len(rest_values),
        start_hue=values_with_target_colors[0][1].hue if len(list(values_with_target_colors)) > 0 else 0,
        lightness=lightness,
    )

    index_to_best_color_value: dict[int, tuple[T, CustomColor]] = {}

    for val, target_color in values_with_target_colors:

        def key_func(index_and_color: tuple[int, CustomColor]) -> float:
            index, color = index_and_color

            if index in index_to_best_color_value:
                return 2  # Out of normal hue range: [0;1[

            return color.hue_dist(target_color)

        index, nearest_color = min(enumerate(colors), key=key_func)
        index_to_best_color_value[index] = (val, nearest_color)

    rest_colors = [color for i, color in enumerate(colors) if i not in index_to_best_color_value]

    return list(index_to_best_color_value.values()) + list(zip(rest_values, rest_colors))


def get_evenly_space_colors(n: int, start_hue: float = 0, lightness: float = 0) -> list["CustomColor"]:
    hue_step = 1 / n
    return [CustomColor((start_hue + hue_step * i) % 1, lightness) for i in range(n)]


def convert_image_to_lightness_hue_rgb_nested_array(
    image_file_path: Path
) -> tuple[tuple[tuple[float, float, float], ...], ...]:
    # TODO: Use Lab color space, instead of RGB
    with Image.open(image_file_path) as hues_img:
        pixels = hues_img.load()
        midtones = [pixels[i, 0] for i in range(hues_img.size[0])]

        array = [[[0.0, 0.0, 0.0] for _ in range(len(midtones))] for _ in range(256)]

        for column_index, (mid_r, mid_g, mid_b) in enumerate(midtones):
            for row_index in range(128):
                array[row_index][column_index][0] = mid_r * (row_index / 128)
                array[row_index][column_index][1] = mid_g * (row_index / 128)
                array[row_index][column_index][2] = mid_b * (row_index / 128)

            for row_index in range(128, 256):
                white_fac = (row_index - 128) / 128

                array[row_index][column_index][0] = mid_r * (1 - white_fac) + 255 * white_fac
                array[row_index][column_index][1] = mid_g * (1 - white_fac) + 255 * white_fac
                array[row_index][column_index][2] = mid_b * (1 - white_fac) + 255 * white_fac

    return tuple(tuple(cast(tuple[float, float, float], color) for color in row) for row in array)



class CustomColor:
    """Color using custom human-friendly, cylindrical color model (see CYCLIC_COLOR_SCALE_IMAGE)."""

    # Rows=lightness; columns=hue
    # Dimensions: rows=256; columns=<width of CYCLIC_COLOR_HUES_IMAGE>
    LIGHTNESS_HUE_RGB = convert_image_to_lightness_hue_rgb_nested_array(CYCLIC_COLOR_HUES_IMAGE)
    _DIMENSIONS = (len(LIGHTNESS_HUE_RGB), len(LIGHTNESS_HUE_RGB[0]), len(LIGHTNESS_HUE_RGB[0][0]))

    def __init__(self, hue = 0, lightness = 0) -> None:
        # interval [ 0;1[ -> 0: 0 degrees; tending towards 1 tends toward 360 degrees
        self.hue: float = hue
        # interval [-1;1] -> -1: black; 0: original; 1: white
        self.lightness: float = lightness
        # We don't need saturation at the moment

    # Logic
    # ------------------------------------------------------------------------

    @classmethod
    def from_rgb(cls, rgb_color: tuple[float, float, float]) -> "CustomColor":
        # Use nearest color - this doesn't need to be precise
        min_dist = math.inf
        min_lightness_index = 0
        min_hue_index = 0
        for lightness_index, row in enumerate(cls.LIGHTNESS_HUE_RGB):
            for hue_index, cmp_rgb_color in enumerate(row):
                dist = math.sqrt(
                    (rgb_color[0] - cmp_rgb_color[0])**2
                    + (rgb_color[1] - cmp_rgb_color[1])**2
                    + (rgb_color[2] - cmp_rgb_color[2])**2
                )

                if dist < min_dist:
                    min_dist = dist
                    min_lightness_index = lightness_index
                    min_hue_index = hue_index

        return cls(
            min_hue_index / cls._DIMENSIONS[1],
            (min_lightness_index / cls._DIMENSIONS[0]) * 2 - 1,
        )

    def to_rgb(self) -> tuple[float, float, float]:
        # Use nearest value - this doesn't need to be precise
        return self.LIGHTNESS_HUE_RGB[
            round(self._DIMENSIONS[0] * ((self.lightness + 1) / 2))
        ][
            round(self._DIMENSIONS[1] * self._hue)
        ]

    def to_rgb_rounded(self) -> tuple[int, int, int]:
        r, g, b = self.to_rgb()
        return (round(r), round(g), round(b))

    def to_hex(self) -> str:
        r, g, b = self.to_rgb_rounded()
        return f"#{r:02X}{g:02X}{b:02X}"

    def hue_dist(self, other: "CustomColor") -> float:
        return abs(other.hue - self.hue)

    # Encapsulation
    # ------------------------------------------------------------------------

    @property
    def hue(self) -> float:
        return self._hue

    @hue.setter
    def hue(self, value: float) -> None:
        # Normalization with modulo is a sensible default sense because hue is cyclic
        normalized_value = value % 1
        # Sanity check - this doesn't need to be fast
        self.set_hue_or_error_if_out_of_range(normalized_value)

    def set_hue_or_error_if_out_of_range(self, value: float) -> None:
        """Strict version of normal setter."""
        if 0 <= value < 1:
            self._hue = value
            return

        raise CustomColorModelError("Hue must be in left inclusive interval [0;1[")

    @property
    def lightness(self) -> float:
        return self._lightness

    @lightness.setter
    def lightness(self, value: float) -> None:
        if -1 <= value <= 1:
            self._lightness = value
            return

        raise CustomColorModelError("Lightness must be in inclusive interval [-1;1]")
