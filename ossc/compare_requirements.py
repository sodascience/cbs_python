
import re 


def read_lines(filename):
    """Read lines from a file and strip trailing whitespace."""
    with open(filename) as file:
        return [line.rstrip() for line in file]
    
def write_lines(filename, lines):
    """Write lines to a file."""
    with open(filename, "w") as f:
        for line in lines:
            f.write(f"{line}\n")


urls = {
    "ra": "environment0000.txt",
    "snellius": "ossc/requirements_ossc.txt"
}
outfile = "ossc/snellius_missing.txt"

lines = {name: read_lines(url) for name, url in urls.items()}

ra = []
snellius = []


for line in lines.get("ra"):
    name, version = line.split("==")
    ra.append((name, version))


for line in lines.get("snellius"):
    if "@" in line:
        name, url = line.split(" @ ")
        try:
            pkg_version = url.split("/")[-1]
            pattern = r'\d+\.\d+\.\d+|\d+\.\d+'
            result = re.search(pattern, pkg_version)
            version = result.group(0)
            snellius.append((name, version))
        except AttributeError:
            print("Could not find version for ", url)
            snellius.append((name, None))
    elif "==" in line:
        name, version = line.split("==")
        snellius.append((name, version))
    else:
        print("failed for", line)


packages = {
    "ra": [x[0] for x in ra],
    "snellius": [x[0] for x in snellius]
}

overlap = [x for x in packages.get("ra") if x in packages.get("snellius")]
snellius_missing = [x for x in packages.get("ra") if x not in packages.get("snellius")]

write_lines(outfile, snellius_missing)

print(f"missing packages are in {outfile}")
