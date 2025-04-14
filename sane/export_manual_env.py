import yaml
import subprocess
import json
from pathlib import Path

# === Step 1: Load packages from original environment.yml ===
with open("environment.yml", "r") as f:
    env_data = yaml.safe_load(f)

original_packages = set()
for dep in env_data.get("dependencies", []):
    if isinstance(dep, str):
        pkg_name = dep.split("=")[0].strip().lower()
        original_packages.add(pkg_name)
    elif isinstance(dep, dict) and "pip" in dep:
        for pip_pkg in dep["pip"]:
            pip_name = pip_pkg.split("==")[0].strip().lower()
            original_packages.add(pip_name)

# === Step 2: Get installed packages from current environment ===
installed = subprocess.check_output(['conda', 'list', '--json'])
installed = json.loads(installed)

installed_versions = {
    pkg['name'].lower(): f"{pkg['name']}={pkg['version']}"
    for pkg in installed if pkg['channel'] != 'pypi'
}

installed_versions_pip = {
    pkg['name'].lower(): f"{pkg['name']}={pkg['version']}"
    for pkg in installed if pkg['channel'] == 'pypi'
}

# === Step 3: Match and build new list with pinned versions ===
conda_pkgs = []
pip_pkgs = []

for name in original_packages:
    if name in installed_versions:
        conda_pkgs.append(installed_versions[name])
    elif name in installed_versions_pip:
        # Try to find pip-installed version
        try:
            version = subprocess.check_output(
                ['pip', 'show', name]
            ).decode()
            for line in version.splitlines():
                if line.startswith("Version:"):
                    pip_version = line.split(":")[1].strip()
                    pip_pkgs.append(f"{name}=={pip_version}")
                    break
        except subprocess.CalledProcessError:
            print(f"⚠️  Package not found via conda or pip: {name}")
    else:
        print(f"⚠️  Package not found via conda or pip: {name}")
# === Step 4: Write new environment.yml with pinned versions ===
precise_env = {
    "name": env_data.get("name", "precise_env"),
    "channels": env_data.get("channels", ["conda-forge"]),
    "dependencies": sorted(conda_pkgs)
}

# Ensure pip section is a dictionary under dependencies
if pip_pkgs:
    precise_env["dependencies"].append({"pip": sorted(pip_pkgs)})

# Save the file
output_path = Path("environment_precise.yml")
with output_path.open("w") as f:
    yaml.dump(precise_env, f, sort_keys=False)

print(f"✅ Saved precise environment to: {output_path.resolve()}")
