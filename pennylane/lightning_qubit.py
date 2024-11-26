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
