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
> Should you have issues exposing you public facing interface to your Jupyter Lab server, remember that you can use a local SSH forwarding tunnel, between your local machine and your remote server: `ssh -N -L 8889:localhost:8889 <USER>@<HEADNODE_IP> -i ~/.ssh/<PATH_TO_SSH_KEY>`

# Variational Quantum Eigensolver (VQE)

In this benchmark you will be reproducing the results from the recent paper published by some of Xanadu's authors [Hybrid quantum programming with PennyLane Lightning on HPC platforms](https://arxiv.org/abs/2403.02512)

Add some flavour text to explain whats going on

```python
import pennylane as qml
from pennylane import numpy as np

mol = qml.data.load("qchem", molname="H2O", bondlength=0.958, basis="STO-3G")[0]
hf_state, ham = mol.hf_state,  mol.hamiltonian
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

## Single Node Workload [4%]

### Lightning-Qubit (Single Thread)

You can install / upgrade PennyLane and `lightning.qubit` with either of the following two commands. All the core dependencies will be satisfied and resolved implicitly.

```bash
pip install pennylane --upgrade

# or you can explicitly install lightning, which will also pull pennylane dependencies.
# pip install penylane-lightning
```

### Lightning-Kokkos (Multiple OpenMP Threads)

You can install the OpenMP `lightning.kokkos` variant using the following:

```bash
pip install pennylane-lightning[kokkos]
```

add some flavour text to explain and describe changing threads

```python
import os
os.environ["MKL_NUM_THREADS"] = "<NUM_THREADS>"
os.environ["NUMEXPR_NUM_THREADS"] = "<NUM_THREADS>"
os.environ["OMP_NUM_THREADS"] = "<NUM_THREADS>"
```

### Graph [2%]

## Quantum Circuit Execution Across HPC System [4%]

MPI

## Running the Benchmark on Actual Quantum Hardware
### Pennylane-Qiskit.Aer

### Pennylane-Qiskit.IBMQ
