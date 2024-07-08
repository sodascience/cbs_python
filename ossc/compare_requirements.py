"""Compare the requirements of the requirements in the OSSC with the requirements of the "main" environment000.txt file in the repository root
"""

import argparse
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


def check_overlap(ra: dict, snellius: dict, dest_file):
    "Check overlap between requirements on RA and snellius."

    overlap = [x for x in ra.keys() if x in snellius.keys()]
    d_overlap = []
    for package_name in overlap:
        record = {}
        record["pkg_name"] = package_name
        record["version_ra"] = ra.get(package_name)
        record["version_snellius"] = snellius.get(package_name)
        d_overlap.append(record)

    d_overlap = pd.DataFrame.from_records(d_overlap)

    d_overlap.to_csv(dest_file, index=None)


def extract_packages(input_requirements: list):
    "From a list of requirements, extract package name and versions"
    output = {}
    for line in input_requirements:
    # for line in lines.get("snellius"):
        if "@" in line:
            name, url = line.split(" @ ")
            try:
                pkg_version = url.split("/")[-1]
                pattern = r'\d+\.\d+\.\d+|\d+\.\d+'
                result = re.search(pattern, pkg_version)
                version = result.group(0)
                output[name] = version
            except AttributeError:
                print("Could not find version for ", url)
                output[name] = None
        elif "==" in line:
            name, version = line.split("==")
            output[name] = version
        else:
            print("failed for", line)

    return output



def main(source_url: str):
    urls = {
        "ra": "environment0000.txt",
        "snellius": source_url
    }
    outfile_missing = "ossc/snellius_missing.txt"
    outfile_versions = "ossc/version_comparison.csv"

    lines = {name: read_lines(url) for name, url in urls.items()}

    ra = {}

    for line in lines.get("ra"):
        name, version = line.split("==")
        ra[name] = version
        # ra.append((name, version))

    snellius = extract_packages(lines.get("snellius"))

    snellius_missing = [x for x in ra.keys() if x not in snellius.keys()]
    write_lines(outfile_missing, snellius_missing)

    check_overlap(ra, snellius, outfile_versions)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--ossc_src', type=str,
            default="ossc/requirements_ossc.txt",
            help="The snellius/OSSC requirements to compare with the environment0000.txt at repository root.")


    args = parser.parse_args()

    main(args.ossc_src)

