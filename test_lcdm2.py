from classy import Class

# 1. Define parameters to match explanatory.ini defaults
params = {
    'h': 0.67556,
    'omega_b': 0.022032,
    'omega_cdm': 0.12038,
    'tau_reio': 0.0543,
    'n_s': 0.9667,
    'A_s': 2.215e-9,
    'N_ur': 3.044,
    # Adding output to ensure thermodynamics are computed
    'output': 'tCl, pCl', 
}

cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    
    # Extract Background quantities
    derived = cosmo.get_current_derived_parameters(['z_eq', 'tau_eq'])
    
    print("-" * 50)
    print("PYTHON WRAPPER OUTPUT (Matching explanatory.ini)")
    print("-" * 50)
    
    print(f"-> age = {cosmo.age():.6f} Gyr")
    # Conformal age in CLASS is the end value of the background tau table
    print(f"-> conformal age = {cosmo.get_background()['conf. time [Mpc]'][-1]:.6f} Mpc")
    
    # N_eff check
    print(f"-> N_eff = {params['N_ur']}")
    
    # Equality
    print(f"-> radiation/matter equality at z = {derived['z_eq']:.6f}")
    print(f"-> corresponding to conformal time = {derived['tau_eq']:.6f} Mpc")
    
    # Thermodynamics
    thermo = cosmo.get_thermodynamics()
    # Find index of maximum of visibility function
    import numpy as np
    idx_rec = np.argmax(thermo['visibility g [Mpc^-1]'])
    
    print(f"-> recombination (max visibility) at z = {thermo['z'][idx_rec]:.6f}")
    print(f"-> corresponding to conformal time = {thermo['conf. time [Mpc]'][idx_rec]:.6f} Mpc")
    print(f"-> sound horizon angle 100*theta_s = {100*cosmo.theta_s():.6f}")
    
    # Reionization
    print(f"-> reionization with optical depth = {params['tau_reio']}")

    print("-" * 50)

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
