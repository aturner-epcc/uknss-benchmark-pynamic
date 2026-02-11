#!/bin/bash
#SBATCH --job-name=pynamic
#SBATCH --exclusive
#SBATCH --nodes=8
#SBATCH --time=00:30:00
#SBATCH --gpus-per-node=4
#
PYNAMIC_DIR=/projects/u6cb/benchmarks/Pynamic/pynamic-2.6a1

module load craype-network-ofi
module load PrgEnv-gnu 
module load gcc-native/13.2 
module load cray-mpich
module load craype-arm-grace
module load cray-python

export LD_LIBRARY_PATH=$PYNAMIC_DIR:$LD_LIBRARY_PATH

srun ${srunopts} --nodes=8 --ntasks=32 --cpus-per-task=72 \
     ${PYNAMIC_DIR}/pynamic-mpi4py `date +%s`


