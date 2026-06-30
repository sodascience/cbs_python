"""Smoke test: for every package in requirements.in, check it imports and report its version.

Run with: uv run python check_environment.py
(or: python check_environment.py, inside the venv you're testing)
"""

import re
import subprocess
import sys
from importlib.metadata import PackageNotFoundError, version

# pip name -> import name, only where they differ
IMPORT_NAME = {
    "pyyaml": "yaml",
    "scikit-learn": "sklearn",
    "duckdb-engine": "duckdb_engine",
    "pre-commit": "pre_commit",
    "ipython": "IPython",
    "hydra-core": "hydra",
    "umap-learn": "umap",
    "metasyn-disclosure": "metasyncontrib.disclosure",
    "jupysql": "sql",
}
# packages with no importable module (CLI tools) - version-check only
NOT_IMPORTABLE = {"ruff"}


def package_names(path: str = "requirements.in") -> list[str]:
    names = []
    for line in open(path):
        line = line.split("#", 1)[0].strip()
        if not line or line.startswith("--"):
            continue
        name = re.split(r"[;<>=\[\s]", line, 1)[0]
        names.append(name)
    return names


def main() -> int:
    failed = []
    for pip_name in package_names():
        key = pip_name.lower()
        try:
            v = version(pip_name)
        except PackageNotFoundError:
            print(f"FAIL  {pip_name:25} not installed")
            failed.append(pip_name)
            continue

        if key in NOT_IMPORTABLE:
            print(f"OK    {pip_name:25} {v}  (not importable, skipped import check)")
            continue

        import_name = IMPORT_NAME.get(key, key.replace("-", "_"))
        # run each import in its own subprocess: a crashing native extension
        # (e.g. an ABI mismatch) would otherwise take the whole script down
        result = subprocess.run(
            [sys.executable, "-c", f"import {import_name}"], capture_output=True, text=True
        )
        if result.returncode == 0:
            print(f"OK    {pip_name:25} {v}")
        else:
            err = result.stderr.strip().splitlines()[-1] if result.stderr else f"exit code {result.returncode}"
            print(f"FAIL  {pip_name:25} {v}  import error -> {err}")
            failed.append(pip_name)

    print()
    if failed:
        print(f"FAILED: {len(failed)} package(s) -> {', '.join(failed)}")
        print(
            "Note: a 'ModuleNotFoundError' above may just mean this script guessed the "
            "wrong import name, not that the package is broken. If you hit one, find the "
            "real import name (e.g. check the package's docs) and add it to IMPORT_NAME."
        )
        return 1
    print("PASS: all packages imported and reported a version.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
