import numpy as np
import matplotlib.pyplot as plt
import glob
import sys

# Auto-find the background data file
files = glob.glob('output/*background.dat')
if not files:
    print("Error: Could not find any background.dat file in the output/ folder.")
    sys.exit()

# Grab the most recently modified one (if there are multiple)
files.sort()
data_file = files[-1]
print(f"Successfully found data: {data_file}")

data = np.loadtxt(data_file)

# Extract z and H (Column 0 is z, Column 3 is H in 1/Mpc)
z = data[:, 0]
H_invMpc = data[:, 3]

# Convert units
a = 1.0 / (1.0 + z)
c = 299792.458
H_kmsMpc = H_invMpc * c

# Filter for a = [0.1, 1.0]
mask = (a >= 0.1) & (a <= 1.0)
a_filtered = a[mask]
H_filtered = H_kmsMpc[mask]

# Plot
plt.figure(figsize=(8, 5))
plt.plot(a_filtered, H_filtered, color='black', linewidth=2.5, label=r'Standard CLASS ($\Lambda$CDM)')
plt.xlabel('Scale Factor $a$', fontsize=12)
plt.ylabel('Hubble Parameter $H(a)$ [km/s/Mpc]', fontsize=12)
plt.title('CLASS Baseline: Hubble Parameter vs Scale Factor', fontsize=14)
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.tight_layout()
plt.show()
