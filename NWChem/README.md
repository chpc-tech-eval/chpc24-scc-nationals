NWChem 
=====

NWChem is an open-source, high performance, computational chemistry suite of software tools, that are scalable in both their ability to efficiently treat large scientific problems, as well as in their use of available computing resources, from consumer laptops to high-performance parallel supercomputers. NWChem uses MPI for parallelism, usually hidden by the Global Arrays programming model, which implements one-sided communication to support a data-centric abstraction of multidimensional arrays across shared and distributed memory protocols. See NWChem documentation for a complete overview **https://nwchemgit.github.io/Home.html**

# Installation

## Setup outline

1. Your choice of **Compiler** and **MPI**.
2. Math Library (**BLAS, LAPACK and SCALAPACK**).
3. Export Environment variables.
4. You are required to build and use ARMCI-MPI.
5. Build NWChem and generate an executable binary.
6. Run a test benchmark using MPI.


### Obtaining the source code

 NWChem’s source and corresponding tools can be obtained from GitHub:

 - **master** 
```bash
    $ git clone https://github.com/nwchemgit/nwchem.git
    $ cd nwchem/src/tools && ./get-tools-github
```

- **7.2.3 Release** 

```bash
    $ git clone  -b hotfix/release-7-2-0 https://github.com/nwchemgit/nwchem.git nwchem-7.2.3
    $ cd nwchem-7.2.3/src/tools && ./get-tools-github
```

- **7.2.2 Release**
```bash
    $ git clone  -b hotfix/release-7-2-0 https://github.com/nwchemgit/nwchem.git nwchem-7.2.2
    cd nwchem-7.2.2/src/tools && ./get-tools-github
```

Choose your prefered release

### use the hotfix/release-7-2-0 branch

The `master` branch may not be well maintained. For that reason you should checkout to the `hotfix/release-7-2-0` branch:
```bash
$ cd nwchem
$ git checkout hotfix/release-7-2-0
```

Detailed instructions and explaination of building, compiling and installing NWChem can be found here ***https://nwchemgit.github.io/Compiling-NWChem.html.***

### load appropriate modules 

```bash
module load path/to/gcc 
```

### The following environment variables need to be set
```bash
$ cd nwchem(-7.2.x)
$ git checkout hotfix/release-7-2-0
$ export NWCHEM_TOP=/path/to/git/clone/nwchem
$ export NWCHEM_TARGET=LINUX64
$ export ARMCI_NETWORK=MPI-PR
$ cd cnwchem/src/tools
$ ./install-armci-mpi
```

### To compile, use the ff commands
1. **Ensure to set the env. variable USE_MPI and provide a working MPI installation**
2. **Redirect `make` output to a log file**

```bash
$ cd cnwchem/src
$ make nwchem_config
$ make -j<Num_Procs> >& make_logfile.log
```


### sample build script for NWChem application on LENGAU:

```bash

#!/bin/bash
##########################################################
# 		Dr Krishna Govender			 #
# Compile script for NWChem 7.2.2 on LENGAU              #
# 		20 Nov 2023				 #
##########################################################
# Load appropriate modules
module purge
module load gcc/7.3.0
module load chpc/openmpi/4.0.0/gcc-7.3.0
module load chpc/cmake/3.17.0/gcc-7.3.0
module load chpc/python/anaconda/3-2021.11
# Set various environment variables 
export NWCHEM_TOP=/apps/chpc/chem/nwchem/7.2.2
export NWCHEM_TARGET=LINUX64
export LARGE_FILES="TRUE"
export USE_NOFSCHECK="TRUE"
export USE_NOIO="TRUE"
export USE_MPI=y
export USE_MPIF=y
export USE_MPIF4=y
export MSG_COMMS=MPI
export USE_PYTHONCONFIG=y
export USE_64TO32=y
export PYTHONHOME=/apps/chpc/chem/anaconda3-2021.11
export PYTHONVERSION=3.9
export USE_PYTHON64=y
export NWCHEM_MODULES="pnnl"
export ARMCI_NETWORK=MPI-PR
export BUILD_OPENBLAS="TRUE"
export BUILD_SCALAPACK="TRUE"
export BLAS_SIZE=4
export SCALAPACK_SIZE=4
export MRCC_METHODS="TRUE"
# Run make
pushd $NWCHEM_TOP/src
make realclean
make nwchem_config >& make_config.log
make 64_to_32 >& make_64to32.log
make -j12 FC=gfortran CC=gcc CXX=g++ >& make_compile.log
popd
```
