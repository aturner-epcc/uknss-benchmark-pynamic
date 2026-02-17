#!/bin/bash
#SBATCH --job-name=pynamic
#SBATCH --output=Pynamic-%j.out
#SBATCH --exclusive
#SBATCH --nodes=256
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

tasks_per_node=72
stride=4

export LD_LIBRARY_PATH=$PYNAMIC_DIR:$LD_LIBRARY_PATH

nodes=$SLURM_JOB_NUM_NODES
tasks=$(( SLURM_JOB_NUM_NODES * tasks_per_node ))

srunopts="--hint=nomultithread --distribution=block:block"

srun ${srunopts} --nodes=$nodes --ntasks=$tasks --ntasks-per-node=$tasks_per_node --cpus-per-task=$stride \
     ${PYNAMIC_DIR}/pynamic-mpi4py `date +%s`


