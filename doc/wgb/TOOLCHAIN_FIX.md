# Build/toolchain notes — `class_wgb_ccg` (NOA tower, `eratosthenes`)

**Date:** 2026-09-16
**Scope:** Two independent fixes bundled in this checkpoint:

1. **Physics fix** — corrected coefficient in the WGB dark-energy sector
   (`source/background.c`): the equation-of-state denominator changes from
   the erroneous `+6·Cn` to the derived `-24·Cn` (`+24·Cn` in code, since the
   spline stores `Iz = -I(a)`). Six lines across three functions
   (`w_fld`, `dw_over_da_fld`, `integral_fld`). Full analytical derivation in
   `wgb_wa_derivation.pdf`.
2. **Toolchain fix** — this document. Getting the *rebuilt* code to actually
   import and run required fixing a chain of independent environment issues
   that had nothing to do with (1). Recorded here so the next rebuild on this
   machine (or a fresh one) doesn't repeat the same multi-hour diagnosis.

---

## Environment as found

- Conda `(base)`, Python 3.8
- `numpy 1.18.5` (old, pinned — other work in this environment may depend on
  it; **do not upgrade it** to fix classy)
- `Cython 3.2.5` (modern, and the actual source of problem #1 below)
- Build system: PEP 517 (`pyproject.toml`), installed via `pip install .`

## Symptom chain and fixes, in the order encountered

### 1. `ImportError: numpy.core.multiarray failed to import`

```
File "python/classy.pyx", line 1, in init classy._classy
ImportError: numpy.core.multiarray failed to import (auto-generated because
you didn't call 'numpy.import_array()' ...)
```

**Cause:** Cython ≥3.0 generates numpy safety-check code that is incompatible
with numpy as old as 1.18.5. The installed Cython (3.2.5) was regenerating
`classy.c`/`classy.cpp` from `classy.pyx` on every rebuild, baking in this
incompatibility fresh each time — so repeated `pip install --force-reinstall`
did *not* fix it, because the same bad Cython kept running.

**First fix attempt (insufficient on its own):**
```bash
python -m pip install "cython==0.29.36"
```
This alone did **not** fix the problem — see #2.

### 2. Cython downgrade appeared to have no effect

Rebuilding after the downgrade reproduced the *exact same* numpy error. The
build log showed why:

```
Running command ... pip install --ignore-installed --no-user \
    --prefix /tmp/pip-build-env-XXXX/overlay ... setuptools wheel numpy cython
```

**Cause:** PEP 517 build isolation. `pip install .` creates a *fresh, throwaway*
build environment for every install and installs its own `cython`/`numpy` from
PyPI into it — completely ignoring the versions pinned in `(base)`. The
Cython 0.29 downgrade in `(base)` was never consulted.

**Fix:** disable build isolation so the build uses the environment's own
(pinned) tool versions:
```bash
pip install . --no-cache-dir --force-reinstall --no-deps --no-build-isolation -v
```
Confirmed working via the build log:
```
cythoning python/classy.pyx to python/classy.cpp
```
`--no-build-isolation` requires `setuptools`, `wheel`, `numpy`, and the
pinned `cython` to already be importable in the active environment (they
were, in `(base)`).

### 3. `AttributeError: module 'importlib.resources' has no attribute 'files'`

```
File "python/classy.pyx", line 349, in classy._classy.Class.__cinit__
    resource_path = abspath(importlib.resources.files('classy'))
AttributeError: module 'importlib.resources' has no attribute 'files'
```

**Cause:** `importlib.resources.files()` was added in Python 3.9. This
environment is Python 3.8. The wrapper's existing `try/except` only caught
`ImportError`, not `AttributeError`, so its intended fallback never
triggered.

**Fix:** installed the backport,
```bash
pip install importlib_resources
```
and patched `python/classy.pyx` (the constructor's resource-path lookup) to
catch `AttributeError` as well and fall back to the backport:
```python
try:
    import importlib.resources
    resource_path = abspath(importlib.resources.files('classy'))
except (ImportError, AttributeError):
    try:
        import importlib_resources
        resource_path = abspath(importlib_resources.files('classy'))
    except Exception:
        resource_path = dirname(abspath(__file__))
```
This patch is a no-op on Python ≥3.9 (the `try` succeeds there), so it is
safe to carry upstream without affecting other users' environments.

Rebuilt with the same `--no-build-isolation` command; `Class()` then
constructed successfully.

---

## Full rebuild recipe (for next time)

```bash
cd ~/Desktop/numerics/tsilioukas/class_wgb_ccg

# one-time environment prerequisites (already satisfied in (base) as of this fix):
python -m pip install "cython==0.29.36" importlib_resources

# clean rebuild — MUST use --no-build-isolation or the Cython pin is ignored
rm -rf build/ python/build/ python/*.egg-info
pip install . --no-cache-dir --force-reinstall --no-deps --no-build-isolation -v \
    2>&1 | tee rebuild.log

# verify
grep -i "cythoning python/classy.pyx" rebuild.log   # confirm it re-cythonized
python -c "from classy import Class; c=Class(); print('Class() constructed OK')"
```

## Verification performed after this fix (see also `wgb_wa_derivation.pdf`)

1. `Cn_wgb=0.0` reproduces the exact $\Lambda$CDM limit: `w_fld` in
   `[-1.000000, -1.000000]`.
2. `Cn_wgb=0.435` gives phantom behaviour, `w_fld` reaching $\approx -1.375$.
3. The coded `w(a)` matches the analytical `-24·Cn` derivation to
   $2\times10^{-5}$–$2\times10^{-4}$ across $z=0.5$–$3$ (residual is
   integration-quadrature noise, not a physics mismatch); the old `+6·Cn`
   convention would have shown a discrepancy of order $0.15$ at $z\sim2$.

## Files touched in this checkpoint

- `source/background.c` — physics fix (6 lines; see commit message / patch)
- `python/classy.pyx` — toolchain fix (`importlib.resources` fallback; ~6 lines)

## Notes for whoever commits this

- The `source/background.c` fix should go to the public `class_wgb` repo.
- The `classy.pyx` `importlib.resources` fix is environment-driven but
  harmless everywhere (no-op on Python ≥3.9) — fine to include in the same
  push, just flag it as a separate concern in the commit message so it
  doesn't get mistaken for part of the physics fix.
- **`numpy` and the wider `(base)` environment were left untouched** by
  design, to avoid breaking other work sharing this conda env. Only
  build-time tooling (`cython`, `importlib_resources`) was added/pinned.
