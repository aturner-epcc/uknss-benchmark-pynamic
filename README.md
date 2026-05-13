# UK-NNSS Pynamic Benchmark

This repository contains information on the GRID benchmark for the UK NNSS
procurement. 

> [!IMPORTANT]
> Please do not contact the benchmark or code maintainers directly with any questions. All questions must be submitted via the procurement response mechanism.

## Benchmark Overview
Pynamic is a benchmark designed to test a system's ability
to handle the Dynamic Linking and Loading requirements
of Python-based scientific applications. 
Pynamic includes a code generator that automatically
generates Python C-extension dummy codes and a glue layer
that facilitates linking and loading of the generated dynamic
modules. Pynamic is configurable, enabling modeling the static
properties of a specific code as described. It does not, however,
model any significant computations of the target.

The heart of Pynamic is a Python script that generates C files
and compiles them into shared object libraries.  Each library
contains a Python callable entry function as well as a number
of utility functions.  The user can also enable cross library
function calls with a command line argument. The Pynamic configure
script then links these libraries into the pynamic executable
and creates a  driver script to exercise the functions in the
generated libraries. The user can specify the number of libraries
to create, as well as the average number of utility functions
per library, thus tailoring the benchmark to match some application
of interest. Pynamic introduces randomness in the number of functions
per module and the function signatures, thus ensuring some
heterogeneity of the libraries and functions.

## Software

The required software is provided in this repository.

