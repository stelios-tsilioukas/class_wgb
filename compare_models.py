import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# 1. Load CLASS Data (Standard LCDM)
class_files = sorted(glob.glob('output/*background.dat'))
if not class_files:
    print("Error: No CLASS background file found in output/.")
    exit()
c_data = np.loadtxt(class_files[-1])
a_class = 1.0 / (1.0 + c_data[:, 0])
h_class = c_data[:, 3] * 299792.458 # Convert 1/Mpc to km/s/Mpc

# 2. Load WGB Data (Your C-code output)
if not os.path.exists('wgb_results.txt'):
    print("Error: wgb_results.txt not found.")
    exit()
# We use delimiter='|' because of the format we used in C
w_data = np.loadtxt('wgb_results.txt', delimiter='|', comments='#')
a_wgb = w_data[:, 0]
h_wgb = w_data[:, 2]

# 3. Interpolate CLASS to match WGB points for a direct 1-to-1 comparison
h_class_interp = np.interp(a_wgb, a_class[::-1], h_class[::-1])

# 4. Print Table
print(f"{'a':<10} | {'H_LCDM':<12} | {'H_WGB':<12} | {'% Diff':<10}")
print("-" * 55)
for i in range(len(a_wgb)):
    diff = ((h_wgb[i] - h_class_interp[i]) / h_class_interp[i]) * 100
    print(f"{a_wgb[i]:<10.4f} | {h_class_interp[i]:<12.4f} | {h_wgb[i]:<12.4f} | {diff:<10.2f}%")

# 5. Plot
plt.figure(figsize=(10, 6))
plt.plot(a_class, h_class, 'k--', label='CLASS (LCDM)', alpha=0.6)
plt.plot(a_wgb, h_wgb, 'ro', label='Your WGB Model')
plt.xlabel('Scale Factor a')
plt.ylabel('H(a) [km/s/Mpc]')
plt.title('Comparison: Standard LCDM vs. WGB Modification')
plt.legend()
plt.grid(True, linestyle=':', alpha=0.7)
plt.show()
