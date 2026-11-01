def div(a: int, b: int) -> int:
    """Integer division truncating toward zero (like Rust)."""
    q = abs(a) // abs(b)
    return q if (a < 0) == (b < 0) else -q


def signum(a: int) -> int:
    return (a > 0) - (a < 0)