Original git repository: [https://github.com/llnl/pynamic](https://github.com/llnl/pynamic)

> [!CAUTION]
> All results submitted should be based on the version of Pynamic included
in this repository


## Building the benchmark

You must have a working installation of [mpi4py](https://mpi4py.readthedocs.io/en/stable/)
already installed to be able to install Pynamic as the Python 3 version of Pynamic requires
mpi4py.

We provide an example build process based on the process used to install on the
[IsambardAI](https://docs.isambard.ac.uk/specs/#system-specifications-isambard-ai-phase-2) system.

```bash
module load craype-network-ofi
module load PrgEnv-gnu 
module load gcc-native/13.2 
module load cray-mpich
module load craype-arm-grace
module load cray-python

./config_pynamic.py 900 1250 \
        -e -u 350 1250 -n 150 \
        --with-cc=cc --with-mpi4py -j 16
```

The `config_pynamic.py` script to configure and build the benchmark
has the following call structure:

```
config_pynamic.py <num_files> <avg_num_functions> [options] [-c <configure_options>]

              <num_files> = total number of shared objects to produce
              <avg_num_functions> = average number of functions per shared object
```

The key options to `config_pynamic.py` are:

```
      -e
              enables external functions to call across modules

      -j <num_processes>
              build in parallel with a max of <num_processes> processes

      -n <length>
              add <length> characters to the function names

      -u <num_utility_mods> <avg_num_u_functions>
              create <num_utility_mods> math library-like utility modules
              with an average of <avg_num_u_functions> functions
              NOTE: Number of python modules = <num_files> - <avg_num_u_functions>

      --with-cc=<command>
              use the C compiler located at <command> to build Pynamic modules.

      --with-mpi4py
              Build against mpi4py rather than pyMPI.  This requires the backing
              python to have the mpi4py module installed, and is default when
              building pynamic with Python3+.
```

The full set of options are documented in the
[Pynamic README](https://github.com/llnl/pynamic/blob/master/pynamic.README).


### Pre-approved code modifications

The only permitted source code modifications allowed are those that
modify the source code or build/installation files to resolve unavoidable compilation or
runtime errors. Any modifications must be fully documented (e.g., as a pull request, diff or patch file)
and reported with the benchmark results.

Bidders may make use of tools such as [Spindle](https://github.com/llnl/Spindle) to
improve performance for the benchmark if they wish.


## Running the benchmark

### Required tests

The Pynamic build for the benchmark should use the following parameters:

- `<num_files>` = 900
- `<avg_num_functions>` = 1250
- `<num_utility_mods>` = 350
- `<avg_num_u_functions>` = 1250
- `<length>` = 150
- `--with-mpi4py`

This corresponds to running `config_pynamic.py` with the following options:

```
./config_pynamic.py 900 1250 \
        -e -u 350 1250 -n 150 \
        --with-mpi4py
```

Pynamic should be run using at least 99% of the compute nodes,
and at least 1 MPI rank per NIC.

### Benchmark execution

Once Pynamic has been built, it should be launched in the usual way for any parallel
executable (e.g. using `srun` or `mpirun`).

We provide an example job submission script from runs on the
[IsambardAI](https://docs.isambard.ac.uk/specs/#system-specifications-isambard-ai-phase-2) system
in the [run](./run) directory.


## Results

### Performance results
Performance results can be extracted using the [validate.py](./validate.py) script. For example:

```bash
python3 ./validate.py example-output/isambardai-512nodes.out
 
# Pynamic benchmark validation
 
  Pynamic version     : 1.3.3
  MPI tasks           : 2048
 
  Validation: PASSED
 
  Module import time : 1.0578055381774902 secs
  Module visit time  : 10.863801717758179 secs
  Total time         : 11.921607255935669 secs
 
```

### Reference data

#### Isambard-AI (GH200)

| Nodes  | MPI Ranks | Import time (s) | Visit time (s) | Total time (s) |
|--------|-----------|----------|--------|--------|
| 128    | 512       | 0.99331  | 10.589 | 11.582 |
| 512    | 2048      | 1.0578   | 10.864 | 11.922 |

> [!NOTE]
> Values shown above have been truncated to 5 significant figures to aid readability. Please report values as given in Pynamic output.

Full output for the above configurations is provided below:
- [128 nodes, 4 MPI processes per node](example-output/isambardai-128nodes.out)
- [512 nodes, 4 MPI processes per node](example-output/isambardai-512nodes.out)


## License

This benchmark description and associated files are released under the
MIT license. 

### Pynamic License

(Pynamic is built on pyMPI.  For pyMPI licensing information, please see
pynamic-2.4a1/LICENSE.txt.  The following notice applies to the following
files: pynamic-2.4a1/addall.c, pynamic-2.4a1/config_pynamic.py,
 pynamic-2.4a1/get-symtab-sizes, pynamic-2.4a1/so_generator.py.)

COPYRIGHT AND LICENSE

Copyright (c) 2007, The Regents of the University of California. 
Produced at the Lawrence Livermore National Laboratory 
Written by Gregory Lee, Dong Ahn, John Gyllenhaal, Bronis de Supinski. 
UCRL-CODE-228991. 
All rights reserved. 
 
This file is part of Pynamic.   For details, contact Greg Lee (lee218@llnl.gov). 
 
Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met: 
 
* Redistributions of source code must retain the above copyright notice, this
list of conditions and the disclaimer below.  
* Redistributions in binary form must reproduce the above copyright notice, this
list of conditions and the disclaimer (as noted below) in the documentation and/or
other materials provided with the distribution.  
* Neither the name of the UC/LLNL nor the names of its contributors may be used
to endorse or promote products derived from this software without specific prior
written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  IN NO EVENT
SHALL THE REGENTS OF THE UNIVERSITY OF CALIFORNIA, THE U.S. DEPARTMENT OF ENERGY OR
CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
OR SERVICES;  LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE. 

ADDITIONAL BSD NOTICE

1. This notice is required to be provided under our contract with the U.S. Department of Energy (DOE).  This work was produced at the University of California, Lawrence Livermore National Laboratory under Contract No. W-7405-ENG-48 with the DOE. 
 
2. Neither the United States Government nor the University of California nor any of their employees, makes any warranty, express or implied, or assumes any liability or responsibility for the accuracy, completeness, or usefulness of any information, apparatus, product, or process disclosed, or represents that its use would not infringe privately-owned rights. 
 
3.  Also, reference herein to any specific commercial products, process, or services by trade name, trademark, manufacturer or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or the University of California.  The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or the University of California, and shall not be used for advertising or product endorsement purposes. 


## Changelog

The following changes to this document have been made since initial release:

| <div style="width:90px">Date</div> | Change |
|-----------:|--------|
| 2026-05-13 | Extracted Isambard-AI reference data into table. Added validation script. |