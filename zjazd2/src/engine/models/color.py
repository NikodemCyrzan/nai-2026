from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    """Color with red, green, blue and alpha values."""

    r: int
    g: int
    b: int
    a: int = 255
