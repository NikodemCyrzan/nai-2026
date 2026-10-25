class Vector2:
    def __init__(self, x: int | float=0.0, y: int | float=0.0):
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        return f"Vector2(x={self.x}, y={self.y})"

    def __add__(self, other: Vector2 | int | float):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        return Vector2(self.x + other, self.y + other)

    def __radd__(self, other: int | float):
        return self + other

    def __sub__(self, other: Vector2 | int | float):
        return self + (-other)

    def __mul__(self, other: Vector2 | int | float):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        return Vector2(self.x * other, self.y * other)

    def __rmul__(self, other: int | float):
        return self * other

    def __neg__(self):
        return Vector2(-self.x, -self.y)

    def __truediv__(self, other: Vector2):
        return self ** -1

    def __pow__(self, power: int | float):
        return Vector2(self.x ** power, self.y ** power)

    @staticmethod
    def lerp(a: Vector2, b: Vector2, t: float):
        return Vector2(
            a.x + (b.x - a.x) * t,
            a.y + (b.y - a.y) * t,
        )
