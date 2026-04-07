import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Define the filenames
# CLASS outputs the linear matter power spectrum as '_pk.dat'
file_wgb = 'output/explanatory-wgb00_pk.dat'
file_lcdm = 'output/explanatory00_pk.dat'

# Safety check
if not os.path.exists(file_wgb) or not os.path.exists(file_lcdm):
    print("Error: Could not find one or both output files.")
    print("Ensure your .ini files have 'output = tCl, pCl, lCl, mPk' so CLASS generates P(k).")
    exit()

# 2. Load the data
# CLASS pk.dat files have columns: 0 = k [h/Mpc], 1 = P(k) [(Mpc/h)^3]
data_wgb = np.loadtxt(file_wgb, comments='#')
k_wgb = data_wgb[:, 0]
pk_wgb = data_wgb[:, 1]

data_lcdm = np.loadtxt(file_lcdm, comments='#')
k_lcdm = data_lcdm[:, 0]
pk_lcdm = data_lcdm[:, 1]

# 3. Ensure arrays match for the residual calculation
# We truncate the arrays to the shortest length just in case
min_length = min(len(k_wgb), len(k_lcdm))
k = k_wgb[:min_length]
pk_wgb = pk_wgb[:min_length]
pk_lcdm = pk_lcdm[:min_length]

# Calculate percentage difference: (WGB - LCDM) / LCDM * 100
percent_diff = ((pk_wgb - pk_lcdm) / pk_lcdm) * 100.0

# 4. Create the Two-Panel Plot
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

# --- Top Panel: Absolute Spectra ---
# Matter power spectra are almost always plotted on a log-log scale
ax1.plot(k, pk_lcdm, color='black', linestyle='--', linewidth=2, label='$\Lambda$CDM (Baseline)')
ax1.plot(k, pk_wgb, color='darkblue', linewidth=2.5, alpha=0.8, label='WGB Model')

ax1.set_yscale('log')
ax1.set_ylabel('$P(k) \quad [(\mathrm{Mpc}/h)^3]$', fontsize=14)
ax1.set_title('Linear Matter Power Spectrum at $z=0$', fontsize=16)
ax1.grid(True, which="major", linestyle="-", alpha=0.5)
ax1.grid(True, which="minor", linestyle=":", alpha=0.3)
ax1.legend(fontsize=12)

# --- Bottom Panel: Percentage Difference ---
# We keep the x-axis log scale, but the y-axis is linear for percentages
ax2.axhline(0, color='black', linestyle='--', linewidth=1.5) 
ax2.plot(k, percent_diff, color='darkblue', linewidth=2)

ax2.set_xscale('log')
ax2.set_ylabel('$\Delta P(k) / P(k)$ (%)', fontsize=14)
ax2.set_xlabel('Wavenumber $k \quad [h/\mathrm{Mpc}]$', fontsize=14)
ax2.grid(True, which="major", linestyle="-", alpha=0.5)
ax2.grid(True, which="minor", linestyle=":", alpha=0.3)

# 5. Final Formatting
# Adjust the spacing between panels
plt.subplots_adjust(hspace=0.05)
plt.show()