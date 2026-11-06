from dataclasses import dataclass


@dataclass(frozen=True)
class Color:
    r: int
    g: int
    b: int
    a: int = 255
