import math
from .vector2 import Vector2
from ..mathematics.perlin_noise import PerlinNoise


class Terrain:
    def __init__(
        self,
        seed: int = 0,
        scale: float = 0.05,
        amplitude: float = 100.0,
        octaves: int = 4,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
    ):
        self._noise = PerlinNoise(seed)
        self._scale = scale
        self._amplitude = amplitude
        self._octaves = octaves
        self._persistence = persistence
        self._lacunarity = lacunarity

    def height_at(self, x: float) -> float:
        h = self._noise.height(
            x * self._scale,
            octaves=self._octaves,
            persistence=self._persistence,
            lacunarity=self._lacunarity,
        )
        return h * self._amplitude

    def slope_at(self, x: float, eps: float = 0.25) -> float:
        return (self.height_at(x + eps) - self.height_at(x - eps)) / (2 * eps)

    def normal_at(self, x: float) -> Vector2:
        slope = self.slope_at(x)
        length = math.sqrt(1.0 + slope * slope)
        return Vector2(-slope / length, 1.0 / length)

    def raycast(
        self,
        origin: Vector2,
        direction: Vector2,
        max_distance: float,
        step: float = 1.0,
        refine_iterations: int = 12,
    ) -> float | None:
        """Distance along a ray to the terrain, or None if not hit."""

        def clearance(t: float) -> float:
            x = origin.x + direction.x * t
            y = origin.y + direction.y * t
            return y - self.height_at(x)

        if clearance(0.0) <= 0.0:
            return 0.0

        prev = 0.0
        t = 0.0
        while t < max_distance:
            t = min(t + step, max_distance)
            if clearance(t) <= 0.0:
                lo, hi = prev, t
                for _ in range(refine_iterations):
                    mid = (lo + hi) / 2
                    if clearance(mid) > 0.0:
                        lo = mid
                    else:
                        hi = mid
                return hi
            prev = t
        return None

    def tangent_at(self, x: float) -> Vector2:
        slope = self.slope_at(x)
        length = math.sqrt(1.0 + slope * slope)
        return Vector2(1.0 / length, slope / length)
