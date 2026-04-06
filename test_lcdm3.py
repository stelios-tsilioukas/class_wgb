from classy import Class
import numpy as np

# Parameters pulled directly from the explanatory.ini logic
params = {
    'H0': 67.556,
    'omega_b': 0.022032,
    'omega_cdm': 0.12038,
    'tau_reio': 0.054311,
    'n_s': 0.9667,
    'A_s': 2.215e-9,
    'N_ur': 3.044,
    'output': 'tCl, pCl',
}

cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    derived = cosmo.get_current_derived_parameters(['z_eq', 'tau_eq'])
    bg = cosmo.get_background()
    
    print("-" * 50)
    print("MATCHING TEST: PYTHON vs INI")
    print("-" * 50)
    print(f"-> age           = {cosmo.age():.6f} Gyr")
    print(f"-> conformal age = {bg['conf. time [Mpc]'][-1]:.6f} Mpc")
    print(f"-> z_eq          = {derived['z_eq']:.6f}")
    
    # Thermodynamics fix
    thermo = cosmo.get_thermodynamics()
    # Try different possible keys for visibility function
    vis_key = 'visibility g [Mpc^-1]' if 'visibility g [Mpc^-1]' in thermo else 'visibility'
    
    idx_rec = np.argmax(thermo[vis_key])
    print(f"-> recombination (z) = {thermo['z'][idx_rec]:.6f}")
    print(f"-> 100*theta_s       = {100*cosmo.theta_s():.6f}")
    print("-" * 50)

except Exception as e:
    print(f"Error: {e}")
    # Print keys to help debug if it fails again
    if 'thermo' in locals(): print(f"Available keys: {thermo.keys()}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
