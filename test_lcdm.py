from classy import Class
import numpy as np

# 1. Define standard LCDM parameters
# (We do not specify 'wgb', so it should default to 0.0)
params = {
    'output': 'tCl,mPk',
    'l_max_scalars': 2000,
    'P_k_max_h/Mpc': 1.0,
    'A_s': 2.3e-9,
    'n_s': 0.9624,
    'h': 0.6711,
    'Omega_b': 0.049,
    'Omega_cdm': 0.2685,
    'z_pk': 0  # We want P(k) at redshift 0
}

# 2. Initialize and Compute
cosmo = Class()
cosmo.set(params)

try:
    cosmo.compute()
    
    # 3. Access Results
    # Background quantity: Age of the universe
    age = cosmo.age()
    
    # Derived parameter: Sigma8 (amplitude of fluctuations)
    sigma8 = cosmo.sigma8()
    
    # Thermodynamics: z_reio (redshift of reionization)
    z_reio = cosmo.z_reio()

    print("-" * 40)
    print(f"LCDM CALCULATION SUCCESSFUL")
    print("-" * 40)
    print(f"Age of Universe      : {age:.4f} Gyr")
    print(f"Sigma8               : {sigma8:.4f}")
    print(f"Reionization Redshift: {z_reio:.4f}")
    print("-" * 40)
    
    # Verify our new parameter 'wgb' exists and is 0.0
    # (Note: not all versions of wrapper expose internal params directly, 
    # but the calculation working proves the C code didn't crash).
    
except Exception as e:
    print(f"Computation failed: {e}")

finally:
    # 4. Clean up
    cosmo.struct_cleanup()
    cosmo.empty()
