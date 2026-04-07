import numpy as np
import matplotlib.pyplot as plt
import os

# 1. Define the updated filename with the correct folder path!
filename = 'output/explanatory-wgb01_background.dat' 

# Safety check to ensure the file exists before we try to load it
if not os.path.exists(filename):
    print(f"Error: Could not find '{filename}'.")
    print("Make sure you are running this script from your main CLASS folder.")
else:
    # 2. Load the data
    # usecols=(0, 12) grabs the 1st (z) and 13th (w) columns. 
    z, w = np.loadtxt(filename, usecols=(0, 12), unpack=True)

    # 3. Filter out z = 0 for the logarithmic scale
    # This prevents math errors since log(0) is undefined
    valid_mask = z > 0
    z_log = z[valid_mask]
    w_log = w[valid_mask]

    # 4. Create the Plot
    fig, ax = plt.subplots(figsize=(9, 6))

    # Plot the filtered data
    ax.plot(z_log, w_log, color='blue', linewidth=2.5, label='WGB Model ($w_{fld}$)')

    # Add a dashed line at w = -1 to compare against standard Lambda-CDM
    ax.axhline(-1.0, color='black', linestyle='--', alpha=0.6, label='$\Lambda$CDM ($w=-1$)')

    # 5. Formatting
    ax.set_xscale('log')
    
    # Invert the x-axis so the present day (z near 0) is on the right, 
    # and the Big Bang (high z) is on the left.
    ax.invert_xaxis() 

    ax.set_xlabel('Redshift ($z$)', fontsize=14)
    ax.set_ylabel('Equation of State $w(z)$', fontsize=14)
    ax.set_title('Evolution of WGB Dark Energy', fontsize=16)
    
    # Add minor gridlines for better log-scale readability
    ax.grid(True, which="major", linestyle="-", alpha=0.5)
    ax.grid(True, which="minor", linestyle=":", alpha=0.3)
    ax.legend(fontsize=12)

    plt.tight_layout()
    plt.show()