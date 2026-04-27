"""scitex-repro quickstart: reproducibility helpers (seeds, ids, hashes)."""

import numpy as np

import scitex_repro


def main():
    # 1. fix_seeds — deterministic random for python/numpy.
    scitex_repro.fix_seeds(seed=42)
    a = np.random.rand(3)
    scitex_repro.fix_seeds(seed=42)
    b = np.random.rand(3)
    print("seeds reproducible:", np.allclose(a, b))
    assert np.allclose(a, b)

    # 2. gen_id / gen_ID — short readable run identifier.
    rid = scitex_repro.gen_id()
    print("gen_id:", rid)
    assert isinstance(rid, str) and len(rid) > 0

    # 3. gen_timestamp / timestamp — formatted current time.
    ts = scitex_repro.gen_timestamp()
    print("timestamp:", ts)
    assert isinstance(ts, str)

    # 4. hash_array — stable hash of numerical content.
    h1 = scitex_repro.hash_array(np.array([1, 2, 3]))
    h2 = scitex_repro.hash_array(np.array([1, 2, 3]))
    print("array hash stable:", h1 == h2)
    assert h1 == h2


if __name__ == "__main__":
    main()
