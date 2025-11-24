#!/usr/bin/env python3
import math
import random
import struct

# === CONFIG ===

TARGET_COUNT = 1_000_000
OUTFILE = "hellfloat64.txt"
SEED = 123456789  # for reproducibility

# === Helpers ===


def float_from_bits(bits: int) -> float:
    """Build a float64 from a 64-bit integer."""
    return struct.unpack(">d", bits.to_bytes(8, "big"))[0]


def is_finite(x: float) -> bool:
    return math.isfinite(x)


def fmt(x: float) -> str:
    return format(x, ".17g")


# === IEEE754 constants ===

DBL_MAX = float.fromhex("0x1.fffffffffffffp+1023")  # max normal
DBL_MIN_NORMAL = float.fromhex("0x1.0p-1022")  # min normal
DBL_MIN_SUB = float.fromhex("0x0.0000000000001p-1022")  # min positive subnormal
DBL_EPS = 2.220446049250313e-16  # 2^-52

# === Generators ===


def gen_special_core() -> list[float]:
    """
    Small fixed set of very important values, repeated a bit:
    zeros, ones, eps, min/max normals, min subnormal, etc.
    """
    base = [
        0.0,
        -0.0,
        1.0,
        -1.0,
        10.0,
        -10.0,
        0.1,
        -0.1,
        DBL_MAX,
        -DBL_MAX,
        DBL_MIN_NORMAL,
        -DBL_MIN_NORMAL,
        DBL_MIN_SUB,
        -DBL_MIN_SUB,
        DBL_EPS,
        -DBL_EPS,
    ]
    out: list[float] = []
    repeat = 64
    for v in base:
        out.extend([v] * repeat)
    return out  # length = len(base) * repeat = 16 * 64 = 1024


def gen_powers_of_two(n: int) -> list[float]:
    """
    Powers of two across the full exponent range [-1074, 1023],
    cycling through exponents and alternating sign, for exactly n values.
    """
    if n <= 0:
        return []
    exp_min = -1074
    exp_max = 1023
    exps = list(range(exp_min, exp_max + 1))  # 2098 exponents

    out: list[float] = []
    for i in range(n):
        e = exps[i % len(exps)]
        sign = 1.0 if (i & 1) == 0 else -1.0
        x = math.ldexp(sign, e)  # sign * 2^e
        out.append(x)
    return out


def gen_powers_of_ten(n: int) -> list[float]:
    """
    Powers of ten over [-308, 308], cycling exponents and alternating sign.
    Exactly n values.
    """
    if n <= 0:
        return []
    exp_min = -308
    exp_max = 308
    exps = list(range(exp_min, exp_max + 1))  # 617 exponents

    out: list[float] = []
    for i in range(n):
        e = exps[i % len(exps)]
        sign = 1.0 if (i & 1) == 0 else -1.0
        x = sign * (10.0**e)
        out.append(x)
    return out


def gen_logspace_extremes(n: int) -> list[float]:
    """
    Values of the form mantissa * 10^exp, with:
      - exp uniform in [-308, 308]
      - mantissa in [1, 10)
      - random sign
    Exactly n finite values.
    """
    out: list[float] = []
    if n <= 0:
        return out

    while len(out) < n:
        exp10 = random.randint(-308, 308)
        mant = 1.0 + random.random() * 9.0
        sign = -1.0 if random.getrandbits(1) else 1.0
        try:
            x = sign * mant * (10.0**exp10)
        except OverflowError:
            continue
        if is_finite(x):
            out.append(x)

    return out


def gen_subnormals(n: int) -> list[float]:
    """
    Subnormal doubles, by sampling mantissas across [1, 2^52-1].
    We generate exactly n distinct subnormals, with sign alternating.
    """
    out: list[float] = []
    if n <= 0:
        return out

    max_mant = (1 << 52) - 1
    step = max(1, max_mant // n)

    for i in range(n):
        mant = 1 + (i * step) % max_mant
        sign_bit = (i & 1)  # alternate sign
        bits = (sign_bit << 63) | mant  # exponent = 0 → subnormal
        x = float_from_bits(bits)
        out.append(x)

    return out


def gen_near_powers_of_ten(n: int) -> list[float]:
    """
    Values just before/after powers of ten, to stress rounding:
      x ≈ 10^e * (1 ± eps, 1 ± eps/2)
    We cycle over a set of exponents and deltas, with alternating sign,
    returning exactly n finite values.
    """
    out: list[float] = []
    if n <= 0:
        return out

    candidates = [-308, -200, -100, -50, -10, -1, 0, 1, 10, 50, 100, 200, 308]
    deltas = [-DBL_EPS, -DBL_EPS / 2.0, DBL_EPS / 2.0, DBL_EPS]

    num_exp = len(candidates)
    num_delta = len(deltas)

    i = 0
    while len(out) < n:
        e = candidates[i % num_exp]
        d = deltas[(i // num_exp) % num_delta]
        base = 10.0**e
        x = base * (1.0 + d)
        sign = 1.0 if (i & 1) == 0 else -1.0
        val = sign * x
        if is_finite(val):
            out.append(val)
        i += 1

    return out


# === MAIN ===


def main():
    random.seed(SEED)

    values: list[float] = []

    # 1) Fixed special core
    core = gen_special_core()
    values.extend(core)
    core_len = len(core)

    remaining = TARGET_COUNT - core_len
    if remaining <= 0:
        # In case someone sets TARGET_COUNT < core_len
        values = values[:TARGET_COUNT]
    else:
        # Distribute remaining values across 5 generators.
        base_chunk = remaining // 5
        n_pow2 = base_chunk
        n_pow10 = base_chunk
        n_log = base_chunk
        n_sub = base_chunk
        n_near = remaining - (n_pow2 + n_pow10 + n_log + n_sub)

        values.extend(gen_powers_of_two(n_pow2))
        values.extend(gen_powers_of_ten(n_pow10))
        values.extend(gen_logspace_extremes(n_log))
        values.extend(gen_subnormals(n_sub))
        values.extend(gen_near_powers_of_ten(n_near))

    # Final sanity: we should now have exactly TARGET_COUNT
    assert len(
        values
    ) == TARGET_COUNT, f"Got {len(values)} values, expected {TARGET_COUNT}"

    random.shuffle(values)

    with open(OUTFILE, "w") as f:
        for x in values:
            f.write(fmt(x) + "\n")

    print(f"Wrote {len(values)} float64 values to {OUTFILE}")


if __name__ == "__main__":
    main()
