NWChem 
=====

NWChem is an open-source, high performance, computational chemistry suite of software tools, that are scalable in both their ability to efficiently treat large scientific problems, as well as in their use of available computing resources, from consumer laptops to high-performance parallel supercomputers. NWChem uses MPI for parallelism, usually hidden by the Global Arrays programming model, which implements one-sided communication to support a data-centric abstraction of multidimensional arrays across shared and distributed memory protocols. See [NWChem documentation](https://nwchemgit.github.io/Home.html) for a complete overview.

NWChem’s source and corresponding tools can be obtained from GitHub, use the 7.2.2 release:
```bash
git clone  -b hotfix/release-7-2-0 https://github.com/nwchemgit/nwchem.git nwchem-7.2.2
cd nwchem-7.2.2/src/tools && ./get-tools-github
```

## Setup outline

1. Your choice of **Compiler** and **MPI**.
2. Math Library (**BLAS, LAPACK and SCALAPACK**).
3. Export Environment variables.
4. You are required to build and use ARMCI-MPI.
5. Build NWChem and generate an executable binary.
6. Run a test benchmark using MPI.

```bash
cd nwchem-7.2.2
export NWCHEM_TOP=/path/to/git/clone/nwchem
export ARMCI_NETWORK=ARMCI-MPI  
cd cnwchem/src/tools
./install-armci-mpi
cd ../
make nwchem_config
make -j<Num_Procs>
```
## Density functional calculation of a zeolite fragment
This Local Density Approximation (LDA) calculations on a 533-atom SiO-Si8 zeolite fragment, a computationally intensive task designed to evaluate the performance of high-performance computing systems. The input specifies:

- Atomic Orbital Basis Set with 7108 functions for describing electronic states.
- Charge Density Fitting Basis Set with 16,501 functions for efficient evaluation of Coulomb interactions.

The benchmark calculates both the total electronic energy and gradients (first derivatives of energy with respect to atomic positions), which are crucial for tasks like geometry optimization or molecular dynamics. Due to the large size of the system and extensive basis sets, this benchmark tests a system’s ability to handle significant computational workloads, memory requirements, and parallel efficiency. It is particularly relevant for simulating real-world materials and assessing the performance of modern HPC architectures in large-scale quantum chemistry applications.

Verify that you have a working basic installation by running the test benchmark

```bash
mpirun -np <MPI_Ranks> $NWChem_TOP/bin_armci-mpi/$DISTRO/nwchem \
$NWChem_TOP/web/benchmarks/dft/siosi3.nw
```
Once you have verified your installation, download the input file from  this link https://nwchemgit.github.io/benchmarks/siosi8.nw

Run the application across your cluster with an appropriate number of OpenMP threads.

### Submission
You are required to submit your (1) input file used for the run, (2) the nwchem binary, as well as the
output results including wall time and total energy calculations.
