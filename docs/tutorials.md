# Tutorials

**Status: placeholder.** No tutorial is written yet. The titles below are planned
and may change.

| Tutorial | You will learn to | Status |
|---|---|---|
| 1. Build the example engine | Build FLARE's `Tests/FireEngineExample` against the ERF submodule, run it, and find its output | To be written |
| 2. Write your own engine | Start a repository with ERF as a submodule, copy the example, register a new engine, and pass the restart check | To be written |
| 3. Run a FLARE fire | Build FLARE, run a small coupled fire, and read its diagnostics | To be written |

## Cases you can run now

Until the tutorials are written, these FLARE cases each have a README with the
setup, the commands and the expected results.

| Case in FLARE | What it shows | Kind |
|---|---|---|
| [`Structures/Exec/FireUnderLine`](https://github.com/erf-model/FLARE/tree/development/Structures/Exec/FireUnderLine) | A grass fire under three spans of conductor on two lattice towers, run with and without the fire's heat in the air; conductor and tower steel temperatures and the conductor sag. See [Fire and Transmission Lines](fire-and-transmission-lines.md). | Benchmark, with a CTest |
| [`Exec/CanonicalTests/Fire/Real_Terrain/Marshall_Fire`](https://github.com/erf-model/FLARE/tree/development/Exec/CanonicalTests/Fire/Real_Terrain/Marshall_Fire) | The 30 December 2021 Marshall Fire region: 25.6 km of SRTM1 terrain, a 35 m/s westerly, three ignitions and spotting. Scripts load the LANDFIRE fuel map and print HRRR winds for the event. | Demonstration: idealised wind, one fuel model, fire does not feed back on the air |
| [`Exec/CanonicalTests/Fire/Real_Terrain/Palisades_Fire`](https://github.com/erf-model/FLARE/tree/development/Exec/CanonicalTests/Fire/Real_Terrain/Palisades_Fire) | The 7 January 2025 Palisades Fire region: 24 km of SRTM1 terrain, a 30 m fire grid with its own elevation model under a 300 m atmosphere, chaparral to the shoreline, two-way coupling. | Demonstration: idealised wind, one fuel model |

The two real-terrain cases use public SRTM1 elevation data from NASA and the
USGS. They are not reconstructions of the events: neither is compared with the
observed fire perimeters.

## Layout of each tutorial

Each tutorial will have its own page, `docs/tutorial_<name>.md`, with these
sections:

1. **Title and short introduction:** what the case is and how long it takes to run.
2. **You will learn to / Before you start:** the skills covered and what must be
   built first.
3. **The physical problem:** the setup, and the known answer if there is one.
4. **The input file:** the deck, with its main inputs explained.
5. **Run the case:** the exact commands.
6. **Read the log:** what to look for.
7. **The output:** which files appear and what they hold.
8. **Compare with a reference:** a closed-form answer or published numbers.
9. **Next steps:** the next tutorial and related pages.
