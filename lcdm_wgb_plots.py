import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import os
import glob

print("--- Starting WGB vs LCDM Plotter ---")

# --- 1. Configuration & Safe File Finding ---
folder = 'output/'

def get_latest_file(pattern):
    files = glob.glob(os.path.join(folder, pattern))
    if not files:
        return None
    return max(files, key=os.path.getctime)

print("Looking for files...")
f_wgb_bg = get_latest_file('explanatory-wgb*_background.dat')
f_wgb_cl = get_latest_file('explanatory-wgb*_cl_lensed.dat')
f_wgb_pk = get_latest_file('explanatory-wgb*_pk.dat')

f_lcdm_cl = get_latest_file('explanatory[0-9]*_cl_lensed.dat') 
f_lcdm_pk = get_latest_file('explanatory[0-9]*_pk.dat')

files_dict = {
    "WGB Background": f_wgb_bg,
    "WGB Cl": f_wgb_cl,
    "WGB P(k)": f_wgb_pk,
    "LCDM Cl": f_lcdm_cl,
    "LCDM P(k)": f_lcdm_pk
}

# --- 2. Verification ---
missing = [name for name, path in files_dict.items() if path is None]
if missing:
    print(f"🚨 ERROR: Missing files: {missing}")
    exit()

print("All files found! Loading data...")

# --- 3. Advanced Grid Setup ---
fig = plt.figure(figsize=(18, 7))
fig.suptitle('Cosmological Observables: WGB vs $\Lambda$CDM', fontsize=18, fontweight='bold', y=0.95)

# 2 rows, 3 columns. Height ratio 3:1
gs = gridspec.GridSpec(2, 3, height_ratios=[3, 1], hspace=0.05, wspace=0.25)

# Axis 0: w(z) spans both rows on the left
ax_w = fig.add_subplot(gs[:, 0])

# Axis 1: P(k) Main and Residual (Middle)
ax_pk_main = fig.add_subplot(gs[0, 1])
ax_pk_res = fig.add_subplot(gs[1, 1], sharex=ax_pk_main)

# Axis 2: CMB Main and Residual (Right)
ax_cl_main = fig.add_subplot(gs[0, 2])
ax_cl_res = fig.add_subplot(gs[1, 2], sharex=ax_cl_main)

# ==========================================
# PLOT 1: Background Equation of State w(z)
# ==========================================
print("Plotting Equation of State...")
z_bg, w_bg = np.loadtxt(f_wgb_bg, usecols=(0, 12), unpack=True)
valid_mask = z_bg > 0
z_log, w_log = z_bg[valid_mask], w_bg[valid_mask]

ax_w.plot(z_log, w_log, color='blue', lw=2.5, label='WGB Model ($w_{fld}$)')
ax_w.axhline(-1.0, color='black', ls='--', alpha=0.6, label=r'$\Lambda$CDM ($w=-1$)')

ax_w.set_xscale('log')
ax_w.invert_xaxis()
ax_w.set_xlabel('Redshift ($z$)', fontsize=14)
ax_w.set_ylabel('Equation of State $w(z)$', fontsize=14)
ax_w.set_title('Dark Energy Evolution', fontsize=16)
ax_w.grid(True, which="major", ls="-", alpha=0.5)
ax_w.grid(True, which="minor", ls=":", alpha=0.3)
ax_w.legend(fontsize=12)

# ==========================================
# PLOT 2: Matter Power Spectrum P(k)
# ==========================================
print("Plotting Matter Power Spectrum & Residuals...")
data_wgb_pk = np.loadtxt(f_wgb_pk, comments='#')
k_wgb, pk_wgb = data_wgb_pk[:, 0], data_wgb_pk[:, 1]

data_lcdm_pk = np.loadtxt(f_lcdm_pk, comments='#')
k_lcdm, pk_lcdm = data_lcdm_pk[:, 0], data_lcdm_pk[:, 1]

# Apply truncation logic exactly as requested
min_len_pk = min(len(k_wgb), len(k_lcdm))
k_trunc = k_wgb[:min_len_pk]
pk_wgb_trunc = pk_wgb[:min_len_pk]
pk_lcdm_trunc = pk_lcdm[:min_len_pk]

