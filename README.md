# class_wgb

A modified version of the [CLASS](https://github.com/lesgourg/class_public) Boltzmann code (v3.3.4.0) implementing the **Wald–Gauss–Bonnet (WGB) topological dark energy** model.

---

## The WGB Model

Wald–Gauss–Bonnet topological dark energy is a modified cosmological framework derived from the gravity-thermodynamics conjecture applied to the Universe's apparent horizon, with the Wald–Gauss–Bonnet entropy replacing the standard Bekenstein–Hawking one. Assuming a topological connection between the apparent horizon and interior black hole horizons, the modified Friedmann equations describe a dark energy sector whose evolution depends on the black hole formation and merger rates — approximated by the cosmic star formation rate.

This introduces an astrophysics-dependent contribution to the cosmological constant, parametrised by the coupling constant **C_n** (`Cn_wgb` in CLASS).

**ΛCDM limit:** the WGB model reduces exactly to ΛCDM when `Cn_wgb → 0`.

**Two scenarios are implemented:**
- `Omega_Lambda: 0` — vanishing bare cosmological constant (pure WGB dark energy)
- `Omega_Lambda:` free — modified Λ scenario

For full theoretical details see the papers listed in the [Citation](#citation) section.

---

## Modified Files

The WGB modifications relative to vanilla CLASS v3.3.4.0 are contained in:

| File | Description |
|------|-------------|
| `source/background.c` | WGB dark energy evolution in the background equations |
| `source/input.c` | Reading of `Cn_wgb` parameter |
| `include/background.h` | Declaration of `Cn_wgb` in the background structure |

All other files are identical to the CLASS v3.3.4.0 public release.

---

## Dependencies

- C compiler (`gcc` or `clang`)
- Python ≥ 3.10
- Cython ≥ 3.0
- numpy
- A Fortran compiler is **not** required

---

## Compilation

### 1. Build the C library and executable

```bash
cd class_wgb
make clean && make
```

This produces `libclass.a` and the `class` executable.

### 2. Build the Python interface

```bash
python setup.py build_ext --inplace
```

This produces `_classy.cpython-*.so` in the root directory.

### 3. Install as a Python package (editable)

```bash
pip install -e .
```

### 4. Verify the installation

Run the WGB and ΛCDM example configurations and compare the outputs visually:

```bash
rm -f output/* && ./class explanatory-wgb.ini && ./class explanatory.ini && python lcdm_wgb_plots.py
```

This clears previous outputs, runs CLASS with both the WGB and standard ΛCDM settings, then plots a comparison of the two. A successful run confirms the C library, Python interface, and WGB modifications are all working correctly.

---

## WGB Parameters

| Parameter | CLASS key | Type | Description |
|-----------|-----------|------|-------------|
| `Cn_wgb` | `Cn_wgb` | sampled | WGB coupling constant. ΛCDM limit: `Cn_wgb → 0` |
| `fluid_equation_of_state` | `fluid_equation_of_state` | fixed | Must be set to `WGB` |
| `use_ppf` | `use_ppf` | fixed | Must be `yes` |
| `c_gamma_over_c_fld` | `c_gamma_over_c_fld` | fixed | Set to `0.4` |
| `Omega_Lambda` | `Omega_Lambda` | fixed/free | Set to `0` for pure WGB scenario |

See `explanatory-wgb.ini` for a fully documented example input file.

---

## Cobaya Integration

To use `class_wgb` with [Cobaya](https://cobaya.readthedocs.io/) for MCMC sampling, add the following to your Cobaya YAML file:

```yaml
theory:
  classy:
    stop_at_error: true
    extra_args:
      fluid_equation_of_state: WGB
      use_ppf: 'yes'
      c_gamma_over_c_fld: 0.4
      Omega_Lambda: 0
      nonlinear_min_k_max: 25
      N_ncdm: 1
      N_ur: 2.046
      non linear: hmcode
      hmcode_version: 2020

params:
  Cn_wgb:
    prior: {min: 0.0, max: 1.0}
    ref: {dist: norm, loc: 0.2, scale: 0.05}
    proposal: 0.02
    latex: C_{n,\mathrm{WGB}}
```

Make sure `class_wgb` is installed as an editable pip package in your Cobaya environment before running. When Cobaya initialises it will confirm:
```
[classy] `classy` module loaded successfully from .../class_wgb
```

---

## Authors

- **Stylianos A. Tsilioukas** — Department of Physics, University of Thessaly, 35100 Lamia, Greece; National Observatory of Athens, Lofos Nymfon, 11852 Athens, Greece
- **Maria Petronikolou** — National Observatory of Athens; National Technical University of Athens
- **Fotios K. Anagnostopoulos** — University of Peloponnese
- **Spyros Basilakos** — National Observatory of Athens; Academy of Athens
- **Emmanuel N. Saridakis** — National Observatory of Athens; USTC; Universidad Católica del Norte

---

## Citation

If you use `class_wgb` in your research, please cite:

**Original WGB model (Phys. Rev. D 109, 084010):**
```bibtex
@article{Tsilioukas:2024wgb,
  author  = {Tsilioukas, Stylianos A. and Saridakis, Emmanuel N. and Tzerefos, Charalampos},
  title   = {Dark energy from topology change induced by microscopic Gauss-Bonnet wormholes},
  journal = {Phys. Rev. D},
  volume  = {109},
  pages   = {084010},
  year    = {2024},
  doi     = {10.1103/PhysRevD.109.084010},
  eprint  = {2312.07486},
  archivePrefix = {arXiv},
  primaryClass  = {gr-qc}
}
```

**Observational implications paper (arXiv:2501.15927):**
```bibtex
@article{Petronikolou:2025wgb,
  author  = {Petronikolou, Maria and Anagnostopoulos, Fotios K. and
             Tsilioukas, Stylianos A. and Basilakos, Spyros and
             Saridakis, Emmanuel N.},
  title   = {Observational implications of Wald--Gauss--Bonnet topological dark energy},
  eprint  = {2501.15927},
  archivePrefix = {arXiv},
  primaryClass  = {astro-ph.CO},
  year    = {2025}
}
```

**CLASS (the base code):**
```bibtex
@article{Blas:2011rf,
  author  = {Blas, Diego and Lesgourgues, Julien and Tram, Thomas},
  title   = {The Cosmic Linear Anisotropy Solving System (CLASS) II},
  journal = {JCAP},
  volume  = {07},
  pages   = {034},
  year    = {2011},
  doi     = {10.1088/1475-7516/2011/07/034},
  eprint  = {1104.2933},
  archivePrefix = {arXiv}
}
```

---

## License

The WGB modifications are released under the same license as CLASS.
The original CLASS code is the property of its authors — see the CLASS [repository](https://github.com/lesgourg/class_public) for details.