## What this is for

CBS Remote Access (RA) only lets you use Python packages that CBS has approved and
installed in advance. To get a package approved, you submit a file listing exactly
which packages (and versions) you need, and CBS installs them for you.

This repository helps you build that file correctly, without needing to understand
Python packaging in depth. You will:

1. Write down which packages you want, in a simple text file (`requirements.in`).
2. Run two commands that figure out the exact versions that work together.
3. Get a ready-to-send file (`environment0000.txt`) to email to CBS.
4. Use the same setup on your own computer, outside of CBS RA, while you work.

You only need to follow these steps once per project (and again whenever you want
to add a new package).

---

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

**Some packages aren't on the normal package index and need to be installed
from a URL instead** — for example the PyTorch Geometric (PyG) wheels used by
`pyg-lib`, `torch-sparse`, etc. The URL for that is kept in one place,
`pyproject.toml`, instead of in `requirements.in`:

```toml
[tool.uv.pip]
find-links = ["https://data.pyg.org/whl/torch-2.9.0+cpu.html"]
emit-find-links = true
```

- `find-links` makes `uv pip compile` (step 4) look at that URL too, so you
  don't need to pass `--find-links` again on that command.
- `emit-find-links = true` makes `uv pip compile` write the `--find-links`
  line at the top of the generated `environment0000.txt`. That way, whoever
  installs that file with plain `pip install -r environment0000.txt` (e.g.
  CBS RA) automatically knows where to find these packages too — without it,
  `pip` would fail the same way `uv` did before you added this section.

This `[tool.uv.pip]` section only applies to `uv pip compile` (step 4). If you
add a new PyG package and need to run `uv add` or `uv lock` again (step 3),
pass the same URL on the command itself:

```sh
uv add --bounds exact -r requirements.in --find-links https://data.pyg.org/whl/torch-2.9.0+cpu.html
```

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
