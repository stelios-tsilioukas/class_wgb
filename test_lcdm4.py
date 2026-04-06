from classy import Class
import numpy as np

# Exact parameters from your explanatory.ini run
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
    
    # Background data
    bg = cosmo.get_background()
    derived = cosmo.get_current_derived_parameters(['z_eq', 'tau_eq'])
    
    # Thermodynamics data
    thermo = cosmo.get_thermodynamics()
    
    print("-" * 50)
    print("MATCHING TEST: FINAL BASELINE")
    print("-" * 50)
    
    # Pulling age from the last entry of the background table (more precise)
    print(f"-> age           = {bg['age [Gyr]'][-1]:.6f} Gyr")
    print(f"-> conformal age = {bg['conf. time [Mpc]'][-1]:.6f} Mpc")
    print(f"-> z_eq          = {derived['z_eq']:.6f}")
    print(f"-> tau_eq        = {derived['tau_eq']:.6f} Mpc")
    
    # Using your specific key: 'g [Mpc^-1]'
    idx_rec = np.argmax(thermo['g [Mpc^-1]'])
    print(f"-> recombination (z) = {thermo['z'][idx_rec]:.6f}")
    
    # Sound horizon angle
    print(f"-> 100*theta_s       = {100*cosmo.theta_s():.6f}")
    print("-" * 50)

except Exception as e:
    print(f"Error: {e}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
