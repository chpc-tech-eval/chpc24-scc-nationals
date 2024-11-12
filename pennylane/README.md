Pennylane
==========

[PennyLane](https://pennylane.ai/) is a cross-platform Python library for [quantum computing](https://pennylane.ai/qml/quantum-computing/), [quantum machine learning](https://pennylane.ai/qml/quantum-machine-learning/), and [quantum chemistry](https://pennylane.ai/qml/quantum-chemistry/). Train a quantum computer the same way as a neural network.

# Installation Instructions

There are a number of ways to deploy PennyLane. You may use a package manager such as `python pip` or `conda` or Docker container:
* PyPI is the official repository for PennyLane and Lightning’s compiled binaries, and installation through pip is recommended when it is
available.
* Conda-Forge is an organization maintaining a large database of conda recipes. A so-called feedstock exists for each Lightning plugin, which
enables installing PennyLane and Lightning in Conda environments.
* Should there be one reason or another PyPI and Conda are not reliable options, it is possible to use Lightning in a Docker container. The PennyLaneAI
DockerHub account hosts a number of different images of the various Lightning plugins.

PennyLane requires Python version 3.10 and above. Installation of PennyLane, as well as all dependencies, will be done using `pip`.

## Install PyPI and JupterLab

[Project Jupyter](https://jupyter.org/) provides powerful tools for scientific investigations due to their interactive and flexible nature. Jupyter Notebooks provide a versatile and powerful environment for conducting scientific investigations, facilitating both the analysis and the clear communication of results.

1. Install all the prerequisites and dependencies
   * DNF / YUM

     ```bash
     # RHEL, Rocky, Alma, CentOS Stream
     sudo dnf install python python-pip
     ```
   * APT

     ```bash
     # Ubuntu
     sudo apt install python python-pip
     ```
   * Pacman

     ```bash
     # Arch
     sudo dnf install python python-pip
     ```
1. Create and Activate a New Virtual Environment

   Separate your python projects and ensure that they exist in their own, clean environments:
   ```bash
   python -m venv pennylane
   source pennylane/bin/activate
   ```
1. Install Project Jupyter and Plotly plotting utilities and dependencies
   ```bash
   pip install jupyterlab ipywidgets plotly jupyter-dash
   pip install aiohttp fsspec h5py
   ```
1. Start the JupyterLab server
   ```bash
   jupyter lab --ip 0.0.0.0 --port 8889 --no-browser
   ```
   * `--ip` binds to all interfaces on your head node, including the public facing address
   * `--port` bind to the port that you granted access to in `nftables`
   * --no-browser, do not try to launch a browser directly on your head node.
1. Carefully copy your `<TOKEN>` from the command line after successfully launching your JupyterLab server.
   ```bash
   # Look for a line similar to the one below, and carefully copy your <TOKEN>
   http://127.0.0.1:8889/lab?token=<TOKEN>
   ```
1. Open a browser on you workstation and navigate to your JupyterLab server on your headnode:
   ```bash
   http://<headnode_public_ip>:8889
   ```
1. Login to your JupyterLab server using your `<TOKEN>`.

> [!TIP]
> Should you have issues exposing you public facing interface to your Jupyter Lab server, remember that you can use a local SSH forwarding tunnel, between your local machine and your remote server:
>
> `ssh -N -L 8889:localhost:8889 <USER>@<HEADNODE_IP> -i ~/.ssh/<PATH_TO_SSH_KEY>`

# PennyLane Lightning-Qubit

You can install / upgrade PennyLane and `lightning.qubit` with either of the following command. All the core dependencies will be satisfied and resolved implicitly.

```bash
pip install pennylane --upgrade

# or you can explicitly install lightning, which will also pull pennylane dependencies.
# pip install penylane-lightning
```
The Lightning plugin ecosystem provides fast state-vector and tensor network simulators written in C++ `lightning.qubit` device uses a custom-built backend to perform fast linear algebra calculations for simulating quantum state-vector evolution, you can find more details about it [here]()


# Variational Quantum Eigensolver (VQE)

In this benchmark you will be reproducing the results from the recent paper published by some of Xanadu's authors [Hybrid quantum programming with PennyLane Lightning on HPC platforms](https://arxiv.org/abs/2403.02512)

Add some flavour text to explain whats going on

...

and save the following as a `lightning_qubit.py`

```python
import pennylane as qml
from pennylane import numpy as np

mol = qml.data.load("qchem", molname="H2O", bondlength=0.958, basis="STO-3G")[0]
hf_state, ham = mol.hf_state, mol.hamiltonian
wires = ham.wires
dev = qml.device("lightning.qubit", wires=wires, batch_obs=True)

n_electrons = mol.molecule.n_electrons
singles, doubles = qml.qchem.excitations(n_electrons, len(wires))

# Create the QNode
@qml.qnode(dev, diff_method="adjoint")
def cost(weights):
    qml.AllSinglesDoubles(weights, wires, hf_state, singles, doubles)
    return qml.expval(ham)

params = qml.numpy.array(np.random.normal(0, np.pi, len(singles) + len(doubles)))
opt = qml.AdagradOptimizer(stepsize=0.2)
max_iterations = 1000
energies = [np.nan]
conv_tolerance = 1e-7

# Loop until converged, or the max iterations are hit
for n in range(max_iterations):
    params, prev_energy = opt.step_and_cost(cost, params)
    energies.append(prev_energy)
    if not n % 10: # print every 10 steps
        print(f"Step={n}, energy={prev_energy}")
    if np.abs(energies[-1] - energies[-2]) < conv_tolerance:
        break

print(f"Energy={cost(params)}")
```

## Single Thread Workload [2%]

Run the benchmark using ***either*** of the following methods:
1. Pass the Python script to the `python` command in your `venv` environment
   ```bash
   # Trying to use you system's Python binary, instead of the one in your local Python Virtual Environment may result in missing library errors.

   python lightning_qubit.py
   ```
1. Make the Python script executable from directly within the Command Shell:
   * Prepend the appropriate Bash Shebang to the beginning of the script, to indicate which interpreter to use:
     ```python
     #!/<PATH-TO-YOUR-VENV-DIR>/bin/python
     ```
   * Use `chmod` to add the executable flag to the script:
     ```bash
     chmod +x lightning_qubit.py
     ```
   * Run the executable Python script:
     ```bash
     ./lightning_qubit.py
     ```

You are required to redirect and save the output to a file and should see the following output:
```bash
qchem/H2O/STO-3G/0.958/H2O_STO-3G_0.958.h5 117.38/117.38 MB
Step=0, energy=-49.25521883614754
Step=10, energy=-71.6135397945159
Step=20, energy=-73.89606868879673

...

Step=900, energy=-74.9736932457384
Step=910, energy=-74.97372216409832
Step=920, energy=-74.97374818042671
Energy=-74.97375639361245
```

Verify the number of cores that this benchmark ran on with a screenshot from either 'Grafana' or your *preferred* implementation of `top`.

## Multi-Threaded Workload Using Kokkos [4%]

For the next part of the benchmark, you'll be required to rebuild [PennyLane Lightning](https://docs.pennylane.ai/projects/lightning/en/stable/lightning_kokkos/installation.html) using [Kokkos](https://kokkos.org/kokkos-core-wiki/index.html), the C++ Performance Portability Programming Ecosystem. Kokkos exploits the inherent parallelism of modern processing units, in this case those specifically supporting the [OpenMP Threads](https://www.openmp.org/) programming model.

> [!TIP]
> You are ***strongly*** advised to make use of modules, or at the very least locally deploy your cluster software onto a directory accessible to all of your nodes over `NFS`, i.e. `<PATH_TO_SOFTWARE_DIR>`.

You can build PennyLane Lightning's Kokkos variant from source.
1. Install the required system build toolchains:
   * DNF / YUM
     ```bash
     cmake make gcc etc...
     ```
   * APT
   * Pacman
     ```bash
     sudo pacman -S base-devel gcc-fortran
     sudo pacman -S openmp
     ```
1. Download, Build and Configure Kokkos:
   ```bash
   git clone https://github.com/kokkos/kokkos
   cd kokkos

   # You will need to ensure that <PATH_TO_SOFTWARE_DIR> exists if you want to make use of the prefix variable:
   cmake -S . -B build -G Ninja \
    -DCMAKE_BUILD_TYPE=RelWithDebugInfo \
    -DCMAKE_INSTALL_PREFIX=<PATH_TO_SOFTWARE_DIR> \
    -DCMAKE_CXX_STANDARD=20 \
    -DBUILD_SHARED_LIBS:BOOL=ON \
    -DBUILD_TESTING:BOOL=OFF \
    -DKokkos_ENABLE_SERIAL:BOOL=ON \
    -DKokkos_ENABLE_EXAMPLES:BOOL=OFF \
    -DKokkos_ENABLE_TESTS:BOOL=OFF \
    -DKokkos_ENABLE_LIBDL:BOOL=OFF
   ```
1. Make and install Kokkos into `<PATH_TO_SOFTWARE_DIR>`:
   ```bash
   cmake --build build && cmake --install build
   ```
1. Append the install location to the `CMAKE_PREFIX_PATH` variable:
   ```bash
   export CMAKE_PREFIX_PATH=<PATH_TO_SOFTWARE_DIR>:$CMAKE_PREFIX_PATH
   ```
1. Download PennyLane from GitHub:
   ```bash
   git clone https://github.com/PennyLaneAI/pennylane-lightning
   cd pennylane-lightning

   # This benchmark has been tested against Release 0.038, you may experience problems with the latest build, there try
   git checkout v0.38.0_release
   ```

> [!TIP]
> If you're struggling to find your C/C++ Compiler(s), you can either set the following environment variable(s) by prepending the `cmake` command:
>
> `CC=$(which gcc) CXX=$(which g++)`
>
> Alternatively these can be passed as options into `cmake`:
>
> `-DCMAKE_C_COMPILER=$(which gcc) -DCMAKE_CXX_COMPILER=$(which g++)`.
>
> Remember that there are many versions available of `gcc`, `icc`, or even `mpicc`, and that instead of `which` you may want to use a specific version, i.e. `lmod`...

### PennyLane-Lightning.Kokkos[Serial]

You will now build, compile and install the serial device backend for PennyLane-Lightning.Kokkos:
```bash
PL_BACKEND="lightning_kokkos" python scripts/configure_pyproject_toml.py
CMAKE_ARGS="-DKokkos_ENABLE_SERIAL=ON" PL_BACKEND="lightning_kokkos" pip install -e . --config-settings editable_mode=compat --force --no-cache-dir --verbose
```

Copy your `lightning_qubit.py` script to `lightning_kokkos_serial.py` and make use of the `time` module to measure your scripts execution time:
* Edit the top of the file and record the start time *(this will optionally go below your Shabang if you make your Python script executable)*:
  ```python
  #!/<PATH-TO-YOUR-VENV-DIR>/bin/python
  import time
  start_time = time.time()
  ```
* Replace the serial `lightning.qubit` device backend with the serial one `lighting_kokkos`:
  ```python
  dev = qml.device("lightning.kokkos", wires=wires, batch_obs=True)
  ```
* Record the execution time at the very end of the file
  ```python
  end_time = time.time()
  run_time = end_time - start_time
  print(f"Execution time: {run_time}")
  ```

Rerun the benchmark. You must once again redirect the output and take note of the number of CPU cores being utilized during the run.

### PennyLane-Lightning.Kokkos[OpenMP]

You will now build, compile and install the OpenMP device backend for PennyLane-Lightning.Kokkos:

1. Install the required system `openmp` threads package:
   * DNF / YUM
     ```bash
     cmake make gcc etc...
     ```
   * APT
   * Pacman
     ```bash
     sudo pacman -S openmp
     ```
1. Rebuild and Reconfigure Kokkos:
   * Enable the `OPENMP` build option for `cmake`:
     ```bash
     -DKokkos_ENABLE_OPENMP:BOOL=ON
     ```
   * If you're not making use of `lmod`, it may be beneficial to you to make use of an alternative install path for `<PATH_TO_KOKKOS[OPENMP]>`:
     ```bash
     -DCMAKE_INSTALL_PREFIX=<PATH_TO_KOKKOS[OPENMP]>
     ```
1. Rebuild and Reconfigure PennyLane-Lightning.Kokkos:
   * Ensure that you enable the `OPENMP` arguments for `cmake`
   ```bash
   PL_BACKEND="lightning_kokkos" python scripts/configure_pyproject_toml.py
   CMAKE_ARGS="-DKokkos_ENABLE_OPENMP=ON" PL_BACKEND="lightning_kokkos" pip install -e . --config-settings editable_mode=compat --force --no-cache-dir --verbose
   ```
1. Copy `lightning_kokkos_serial.py` to `lightning_kokkos_openmp.py` and edit the script to configure and set the `ENVIRONMENT VARIABLE` for the number of OpenMP threads.
   * At the top of the file, after you've recorded the `start_time`:
     ```python
     start_time = time.time()
     import os
     os.environ["OMP_NUM_THREADS"] = "<NUM_THREADS>"
     ```

> [!NOTE]
> Typically the environment variable is configured as a shell export. Depending on the implementation of your compiler, you may need to also set similar variable for `"MKL_NUM_THREADS"` and similarly, if you'd like squeeze out additional performance consider configuring `numpy` with OpenMP support and setting again a similar variable for `"NUMEXPR_NUM_THREADS"`.

#### Kernel Performance Tuning

Build Options
-DLQ_ENABLE_KERNEL_OMP=ON -DLQ_ENABLE_KERNEL_AVX_STREAMING=ON" 

Environment settings
Setting number of threads and tests for n-1 and n-2
os.environ["OMP_PROC_BIND"] = "spread"
os.environ["OMP_PLACES"] = "threads"

### Graph [2%]

Different molecules and binding energies....?!?!?

## Quantum Circuit Execution Across HPC System [4%]

Speak a bit about MPI here for qubits

1. Build and Configure Parallel HDF5
1. Build and Configure `h5py` against Parallel HDF5

1. Install the required system build toolchains
   * DNF / YUM
   * APT
   * Pacman
     ```bash
     sudo pacman -S openmpi
     ```

```bash
PL_BACKEND="lightning_kokkos" python scripts/configure_pyproject_toml.py
CMAKE_ARGS="-DENABLE_MPI=ON -DCMAKE_C_COMPILER=$(which mpicc) -DCMAKE_CXX_COMPILER=$(which mpicxx) -DKokkos_ENABLE_OPENMP=ON" PL_BACKEND="lightning_kokkos" pip install -e . --config-settings editable_mode=compat --force --no-cache-dir --verbose
```

## Running the Benchmark on Actual Quantum Hardware
### Pennylane-Qiskit.Aer

### Pennylane-Qiskit.IBMQ
