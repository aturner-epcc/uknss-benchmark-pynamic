#!/usr/bin/env python3

import re
import sys

EXPECTED_VERSION = "1.3.3"

if len(sys.argv) != 2:
    print("validate.py: test output correctness and extract timings for the UK-NNSS Pynamic benchmark.")
    print("Usage: validate.py <pynamic-stdout>")
    sys.exit(1)

with open(sys.argv[1], "r") as f:
    text = f.read()

print("\n# Pynamic benchmark validation")

version_match = re.search(r"Pynamic:\s+Version\s+([0-9.]+)", text)
mpi_match     = re.search(r"with\s+(\d+)\s+MPI tasks", text)
import_match  = re.search(r"module import time = ([0-9.]+)", text)
visit_match   = re.search(r"module visit time = ([0-9.]+)", text)

# Validate version
if not version_match:
    print("\n  Validation: FAILED")
    print()
    print("  Error: Could not find Pynamic version.")
    sys.exit(1)

version = version_match.group(1)

if version != EXPECTED_VERSION:
    print("\n  Validation: FAILED")
    print()
    print(f"  Error: Expected Pynamic version {EXPECTED_VERSION}, found {version}.")
    sys.exit(1)

if not mpi_match:
    print("\n  Validation: FAILED")
    print()
    print("  Error: Could not find MPI task count.")
    sys.exit(1)

if not import_match or not visit_match:
    print("\n  Validation: FAILED")
    print()
    print("  Error: Could not find required timing information.")
    sys.exit(1)

mpi_tasks   = int(mpi_match.group(1))
import_time = float(import_match.group(1))
visit_time  = float(visit_match.group(1))

total_time  = import_time + visit_time

print()
print(f"  Pynamic version     : {version}")
print(f"  MPI tasks           : {mpi_tasks}")

print("\n  Validation: PASSED")
print()
print(f"  Module import time : {import_time} secs")
print(f"  Module visit time  : {visit_time} secs")
print(f"  Total time         : {total_time} secs")
print()
