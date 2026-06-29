"""Quick smoke test that pyg-lib imports and is usable.

Run with: uv run python test.py
(pyg-lib's import name is `pyg_lib`, with an underscore.)
"""

import sys


def main() -> int:
    # torch must import first; pyg_lib is built against a specific torch version.
    try:
        import torch
        print(f"torch        {torch.__version__}")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: could not import torch -> {exc!r}")
        return 1

    try:
        import pyg_lib
        print(f"pyg_lib      {pyg_lib.__version__}")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: could not import pyg_lib -> {exc!r}")
        return 1

    # Exercise the compiled extension a little so we know the binary actually loaded,
    # not just the Python wrapper.
    try:
        print(f"cuda_version {pyg_lib.cuda_version()}")
        # A real op: grouped/segment matmul over a tiny input.
        inputs = torch.randn(5, 4)
        ptr = torch.tensor([0, 2, 5])          # two segments: rows [0:2) and [2:5)
        other = torch.randn(2, 4, 3)
        out = pyg_lib.ops.segment_matmul(inputs, ptr, other)
        assert out.shape == (5, 3), out.shape
        print(f"segment_matmul OK -> output shape {tuple(out.shape)}")
    except Exception as exc:  # noqa: BLE001
        print(f"FAIL: pyg_lib imported but an op failed -> {exc!r}")
        return 1

    print("\nPASS: pyg_lib imported and ran successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
