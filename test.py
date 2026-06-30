"""Smoke tests for the CBS environment.

For every dependency, run a tiny example (or at least import + version) and
report PASS/FAIL per package without stopping on the first failure.

Run with:  uv run python test.py
"""

from __future__ import annotations

import os

# Headless plotting + quiet libs BEFORE anything imports matplotlib/wandb.
os.environ.setdefault("MPLBACKEND", "Agg")
os.environ.setdefault("WANDB_SILENT", "true")
os.environ.setdefault("WANDB_MODE", "offline")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

import importlib
import sys
import warnings
from importlib.metadata import PackageNotFoundError, version

warnings.filterwarnings("ignore")

TESTS: list[tuple[str, callable]] = []


def test(name: str):
    """Register a functional test under a display name."""
    def deco(fn):
        TESTS.append((name, fn))
        return fn
    return deco


def meta(dist: str) -> str:
    """Version-only check (no import) -- for CLI tools / apps."""
    return f"v{version(dist)}"


def imp(module: str, dist: str | None = None) -> str:
    """Import the module and report its version (a real load test)."""
    m = importlib.import_module(module)
    v = getattr(m, "__version__", None)
    if v is None:
        try:
            v = version(dist or module)
        except PackageNotFoundError:
            v = "?"
    return f"v{v}"


# --------------------------------------------------------------------------
# Functional micro-tests: each does a tiny real computation and asserts.
# --------------------------------------------------------------------------

@test("numpy")
def _():
    import numpy as np
    assert np.arange(10).sum() == 45
    return f"v{np.__version__}"


@test("pandas")
def _():
    import pandas as pd
    df = pd.DataFrame({"a": [1, 2, 3]})
    assert df["a"].sum() == 6
    return f"v{pd.__version__}"


@test("scipy")
def _():
    from scipy import stats
    assert abs(stats.norm.cdf(0) - 0.5) < 1e-9
    import scipy
    return f"v{scipy.__version__}"


@test("scikit-learn")
def _():
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression().fit(np.array([[0], [1], [2], [3]]), [0, 0, 1, 1])
    assert clf.predict([[3]])[0] == 1
    import sklearn
    return f"v{sklearn.__version__}"


@test("statsmodels")
def _():
    import numpy as np
    import statsmodels.api as sm
    x = sm.add_constant(np.arange(10.0))
    res = sm.OLS(2 * np.arange(10.0) + 1, x).fit()
    assert abs(res.params[1] - 2.0) < 1e-6
    return f"slope={res.params[1]:.2f}"


@test("polars")
def _():
    import polars as pl
    assert pl.DataFrame({"a": [1, 2, 3]})["a"].sum() == 6
    return f"v{pl.__version__}"


@test("pyarrow")
def _():
    import pyarrow as pa
    assert pa.table({"a": [1, 2, 3]}).num_rows == 3
    return f"v{pa.__version__}"


@test("duckdb")
def _():
    import duckdb
    assert duckdb.sql("SELECT 40 + 2 AS x").fetchone()[0] == 42
    return f"v{duckdb.__version__}"


@test("duckdb-engine")
def _():
    from sqlalchemy import create_engine, text
    eng = create_engine("duckdb:///:memory:")
    with eng.connect() as c:
        assert c.execute(text("SELECT 42")).scalar() == 42
    return meta("duckdb-engine")


@test("dask")
def _():
    import dask.array as da
    assert float(da.ones((100,), chunks=10).sum().compute()) == 100.0
    import dask
    return f"v{dask.__version__}"


@test("networkx")
def _():
    import networkx as nx
    assert nx.shortest_path_length(nx.path_graph(4), 0, 3) == 3
    return f"v{nx.__version__}"


@test("igraph")
def _():
    import igraph as ig
    assert ig.Graph.Ring(5).vcount() == 5
    return f"v{ig.__version__}"


@test("numba")
def _():
    from numba import njit

    @njit
    def s(n):
        acc = 0
        for i in range(n):
            acc += i
        return acc

    assert s(5) == 10
    import numba
    return f"v{numba.__version__}"


@test("jax")
def _():
    import jax
    g = float(jax.grad(lambda x: x ** 2)(3.0))
    assert abs(g - 6.0) < 1e-5
    return f"grad(x^2)|3={g:.1f}"


@test("matplotlib")
def _():
    import io
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4])
    buf = io.BytesIO()
    fig.savefig(buf, format="png")
    plt.close(fig)
    assert buf.getbuffer().nbytes > 0
    import matplotlib
    return f"v{matplotlib.__version__}"


@test("seaborn")
def _():
    import matplotlib.pyplot as plt
    import seaborn as sns
    sns.lineplot(x=[0, 1, 2], y=[0, 1, 4])
    plt.close("all")
    return f"v{sns.__version__}"


@test("plotly")
def _():
    import plotly.graph_objects as go
    fig = go.Figure(go.Scatter(x=[1, 2], y=[3, 4]))
    assert len(fig.to_json()) > 0
    import plotly
    return f"v{plotly.__version__}"


@test("openpyxl")
def _():
    from openpyxl import Workbook
    wb = Workbook()
    wb.active["A1"] = 42
    assert wb.active["A1"].value == 42
    import openpyxl
    return f"v{openpyxl.__version__}"


