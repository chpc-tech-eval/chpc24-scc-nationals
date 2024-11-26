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

### install required dependancies 
- make sure you have essential libraries like  **BLAS, LAPACK, LAPACK and SCALAPACK** 

```bash
sudo dnf groupinstall "Development Tools"
sudo dnf install gcc g++ gfortran make cmake libtool automake 
sudo dnf install blas-devel lapack-devel openblas-devel fftw-devel mkl-devel libxml2-devel zlib-devel
```
Here’s what each package provides:

- **Development Tools:** Includes compilers, debuggers, and other utilities needed to build software.
- **GCC, GFortran:** For compiling C and Fortran code.
- **Make, CMake, Automake:** Build tools.
- **OpenBLAS, FFTW, MKL:** Math libraries, which are often used for high-performance calculations in scientific software.
- **libxml2-devel:** XML parsing library.


### Obtaining the source code

 NWChem’s source and corresponding tools can be obtained from GitHub, please choose 7.2.2 release:
```bash
git clone  -b hotfix/release-7-2-0 https://github.com/nwchemgit/nwchem.git nwchem-7.2.2
cd nwchem-7.2.2/src/tools && ./get-tools-github
```

### The following environment variables need to be set atleast
- Ensure gcc, gfortran, g++  compilers are installed 
-  Add the following environment variables to your ~/.bashrc or ~/.bash_profile file
- If NWChem is not installed through modules, you may need to ensure the environment variables (such as PATH and LD_LIBRARY_PATH) are set correctly to locate the NWChem executable.

```bash
cd nwchem-7.2.2
export NWCHEM_TOP=/path/to/git/clone/nwchem
export NWCHEM_TARGET=LINUX64
export ARMCI_NETWORK=MPI-PR
export USE_MPI=/path/to/MPI 
export FC=gfortran 
export CC=gcc 
export CXX=g++
export PATH=$NWCHEM_TOP/path/to/bin
export LD_LIBRARY_PATH=$NWCHEM_TOP/path/to/gcc-compiler/lib  
cd cnwchem/src/tools
./install-armci-mpi
```

- Note: For NWChem dependencies, the paths to the libraries of these dependencies must be included in the `LD_LIBRARY_PATH`.

```bash
#example 

export LD_LIBRARY_PATH=$DIR/grib2/lib:/apps/compilers/intel/parallel_studio_xe_2018_update2/compilers_and_libraries_2018.2.199/linux/compiler/lib/intel64_lin:$DIR/netcdf/lib:$DIR/pnetcdf/lib:$LD_LIBRARY_PATH
```

**OR**

### Load appropriate modules 
- first create a module file before loading it. 

```bash
module load path/to/gcc 
```

### To compile, use the following commands
- Ensure to set the env. variable USE_MPI and provide a working MPI installation.
- Redirect `make` output to a log file.

```bash
cd cnwchem/src
make nwchem_config
make -j<Num_Procs> >& make_logfile.log
```

Detailed instructions and explainations of building, compiling and installing NWChem can be found here ***https://nwchemgit.github.io/Compiling-NWChem.html.***


## Density functional calculation of a zeolite fragment
This section is about finding the benchmark results with NWChem 7.2.0 for LDA calculations (energy plus gradient) on a 533 atoms siosi8 zeolite fragment. The input uses an atomic orbital basis set with 7108 functions and a charge density fitting basis with 16501 functions. 

### Input file 
The input file can be downloaded on this link **https://nwchemgit.github.io/benchmarks/siosi8.nw** 

Submit your output energy calculation results including wall time (s) to the judges. 

Run the application within a 2hr walltime across at your nodes

### set environment variaable/PATHS 

If NWChem is not installed through modules, you may need to ensure the environment variables (such as PATH and LD_LIBRARY_PATH) are set correctly to locate the NWChem executable.

### Run the benchmark
- Run NWChem with your input file 

```bash
mpirun -np 10 nwchem input.nw > output.log &   # where 10 = number of CPUs
disown -h 

```

### Analyze your ouput 
```bash
cat output.log
```
 


