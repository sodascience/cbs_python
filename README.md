## Install Python at CBS

Python is not installed by default at the CBS RA (yet). In order to use Python you need to ask CBS (`microdata@cbs.nl`) to activate it for you. 

There are a few packages that are installed by default (e.g., pandas, pyreadstat, matplotlib). 

If you need specific versions, you need to email CBS a requirements.txt file with your requirements. This repository has a standard requirements.txt (updated in March 2025) with most of the packages that researchers use. 


To create the txt file from scratch, you need to create your own environment outside the RA environment, in Python on Windows, using Mambaforge installed in C:\mambaforge. Follow the steps below to generate a text file and send it to us via email as a reply. With the text file, we can make the environment available for you within RA.


    On your own Windows system in Python, create a new environment named after the project code and activate it. As an example, we use project code 0000.

a.       `conda create –n 0000`

b.       `conda activate 0000`

    Install pip.
        `conda install pip`

    Then, install the required packages with pip.
        `pip install package_name`

    Export the environment with pip.
        `pip freeze > C:\temp\environment0000.txt`
        Check that the file does not contain references to local paths (file://).
        If it does, use the following command:
        pip list --format=freeze > C:\temp\environment0000.txt

    Test the environment by removing and recreating it.
        `rd /q /s <path to python>\envs\0000`
        `conda create –n 0000`
        `conda activate 0000`
        `conda install pip`
        `pip install –r C:\temp\environment0000.txt`
        Test the Python environment.

    Send the environment text file to us via email.

 
Note! If you want to use Jupyter Notebook or Spyder, you need to install them in the environment as well.

## Local install instructions (miniconda)
**This step is only necessary if you don't have conda installed already**:
- Follow the instructions [here](https://conda.io/projects/conda/en/latest/user-guide/install/index.html#regular-installation). Use Anaconda if you are not comfortable with terminals (CLI).


## Use Python at CBS

We recommend using Python through Visual Studio Code (installed by default). You will need to change the Python interpreter (by clicking 

In the RA
```sh
conda activate 0000.
jupyter notebook --notebook-dir=H:
```

That will open a jupyter notebook based on your shared disk (`H:`).


## Contact
This is a project by the [ODISSEI Social Data Science (SoDa)](https://odissei-data.nl/nl/soda/) team.
Do you have questions, suggestions, or remarks on the technical implementation? File an issue in the
issue tracker or feel free to contact [Erik-Jan van Kesteren](https://github.com/vankesteren).

