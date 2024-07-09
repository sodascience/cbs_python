
## Virtual environments on the OSSC and on the RA together

It is important to have the *exactly* same versions on both computers. For performance reasons, it is recommended to use software from the modules as much as possible. Because modules tend to lag slightly behind the latest versions, one should first create a virtual environment on snellius, and then derive the requirements for the environment on the RA based on this. 

The following procedure allows to do this.

### Building the virtual environments

0. Access a *regular* snellius node.
1. Define software to load from snellius with `module load XYZ` in `modules.sh`. Try to have as much software as possible in this file.
2. Add more packages to `pip_requirements`. 
3. Run

    ```bash
    bash ossc/build_requirements.sh
    ```

    This command
    - loads all modules
    - creates a virtual environment and installs more packages from pip 
    - exports the exact requirements from this venv to the file defined in `OSSC_requirements`
    - translates these requirements to a "regular" requirements.txt file, defined by `RA_requirements`.
    - compares these requirements to the `environment0000.txt` defined in the repository root. (Most people can probably ignore this.)

4. Try to create the regular venv as follows
    ```bash
    declare PYTHON_VERSION=3.11.3 # this should match the Python module version from snellius
    declare RA_requirements="ossc/environment0000.txt" # match the same variable in modules.sh

    pyenv local "$PYTHON_VERSION"
    python -m venv .venv
    source .venv/bin/activate
    pip install -r "$RA_requirements"
    ```
    If this works continue to 6. Otherwise, continue with 5.
5. Iterate steps 1-4 by finding the right dependency versions. I found that moving software from `modules.sh` to `pip_requirements.txt` can help resolve dependencies.

6. Follow CBS instructions to install `environment0000.txt`

7. Give `OSSC_requirements` and `modules.sh` to SURF for installation on the OSSC. 


### Using the virtual environment on the OSSC

After SURF has installed the environment -- say it's stored under `ossc_env/` --, you should be able to use it as follows

```bash
#!/bin/bash
source modules.sh
source ossc_env/bin/activate
```