import numpy as np
import os

# 1. Point directly to the existing background file
data_file = 'output/test_bg_00_background.dat'

if not os.path.exists(data_file):
    print(f"❌ Error: {data_file} not found in output/.")
    exit()

print(f"✅ Processing: {data_file}")

# 2. Load the data
data = np.loadtxt(data_file)

# 3. Standard CLASS columns: 0 is z, 3 is H [1/Mpc]
z = data[:, 0]
a = 1.0 / (1.0 + z)
c = 299792.458
H_kmsMpc = data[:, 3] * c

# 4. Filter for a = [0.1, 1.0]
mask = (a >= 0.1) & (a <= 1.0)
a_filtered = a[mask]
H_filtered = H_kmsMpc[mask]

# 5. Pick exactly 20 points (to match your WGB grid)
indices = np.linspace(0, len(a_filtered) - 1, 20, dtype=int)

# 6. Save to lcdm_results.txt
with open('lcdm_results.txt', 'w') as f:
    f.write("# LCDM BASELINE DATA (FROM CLASS)\n")
    f.write(f"# {'Scale Factor (a)':<18} | {'Integral I(a)':<18} | {'H_LCDM [km/s/Mpc]':<15}\n")
    for i in indices:
        f.write(f"{a_filtered[i]:<18.4f} | {0.0:<18.6e} | {H_filtered[i]:<15.4f}\n")

print("✅ lcdm_results.txt generated successfully.")
