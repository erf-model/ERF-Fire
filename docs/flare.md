# FLARE

FLARE (Fire-Line Advancement and Reaction Engine) is the fire engine in
[erf-model/FLARE](https://github.com/erf-model/FLARE). It was the native fire
model on the `ERF-Fire` branch of `hgopalan/ERF` until October 2026.

The FLARE repository is a full copy of ERF plus the engine and other additions.
It takes ERF `development` merges regularly. The
[FLARE README](https://github.com/erf-model/FLARE/blob/development/README.rst)
describes its capabilities and how to build it. This page covers how FLARE maps to
ERF, and what its repository holds that is not the engine.

![What is inside each repository](images/what-is-where.svg)

## How FLARE maps to ERF

| Coupling item | In FLARE |
|---|---|
| Engine directory | `FireEngine/` |
| Registration | `ERF_REGISTER_FIRE_ENGINE(NativeFireEngine, "flare")` in `ERF_NativeFireEngine.cpp` |
| Selection | `erf.fire.engine = flare`, the default in a FLARE build |
| Build | `ERF_ENABLE_FIRE` is ON by default in FLARE; it is OFF in ERF |

**Fire engine contents.** The rate-of-spread models, the Huygens and level-set
front propagation, fuel and fuel moisture, ignition, acceleration, spotting, crown
fire, suppression, structure ignition, and the fire plotfile, statistics and
checkpoint.

## In the FLARE repository but not in the engine

These items are outside `FireEngine/`. Some are used by fire runs, but none is
part of the engine, and none is in ERF `development` yet.

| Item | Where in FLARE | Inputs | What it does | Tied to fire? |
|---|---|---|---|---|
| Dust model | `Source/Dust`, `Source/Particles/ERF_DustPC.*` | `erf.dust.*`, `ERF_ENABLE_DUST` | Emission, settling, deposition and health diagnostics for bare mineral surfaces | No |
| Fire-dust coupling | `Source/FireDust`, `Source/Dust/ERF_DustFireLofting.*` | `erf.fire_dust_coupling`, `erf.fire_dust_crust_reduction`, `erf.fire_dust_wind_*`, `erf.fire_dust_lofting_*` | Feeds the fire's burned area, outflow wind and heat flux into dust emission | Yes |
| MRF fire boost | `Source/PBL/ERF_ComputeDiffusivityMRF.cpp` | `erf.pbl_mrf_fire_thermal_excess`, `erf.mrf_fire_q_threshold`, `erf.mrf_fire_t_excess_cap` | Raises the convective velocity scale of the MRF scheme with the fire's heat flux | Yes |
| Terrain-following inflow | `Source/BoundaryConditions/ERF_InflowProfile.*`, `ERF_BoundaryConditionsInflowProfile.cpp` | `<face>.inflow_profile = log_law` or `file`, `<face>.inflow_profile_file` | Looks up the inflow at each boundary cell's height above its own ground | No |
| Sounding above ground | `Source/DataStructs/ERF_InputSoundingData.H` | `erf.input_sounding_wind_above_ground`, `erf.input_sounding_theta_above_ground` | Two separate switches that measure sounding winds, or theta, from each column's ground; with theta, each column is then rebalanced hydrostatically | No |
| Geostrophic start | `Exec/ERF_Prob.cpp` | `erf.abl_geo_wind` | ERF uses this key as forcing only. FLARE also starts the velocity from it, for uniform initialisation with no problem-specific velocity | No |
| Warm bubble | `Source/Prob/ERF_InitCustomPert_ABL.H` | `prob.bubble_dT`, `prob.bubble_{x,y,z}_c`, `prob.bubble_{x,y,z}_r` | Adds a theta bubble in the form of WRF's idealized fire start | No |
| Building-roof stability | `Source/ImmersedBoundarySEB/ERF_IBSEBWallFunction.H` | `erf.ibseb.stability_scheme = louis`, needs `erf.ibseb.stability_correction = true` | Adds the Louis (1979) stability factors on roofs | No |
| Imposed surface heat flux | `Source/BoundaryConditions/ERF_MOSTStress.H`, `ERF_SurfaceLayer.*` | `erf.most.surf_temp_flux` with `bulk_coeff` | ERF has this key for other flux types. FLARE also accepts it with `erf.surface_layer.flux_type = bulk_coeff`, where it replaces the Ch form of the heat flux | No |
| Joining fine boxes stacked in z | `Source/Utils/ERF_ChopGrids.cpp`, `Source/ERF_MakeNewLevel.cpp` | None | Joins refined boxes stacked in z when a level is made, and checks that column PBL schemes get full columns | No |
| Cases and tools | `Exec/CanonicalTests/{Fire,Dust,Hazard}`, `Exec/Tools` | | Fire and dust cases; LANDFIRE fuel map, HRRR winds and map movie scripts | Mostly |

The dust model is the largest of these. It uses the same surface-grid design as
the fire model, but it runs with `ERF_ENABLE_DUST=ON` and a fire is not required.

FLARE also has one small addition to the coupling code that ERF does not have: the
`ERF_FIRE_DEFAULT_ENGINE` compile definition, read in
`Source/FireCoupling/ERF_FireCouplingParams.cpp` and set in
`CMake/BuildERFExe.cmake` and `Exec/Make.ERF`. It lets a build name the engine a deck
gets when the deck names none.

This list compares FLARE `690bc4668` with its last common commit with ERF,
`6e260ec28`, and ERF `development` at `44c18fd4a`, on 2026-10-30. Merges in either
direction will change it. To repeat the comparison:

```bash
git diff --name-status $(git merge-base upstream/development flare/development) flare/development -- Source
```
