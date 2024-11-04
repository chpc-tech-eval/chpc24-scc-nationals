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

 NWChem’s source and corresponding tools can be obtained from GitHub, please choose 7.2.2 release:

- **7.2.2 Release**
```bash
    $ git clone  -b hotfix/release-7-2-0 https://github.com/nwchemgit/nwchem.git nwchem-7.2.2
    cd nwchem-7.2.2/src/tools && ./get-tools-github
```

### Load appropriate modules 

```bash
module load path/to/gcc 
```

### The following environment variables need to be set atleast
```bash
$ cd nwchem-7.2.2
$ export NWCHEM_TOP=/path/to/git/clone/nwchem
$ export NWCHEM_TARGET=LINUX64
$ export ARMCI_NETWORK=MPI-PR
$ cd cnwchem/src/tools
$ ./install-armci-mpi
```

### To compile, use the following commands
- Ensure to set the env. variable USE_MPI and provide a working MPI installation.
- Redirect `make` output to a log file.

```bash
$ cd cnwchem/src
$ make nwchem_config
$ make -j<Num_Procs> >& make_logfile.log
```

Detailed instructions and explainations of building, compiling and installing NWChem can be found here ***https://nwchemgit.github.io/Compiling-NWChem.html.***
