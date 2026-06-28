## Configuring Python in CBS Remote Access (RA)

**Python is not installed by default at CBS RA (yet).** To activate Python, contact the CBS microdata team at [`microdata@cbs.nl`](mailto:microdata@cbs.nl).

### Default Python Packages

By default, some packages are available in Python at CBS RA, such as `pandas`, `pyreadstat` or `matplotlib`

If you require additional packages or specific versions, follow the steps below to create and submit your own Python environment. UV is able to create a library of dependencies that can run on multiple OS. However, to install dependencies specifically for Windows follow the next steps.

---

### Creating a Custom Python Environment

Follow these instructions to set up and submit a customized Python environment. You need to use a **Windows** computer.

#### Step 1: Check Existing Environment

- Check if `environment0000.txt` (replace `0000` with your actual project number) already contains the required packages and suitable versions.
- **If yes:** Send this file directly to CBS.
- **If no:** Continue to Step 2.

#### Step 2: Create the Environment (Windows + UV)

Install UV locally (only needed if you do not already have UV installed):
- Follow the official UV installation instructions [here](https://docs.astral.sh/uv/getting-started/installation/).


On your local Terminal machine:

If the project has not been initialized with uv then write the
next command in your machine terminal:

```sh
uv init --python python_version
```

If the project requires to run the code outside the RA environment then it is possible to select on which OS the code should run.

in the pyproject.toml file insert the following lines:

[tool.uv]
environments = [
    "sys_platform == 'win32'",
    "sys_platform == 'darwin' and platform_machine == 'arm64'",
]

It is possible to add more OS system

[tool.uv]
environments = [
    "sys_platform == 'win32'",
    "sys_platform == 'linux'",
    "sys_platform == 'darwin' and platform_machine == 'arm64'",
]


To add a package
```sh
uv add package_name
```


Aternatively If you want to install all the packages in the requirements.txt file in this repository, use `uv add --bounds exact -r requirements_base.txt` this command will pin the exact dependency version

**(to be updated with uv)Note:** If using Jupyter Notebook or Spyder, install these explicitly, e.g.:

```sh
pip install jupyter spyder
```

#### Step 4: Export the Environment (Windows + UV)

Export the environment into a requirements file:

```sh
uv pip compile requirements_base.txt --python-version 3.12 --python-platform windows --no-annotate --no-header -o environment0000.txt
```

Aternatively If you want to export a requirement.txt that contains dependencies for different platforms use
```sh
uv export --format requirements-txt --no-hashes --no-header --no-annotate --no-emit-project --python 3.12 |
  ForEach-Object { ($_ -split ';')[0].TrimEnd() } |
  Set-Content -Encoding ascii environment_9424.txt
```


#### (update with UV)Step 4: Verify Environment

Validate your environment by removing and recreating it:

```sh
conda remove -n 0000 --all
conda create -n 0000 
conda activate 0000
conda install pip
pip install -r C:\temp\environment0000.txt
```

Test thoroughly before submission by running python and importing your packages one by one.

#### Step 5: Submit Your Environment

Send your verified `environment0000.txt`  (replace 0000 by your project number) to CBS via email.



---

## (update with UV) Using Python at CBS RA 

We recommend to use Python through Visual Studio Code (VS Code), installed by default:

- In VS Code, select the Python interpreter in the bottom-right corner of the editor.

You could also use Python through Jupyter in RA, for that, open an Anaconda terminal in the RA and run:

```sh
conda activate 0000
jupyter notebook --notebook-dir=H:
```

This opens Jupyter in your shared directory (`H:`).

---

## Contact

This documentation is maintained by the [ODISSEI Social Data Science (SoDa)](https://odissei-data.nl/nl/soda/) team.

For technical questions or suggestions:

- File an issue in the project's issue tracker, or
- Contact [Javier Garcia-Bernardo](https://github.com/jgarciab).
