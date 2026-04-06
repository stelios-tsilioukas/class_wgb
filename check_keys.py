from classy import Class
cosmo = Class()
cosmo.set({'h':0.67556})
cosmo.compute()
print("\n--- YOUR BACKGROUND KEYS ---")
print(list(cosmo.get_background().keys()))
print("--- END ---\n")
cosmo.struct_cleanup()
cosmo.empty()
