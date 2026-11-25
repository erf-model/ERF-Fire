# Fire and Transmission Lines

FLARE couples its fire to a transmission line, so that a simulation can follow
how a wildland fire heats the conductors and the towers it passes under. The
line is FLARE's structure model, in the FLARE folder `Structures/`. It plugs
into ERF through ERF's structure coupling, the same way the fire plugs into
ERF's fire coupling.

| Part | What it does | Page |
|---|---|---|
| Conductors | Each conductor and shield wire is a MoorDyn-C line that moves in ERF's wind. Its temperature follows the heat balance of IEEE Std 738-2023, with the fire's radiation and the air the fire warms. The thermal sag follows from that temperature. | [Conductor lines in the wind](flare/Conductors.rst) |
| Towers | Each lattice tower is a finite-element frame. Its members heat as unprotected steel (EN 1993-1-2), and the frame is rebuilt as the steel softens. | [Lattice tower frame model](flare/TowerFrame.rst) |
| Coupling to ERF | ERF's structure coupling hands the model the wind, and since erf-model/ERF#5018 the fire's fields. It spreads the line's drag back into the air. | [Structure coupling in the ERF documentation](https://erf.readthedocs.io/en/latest/theory/StructureCoupling.html) |
| Build | FLARE builds the lines with `ERF_ENABLE_STRUCTURES`, against MoorDyn-C or a stub for tests. | [Coupling to MoorDyn](flare/CouplingToMoorDyn.rst) |
| Inputs | The `conductors.*` inputs for lines, towers, insulators and the thermal model. | [Conductor inputs](flare/ConductorInputs.rst) |

## Benchmark: a grass fire under a line

The benchmark is FLARE's case `Structures/Exec/FireUnderLine`. A grass fire
runs under three spans of Drake conductor hung on two lattice towers. The case
runs twice: once with the fire's heat put into the air, and once without it.
The comparison shows what the two-way coupling changes for the line.

| Result (MoorDyn-C, 4 ranks) | Fire heat in the air | Fire heat not in the air |
|---|---|---|
| Fire reaches the line | 6.3 min | 15.8 min |
| Middle span, hottest conductor (31.5 °C before) | **77.5 °C** | 51.1 °C |
| Middle span, largest added sag | 0.93 m | 0.56 m |
| Towers, hottest member steel | **116 °C** | 98 °C |

With the fire's heat in the air, the fire spreads faster and the plume brings
hot air to the line before the front arrives. Without it, the conductor's
temperature rise is 57 % smaller. The case is a demonstration on flat ground
with one fuel model, not a validation: no measured data of a fire under a line
are used. The [benchmark page](flare/FireUnderLine.rst) gives the setup, the
figures, an independent check of the peak temperatures and the limits.

The models and the data they use come from the work credited on the pages
below: Rothermel (1972), Anderson (1982) and Andrews (2012) for the fire;
IEEE Std 738-2023 for the conductor heat balance; and the JRC worked examples
for EN 1993-1-2 (Vassart et al. 2014) for the tower steel.

These pages are copied from the
[FLARE documentation](https://github.com/erf-model/FLARE/tree/development/Docs/sphinx_doc)
by `tools/sync_flare_docs.py`; edit them in FLARE and rerun the script.

```{toctree}
:maxdepth: 1

flare/FireUnderLine
flare/Conductors
flare/TowerFrame
flare/CouplingToMoorDyn
flare/ConductorInputs
```
