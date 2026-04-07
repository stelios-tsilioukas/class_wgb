import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Define the filenames
# CLASS automatically appends '00_' to the first run in an empty output folder.
file_wgb = 'output/explanatory-wgb00_cl_lensed.dat'
file_lcdm = 'output/explanatory00_cl_lensed.dat'

# Safety check
if not os.path.exists(file_wgb) or not os.path.exists(file_lcdm):
    print("Error: Could not find one or both output files.")
    print("Ensure you ran both ./class explanatory-wgb.ini and ./class explanatory.ini")
    exit()

# 2. Load the data
# Columns: 0=l, 1=TT, 2=EE, 3=TE, 4=PP, 5=phi_phi
data_wgb = np.loadtxt(file_wgb, comments='#')
l_wgb = data_wgb[:, 0]
tt_wgb = data_wgb[:, 1]

data_lcdm = np.loadtxt(file_lcdm, comments='#')
l_lcdm = data_lcdm[:, 0]
tt_lcdm = data_lcdm[:, 1]

# 3. Ensure arrays match for the residual calculation
# We truncate the arrays to the shortest length in case the l_max differs
min_length = min(len(l_wgb), len(l_lcdm))
l = l_wgb[:min_length]
tt_wgb = tt_wgb[:min_length]
tt_lcdm = tt_lcdm[:min_length]

# Calculate percentage difference: (WGB - LCDM) / LCDM * 100
percent_diff = ((tt_wgb - tt_lcdm) / tt_lcdm) * 100.0

# 4. Create the Two-Panel Plot
# gridspec_kw sets the top panel to be 3x taller than the bottom panel
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

# --- Top Panel: Absolute Spectra ---
ax1.plot(l, tt_lcdm, color='black', linestyle='--', linewidth=2, label='$\Lambda$CDM (Baseline)')
ax1.plot(l, tt_wgb, color='darkred', linewidth=2.5, alpha=0.8, label='WGB Model')

ax1.set_ylabel('$\mathcal{D}_\ell^{TT} \quad [\mu K^2]$', fontsize=14)
ax1.set_title('CMB Temperature Power Spectrum Comparison', fontsize=16)
ax1.grid(True, linestyle=':', alpha=0.6)
ax1.legend(fontsize=12)

# --- Bottom Panel: Percentage Difference ---
ax2.axhline(0, color='black', linestyle='--', linewidth=1.5) # Zero line
ax2.plot(l, percent_diff, color='darkred', linewidth=2)

ax2.set_ylabel('$\Delta \mathcal{D}_\ell / \mathcal{D}_\ell$ (%)', fontsize=14)
ax2.set_xlabel('Multipole moment ($\ell$)', fontsize=14)
ax2.grid(True, linestyle=':', alpha=0.6)

# 5. Final Formatting
# Focus on the observable range of Planck
ax1.set_xlim(2, 2500) 

# Adjust the spacing between panels
plt.subplots_adjust(hspace=0.05)
plt.show()