## What this is for

CBS Remote Access (RA) only lets you use Python packages that CBS has approved and installed in advance. To get a package approved, you submit a file pip requirements.txt file listing exactly which packages (and versions) you need, and CBS installs them for you.

This repository helps you build that file correctly, without needing to understand Python packaging in depth. You will:

1. Write down which packages you want, in a simple text file (`requirements.in`).
2. Run two commands that figure out the exact versions that work together.
3. Get a ready-to-send file (`environment0000.txt`) to email to CBS.
4. Use the same setup on your own computer, outside of CBS RA, while you work.

You only need to follow these steps once per project (and again whenever you want to add a new package).

---

## Basic configuration

### Step 0: Install `uv`

`uv` is the tool that does the heavy lifting (figuring out compatible package
versions). Install it once, following the official instructions:
https://docs.astral.sh/uv/getting-started/installation/

If you've never used a terminal before: a terminal is just a window where you
type commands instead of clicking buttons. On Windows, open "PowerShell" or
"Command Prompt"; on Mac, open "Terminal" (both are pre-installed). The
installation instructions above include a single command to paste in and run.

### Step 1: Download this repository to your computer

Important: save it to a normal folder on your computer's hard drive — **not** a
folder that syncs to the cloud (OneDrive, pCloud Drive, Dropbox, Google Drive, etc).
Cloud-sync folders can silently break the setup in step 3.

If you're comfortable with git:

```sh
git clone <repo-url>
cd cbs_python
```

Otherwise, download the repository as a ZIP from its webpage and unzip it into a
local folder.

### Step 2: Say which packages you want

Open `requirements.in` in a text editor. It's a plain list of package names, one
per line, already organized into groups (data handling, visualization, etc.), with
a short comment next to each one explaining what it's for.

- To add a package, add a new line with its name.
- To remove one, delete its line (or put a `#` in front of it to keep it for later).

You don't need to write version numbers — the next step figures those out for you.

### Step 3: Let `uv` work out the exact versions

Open a terminal in the repository folder and run:

```sh
uv init --bare      # only needed the very first time
uv add --bounds exact -r requirements.in
```

This checks that all the packages you listed actually work together, and writes
the result into two files that you don't need to edit by hand:

- `pyproject.toml` — the exact version of each package you asked for in
  `requirements.in` (e.g. `pandas==2.3.3`), so the choice is recorded and won't
  silently change later.
- `uv.lock` — every other package those packages depend on internally, also
  pinned to an exact version, so the same complete set can be reproduced
  identically on any computer.

Together they're the "recipe" that `uv run` (step 5) and the CBS export (step 4)
both read from.

If this command fails with an error, see "Advanced configuration" below — most
failures come from specific packages (PyTorch Geometric, flash-attn, etc.) that
need a bit of extra setup in `pyproject.toml`.

### Step 4: Create the file to send to CBS

CBS RA runs Windows, so generate a Windows-specific version of the package list:

```sh
uv pip compile pyproject.toml --python-version 3.12 --python-platform windows --no-annotate --no-header -o environment0000.txt
```

Rename `environment0000.txt` so `0000` matches your project number. This file can
be installed with plain `pip` (no `uv` needed), which is what CBS RA will do.
Email it to CBS as described in the "Creating a Custom Python Environment" section
above.

### Step 5: Use the same packages on your own computer

```sh
uv run jupyterlab
```

`uv run <command>` runs any command (Jupyter, a script, etc.) using exactly the
packages you listed, installing anything missing automatically. This way, what you
test on your own computer matches what you'll have access to in CBS RA.

---

## Advanced configuration

A few packages need extra settings in `pyproject.toml`, added by hand, before
`uv add` / `uv lock` / `uv pip compile` will work. These settings only need to
be added once — after that, steps 3 and 4 above work normally.

### Packages installed from a URL instead of the normal package index

Some packages aren't on the normal package index and need to be installed from
a URL instead — for example the PyTorch Geometric (PyG) wheels used by
`pyg-lib`, `torch-sparse`, etc. Add the URL under `[tool.uv]` (used by `uv add`
and `uv lock`) and under `[tool.uv.pip]` (used by `uv pip compile`):

```toml
[tool.uv.pip]
find-links = ["https://data.pyg.org/whl/torch-2.9.0+cpu.html"]
emit-find-links = true
```

- `[tool.uv] find-links` makes `uv add`/`uv lock` (step 3) look at that URL.
- `[tool.uv.pip] find-links` makes `uv pip compile` (step 4) look at that URL.
  Both are needed — they're read by different commands.
- `emit-find-links = true` makes `uv pip compile` write the `--find-links`
  line at the top of the generated `environment0000.txt`. That way, whoever
  installs that file with plain `pip install -r environment0000.txt` (e.g.
  CBS RA) automatically knows where to find these packages too — without it,
  `pip` would fail to find them.

If you don't add this, `uv` may report that no matching version exists for a
package, even though it's listed correctly in `requirements.in`.

### Packages that fail to build with "ModuleNotFoundError: No module named 'torch'"

Some packages (e.g. `torch-cluster`, `torch-scatter`, `torch-sparse`,
`torch-spline-conv`, `flash-attn`) are compiled from source, and their build
script imports `torch` without declaring it as something it needs in order to
build — so `uv` builds them in a clean environment that doesn't have `torch`
yet, and the build fails with `ModuleNotFoundError: No module named 'torch'`.

The error message includes the fix. Add the affected package(s) under
`[tool.uv.extra-build-dependencies]` in `pyproject.toml`:

```toml
[tool.uv.extra-build-dependencies]
flash-attn = ["torch"]
torch-sparse = ["torch"]
torch-scatter = ["torch"]
torch-cluster = ["torch"]
torch-spline-conv = ["torch"]
```

This tells `uv` to install `torch` into the temporary build environment first,
so the package's build script can find it. Without this, both `uv add` and
`uv pip compile` fail with the same error.
