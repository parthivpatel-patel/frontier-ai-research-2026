"""Bounded infinite-trace LTL lasso witness search; standard-library only.

Protocol 025. This is classical bounded model checking, NOT a new theorem.
A witness proves two parsed formulas differ on the constructed infinite lasso.
Absence of a witness within a finite bound DOES NOT prove equivalence.
Only small constructed tests and pinned external audits run on GitHub cloud.
"""
from __future__ import annotations

import re

_TOKEN = re.compile(r"prop_[0-9]+|->|&&|\|\||[()!&|]|[A-Za-z_][A-Za-z_0-9]*")
_ALIASES = {
    "!": "not", "not": "not",
    "&": "and", "&&": "and", "and": "and",
    "|": "or", "||": "or", "or": "or",
    "->": "implies", "implies": "implies",
    "u": "until", "until": "until",
    "x": "next", "next": "next",
    "f": "finally", "finally": "finally", "eventually": "finally",
    "g": "always", "always": "always", "globally": "always",
    "true": "true", "false": "false",
}


class UnsupportedFormula(ValueError):
    """Syntax outside the explicitly supported, limited LTL fragment."""


def tokenize(text: str) -> list[str]:
    if not isinstance(text, str) or not text.strip() or len(text) > 512:
        raise UnsupportedFormula("empty or oversized formula")
    tokens = []
    end = 0
    for match in _TOKEN.finditer(text):
        if text[end:match.start()].strip():
            raise UnsupportedFormula("unknown token")
        raw = match.group()
        token = raw if raw.startswith("prop_") or raw in ("(", ")") else _ALIASES.get(raw.lower())
        if token is None:
            raise UnsupportedFormula("unsupported operator")
        tokens.append(token)
        end = match.end()
    if text[end:].strip() or len(tokens) > 96:
        raise UnsupportedFormula("trailing unknown characters or too many tokens")
    return tokens


class _Parser:
    def __init__(self, tokens: list[str]):
        self.tokens = tokens
        self.i = 0

    def take(self, token: str) -> bool:
        if self.i < len(self.tokens) and self.tokens[self.i] == token:
            self.i += 1
            return True
        return False

    def parse(self):
        result = self.implies()
        if self.i != len(self.tokens):
            raise UnsupportedFormula("unexpected trailing token")
        return result

    def implies(self):
        lhs = self.disjunction()
        if self.take("implies"):
            return ("or", ("not", lhs), self.implies())
        return lhs

    def disjunction(self):
        lhs = self.conjunction()
        while self.take("or"):
            lhs = ("or", lhs, self.conjunction())
        return lhs

    def conjunction(self):
        lhs = self.until()
        while self.take("and"):
            lhs = ("and", lhs, self.until())
        return lhs

    def until(self):
        lhs = self.unary()
        if self.take("until"):
            return ("until", lhs, self.until())
        return lhs

    def unary(self):
        for op in ("not", "next", "finally", "always"):
            if self.take(op):
                return (op, self.unary())
        if self.take("("):
            expr = self.implies()
            if not self.take(")"):
                raise UnsupportedFormula("missing closing parenthesis")
            return expr
        if self.i >= len(self.tokens):
            raise UnsupportedFormula("missing operand")
        token = self.tokens[self.i]
        self.i += 1
        if token.startswith("prop_"):
            return ("atom", token)
        if token in ("true", "false"):
            return (token,)
        raise UnsupportedFormula("expected atomic proposition")


def parse(text: str):
    return _Parser(tokenize(text)).parse()


def atoms(node) -> set[str]:
    if node[0] == "atom":
        return {node[1]}
    result = set()
    for child in node[1:]:
        if isinstance(child, tuple):
            result.update(atoms(child))
    return result


def _truth(node, values: dict[str, int], n: int, loop: int) -> int:
    """Return an n-bit mask of satisfaction at every state of an infinite lasso."""
    all_states = (1 << n) - 1

    def predecessor(mask: int) -> int:
        result = 0
        for i in range(n):
            next_i = i + 1 if i + 1 < n else loop
            if mask & (1 << next_i):
                result |= 1 << i
        return result

    op = node[0]
    if op == "atom":
        return values[node[1]]
    if op == "true":
        return all_states
    if op == "false":
        return 0
    if op == "not":
        return all_states ^ _truth(node[1], values, n, loop)
    if op == "and":
        return _truth(node[1], values, n, loop) & _truth(node[2], values, n, loop)
    if op == "or":
        return _truth(node[1], values, n, loop) | _truth(node[2], values, n, loop)
    if op == "next":
        return predecessor(_truth(node[1], values, n, loop))
    if op == "always":
        negated = ("not", node[1])
        return all_states ^ _truth(("finally", negated), values, n, loop)
    if op == "finally":
        right = _truth(node[1], values, n, loop)
        left = all_states
    elif op == "until":
        left = _truth(node[1], values, n, loop)
        right = _truth(node[2], values, n, loop)
    else:
        raise UnsupportedFormula("unsupported AST node")
    # Least fixpoint of Z = right OR (left AND X Z), valid on infinite lassos.
    current = right
    for _ in range(n + 1):
        updated = right | (left & predecessor(current))
        if updated == current:
            return current
        current = updated
    raise AssertionError("least fixpoint did not converge")


def find_counterexample(
    predicted: str, reference: str, *, max_states: int = 3,
    max_propositions: int = 3, max_cases: int = 20000,
    equalities: tuple[tuple[str, ...], ...] = (),
) -> dict:
    """Enumerate small infinite lassos, with optional assumed proposition identities.

    A 'witness' is a real counterexample under the chosen assumptions.
    'no_witness_within_bound' is strictly inconclusive for unrestricted LTL.
    No formulas, source text, or valuations are included in the result.
    """
    if (type(max_states) is not int or not 1 <= max_states <= 4 or
            type(max_propositions) is not int or not 1 <= max_propositions <= 4 or
            type(max_cases) is not int or not 1 <= max_cases <= 100000):
        raise ValueError("invalid bounded-search configuration")
    left, right = parse(predicted), parse(reference)
    symbols = sorted(atoms(left) | atoms(right))
    if len(symbols) > max_propositions:
        return {"status": "unsupported_proposition_count", "checked_lassos": 0}
    parent = {p: p for p in symbols}

    def root(p: str) -> str:
        while parent[p] != p:
            p = parent[p]
        return p

    for group in equalities:
        if not isinstance(group, tuple) or not group or any(
            not isinstance(p, str) or p not in parent for p in group
        ):
            raise ValueError("invalid assumed identity group")
        anchor = root(group[0])
        for p in group[1:]:
            parent[root(p)] = anchor
    classes = sorted({root(p) for p in symbols})
    class_index = {p: classes.index(root(p)) for p in symbols}
    checked = 0
    for n in range(1, max_states + 1):
        for loop in range(n):
            for assignment in range(1 << (n * len(classes))):
                if checked >= max_cases:
                    return {"status": "incomplete_budget", "checked_lassos": checked}
                checked += 1
                values = {}
                for p in symbols:
                    j = class_index[p]
                    mask = 0
                    for t in range(n):
                        if assignment & (1 << (t * len(classes) + j)):
                            mask |= 1 << t
                    values[p] = mask
                a = _truth(left, values, n, loop) & 1
                b = _truth(right, values, n, loop) & 1
                if a != b:
                    return {
                        "status": "witness", "checked_lassos": checked,
                        "witness_states": n, "loop_start": loop,
                    }
    return {
        "status": "no_witness_within_bound",
        "checked_lassos": checked, "bound_states": max_states,
    }
