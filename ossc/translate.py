"""
Translate requirements from Snellius to regular pip

This script translates requirements from Snellius to regular pip, handling the following special cases:
- Packages that need installing from a link with `pip install -f`, such as some torch packages.
- Drops the `blist` package as resolving its installation is not considered worthwhile.
"""

import argparse
import re
from itertools import compress


# URL for finding specific torch packages
find_torch_links = "https://data.pyg.org/whl/torch-2.2.2+cu121.html"

# Packages to find using special links
pkgs_find_links = ["torch-scatter", "torch-sparse"]

# Packages to drop
pkgs_drop = ["blist"]

def read_lines(filename):
    """Read lines from a file and strip trailing whitespace."""
    with open(filename) as file:
        return [line.rstrip() for line in file]


def write_lines(filename, lines):
    """Write lines to a file."""
    with open(filename, "w") as f:
        for line in lines:
            f.write(f"{line}\n")


def parse_line(line):
    """Parse a line to determine if it should be transformed or skipped."""
    check_drop = any(pkg in line for pkg in pkgs_drop)
    if check_drop:
        return False, None

    if " @ " not in line:
        check_find_links = [pkg in line for pkg in pkgs_find_links]
        if any(check_find_links):
            pkg_name = next(compress(pkgs_find_links, check_find_links))
            return True, pkg_name

        return True, line
    else:
        return False, convert_linked_package(line)


def convert_linked_package(line):
    """Convert a package link to a regular pip requirement."""
    parts = line.split()
    assert parts[1] == "@"
    assert len(parts) == 3
    pkg, loc = parts[0], parts[2]
    pkg_version = loc.split("/")[-1]
    
    # Find version in the package URL
    pattern = r'\d+\.\d+\.\d+|\d+\.\d+'
    result = re.search(pattern, pkg_version)
    if result:
        version = result.group(0)
        return f"{pkg}=={version}"
    return None


def main(source_file, target_file):
    """Main function to read, process, and write requirements."""
    lines = read_lines(source_file)
    
    regular_requirements = [f"--find-links {find_torch_links}"]
    #snellius = [f"--find-links {find_torch_links}"]
    for line in lines:
        for_snellius, parsed_line = parse_line(line)
        if parsed_line:
            regular_requirements.append(parsed_line)
            #if for_snellius:
                #snellius.append(line)

    write_lines(target_file, regular_requirements)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
            '--from', type=str,
            dest="from_file",
            default="ossc/requirements_ossc.txt",
            help="The snellius/OSSC requireements to translate.")

    parser.add_argument(
            '--to', type=str,
            dest="to_file",
            default="ossc/environment0000.txt",
            help="The file with the 'regular' pip requirements.")

    args = parser.parse_args()

    main(args.from_file, args.to_file)