@test("h5py")
def _():
    import numpy as np
    import h5py
    with h5py.File("smoke.h5", "w", driver="core", backing_store=False) as f:
        f.create_dataset("d", data=np.arange(5))
        assert f["d"][2] == 2
    return f"v{h5py.__version__}"


@test("pyyaml")
def _():
    import yaml
    assert yaml.safe_load("a: 1")["a"] == 1
    return meta("pyyaml")


@test("json5")
def _():
    import json5
    assert json5.loads("{a: 1, b: 2}")["b"] == 2
    return f"v{json5.__version__}"


@test("hydra-core")
def _():
    from omegaconf import OmegaConf
    cfg = OmegaConf.create({"a": {"b": 1}})
    assert cfg.a.b == 1
    return meta("hydra-core")


@test("optuna")
def _():
    import optuna
    optuna.logging.set_verbosity(optuna.logging.WARNING)
    study = optuna.create_study()
    study.optimize(lambda t: t.suggest_float("x", -10, 10) ** 2, n_trials=5)
    return f"best={study.best_value:.3f}"


@test("lifelines")
def _():
    import numpy as np
    from lifelines import KaplanMeierFitter
    kmf = KaplanMeierFitter().fit(np.array([1.0, 2, 3, 4, 5]), [1, 1, 0, 1, 1])
    return f"median={kmf.median_survival_time_:.0f}"


@test("umap-learn")
def _():
    import numpy as np
    import umap
    rng = np.random.RandomState(0)
    emb = umap.UMAP(n_neighbors=4, n_components=2, random_state=0).fit_transform(rng.rand(20, 5))
    assert emb.shape == (20, 2)
    return f"v{umap.__version__}"


# --- torch + PyG stack (the ABI-sensitive ones) --------------------------

@test("torch")
def _():
    import torch
    a = torch.arange(6.0).reshape(2, 3)
    assert torch.allclose(a.sum(), torch.tensor(15.0))
    return f"v{torch.__version__}"


@test("torch-scatter")
def _():
    import torch
    from torch_scatter import scatter_add
    out = scatter_add(torch.tensor([1.0, 1, 1, 1]), torch.tensor([0, 0, 1, 2]))
    assert out.tolist() == [2.0, 1.0, 1.0]
    return meta("torch-scatter")


@test("torch-sparse")
def _():
    import torch
    from torch_sparse import SparseTensor
    st = SparseTensor(row=torch.tensor([0, 1, 2]), col=torch.tensor([1, 2, 0]),
                      sparse_sizes=(3, 3))
    assert st.sizes() == [3, 3]
    return meta("torch-sparse")

@test("torch-geometric")
def _():
    import torch
    from torch_geometric.data import Data
    from torch_geometric.nn import GCNConv
    edge_index = torch.tensor([[0, 1, 1, 2], [1, 0, 2, 1]])
    data = Data(x=torch.randn(3, 4), edge_index=edge_index)
    out = GCNConv(4, 2)(data.x, data.edge_index)
    assert out.shape == (3, 2)
    import torch_geometric
    return f"v{torch_geometric.__version__}"


@test("transformers")
def _():
    from transformers import AutoConfig
    cfg = AutoConfig.for_model("bert")
    assert cfg.model_type == "bert"
    import transformers
    return f"v{transformers.__version__}"


# --------------------------------------------------------------------------
# Lighter checks: import the package (real load) + report version.
# --------------------------------------------------------------------------

_IMPORT_ONLY = [
    ("accelerate", "accelerate", None),
    ("captum", "captum", None),
    ("eli5", "eli5", None),
    ("gensim", "gensim", None),
    ("hvplot", "hvplot", None),
    ("ibis", "ibis", None),
    ("ipython", "IPython", "ipython"),
    ("kaleido", "kaleido", None),
    ("metasyn", "metasyn", None),
    ("netcbs", "netcbs", None),
    ("pyreadstat", "pyreadstat", None),
    ("shap", "shap", None),
    ("tensorboard", "tensorboard", None),
    ("torchao", "torchao", None),
    ("wandb", "wandb", None),
]
for _n, _m, _d in _IMPORT_ONLY:
    TESTS.append((_n, lambda m=_m, d=_d: imp(m, d)))


# --------------------------------------------------------------------------
# Version-only checks: CLI tools / apps / plugins (importing is pointless).
# --------------------------------------------------------------------------

_META_ONLY = [
    ("jupysql", "jupysql"),
    ("jupyter", "jupyter"),
    ("jupyterlab", "jupyterlab"),
    ("jupyterlab-optuna", "jupyterlab-optuna"),
    ("notebook", "notebook"),
    ("metasyn-disclosure", "metasyn-disclosure"),
    ("pre-commit", "pre-commit"),
    ("pytest", "pytest"),
    ("ruff", "ruff"),
]
for _n, _d in _META_ONLY:
    TESTS.append((_n, lambda d=_d: meta(d)))

# Linux-only package: skip elsewhere.
if sys.platform == "linux":
    TESTS.append(("flash-attn", lambda: meta("flash-attn")))


def main() -> int:
    width = max(len(n) for n, _ in TESTS)
    passed, failed = 0, 0
    for name, fn in sorted(TESTS):
        try:
            detail = fn() or ""
            print(f"  PASS  {name:<{width}}  {detail}")
            passed += 1
        except Exception as exc:  # noqa: BLE001
            print(f"  FAIL  {name:<{width}}  {type(exc).__name__}: {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed, {len(TESTS)} total")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
