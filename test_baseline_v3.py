from classy import Class
import numpy as np

# Parameters mirroring your explanatory.ini exactly
params = {
    'h': 0.67556,
    'omega_b': 0.022032,
    'omega_cdm': 0.12038,
    'tau_reio': 0.054311,
    'n_s': 0.9667,
    'A_s': 2.215e-9,
    'N_ur': 3.044, 
    'YHe': 0.2453,
    'output': 'tCl, pCl, lCl, mPk',
    'lensing': 'yes'
}

cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    bg = cosmo.get_background()
    derived = cosmo.get_current_derived_parameters(['z_eq', 'tau_eq', 'sigma8'])
    thermo = cosmo.get_thermodynamics()
    
    # Using the keys confirmed by your diagnostic
    age_val = bg['proper time [Gyr]'][-1]
    conf_age_val = bg['conf. time [Mpc]'][-1]
    vis_key = 'g [Mpc^-1]'

    print("-" * 50)
    print("CALIBRATED BASELINE MATCH - SUCCESS")
    print("-" * 50)
    print(f"-> age              = {age_val:.6f} Gyr")
    print(f"-> conformal age    = {conf_age_val:.6f} Mpc")
    print(f"-> z_eq             = {derived['z_eq']:.6f}")
    print(f"-> conformal tau_eq = {derived['tau_eq']:.6f} Mpc")
    
    idx_rec = np.argmax(thermo[vis_key])
    print(f"-> recombination z  = {thermo['z'][idx_rec]:.6f}")
    print(f"-> 100*theta_s      = {100*cosmo.theta_s():.6f}")
    print(f"-> sigma8           = {derived['sigma8']:.6f}")
    print("-" * 50)

except Exception as e:
    print(f"Error: {e}")

finally:
    cosmo.struct_cleanup()
    cosmo.empty()
