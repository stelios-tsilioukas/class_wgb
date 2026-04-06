from classy import Class
import numpy as np

params = {
    'h': 0.67556,
    'omega_b': 0.022032,
    'omega_cdm': 0.12038,
    'tau_reio': 0.054311,
    'n_s': 0.9667,
    'A_s': 2.215e-9,
    'N_ur': 2.0328,
    'N_ncdm': 1,
    'm_ncdm': 0.06,
    'T_cmb': 2.7255,
    'YHe': 0.2453,
    'output': 'tCl, pCl, lCl, mPk',
}

cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    bg = cosmo.get_background()
    thermo = cosmo.get_thermodynamics()
    # Pulling specific derived markers
    derived = cosmo.get_current_derived_parameters([
        'z_eq', 'tau_eq', 'z_rec', 'tau_rec', 'rs_rec', 'da_rec', '100*theta_s',
        'z_d', 'tau_d', 'rs_d', 'tau_reio', 'sigma8'
    ])

    print("\nComputing background")
    print(f" -> age = {bg['proper time [Gyr]'][-1]:.6f} Gyr")
    print(f" -> conformal age = {bg['conf. time [Mpc]'][-1]:.6f} Mpc")
    print(f" -> radiation/matter equality at z = {derived['z_eq']:.6f}")
    print(f"    corresponding to conformal time = {derived['tau_eq']:.6f} Mpc")

    print("\nComputing thermodynamics")
    print(f" -> recombination at z = {derived['z_rec']:.6f}")
    print(f"    corresponding to conformal time = {derived['tau_rec']:.6f} Mpc")
    print(f"    with comoving sound horizon = {derived['rs_rec']:.6f} Mpc")
    print(f"    angular diameter distance = {derived['da_rec']:.6f} Mpc")
    print(f"    sound horizon angle 100*theta_s = {derived['100*theta_s']:.6f}")
    
    print(f" -> baryon drag stops at z = {derived['z_d']:.6f}")
    print(f"    corresponding to conformal time = {derived['tau_d']:.6f} Mpc")
    print(f"    with comoving sound horizon rs = {derived['rs_d']:.6f} Mpc")
    
    print(f" -> reionization with optical depth = {params['tau_reio']}")
    print(f"    corresponding to conformal time = {derived['tau_reio']:.6f} Mpc")

    print(f"\nComputing linear Fourier spectra")
    print(f" -> sigma8 = {derived['sigma8']:.6f}")

except Exception as e:
    print(f"Error: {e}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
