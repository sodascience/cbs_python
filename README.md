## Configuring Python in CBS Remote Access (RA)

**Python is not installed by default at CBS RA (yet).** To activate Python, contact the CBS microdata team at [`microdata@cbs.nl`](mailto:microdata@cbs.nl).

### Default Python Packages

By default, some packages are available in Python at CBS RA, such as `pandas`, `pyreadstat` or `matplotlib`

If you require additional packages or specific versions, follow the steps below to create and submit your own Python environment.

---

### Creating a Custom Python Environment

Follow these instructions to set up and submit a customized Python environment. You need to use a **Windows** computer.

#### Step 1: Check Existing Environment

- Check if `environment0000.txt` (replace `0000` with your actual project number) already contains the required packages and suitable versions.
- **If yes:** Send this file directly to CBS.
- **If no:** Continue to Step 2.

#### Step 2: Create the Environment (Windows + Conda)

Install conda locally (only needed if you do not already have Conda installed):
- Follow the official Conda installation instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation).
- If you're unfamiliar with command-line tools, consider installing [Anaconda](https://www.anaconda.com/products/individual) instead.

On your local Windows machine:

```sh
conda create -n 0000 python
conda activate 0000
conda install pip
pip install package_name
```

Replace `package_name` with the packages you need (e.g., `pip install numpy`). If you want to install all the packages in the requirements.txt file in this repository, use `pip install -r requirements.txt`

**Note:** If using Jupyter Notebook or Spyder, install these explicitly, e.g.:

```sh
pip install jupyter spyder
```

#### Step 3: Export the Environment

Export the environment into a requirements file:

```sh
pip freeze > C:\temp\environment0000.txt
```

Check `environment0000.txt` for local paths (`file://`). If found, regenerate using:

```sh
pip list --format=freeze > C:\temp\environment0000.txt
```

#### Step 4: Verify Environment

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

## Using Python at CBS RA

We recommend to use Python through Visual Studio Code (VS Code), installed by default:

- In VS Code, select the Python interpreter in the bottom-right corner of the editor.

You could also use Python through Jupyter in RA, for that, open an Anaconda terminal in the RA and run:

```sh
conda activate 0000
jupyter notebook --notebook-dir=H:
```

This opens Jupyter in your shared directory (`H:`).

---

## Support & Contact

This documentation is maintained by the [ODISSEI Social Data Science (SoDa)](https://odissei-data.nl/nl/soda/) team.

For technical questions or suggestions:

- File an issue in the project's issue tracker, or
- Contact [Javier Garcia-Bernardo](https://github.com/jgarciab).
