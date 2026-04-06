from classy import Class
import numpy as np

# 1. Exact parameters to match your explanatory.ini run
params = {
    'h': 0.67556,
    'omega_b': 0.022032,
    'omega_cdm': 0.12038,
    'tau_reio': 0.054311,
    'n_s': 0.9667,
    'A_s': 2.215e-9,
    # Matching the N_eff = 3.044 from your output
    'N_ur': 3.044, 
    # Helium fraction from your log
    'YHe': 0.2453,
    # Outputs to trigger full modules
    'output': 'tCl, pCl, lCl, mPk',
    'lensing': 'yes'
}

cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    
    # Background and Derived
    bg = cosmo.get_background()
    derived = cosmo.get_current_derived_parameters(['z_eq', 'tau_eq', 'sigma8'])
    
    # Thermodynamics
    thermo = cosmo.get_thermodynamics()
    idx_rec = np.argmax(thermo['g [Mpc^-1]'])
    
    print("-" * 50)
    print("CALIBRATED BASELINE MATCH")
    print("-" * 50)
    
    # 1. Background
    print(f"-> age              = {bg['age [Gyr]'][-1]:.6f} Gyr")
    print(f"-> conformal age    = {bg['conf. time [Mpc]'][-1]:.6f} Mpc")
    print(f"-> z_eq             = {derived['z_eq']:.6f}")
    print(f"-> conformal tau_eq = {derived['tau_eq']:.6f} Mpc")
    
    # 2. Thermodynamics
    print(f"-> recombination z  = {thermo['z'][idx_rec]:.6f}")
    print(f"-> 100*theta_s      = {100*cosmo.theta_s():.6f}")
    
    # 3. LSS
    print(f"-> sigma8           = {derived['sigma8']:.6f}")
    print("-" * 50)

except Exception as e:
    print(f"Error: {e}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
