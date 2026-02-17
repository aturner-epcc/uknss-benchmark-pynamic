# UK-NSS Pynamic Benchmark

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

## Status

Stable

## Maintainers

[@aturner-epcc](https://github.com/aturner-epcc)

## Overview

### Software

- [Pynamic](https://github.com/llnl/pynamic)

### Architectures

- CPU: x86, Arm
- GPU: N/A

### Languages and programming models

- Programming languages: C
- Parallel models: MPI
- Accelerator offload models: N/A

## Building the benchmark

**Important:** All results submitted should be based on the version of Pynamic included
in this repository

Any modifications made to the source code and build/installation files must be 
shared as part of the bidder submission.

### Permitted modifications

The only permitted source code modifications allowed are those that
modify the source code or build/installation files to resolve unavoidable compilation or
runtime errors.

Bidders may make use of tools such as [Spindle](https://github.com/llnl/Spindle) to
improve performance for the benchmark if they wish.

### Manual build

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


## Running the benchmark


### Required Tests

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

Bidders may make use of tools such as [Spindle](https://github.com/llnl/Spindle) to
improve performance for the benchmark if they wish.

### Benchmark execution

Once Pynamic has been built, it should be launched in the usual way for any parallel
executable. For example, using Slurm `srun`, the launch line could look like for a
system with 4 NIC per node:

```
srun --hint=nomulithread --diatribution=block:block \
     --nodes=512 --ntasks-per-node=4 --cpus-per-task=72 \
     pynamic-mpi4py `date +%s`
```

We provide an example job submission script from runs on the
[IsambardAI](https://docs.isambard.ac.uk/specs/#system-specifications-isambard-ai-phase-2) system
in the [run](./run) directory.

## Reporting Results

The primary figure of merit for the Pynamic benchmark is the "module import time"
in seconds.

The bidder should provide:

- Details of any changes made to the Pynamic source code
  and modifications to any build files (e.g. configure scripts, makefiles)
- Details of the build process for the Pynamic software 
- Details on how the tests were run, including any batch job submission
  scripts and use of any additional Python performance tolls such as
  Spindle
- All output to STDOUT from the Pynamic benchmark including the 
  "module import time" figure of merit.

## Example performance data

The following example performance data is from the IsambardAI system

- [256 nodes, 4 MPI processes per node]()

## License

This benchmark description and associated files are released under the
MIT license. 

Pynamic License

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