res_pk = ((pk_wgb_trunc - pk_lcdm_trunc) / pk_lcdm_trunc) * 100.0

# Main P(k)
ax_pk_main.loglog(k_lcdm, pk_lcdm, color='black', ls='--', lw=2, alpha=0.7, label=r'$\Lambda$CDM')
ax_pk_main.loglog(k_wgb, pk_wgb, color='darkblue', lw=2.5, alpha=0.8, label='WGB Model')
ax_pk_main.set_ylabel(r'$P(k) \quad [(\mathrm{Mpc}/h)^3]$', fontsize=14)
ax_pk_main.set_title(r'Linear Matter Power Spectrum at $z=0$', fontsize=16)
ax_pk_main.grid(True, which="major", ls="-", alpha=0.5)
ax_pk_main.grid(True, which="minor", ls=":", alpha=0.3)
ax_pk_main.legend(fontsize=12)
plt.setp(ax_pk_main.get_xticklabels(), visible=False)

# Residual P(k)
ax_pk_res.axhline(0, color='black', ls='--', lw=1.5)
ax_pk_res.semilogx(k_trunc, res_pk, color='darkblue', lw=2)
ax_pk_res.set_xlabel(r'Wavenumber $k \quad [h/\mathrm{Mpc}]$', fontsize=14)
ax_pk_res.set_ylabel(r'$\Delta P/P$ (%)', fontsize=12)
ax_pk_res.grid(True, which="major", ls="-", alpha=0.5)
ax_pk_res.grid(True, which="minor", ls=":", alpha=0.3)

# ==========================================
# PLOT 3: CMB Temperature Anisotropy (TT)
# ==========================================
print("Plotting CMB & Residuals...")
data_wgb_cl = np.loadtxt(f_wgb_cl, comments='#')
l_wgb, tt_wgb = data_wgb_cl[:, 0], data_wgb_cl[:, 1]

data_lcdm_cl = np.loadtxt(f_lcdm_cl, comments='#')
l_lcdm, tt_lcdm = data_lcdm_cl[:, 0], data_lcdm_cl[:, 1]

# Apply truncation logic exactly as requested
min_len_cl = min(len(l_wgb), len(l_lcdm))
l_trunc = l_wgb[:min_len_cl]
tt_wgb_trunc = tt_wgb[:min_len_cl]
tt_lcdm_trunc = tt_lcdm[:min_len_cl]

res_tt = ((tt_wgb_trunc - tt_lcdm_trunc) / tt_lcdm_trunc) * 100.0

# Main CMB
ax_cl_main.plot(l_lcdm, tt_lcdm, color='black', ls='--', lw=2, alpha=0.7, label=r'$\Lambda$CDM')
ax_cl_main.plot(l_wgb, tt_wgb, color='darkred', lw=2.5, alpha=0.8, label='WGB Model')
ax_cl_main.set_xlim(2, 2500)
ax_cl_main.set_ylabel(r'$\mathcal{D}_\ell^{TT} \quad [\mu K^2]$', fontsize=14)
ax_cl_main.set_title('CMB Temperature Power Spectrum', fontsize=16)
ax_cl_main.grid(True, ls=":", alpha=0.6)
ax_cl_main.legend(fontsize=12)
plt.setp(ax_cl_main.get_xticklabels(), visible=False)

# Residual CMB
ax_cl_res.axhline(0, color='black', ls='--', lw=1.5)
ax_cl_res.plot(l_trunc, res_tt, color='darkred', lw=2)
ax_cl_res.set_xlim(2, 2500)
ax_cl_res.set_xlabel(r'Multipole moment ($\ell$)', fontsize=14)
ax_cl_res.set_ylabel(r'$\Delta \mathcal{D}_\ell / \mathcal{D}_\ell$ (%)', fontsize=12)
ax_cl_res.grid(True, ls=":", alpha=0.6)

# ==========================================
# Final Render & Save
# ==========================================
plt.subplots_adjust(bottom=0.12, top=0.88, left=0.05, right=0.98)

output_image = 'wgb_dashboard.png'
plt.savefig(output_image, dpi=300, bbox_inches='tight')
print(f"✅ SUCCESS! Plot saved as: {output_image}")

print("Opening interactive plot window...")
plt.show()