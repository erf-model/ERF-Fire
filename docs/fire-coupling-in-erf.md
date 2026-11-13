# Fire–Atmosphere Coupling in ERF

ERF provides the atmosphere side of a coupled fire simulation: it hosts the fire
grid, supplies the near-surface state to a fire engine, and returns the engine's
heat, water vapour and smoke to the atmosphere. This page summarises that
interface. The complete reference is the ERF documentation page
[Fire-Atmosphere Coupling](https://erf.readthedocs.io/en/latest/theory/FireCoupling.html)
and the Fire Coupling table in
[Inputs.rst](https://github.com/erf-model/ERF/blob/development/Docs/sphinx_doc/Inputs.rst).

## Background

The coupling layer was developed on the `ERF-Fire` branch of `hgopalan/ERF` and
proposed in erf-model/ERF#4288 by Harish Gopalan. Ann Almgren merged it into ERF in
erf-model/ERF#4798 (2026-10-27), together with Nicholas Wimer's hgopalan/ERF#519,
#520 and #521 and the single engine interface for external codes planned in
erf-model/ERF#4768. erf-model/ERF#4288 was closed in favour of that PR.

ERF contains the coupling only. Rate-of-spread models, fuel models and front
propagation schemes remain in the fire engines.

## Components in ERF

| Location | Contents |
|---|---|
| `Source/FireCoupling` | The `FireCoupler` class, the `FireEngine` interface, the engine registry, the input parser, and helpers for the wind and ground height |
| `Source/FireCoupling/ERF_FireEngineTemplate.H` | Annotated declarations of every engine method (reference only; not compiled into a run) |
| ERF core | Hooks for start-up, time advance and source terms, the fire plotfile, and a `ScalarLayout` record in every checkpoint |

ERF holds no fire tests. The example engine (`Tests/FireEngineExample`) and the
fire unit tests (`Tests/Unit/Fire`) moved to FLARE in erf-model/ERF#5095 by Ann
Almgren.

## ERF as a submodule

Every fire engine uses one repository layout: the engine's repository holds ERF
as a Git submodule and builds against it. ERF holds no fire tests, so ERF's CI
runs ERF's tests only. The engine keeps its fire cases and tests in its own
repository. There are two build routes within this layout, described below.

```bash
git submodule add https://github.com/erf-model/ERF.git Submodules/ERF
git submodule update --init --recursive   # also brings AMReX, through ERF
```

Pin the submodule to an ERF release, or to a later ERF commit when the engine
needs one. A change the engine needs in ERF goes to erf-model/ERF as a pull
request; the engine then moves its submodule to a commit that contains it.

The recommended build uses ERF as a library, `ERF::erf` (erf-model/ERF#5096 by
Ann Almgren). The engine's repository has its own `CMakeLists.txt`, compiles its
engine and its own problem file into its own executable, and sets that
executable up with ERF's `erf_setup_executable`. The engine's
`ERF_REGISTER_FIRE_ENGINE` line runs from that executable, so ERF needs no
engine path:

```cmake
cmake_minimum_required(VERSION 3.25)
project(MyFire CXX C)

option(ERF_ENABLE_FIRE "Enable the fire coupling" ON)   # before ERF's own option()

if(ERF_ENABLE_CUDA)
  enable_language(CUDA)   # also needed here, where my_fire is defined
endif()

enable_testing()
add_subdirectory(Submodules/ERF EXCLUDE_FROM_ALL)

add_executable(my_fire Exec/ERF_Prob.cpp)
target_include_directories(my_fire PRIVATE ${PROJECT_SOURCE_DIR}/Exec)
set(ERF_FIRE_ENGINE_DIR "${PROJECT_SOURCE_DIR}/FireEngine")
include("${ERF_FIRE_ENGINE_DIR}/ERFFireEngine.cmake")
erf_fire_engine_add(my_fire)          # adds the engine's sources
erf_setup_executable(my_fire)         # ERF's main.cpp, ERF::erf, compile and GPU flags
```

Every ERF option (`ERF_ENABLE_MPI`, `ERF_ENABLE_CUDA`, `ERF_ENABLE_NETCDF`, ...)
is given on the engine's configure line, as for ERF itself. The section "ERF as
a library" of ERF's
[building page](https://erf.readthedocs.io/en/latest/buildingSystems.html) lists
the rules, and ERF's `Tests/ParentExecutable` is a small working example. ERF's
CTest helpers (`Tests/ERFTestHelpers.cmake`) can register the engine's own
regression cases. FLARE's `CMakeLists.txt` follows this pattern.

The second route builds ERF's own executable from the submodule and passes it
the engine's directory (`ERF_FIRE_ENGINE_DIRS` in CMake, `FIRE_HOME` in GNU
make). LSFIRE uses this route from its `ERF/` submodule. The engine still lives
in its own repository.

Fire coupling is disabled by default in ERF. When it is enabled, the state
carries one additional passive scalar, the smoke tracer, whether or not a fire
is run. Each checkpoint records the number of scalars, so a restart with a
differently configured build is rejected.

A run with `erf.fire.enable = true` stops at start-up if no engine is compiled
in. With one engine compiled in, it is the default. When several engines are
compiled into one executable, `erf.fire.engine` selects one at run time.

## Coupling sequence

![Quantities exchanged between ERF and a fire engine each step](images/coupling-step.svg)

1. At start-up, the coupler builds the fire grid by refining one AMR level by
   `erf.fire.grid_ratio` in x and y.
2. Each step, it passes the engine the face velocities, the cell-centre heights,
   the air temperature and relative humidity of the lowest cell, and the surface
   precipitation if the engine requests it.
3. The engine advances and returns the sensible and latent heat fluxes into the
   air [W/m²], averaged over its step.
4. The coupler averages these fluxes onto the atmospheric columns and holds them
   for one step.
5. It injects them at every Runge-Kutta stage of the next step, together with the
   smoke tracer when smoke is enabled.

Steps 4 and 5 apply to `lagged` and `synchronous` coupling. With `passive`
coupling no heat is injected; only the smoke tracer is, when enabled.

The held fluxes are written to the checkpoint, so a restarted run injects the
same heat in its first step as an uninterrupted run.

## Limitations

- The level that hosts the fire grid must keep the same boxes for the whole run.
- Its boxes must form a single rectangle, and each box must span the full height
  of the level, so a refined fire level must extend to the domain top.
- Every box length in x and y must be divisible by the grid ratio.
- The bottom boundary must be a surface layer, unless the engine declares that it
  reads nothing from one.
- When the fire grid lies below the finest level, average-down overwrites the
  heated cells beneath the finer level and that heat is lost; the coupler warns
  at start-up.
- A restart that regenerates the level-0 grids stops before the checkpoint is
  read.

## Coupling inputs

| Input | Effect |
|---|---|
| `erf.fire.enable` | Enables the fire |
| `erf.fire.engine` | Selects the compiled-in engine |
| `erf.fire.grid_ratio` | Fire cells per atmospheric cell in x and y |
| `erf.fire.anchor_level` | Level refined by the fire grid; -1 selects the finest |
| `erf.fire.coupling_type` | `passive`, `lagged` (default) or `synchronous` |
| `erf.fire.fire_atm_feedback` | Multiplier on the injected fluxes; 0 gives one-way coupling |
| `erf.fire.heat_profile` | `exponential` (default) or `bottom_cell` |
| `erf.fire.heat_flux_alfg` | E-folding depth of the exponential profile (default 45 m) |
| `erf.fire.heat_open_fraction` | Distributes the heat using the open fraction and roof height reported by the engine |
| `erf.fire.heat_tendency_exner` | Divides the tendency by the Exner function (default true) |
| `erf.fire.heat_tendency_density` | Multiplies the tendency by the air density |
| `erf.fire.inject_latent` | Injects the latent flux into the water vapour equation |
| `erf.fire.source_mode` | `overwrite` (default) or `add`, relative to other sources in the same slots; if unset, the run stops at start-up when another source, such as radiation or Rayleigh damping, writes to those slots |
| `erf.fire.smoke_enable` | Injects the smoke tracer; requires `erf.transport_scalar` |
| `erf.fire.smoke_emission_factor` | Smoke mass per unit fuel mass burned (default 0.02 kg/kg) |
| `erf.fire.plot_file`, `plot_int`, `plot_per` | Controls the engine's fire plotfile |
| `erf.fire.fire_debug` | Prints per-step coupling diagnostics |

Each engine reads its own inputs under its own prefix; `fire.<engine>.*` is
recommended.

## Implementing a fire engine

An engine derives from `FireEngine` (`Source/FireCoupling/ERF_FireEngine.H`) and
registers itself in a `.cpp` file compiled as source:

```cpp
ERF_REGISTER_FIRE_ENGINE(MyEngine, "my_fire")
```

| Required method | Purpose |
|---|---|
| `name` | Returns the engine's name |
| `verify_prerequisites` | Checks the mesh and inputs at start-up |
| `initialize` | Sets up the engine on the fire grid |
| `advance` | Advances the fire over one step |
| `fill_fluxes` | Returns the sensible and latent fluxes, averaged over that step |
| `smoke_heat_per_kg` | Heat released per kilogram of fuel burned |

Optional methods cover checkpoint and plotfile output, surface precipitation, the
surface-layer requirement, building open fraction and roof height, and fields
offered to other surface models. An engine that keeps the default
`read_checkpoint` stops a restarted run with an explanatory message.

An engine directory contains `ERFFireEngine.cmake` for CMake and `Make.package`
for GNU make. To start a new engine, copy the example engine,
[`Tests/FireEngineExample` in FLARE](https://github.com/erf-model/FLARE/tree/development/Tests/FireEngineExample),
or ERF's template, then follow the sections "Adding a fire engine" and "The engine
contract" in the ERF documentation, which define the rules for fluxes, water and
GPU memory.
