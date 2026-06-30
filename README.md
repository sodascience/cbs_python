## What this is for

CBS Remote Access (RA) only lets you use Python packages that CBS has approved and installed in advance. To get a package approved, you submit a file pip requirements.txt file listing exactly which packages (and versions) you need, and CBS installs them for you.

This repository helps you build that file correctly, without needing to understand Python packaging in depth. You will:

0. Install a tool called `uv` that does the hard work for you.
1. Download this repository to your computer.
2. Write down which packages you want, in a simple text file (`requirements.in`).
3. Run one command that turns that list into a ready-to-send file (`environment0000.txt`).
4. Test that file on your own computer before sending it (optional, but recommended).
5. Send the file to CBS through microdata.cbs.nl
6. Optionally, set up the same packages on your own computer so you can work locally too.

You only need to follow these steps once per project (and again whenever you want to add or remove a package).

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

CBS RA runs Windows, so generate a Windows-specific version of the package list. Open a terminal in the repository folder and run:

```sh
uv pip compile requirements.in --python-version 3.12 --python-platform windows --no-annotate --no-header --emit-find-links -o environment0000.txt
```

`--emit-find-links` is needed because some packages (e.g. the PyTorch Geometric
ones) aren't on the normal package index — `requirements.in` points `pip` at
an extra URL for those via a `--find-links` line, and this flag copies that
line into `environment0000.txt` so the file still works when installed on its
own with plain `pip`, without `requirements.in` alongside it.

Rename `environment0000.txt` so `0000` matches your project number. This file can
be installed with plain `pip` (no `uv` needed), which is what CBS RA will do.

### Step 4: Test that it works in your own Windows computer [optional, highly recommended]

Before sending the file to CBS, test it in a fresh, empty environment (a
"venv"). This catches problems early, while you can still fix them. The
easiest way is with `uv`, which creates the venv and installs into it without
needing to activate anything:

```sh
uv venv ~/.venvs/cbs-test
uv pip install -r environment0000.txt --python ~/.venvs/cbs-test
```

If this finishes without errors, the file is ready to send. You can also run
`check_environment.py`, which goes through every package in `requirements.in`
and checks that it actually imports and reports a version (not just that it
installed):

```sh
uv run --python ~/.venvs/cbs-test python check_environment.py
```

When you're done testing, delete the test environment:

```sh
rm -rf ~/.venvs/cbs-test
```

(If you want to test with plain `pip` instead — closer to exactly what CBS
will run — replace the two `uv` commands above with `python -m venv ~/.venvs/cbs-test`,
then activate it with `~/.venvs/cbs-test/Scripts/activate` on Windows or
`source ~/.venvs/cbs-test/bin/activate` on Mac/Linux, and run
`pip install -r environment0000.txt`.)

### Step 5: Send environmnet000.txt to CBS

Send it to CBS through microdata.cbs.nl and ask them to activate Python in your project and install the environment.

### Step 6 [optional]: Work on your own non-Windows computer

The environment created in Step 3 is locked to Windows
(`--python-platform windows`), so it won't install on macOS or Linux. To work
locally on a non-Windows computer, compile a second file for your own
platform — just drop `--python-platform windows` so `uv` resolves wheels for
whatever computer you're actually running on:

```sh
uv pip compile requirements.in --python-version 3.12 --no-annotate --no-header --emit-find-links -o environment_local.txt
uv venv ~/.venvs/cbs-python
uv pip install -r environment_local.txt --python ~/.venvs/cbs-python
```

This creates a real environment (not a throwaway test one like Step 4), so
you can use it for actual work:

```sh
uv run --python ~/.venvs/cbs-python jupyterlab
```

`uv run <command>` runs any command (Jupyter, a script, etc.) using that
environment, installing anything missing automatically. You can also run
`uv run --python ~/.venvs/cbs-python python check_environment.py` here to
double-check everything imports correctly on your own machine.
