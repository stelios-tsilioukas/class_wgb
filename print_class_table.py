import numpy as np
import glob
import sys

# Auto-find the background data file
files = glob.glob('output/*background.dat')
if not files:
    print("Error: Could not find any background.dat file in the output/ folder.")
    sys.exit()

files.sort()
data_file = files[-1]

data = np.loadtxt(data_file)

# Extract z and H
z = data[:, 0]
H_invMpc = data[:, 3]

# Convert units
a = 1.0 / (1.0 + z)
c = 299792.458
H_kmsMpc = H_invMpc * c

# Filter for a = [0.1, 1.0]
mask = (a >= 0.1) & (a <= 1.0)
a_filtered = a[mask]
z_filtered = z[mask]
H_filtered = H_kmsMpc[mask]

# Pick ~20 evenly spaced points to print
indices = np.linspace(0, len(a_filtered) - 1, 20, dtype=int)

print(f"\nData loaded from: {data_file}")
print("-" * 55)
print(f"{'Scale Factor (a)':<18} | {'Redshift (z)':<15} | {'H(a) [km/s/Mpc]':<15}")
print("-" * 55)

for i in indices:
    print(f"{a_filtered[i]:<18.4f} | {z_filtered[i]:<15.4f} | {H_filtered[i]:<15.4f}")

print("-" * 55)
