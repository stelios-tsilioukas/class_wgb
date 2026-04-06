from classy import Class
import numpy as np

params = {
    'h': 0.67556,
    'omega_b': 0.022032,
    'omega_cdm': 0.12038,
    'tau_reio': 0.054311,
    'n_s': 0.9667,
    'A_s': 2.215e-9,
    # Explicitly matching the standard explanatory.ini neutrino/temp setup
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
    derived = cosmo.get_current_derived_parameters(['z_eq', 'tau_eq', 'sigma8', '100*theta_s'])
    thermo = cosmo.get_thermodynamics()

    print("-" * 50)
    print("CALIBRATED BASELINE - FINAL ATTEMPT")
    print("-" * 50)
    print(f"-> age           = {bg['proper time [Gyr]'][-1]:.6f} Gyr")
    print(f"-> conformal age = {bg['conf. time [Mpc]'][-1]:.6f} Mpc")
    print(f"-> z_eq          = {derived['z_eq']:.6f}")
    
    # 100*theta_s is often in derived parameters in this version
    print(f"-> 100*theta_s   = {derived['100*theta_s']:.6f}")
    print(f"-> sigma8        = {derived['sigma8']:.6f}")
    print("-" * 50)

except Exception as e:
    print(f"Error: {e}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
