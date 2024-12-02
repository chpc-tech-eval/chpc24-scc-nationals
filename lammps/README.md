LAMMPS
===========

[LAMMPS](https://docs.lammps.org) is a highly flexible, open-source molecular dynamics software used for simulating particles in a variety of systems, from metals and polymers to granular materials. The Polymer chain melt benchmark evaluates the performance of LAMMPS in simulating polymer dynamics and helps gauge computational resource utilization.

# Installation
Follow the general installation instructions.

## System Requirements
LAMMPS requires a functioning C++ compiler and libraries like MPI for parallel processing. Below is a table of recommended minimum software versions:

| Program  | Version | Description                                |
| ---      |     --- | ---                                        |
| gcc      |   7.5 | Higher version recommended                 |
| cmake    |     3.10 | Required for building LAMMPS    |
| MPI      |    3.0 | Required for parallel computations|
| FFTW     |   3.3.8 | Required for FFT operations|
| Python   |   3.x | Optional, for running Python scripts                |

## Downloading the Source Code
Download LAMMPS from the [LAMMPS official website](https://docs.lammps.org/Install.html) either as a tarball or from git:

### Download source as a tarball

```bash
wget https://download.lammps.org/tars/lammps-29Aug2024_update1.tar.gz
```
Unpack the source files to your installation directory:
```bash
tar -xzf lammps-29Aug2024_update1.tar.gz
```


### Download source with git

```bash
git clone https://github.com/lammps/lammps.git
cd lammps
git checkout stable_29Aug2024_update1
```

## Building and Deploying LAMMPS
After downloading, navigate to the source directory and compile with desired options (e.g):

```bash
cd stable_29Aug2024_update1
mkdir build
cd build
cmake ../cmake -D BUILD_MPI=ON -D BUILD_OMP=ON
make -j <N>
```

### Verification
Run a test case to verify the installation by running the benchmark in serial mode:

```bash
cd ../bench
../build/lmp -in in.lj
```

# Benchmark 1: Polymer Chain Melt
The Polymer chain melt benchmark input file should be in the benchmark folder (bench) :


Edit and configure the input simulation file (in.chain) :

```config
units       lj
atom_style  molecular
pair_style  lj/cut 2.5
```
Set the number of OMP threads

```bash
export OMP_NUM_THREADS= <num_threads>
```

Run the benchmark in parallel mode:

```bash
mpirun -np <CORES> ../build/lmp -in in.chain > parallel-output-<CORES>.out
```
Repeat the benchmark in parallel mode with different configurations to study performance scaling:

```bash
mpirun -np <CORES> ../build/lmp -in in.chain > parallel-output-<CORES>.out
```

Collect run times and analyze results across different core counts, should have no less than 5 set of results.

| MPI Ranks | Ranks Per Node | Threads/Rank | RAM Usage Per Node | Run Time |
|             --- |            --- |          --- | ---                | ---      |
|               2 |              1 |          8   | ???                | ???      |
|          etc... |            ... |          ... | ...                | ...      |


# Benchmark 2: Larger Polymer System
Repeat the setup with a larger polymer chain to benchmark LAMMPS in a higher-load scenario.

Edit and configure the input simulation file (in.chain.scaled) :

```config
units       lj
atom_style  molecular
pair_style  lj/cut 2.5
```

Run the domain decomposition:
```bash
$ mpirun -np <MPI PARAMETERS> ./lmp -var x 8 -var y 8 -var z 8 -in in.chain.scaled > large-output.out
```

Collect run times and analyze results across different core counts, should have no less than 5 set of results.

| MPI Ranks | Ranks Per Node | Threads/Rank | RAM Usage Per Node | Run Time |
|             --- |            --- |          --- | ---                | ---      |
|               2 |              1 |          8   | ???                | ???      |
|          etc... |            ... |          ... | ...                | ...      |



# Visualization

Use tools like [OVITO](https://www.ovito.org/) for visualizing the polymer dynamics from the output files. 

Add this line to the LAMMPS input file to generate a dump file in LAMMPS
```bash
dump 1 all atom 100 dump.lammps
```

SSH copy the output file to the destination where it will be visualized 

```bash
scp <username>@<remote_host>:<path_to_remote_file> <path_to_local_destination>
```

# Submission

Submit your `parallel-output.out` for your best result, the table with the results from the performance scaling,  an executable binary and from the visualisation, a screenshot of the visualization for both benchmark 1 and 2.
