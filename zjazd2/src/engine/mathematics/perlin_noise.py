import math
import random


class PerlinNoise:
    def __init__(self, seed: int = 0):
        p = list(range(256))
        random.Random(seed).shuffle(p)
        self._perm = p * 2

    @staticmethod
    def _fade(t: float) -> float:
        return t * t * t * (t * (t * 6 - 15) + 10)

    @staticmethod
    def _lerp(a: float, b: float, t: float) -> float:
        return a + (b - a) * t

    def _grad(self, h: int, x: float) -> float:
        return x if (h & 1) == 0 else -x

    def _noise(self, x: float) -> float:
        xi = math.floor(x)
        xf = x - xi
        xi &= 255

        u = self._fade(xf)
        a = self._grad(self._perm[xi], xf)
        b = self._grad(self._perm[xi + 1], xf - 1)
        return self._lerp(a, b, u)

    def height(
        self,
        x: float,
        octaves: int = 4,
        persistence: float = 0.5,
        lacunarity: float = 2.0,
    ) -> float:
        total = 0.0
        amplitude = 1.0
        frequency = 1.0
        max_amplitude = 0.0

        for _ in range(octaves):
            total += self._noise(x * frequency) * amplitude
            max_amplitude += amplitude
            amplitude *= persistence
            frequency *= lacunarity

        value = total / max_amplitude
        value *= 2
        return max(0.0, min(1.0, (value + 1) / 2))
