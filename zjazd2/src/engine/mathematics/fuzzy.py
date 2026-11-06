from __future__ import annotations

from collections.abc import Callable, Mapping
from dataclasses import dataclass

MembershipFn = Callable[[float], float]


def triangle(a: float, b: float, c: float) -> MembershipFn:
    """Triangular membership function."""
    assert a <= b <= c

    def mu(x: float) -> float:
        if x <= a or x >= c:
            return 1.0 if x == b else 0.0
        if x <= b:
            return (x - a) / (b - a)
        return (c - x) / (c - b)

    return mu


def trapezoid(a: float, b: float, c: float, d: float) -> MembershipFn:
    """Trapezoidal membership function."""
    assert a <= b <= c <= d

    def mu(x: float) -> float:
        if b <= x <= c:
            return 1.0
        if x <= a or x >= d:
            return 0.0
        if x < b:
            return (x - a) / (b - a)
        return (d - x) / (d - c)

    return mu


class FuzzyVariable:
    """Linguistic variable: a range split into named fuzzy sets."""

    def __init__(self, name: str, low: float, high: float, terms: Mapping[str, MembershipFn]):
        assert low < high and terms
        self.name = name
        self.low = low
        self.high = high
        self.terms = dict(terms)

    def clamp(self, x: float) -> float:
        return min(max(x, self.low), self.high)

    def fuzzify(self, x: float) -> dict[str, float]:
        """Membership degree of x in every fuzzy set."""
        x = self.clamp(x)
        return {term: mu(x) for term, mu in self.terms.items()}


@dataclass(frozen=True)
class Rule:
    """Fuzzy rule: IF all conditions THEN output."""
    conditions: Mapping[str, str]
    then: str
    weight: float = 1.0


class MamdaniSystem:
    def __init__(
        self,
        inputs: list[FuzzyVariable],
        output: FuzzyVariable,
        rules: list[Rule],
        resolution: int = 101,
    ):
        self._inputs = {v.name: v for v in inputs}
        self._output = output
        self._rules = list(rules)

        for rule in self._rules:
            assert rule.then in output.terms, f"Unknown output term {rule.then!r}"
            for var, term in rule.conditions.items():
                assert var in self._inputs, f"Unknown input {var!r}"
                assert term in self._inputs[var].terms, f"Unknown term {term!r} of {var!r}"

        step = (output.high - output.low) / (resolution - 1)
        self._xs = [output.low + i * step for i in range(resolution)]
        self._samples = {term: [mu(x) for x in self._xs] for term, mu in output.terms.items()}

    @property
    def rules(self) -> list[Rule]:
        return list(self._rules)

    def firing_strengths(self, values: Mapping[str, float]) -> dict[str, float]:
        """Activation of each output set."""
        memberships = {name: var.fuzzify(values[name]) for name, var in self._inputs.items()}
        strengths = dict.fromkeys(self._output.terms, 0.0)
        for rule in self._rules:
            s = rule.weight * min(memberships[var][term] for var, term in rule.conditions.items())
            if s > strengths[rule.then]:
                strengths[rule.then] = s
        return strengths

    def compute(self, values: Mapping[str, float], default: float | None = None) -> float:
        """Mamdani inference with centroid defuzzification."""
        strengths = self.firing_strengths(values)
        active = [(s, self._samples[t]) for t, s in strengths.items() if s > 0.0]

        num = den = 0.0
        if active:
            for i, x in enumerate(self._xs):
                mu = max(min(s, samples[i]) for s, samples in active)
                num += x * mu
                den += mu

        if den == 0.0:
            return default if default is not None else (self._output.low + self._output.high) / 2
        return num / den
