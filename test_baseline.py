from classy import Class

# Create an instance of the CLASS wrapper
cosmo = Class()

# Set standard parameters
params = {
    'output': 'tCl,pCl,lCl',
    'l_max_scalars': 2500,
    'lensing': 'yes'
}

# Compute
cosmo.set(params)
cosmo.compute()

# Print a success message
print("Baseline CLASS is healthy. Ready for modification.")

# Clean up
cosmo.struct_cleanup()
cosmo.empty()
