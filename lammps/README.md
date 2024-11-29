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


### Downlaod source with git

```bash
git clone https://github.com/lammps/lammps.git
cd lammps
git checkout stable_29Aug2024_update1
```

## Building and Deploying LAMMPS
After downloading, navigate to the source directory and compile with desired options:

```bash
cd stable_29Aug2024_update1
mkdir build
cd build
cmake ../cmake -D BUILD_MPI=ON -D BUILD_OMP=ON
make -j <N>
```

### Verification
Run a test case to verify the installation:

```bash
cd ../bench
mpirun -np 4 ../build/lmp -in in.lj
```

# Benchmark 1: Polymer Chain Melt (Serial)
Copy the Polymer chain melt benchmark file from the benchmark folder:

```bash
$ cp /path/to/PolymerChainMeltBenchmark.tar.gz ~/<path to benchmark>
```

Extract and configure the simulation files. Edit input files to set up a single-core test:

```config
units       lj
atom_style  molecular
pair_style  lj/cut 2.5
```
Run the benchmark in serial mode:

```bash
$ ./lmp -in in.polymer_chain_melt > serial-output.out
```

# Benchmark 1: Parallel Efficiency Investigation
Repeat the benchmark in parallel mode to study performance scaling:

```bash
$ mpirun -np <CORES> ./lmp -in in.polymer_chain_melt > parallel-output-<CORES>.out
```

Collect run times and analyze results across different core counts.

| MPI Ranks | Ranks Per Node | Threads/Rank | RAM Usage Per Node | Run Time |
|             --- |            --- |          --- | ---                | ---      |
|               4 |              1 |            8 | ???                | ???      |
|               8 |              2 |            4 | ???                | ???      |
|              16 |              4 |            2 | ???                | ???      |
|          etc... |            ... |          ... | ...                | ...      |

# Benchmark 1: Visualization

Use tools like [OVITO](https://www.ovito.org/) for visualizing the polymer dynamics from the output files. 

# Benchmark 2: Larger Polymer System
Repeat the setup with a larger polymer chain to benchmark LAMMPS in a higher-load scenario.

Run the domain decomposition:
```bash
$ mpirun -np <MPI PARAMETERS> ./lmp -in in.large_polymer_chain_melt > large-output.out
```

