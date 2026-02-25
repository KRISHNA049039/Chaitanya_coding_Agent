"""
Lightweight string utility helpers for performance-sensitive operations.
"""
from io import StringIO
from collections import deque
import re
from typing import Dict, Iterable, List, Optional


class StringBuilder:
    """Efficiently build strings by appending parts and returning a single string."""
    def __init__(self) -> None:
        self._parts: List[str] = []

    def append(self, s: str) -> None:
        self._parts.append(s)

    def extend(self, parts: Iterable[str]) -> None:
        self._parts.extend(parts)

    def clear(self) -> None:
        self._parts.clear()

    def __len__(self) -> int:
        return sum(len(p) for p in self._parts)

    def build(self, sep: str = "") -> str:
        return sep.join(self._parts)


def fast_replace(s: str, mapping: Dict[str, str]) -> str:
    """Replace multiple substrings efficiently.

    - If mapping keys are all single characters, uses `str.translate` (very fast).
    - Otherwise builds a single regex that matches any of the keys and substitutes via a function.
    """
    if not mapping:
        return s

    # Check if all keys are single characters
    if all(len(k) == 1 for k in mapping.keys()):
        trans = str.maketrans(mapping)
        return s.translate(trans)

    # Otherwise, use regex alternation. Sort keys by length descending to prefer longer matches.
    keys = sorted(mapping.keys(), key=len, reverse=True)
    pattern = re.compile("|".join(re.escape(k) for k in keys))
    return pattern.sub(lambda m: mapping[m.group(0)], s)


def safe_split(s: str, sep: Optional[str] = None, maxsplit: int = -1) -> List[str]:
    """Wrapper around `str.split` that handles edge cases and None separators.

    When `sep` is `None`, uses default whitespace splitting. The function is provided for
    clarity and possible instrumentation.
    """
    if sep is None:
        return s.split(None, maxsplit)
    return s.split(sep, maxsplit)


def join_parts(parts: Iterable[str], sep: str = "") -> str:
    """Simple wrapper for join to make intent explicit."""
    return sep.join(parts)


def merge_lists_with_indices(left: List[int], right: List[int]) -> List[int]:
    """Merge two sorted lists using indices (avoid `pop(0)`)."""
    i, j = 0, 0
    merged: List[int] = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    if i < len(left):
        merged.extend(left[i:])
    if j < len(right):
        merged.extend(right[j:])
    return merged


# Small helpers
def to_deque(iterable: Iterable) -> deque:
    return deque(iterable)


def use_stringio_write(parts: Iterable[str]) -> str:
    buf = StringIO()
    for p in parts:
        buf.write(p)
    return buf.getvalue()
