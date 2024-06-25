
import re 
import pandas as pd

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
outfile_missing = "ossc/snellius_missing.txt"
outfile_versions = "ossc/version_comparison.csv"

lines = {name: read_lines(url) for name, url in urls.items()}

ra = {}
snellius = {}


for line in lines.get("ra"):
    name, version = line.split("==")
    ra[name] = version
    # ra.append((name, version))


for line in lines.get("snellius"):
    if "@" in line:
        name, url = line.split(" @ ")
        try:
            pkg_version = url.split("/")[-1]
            pattern = r'\d+\.\d+\.\d+|\d+\.\d+'
            result = re.search(pattern, pkg_version)
            version = result.group(0)
            snellius[name] = version
        except AttributeError:
            print("Could not find version for ", url)
            snellius[name] = None
    elif "==" in line:
        name, version = line.split("==")
        snellius[name] = version
    else:
        print("failed for", line)




# packages = {
#     "ra": [x[0] for x in ra],
#     "snellius": [x[0] for x in snellius]
# }

overlap = [x for x in ra.keys() if x in snellius.keys()]
snellius_missing = [x for x in ra.keys() if x not in snellius.keys()]

write_lines(outfile_missing, snellius_missing)


d_overlap = []
for p in overlap:
    record = {}
    record["pkg_name"] = p 
    record["version_ra"] = ra.get(p)
    record["version_snellius"] = snellius.get(p)
    d_overlap.append(record)

d_overlap = pd.DataFrame.from_records(d_overlap)

d_overlap.to_csv(outfile_versions, index=None)

print(f"missing packages are in {outfile_missing}; package comparisons are in {outfile_versions}")