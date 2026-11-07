.. Copied from erf-model/FLARE Docs/sphinx_doc/Inputs.rst at 39e777bcc by
.. tools/sync_flare_docs.py. Edit the page in FLARE, then rerun the script.

.. _sec:FireInputs:

.. _inputs-fire-model:

Fire Model Inputs
=================

These inputs configure the fire model described in :ref:`sec:Fire`. Every
key is read once at startup from the ``erf.fire`` prefix (the three plotfile
keys from ``erf``). Defaults are those of the parameter struct in
``FireEngine/ERF_FireParams.H``; the reference deck
``Exec/CanonicalTests/Fire/inputs_fire_master_reference`` lists every key with
a comment but is a configured case, so its values are not all defaults. Keys
marked "read but not consumed" are accepted for compatibility and have no
effect at present.


Master control
--------------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.enable**                            | Enable the fire model                                      | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.engine**                            | Fire engine behind the shared fire-atmosphere coupling     | "flare"                        | "flare"                |
|                                                | (Source/FireCoupling); "flare" is FLARE, this repository's |                                |                        |
|                                                | own model (FireEngine/). Any other value aborts            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fire_debug**                        | Print per-step fire diagnostics to stdout                  | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.grid_ratio**                        | Fire grid refinement factor in x and y; every box length   | Integer > 0                    | 5                      |
|                                                | on the fire grid's level must divide by it                 |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.anchor_level**                      | AMR level whose grid the fire grid refines; -1 is the      | -1, or 0 to the finest level   | -1                     |
|                                                | finest level at start-up. Above level 0 the level must     |                                |                        |
|                                                | keep its boxes (erf.regrid_int = -1), cover one rectangle  |                                |                        |
|                                                | of full-height columns and run without the dust layer; a   |                                |                        |
|                                                | level below the finest prints a warning                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Fuel and moisture
-----------------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.fuel_model_id**                     | Anderson FBFM13 fuel model used everywhere without a fuel  | 1-13; 101-204 with fuel_set    | 1                      |
|                                                | map, and for WAF and coefficients with one                 | = scott_burgan40; 1000-1015    |                        |
|                                                |                                                            | custom codes; others abort     |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_1hr**                      | 1-hour dead fuel moisture [fraction]                       | Real 0-1                       | 0.08                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_10hr**                     | 10-hour dead fuel moisture [fraction]                      | Real 0-1                       | 0.08                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_100hr**                    | 100-hour dead fuel moisture [fraction]                     | Real 0-1                       | 0.10                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_live**                     | Live herbaceous and woody moisture [fraction]; the live    | Real                           | 0.60                   |
|                                                | classes start here (see moisture_live_model)               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_live_model**               | Live classes with moisture_dynamic: the legacy dead-fuel   | "legacy", "fixed"              | "legacy"               |
|                                                | update (a value above 0.40 drops to 0.40 on the first      |                                |                        |
|                                                | step) or held at moisture_live                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_dynamic**                  | Advance the dead classes each step with the Nelson time-   | Boolean                        | true                   |
|                                                | lag model                                                  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.precip_rate_mm_hr**                 | Uniform precipitation rate wetting the dead fuel [mm/hr]   | Real >= 0                      | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.precip_source**                     | Rain wetting the dead classes: precip_rate_mm_hr           | "uniform", "atmosphere"        | "uniform"              |
|                                                | everywhere, or each column's change per step of the        |                                |                        |
|                                                | microphysics surface precipitation accumulation (needs a   |                                |                        |
|                                                | scheme with precipitation, moisture_dynamic, and           |                                |                        |
|                                                | precip_rate_mm_hr = 0)                                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.moisture_model**                    | Dead-class update: one time constant per class, or radial  | "timelag", "stick"             | "timelag"              |
|                                                | diffusion in a cylindrical stick (Nelson 2000 framework)   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.emc_model**                         | Equilibrium moisture curves of the dead-class update: the  | "legacy", "van_wagner"         | "legacy"               |
|                                                | legacy quartics, or Van Wagner and Pickett (1985) drying   |                                |                        |
|                                                | and wetting EMC (temperature dependent, as in WRF-SFIRE)   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.stick.n_shells**                    | Radial shells per stick                                    | Integer 1-16                   | 6                      |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.stick.radius_cm**                   | Stick radii of the 1-h, 10-h and 100-h classes [cm]        | 3 Reals > 0                    | 0.15 0.635 2.5         |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.stick.rain_surface_moisture**       | Surface moisture held while it rains                       | Real 0.01-0.40                 | 0.35                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.stick.diffusivity_scale**           | Multiplier on the lag-calibrated diffusivity               | Real > 0                       | 1.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.file**                     | Spatial fuel map file; empty means uniform fuel. Rows of   | String                         | ""                     |
|                                                | an ESRI ASCII map run north first; one code per fire       |                                |                        |
|                                                | cell, so the map must have the fire grid's size            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.format**                   | Fuel map format                                            | "ascii", "lcp"                 | "ascii"                |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.blending_fraction**        | ROS blending toward neighbours of a different fuel code    | Real 0-1                       | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.nonburnable_codes**        | Fuel codes that are non-burnable; empty keeps the fall-    | Integers                       | none                   |
|                                                | through to fuel model 1                                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.fuel_set**                 | Fuel model set: the Anderson 13, or the Scott and Burgan   | "anderson13",                  | "anderson13"           |
|                                                | 40 (LANDFIRE FBFM40 codes 101-204, 91-99 non-burnable)     | "scott_burgan40"               |                        |
|                                                | alongside them                                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.sb40_crosswalk**           | Translate the Scott-Burgan codes to the Anderson 13 at     | Boolean                        | false                  |
|                                                | load (the CFBM route) instead of using them natively       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fuel_map.load_from_map**            | Start each cell with its own model's fuel load instead of  | Boolean                        | false                  |
|                                                | the uniform model's                                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.rothermel_per_fuel**                | Evaluate Rothermel coefficients per cell from the fuel map | Boolean                        | false                  |
|                                                | instead of fuel_model_id, on the isotropic and the         |                                |                        |
|                                                | level-set paths alike                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.codes**                 | Fuel codes described in the deck instead of a published    | Ints                           | none                   |
|                                                | set; each must be in 1000-1015                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.name**                | Label for code N in the start-up summary                   | String                         | custom_N               |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.w_1h_kg_m2**          | 1-h dead fuel load of code N [kg/m2]; at least one load    | Real in [0, 500]               | required               |
|                                                | must be > 0                                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.w_10h_kg_m2**         | 10-h dead fuel load [kg/m2]                                | Real in [0, 500]               | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.w_100h_kg_m2**        | 100-h dead fuel load [kg/m2]                               | Real in [0, 500]               | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.w_live_herb_kg_m2**   | Live herbaceous load [kg/m2]; no curing transfer is        | Real in [0, 500]               | 0.0                    |
|                                                | applied                                                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.w_live_woody_kg_m2**  | Live woody load [kg/m2]                                    | Real in [0, 500]               | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.sav_1h_1_m**          | 1-h dead surface-area-to-volume ratio [1/m]                | Real in [10, 12000]            | required               |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.sav_live_herb_1_m**   | Live herbaceous surface-area-to-volume ratio [1/m]; kept   | Real in [10, 12000]            | sav_1h_1_m             |
|                                                | only where that load is > 0                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.sav_live_woody_1_m**  | Live woody surface-area-to-volume ratio [1/m]; kept only   | Real in [10, 12000]            | sav_1h_1_m             |
|                                                | where that load is > 0                                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.depth_m**             | Fuel bed depth [m]; the Balbi models return zero spread at | Real in (0.01, 50]             | required               |
|                                                | or below 0.01 m                                            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.moisture_ext**        | Moisture of extinction [fraction]                          | Real in [0.01, 2]              | required               |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.heat_content_J_kg**   | Heat content [J/kg]                                        | Real in [5e6, 5e7]             | required               |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.density_kg_m3**       | Fuel particle density [kg/m3]                              | Real in [50, 2000]             | 512.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.custom_fuel.N.burnout_time_s**      | Flaming burn time [s]; required for code N when            | Real in [0, 1e5]               | 0.0                    |
|                                                | erf.fire.burnout_model = sfire                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.firebreak.N.type**                  | Firebreak N (N = 0..9, consecutive): shape                 | "rect", "circle"               | none                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.firebreak.N.x_lo/y_lo/x_hi/y_hi**   | Rectangle firebreak bounds [m]                             | Reals                          | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.firebreak.N.cx/cy/radius**          | Circular firebreak centre and radius [m]                   | Reals                          | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.firebreak.use_mask**                | Hold firebreak cells in the non-burnable mask as well as   | Boolean                        | true                   |
|                                                | stamping the sentinel; false (the form before 2026-10)     |                                |                        |
|                                                | warns when firebreaks are configured, since the stamp can  |                                |                        |
|                                                | erode                                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.enable**                 | Treat cells of the structure heightmap above min_height as | Boolean                        | false                  |
|                                                | non-burnable                                               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.file**                   | Building heightmap in ERF terrain text format              | String                         | hybrid.structure_file, |
|                                                |                                                            |                                | then erf.buildings_fil |
|                                                |                                                            |                                | e_name                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.min_height**             | Sampled height above which a cell is a structure [m]       | Real >= 0                      | 0.5                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.wind_open_columns**      | Renormalise the bilinear wind weights over the columns open| Boolean                        | false                  |
|                                                | at the wind height; needs structures.enable                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.enable**        | Structures ignite from the exposure accumulators, burn,    | Boolean                        | false                  |
|                                                | radiate and launch brands (:ref:`sec:WUIStructureIgnition`)|                                |                        |
|                                                | ; needs exposure.enable                                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.heat_load_J_m2**| Largest accumulated heat load in the wall band at which a  | Real; <= 0 turns the criterion | 6.0e6                  |
|                                                | structure ignites [J/m2]                                   | off                            |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.ember_count**   | Brands landed on the footprint at which a structure        | Integer; <= 0 turns the        | 50                     |
|                                                | ignites                                                    | criterion off                  |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.intensity_kW_m**| Fireline intensity in the wall band above which time       | Real; <= 0 turns the criterion | 1000.0                 |
|                                                | counts toward residence_s [kW/m]                           | off                            |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.residence_s**   | Time above intensity_kW_m at which a structure ignites [s] | Real >= 0                      | 60.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.peak_flux_W_m2**| Peak heat release of a burning structure per unit          | Real > 0                       | 2.5e5                  |
|                                                | footprint area [W/m2]                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.fuel_load_J_m2**| Heat a structure releases over its whole burn per unit     | Real > 0                       | 7.8e8                  |
|                                                | footprint area [J/m2]                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.growth_time_s** | Time from ignition to the peak flux (t-squared growth) [s];| Real >= 0; peak_flux_W_m2 *    | 600.0                  |
|                                                | 0 starts at the peak                                       | growth_time_s / 3 <= 0.7 *     |                        |
|                                                |                                                            | fuel_load_J_m2                 |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.rad_fraction**  | Share of the release radiated onto the cells around the    | Real in [0, 1]                 | 0.3                    |
|                                                | structure                                                  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.structures.ignition.rad_radius_m**  | Distance within which a burning footprint cell's radiation | Real >= 0; 0 turns the         | 100.0                  |
|                                                | is added to the heat load [m]                              | radiation off                  |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Ignition
--------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.ignition_x**                        | Ignition disc centre x [m]                                 | Real                           | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition_y**                        | Ignition disc centre y [m]                                 | Real                           | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition_r**                        | Ignition disc radius [m]; 0 = no disc (schedule, polygon,  | Real >= 0                      | 20.0                   |
|                                                | line or threshold ignites instead)                         |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.schedule_file**            | CSV of timed ignition events; empty disables               | String                         | ""                     |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.polygon_file**             | One or more CSVs of perimeter vertices, each one polygon   | List of Strings                | ""                     |
|                                                | or polyline ignition of the deck's polygon_type and        |                                |                        |
|                                                | polyline_width; every file is stamped, so several files    |                                |                        |
|                                                | are several fires that merge as they grow                  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.polygon_type**             | Closed polygon or open line fire                           | "polygon", "polyline"          | "polygon"              |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.polygon_time**             | Time [s] at which the polygon is stamped, so the           | Real >= 0                      | 0.0                    |
|                                                | atmosphere spins up first; 0 stamps it at initialisation   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.polygon_interior_ros**     | Spread rate [m/s] behind the interior: arrival time        | Real >= 0                      | 0.0                    |
|                                                | polygon_time - d/R and fuel exp(-d/(R tau)); 0 = off       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.polygon_interior_tau**     | Burnout e-folding time [s] of the interior; 0 = dx_fire/R  | Real >= 0                      | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.polyline_width**           | Half-width of the polyline ignition zone [m]               | Real > 0                       | 10.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.threshold_enable**         | Ignite every burnable, unburned fire cell whose k = 0 air  | true, false                    | false                  |
|                                                | temperature (theta times the Exner function) exceeds       |                                |                        |
|                                                | threshold_temp                                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.threshold_temp**           | Ignition temperature [K]                                   | Real > 0                       | 573.15                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.threshold_radius**         | Radius [m] of the disc stamped around each hot cell;       | Real >= 0                      | 0.0                    |
|                                                | 0 = one fire cell                                          |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.ignition.threshold_start_time**     | No threshold ignition before this time [s]                 | Real >= 0                      | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Wind
----

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.wind_ref_ht**                       | Height above local ground at which the atmospheric wind is | Real > 0                       | 6.1                    |
|                                                | sampled [m]                                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_wind**                   | Bypass atmospheric wind interpolation with a constant      | Boolean                        | false                  |
|                                                | reference wind, for controlled idealized-wind test cases;  |                                |                        |
|                                                | exact everywhere only with use_waf = false and             |                                |                        |
|                                                | use_terrain_wind = false                                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_wind_x**                 | Constant reference wind, x, when prescribed_wind [m/s]     | Real                           | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_wind_y**                 | Constant reference wind, y, when prescribed_wind [m/s]     | Real                           | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.use_per_fuel_wind_ht**              | Sample the wind at the per-fuel fcwh height (6.096 m for   | Boolean                        | false                  |
|                                                | every fuel) instead of wind_ref_ht, with or without a      |                                |                        |
|                                                | fuel map; every reader of the wind's height follows it     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.wind_sample_ht**                    | Sample the wind at this height above ground and bring it   | Real > wind_ref_ht (6.096 with | 0.0                    |
|                                                | to wind_ref_ht (6.096 m with use_per_fuel_wind_ht) with a  | use_per_fuel_wind_ht), or 0    |                        |
|                                                | log profile (CFBM); 0 = off                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.wind_sample_z0**                    | Roughness length [m] of every log profile the fire reads:  | 0 < Real < wind_ref_ht, or     | 0.1                    |
|                                                | the two-height resampling, the wind below the first cell   | < 6.096 with                   |                        |
|                                                | centre and the ember drift; below the height of the        | use_per_fuel_wind_ht           |                        |
|                                                | reference wind, which is 6.096 m with use_per_fuel_wind_ht |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.wind_below_first_cell**             | Wind at a target below the first cell centre: "clamp"      | "clamp", "log"                 | "clamp"                |
|                                                | takes the centre's wind unchanged; "log" scales it by the  |                                |                        |
|                                                | neutral log profile of wind_sample_z0 (recommended for a   |                                |                        |
|                                                | first cell above wind_ref_ht; 12 % lower under a 20 m      |                                |                        |
|                                                | first cell)                                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.wind_interp**                       | Horizontal mapping of atmospheric columns onto fire cells  | "bilinear", "nearest"          | "bilinear"             |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.use_waf**                           | Apply the wind adjustment factor to the reference wind     | Boolean                        | true                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.waf_formula**                       | Wind adjustment factor formula, from the fuel bed depth:   | "andrews", "behaviorplus"      | "andrews"              |
|                                                | the domain model's on a uniform fuel, each cell's own      |                                |                        |
|                                                | wherever a spatial fuel map is read                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.use_wind_limit**                    | Bound the midflame wind by Rothermel's (1972, eq. 87)      | Boolean                        | true                   |
|                                                | limit U <= 0.9 I_R (Rothermel and BEHAVE kernels); false:  |                                |                        |
|                                                | no limit                                                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.wind_limit**                        | Which limit use_wind_limit applies: "rothermel" is 0.9 I_R | "rothermel",                   | "rothermel"            |
|                                                | ft/min; "fuel_class" this code's earlier rule of 300 ft/min| "fuel_class"                   |                        |
|                                                | above a SAV of 1000 1/ft and 500 below (the form before    |                                |                        |
|                                                | 2026-10)                                                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.use_terrain_wind**                  | Apply the terrain wind factors (ridge, shelter, valley,    | Boolean                        | false                  |
|                                                | deflection); default false since 2026-10                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.k_ridge**                           | Ridge speed-up factor (needs use_terrain_wind = true)      | Real > 0                       | 1.5                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.k_shelter**                         | Lee sheltering factor                                      | Real > 0                       | 0.6                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.k_valley**                          | Valley channelling factor                                  | Real > 0                       | 0.8                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.k_deflect**                         | Wind deflection factor                                     | Real > 0                       | 0.3                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.terrain_file_name**                 | Fine-grid terrain file interpolated onto the fire grid for | String                         | ""                     |
|                                                | slopes                                                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Rate of spread
--------------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.ros_model**                         | Rate-of-spread model; "grass_simple" is the fit that       | "rothermel", "behave",         | "rothermel"            |
|                                                | "cheney_gould" selected before 2026-10                     | "macarthur", "cheney_gould",   |                        |
|                                                |                                                            | "grass_simple", "fbp",         |                        |
|                                                |                                                            | "balbi", "hybrid",             |                        |
|                                                |                                                            | "prescribed"                   |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.rothermel_cell_moisture**           | With moisture_dynamic, rebuild the Rothermel coefficients  | Boolean                        | true                   |
|                                                | from each cell's own dead moistures; false takes the       |                                |                        |
|                                                | domain-mean moistures everywhere (the form before 2026-10) |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.macarthur.ros_max**                 | Cap on the McArthur rate [m/s] (WRF-Fire's 6 m/s); 0       | Real >= 0                      | 6.0                    |
|                                                | removes it. The exponent is bounded at 40 in every         |                                |                        |
|                                                | case, so an uncapped rate stops growing at a 47.5 m/s      |                                |                        |
|                                                | midflame wind (4e16 m/s, finite, long past physical)       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.reaction_velocity_formula**         | Rothermel's reaction-velocity exponent A: Albini's (1976)  | "albini", "rothermel"          | "albini"               |
|                                                | revision, A = 133 sigma^-0.7913 (ERF's form so far), or    |                                |                        |
|                                                | Rothermel's (1972) Eq. 39, A = 1/(4.774 sigma^0.1 - 7.27), |                                |                        |
|                                                | the form WRF-Fire uses. Only A changes, and through I_R    |                                |                        |
|                                                | the default wind limit 0.9 I_R (wind_limit = rothermel).   |                                |                        |
|                                                | Read by every run that evaluates Rothermel (ros_model =    |                                |                        |
|                                                | rothermel, or a hybrid with a rothermel member); BEHAVE    |                                |                        |
|                                                | keeps its own Albini form; other models ignore it with a   |                                |                        |
|                                                | warning                                                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.wrf_bmst_compat**                   | WRF-Fire comparison: deflate the fuel load fed to the      | Boolean                        | false                  |
|                                                | Rothermel coefficients by 1 - M/(1+M), M the dead-load-    |                                |                        |
|                                                | weighted dead moisture, as WRF-Fire does to its load. Not  |                                |                        |
|                                                | a physical correction (ERF's loads are oven-dry) and not   |                                |                        |
|                                                | full WRF-Fire parity (bed SAV, net load, heat content and  |                                |                        |
|                                                | wind/rate caps differ); fuel consumption and heat release  |                                |                        |
|                                                | keep the full load. Through I_R it lowers the default wind |                                |                        |
|                                                | limit 0.9 I_R too. Same readers as the row above           |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.directional_ros**                   | Evaluate the rate along the front normal on the level-set  | Boolean                        | true                   |
|                                                | path; false spreads the head rate in every direction       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.directional_shape**                 | Form of that rate: the model along the front normal, or    | "projection", "ellipse"        | "projection"           |
|                                                | the support function of the ellipse with the model's head, |                                |                        |
|                                                | back and flank rates, which keeps a point fire's head at   |                                |                        |
|                                                | the head rate; not for balbi or hybrid                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.directional_wind_coupling**         | With directional_shape = "projection": exponentiate the    | "projection", "advective"      | "projection"           |
|                                                | wind/slope factor from the projected wind (Rothermel's own |                                |                        |
|                                                | form), or from the raw wind and scale by the cosine to the |                                |                        |
|                                                | front normal afterward (matching WRF-Fire's fire_ros),     |                                |                        |
|                                                | which keeps a point or finite-line fire's head at the head |                                |                        |
|                                                | rate; needs ros_model = rothermel                          |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.directional_split_hamiltonian**     | With directional_wind_coupling = advective: upwind the     | true, false                    | false                  |
|                                                | isotropic term and the wind and slope terms of the level-  |                                |                        |
|                                                | set Hamiltonian separately, each advective term by the     |                                |                        |
|                                                | sign of its own velocity, instead of one front-normal      |                                |                        |
|                                                | flux; removes the grid-orientation dependence at oblique   |                                |                        |
|                                                | wind angles; needs ros_model = rothermel                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.directional_ellipse_lw**            | Flank rate of that ellipse: the model's no-wind, no-slope  | "model", "anderson"            | "model"                |
|                                                | rate, or b over Anderson's (1983) length-to-width ratio at |                                |                        |
|                                                | the effective wind speed; head and back unchanged; needs   |                                |                        |
|                                                | directional_shape = "ellipse"                              |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.directional_ellipse_lw_max**        | Cap on that Anderson ratio (the fit itself saturates at 8) | Real >= 1                      | 8.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed.ros**                    | Rate of spread for ros_model = prescribed where by_fuel    | Real >= 0                      | 0.0                    |
|                                                | has no entry; no wind, slope or moisture dependence, and   |                                |                        |
|                                                | directional_ros is turned off [m/s]                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed.gradient**               | Gradient of the prescribed rate, dR/dx and dR/dy [1/s]     | Two Reals                      | 0.0 0.0                |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed.origin**                 | Point where the prescribed rate equals its base value [m]  | Two Reals                      | 0.0 0.0                |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed.min_ros**                | Floor on the prescribed rate [m/s]                         | Real >= 0                      | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed.by_fuel**                | Flat list of fuel code and base rate pairs overriding      | Reals                          | none                   |
|                                                | prescribed.ros per cell; needs fuel_map.file               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.cheney_gould.moisture**             | Cheney-Gould dead fine fuel moisture [%]                   | Real 1-40                      | 10.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.cheney_gould.curing**               | Cheney-Gould degree of curing                              | Real 0-1                       | 1.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.cheney_gould.pasture**              | Cheney-Gould pasture coefficients                          | "natural", "grazed"            | "natural"              |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.cheney_gould.curing_curve**         | Curing coefficient: Cruz et al. (2015) or Cheney et al.    | "cruz2015",                    | "cruz2015"             |
|                                                | (1998)                                                     | "cheney1998"                   |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.cheney_gould.wind_source**          | Wind the 1998 model reads: the reference wind at           | "reference",                   | "reference"            |
|                                                | wind_ref_ht (set it to 10 m) or the WAF-reduced midflame   | "midflame"                     |                        |
|                                                | wind                                                       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.fuel_type**                     | Canadian FBP fuel type (ros_model = fbp)                   | C1-C7, D1, M1-M4, S1-S3,       | "C2"                   |
|                                                |                                                            | O1A, O1B                       |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.ffmc**                          | Fine Fuel Moisture Code                                    | Real 0-101                     | 90.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.bui**                           | Buildup Index                                              | Real >= 0                      | 60.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.curing**                        | Degree of curing of the grass types [%]                    | Real 0-100                     | 60.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.pc**                            | Percent conifer of M1 and M2                               | Real 0-100                     | 50.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.pdf**                           | Percent dead fir of M3 and M4                              | Real 0-100                     | 50.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.use_slope**                     | Slope through the system's equivalent wind                 | Boolean                        | true                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fbp.wind_source**                   | The reference-height wind (set wind_ref_ht = 10) or the    | "reference", "midflame"        | "reference"            |
|                                                | midflame wind after the Wind Adjustment Factor             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.behave.dynamic_transfer_lo**        | BEHAVE live herbaceous moisture [fraction] at and below    | Real < dynamic_transfer_hi     | 0.30                   |
|                                                | which the whole live herbaceous load transfers to dead,    |                                |                        |
|                                                | with a linear share up to dynamic_transfer_hi. Acts only   |                                |                        |
|                                                | on fuels with a live herbaceous load                       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.behave.dynamic_transfer_hi**        | BEHAVE live herbaceous moisture [fraction] at and above    | Real > dynamic_transfer_lo     | 1.20                   |
|                                                | which none transfers; the share is (hi - M)/(hi - lo),     |                                |                        |
|                                                | clamped to [0,1]. Aborts unless greater than               |                                |                        |
|                                                | dynamic_transfer_lo                                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.behave.net_load**                   | Net fuel load of a BEHAVE category: "weighted" is          | "weighted", "sum"              | "weighted"             |
|                                                | Rothermel's surface-area-weighted load with Albini's size  |                                |                        |
|                                                | classes; "sum" the plain sum of the classes (the form      |                                |                        |
|                                                | before 2026-10, 3.3x FM10's reaction intensity)            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Balbi model
-----------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.balbi.formulation**                 | Steady explicit 2009 form or convective-radiative 2020     | "2009", "2020"                 | "2009"                 |
|                                                | form                                                       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.T_a**                         | Ambient temperature [K]                                    | Real                           | 300.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.T_f**                         | Mean flame temperature [K], 2009 form                      | Real                           | 1000.0                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.T_i**                         | Ignition temperature [K]                                   | Real                           | 600.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.delta_H**                     | Latent heat of vaporisation [J/kg]                         | Real                           | 2.26e6                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.C_pf**                        | Specific heat of dry fuel [J/(kg K)]                       | Real                           | 1800.0                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.r_00**                        | Radiation length scale [m]                                 | Real                           | 2.5e-4 (2009), 2.5e-5  |
|                                                |                                                            |                                | (2020)                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.tau_0**                       | Residence time coefficient [s/m]                           | Real                           | 75591.0                |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.chi_0**                       | Radiant fraction, 2020 form                                | Real                           | 0.3                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.C_pa**                        | Specific heat of air [J/(kg K)], 2020 form                 | Real                           | 1150.0                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.C_pw**                        | Specific heat of water [J/(kg K)], 2020 form               | Real                           | 4180.0                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.T_vap**                       | Water vaporisation temperature [K], 2020 form              | Real                           | 373.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.K1**                          | Convective decay coefficient, 2020 form                    | Real                           | 130.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.st**                          | Stoichiometric air to pyrolysis-gas ratio, 2020 form       | Real                           | 17.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.rho_a**                       | Air density [kg/m3], 2020 form                             | Real                           | 1.2                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.sigma_B**                     | Stefan-Boltzmann constant [W/(m2 K4)], 2020 form           | Real > 0                       | 5.670374e-8            |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.max_iter**                    | Root-solve iteration cap, 2020 form                        | Integer >= 1                   | 40                     |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.tol**                         | Root-solve bracket width [m/s], 2020 form                  | Real > 0                       | 1.0e-4                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.directional**                 | Direction-dependent Balbi spread on the level-set path     | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.use_surface_temp**            | Take the ambient temperature per cell from the atmosphere  | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.flame_temp_from_combustion**  | Derive the 2009 flame temperature from the combustion      | Boolean                        | false                  |
|                                                | energy                                                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.use_cell_moisture**           | Take the fuel moisture per cell from the moisture model    | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.use_moisture_extinction**     | Zero the rate at and above the fuel model's moisture of    | Boolean                        | false                  |
|                                                | extinction                                                 |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.herb_curing**                 | Fraction of live herbaceous load carried as cured dead     | Real 0-1                       | 0.0                    |
|                                                | fuel, 2020 form                                            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.wind_source**                 | Wind consumed by the model                                 | "midflame", "reference"        | "midflame"             |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.heat_flux_coupling**          | Add the fire-induced vertical velocity from the surface    | Boolean                        | false                  |
|                                                | heat flux                                                  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.k_upward**                    | Scale on the induced velocity                              | Real                           | 1.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.balbi.hf_ref_height**               | Reference height for the induced velocity [m]              | Real                           | 10.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Hybrid model
------------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.hybrid.primary**                    | Model used where the weight is 0                           | a member model; see theory     | "rothermel"            |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.secondary**                  | Model used where the weight is 1                           | a member model; see theory     | "balbi"                |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.selector**                   | How the per-cell weight is set                             | "region", "fuel", "structure", | "region"               |
|                                                |                                                            | "wind"                         |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.region**                     | Rectangle x_lo y_lo x_hi y_hi [m] taking the secondary     | 4 Reals                        | required               |
|                                                | model (selector = region)                                  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.blend_width**                | Linear ramp width across the region or structure edge [m]  | Real >= 0                      | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.secondary_fuel_codes**       | Fuel codes taking the secondary model (selector = fuel)    | Integers                       | required               |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.structure_file**             | Building heightmap in ERF terrain text format (selector =  | String                         | erf.buildings_file_nam |
|                                                | structure)                                                 |                                | e                      |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.structure_min_height**       | Sampled height above which a cell is a structure [m]       | Real                           | 0.5                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.structure_distance**         | Distance from a structure within which the secondary       | Real >= 0                      | 10.0                   |
|                                                | applies [m]                                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.wind_lo**                    | Effective wind speed at and below which the weight is 0    | Real                           | 8.0                    |
|                                                | [m/s] (selector = wind)                                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.hybrid.wind_hi**                    | Effective wind speed at and above which the weight is 1    | Real > wind_lo                 | 12.0                   |
|                                                | [m/s]                                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Propagation
-----------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.propagation_method**                | Front propagation scheme                                   | "farsite", "levelset"          | "farsite"              |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.phi_threshold**             | Legacy update: level-set value at or below which a cell    | Real                           | 0.1                    |
|                                                | is a front cell                                            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.use_anderson_lw**           | Derive the ellipse coefficients from the Anderson length-  | 0, 1                           | 1                      |
|                                                | to-width ratio                                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.coeff_a**                   | Richards head coefficient when use_anderson_lw = 0 (the    | Real > 0                       | 0.5                    |
|                                                | rectangle's head rate a R; with farsite.shape = ellipse    |                                |                        |
|                                                | only the ratio (a + c) / (2 b) is read, as the length-to-  |                                |                        |
|                                                | width ratio)                                               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.coeff_b**                   | Richards flank coefficient when use_anderson_lw = 0 (the   | Real > 0                       | 0.25                   |
|                                                | rectangle's flank rate b R; ellipse: see coeff_a)          |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.coeff_c**                   | Richards backing coefficient when use_anderson_lw = 0 (the | Real > 0                       | 0.1                    |
|                                                | rectangle's back rate c R; the ellipse's back is R / HB of |                                |                        |
|                                                | the ratio, not c R)                                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.gaussian_sigma**            | Legacy update: stamp radius [m], < 0 single cell,          | Real                           | -1.0                   |
|                                                | 0 automatic, > 0 fixed Gaussian                            |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.cfl_fire**                  | CFL number of the FARSITE subcycle                         | Real > 0                       | 0.5                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.front_update**              | Front update: "front_cell" burns the unburned cells next   | "front_cell", "legacy"         | "front_cell"           |
|                                                | to the burned region at their Hopf-Lax arrival times;      |                                |                        |
|                                                | "legacy" is the stamping used before 2026-09, which        |                                |                        |
|                                                | ran about twice the rate of spread                         |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.farsite.shape**                     | Spread shape of the front-cell update: the Richards (1990) | "ellipse", "rectangle"         | "ellipse"              |
|                                                | ellipse with Alexander's head-to-back ratio, or the        |                                |                        |
|                                                | rectangle of the Richards coefficients read as a support   |                                |                        |
|                                                | function (the shape before 2026-10, head/back ratio 5)     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.cfl**                      | CFL number of the level-set subcycle, dt = cfl h / R_max.  | Real > 0                       | 0.4                    |
|                                                | Start-up aborts when it makes the substep unstable with    |                                |                        |
|                                                | the viscosity (see eps_visc). Without viscosity, on square |                                |                        |
|                                                | cells, the substep is stable up to cfl 0.888 with          |                                |                        |
|                                                | first-order differences and 1.015 with WENO5               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.eps_visc**                 | Artificial viscosity coefficient [m] away from the front:  | Real >= 0, below the stability | 0.4                    |
|                                                | a length, so the smoothing in cells is eps_visc / dx.      | limit                          |                        |
|                                                | Start-up aborts, naming the largest stable eps_visc and    |                                |                        |
|                                                | cfl, when the substep is unstable for any front direction  |                                |                        |
|                                                | (a von Neumann scan of the RK3 substep; see the theory     |                                |                        |
|                                                | page). On square cells at cfl 0.4 the limit is 0.432 dx    |                                |                        |
|                                                | with first-order differences (gradient "upwind" or         |                                |                        |
|                                                | "weno5z_front") and 0.597 dx with "weno5z", so the default |                                |                        |
|                                                | 0.4 m aborts on fire cells finer than 0.927 m; set         |                                |                        |
|                                                | eps_visc to about 0.4 dx there                             |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.gradient**                 | One-sided derivatives of the level set: first-order        | "upwind" / "weno5z" /          | "weno5z_front"         |
|                                                | everywhere, HJ-WENO5-Z everywhere, or HJ-WENO5-Z within    | "weno5z_front"                 |                        |
|                                                | the front band and first order elsewhere (WRF-Fire)        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.weno_band_cells**          | Half-width of the front band, in fire cells, that uses     | Integer > 0                    | 4                      |
|                                                | WENO with "weno5z_front"                                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.eps_visc_front**           | Artificial viscosity within visc_front_cells of the front  | Real; when >= 0, below the     | 0.1                    |
|                                                | (WRF-Fire fire_viscosity_bg); negative keeps eps_visc      | stability limit                |                        |
|                                                | everywhere. Checked at start-up like eps_visc: with WENO5  |                                |                        |
|                                                | inside the WENO band of "weno5z_front" (0.597 dx at cfl    |                                |                        |
|                                                | 0.4, so the default 0.1 m aborts on fire cells finer than  |                                |                        |
|                                                | 0.168 m), and with first-order differences for the value   |                                |                        |
|                                                | just beyond the band when that is larger than eps_visc (a  |                                |                        |
|                                                | band that ends inside visc_front_cells or inside the       |                                |                        |
|                                                | blend)                                                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.visc_front_cells**         | Half-width, in fire cells, of the near-front viscosity     | Integer >= 0                   | 2                      |
|                                                | band (WRF-Fire fire_viscosity_ngp)                         |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.visc_transition_cells**    | Width, in fire cells, of the linear blend from             | Real >= 0                      | 2.0                    |
|                                                | eps_visc_front to eps_visc beyond that band (WRF-Fire      |                                |                        |
|                                                | blends over fire_viscosity_band x fire_viscosity_ngp       |                                |                        |
|                                                | cells, 1 cell with its defaults)                           |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.reinit_every**             | Reinitialise every N subcycles                             | Integer > 0                    | 5                      |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.reinit_iters**             | Outer RK3 pseudo-time steps per reinitialisation; 0 skips  | Integer >= 0                   | 1                      |
|                                                | the reinitialisation and its final clamp (see              |                                |                        |
|                                                | reinit_clamp)                                              |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.reinit_dtau**              | Reinitialisation pseudo-timestep [m]; <= 0 selects 0.01 dx | Real                           | -1.0                   |
|                                                | (WRF-Fire's value) for both schemes                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.reinit_scheme**            | Reinitialisation scheme: WRF-Fire's reinit_ls_rk3, or      | "wrf", "jiang_peng"            | "wrf"                  |
|                                                | Jiang and Peng's (2000) HJ-WENO5 with SSP-RK3              |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.reinit_clamp**             | Reference of the reinitialisation's final clamp phi =      | "step_start", "post_advection" | "step_start"           |
|                                                | min(phi, phi_ref), "the burned area only grows": the level |                                |                        |
|                                                | set at the start of the subcycle that ends with the        |                                |                        |
|                                                | reinitialisation, before its advection (WRF-Fire's), or    |                                |                        |
|                                                | the advected field the reinitialisation starts from (the   |                                |                        |
|                                                | form before 2026-10, which never lets a too-steep burned   |                                |                        |
|                                                | side relax and moves the front forward). No effect with    |                                |                        |
|                                                | reinit_iters = 0                                           |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.reinit_jp_sign_eps2**      | jiang_peng only: term added to phi0^2 under the            | Real                           | -1.0                   |
|                                                | smoothed-sign square root; <= 0 selects dx^2               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.wall_extrapolate**         | Extrapolate the level set into non-burnable cells inside   | Boolean                        | false                  |
|                                                | every stencil, so a masked wall is a zero-gradient boundary|                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.mask_mode**                | Non-burnable cells: "wall" holds them at phi >= 0 with a   | "wall", "wrf"                  | "wall"                 |
|                                                | wall stencil, "wrf" (as WRF-Fire) only zeroes their rate   |                                |                        |
|                                                | (split Hamiltonian path): no hold, no wall stencil,        |                                |                        |
|                                                | reinitialisation acts on every cell                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.ellipse**                  | Spread as a Huygens ellipse set by the midflame wind       | Boolean                        | false                  |
|                                                | (FARSITE family); turns the directional_ros default off,   |                                |                        |
|                                                | and cannot be combined with an explicit true               |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.ellipse_lw**               | Fixed length-to-width ratio of that ellipse; 0 = Anderson  | Real >= 0                      | 0.0                    |
|                                                | (1983) from the wind                                       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.levelset.ellipse_lw_max**           | Cap on the length-to-width ratio                           | Real >= 1                      | 8.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.enable**                      | Startup acceleration of the rate of spread                 | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.use_temporal**                | Temporal per-cell model instead of the size-based model    | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.L_acc**                       | Size-based acceleration length scale [m]                   | Real > 0                       | 50.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.A_point**                     | Temporal acceleration constant, point fire [1/min]         | Real > 0                       | 0.115                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.A_line**                      | Temporal acceleration constant, line fire [1/min]          | Real > 0                       | 0.886                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.perim_limit**                 | Perimeter length separating point and line fires [m]       | Real > 0                       | 500.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.enable_wind_lag**             | Exponential lag on wind increases (legacy clock only)      | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.tau_wind**                    | Wind-lag time constant [s]                                 | Real > 0                       | 60.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.accel.clock**                       | Clock of the temporal model: "legacy" per burned cell,     | String                         | "legacy"               |
|                                                | restarted when the cell burns and written to burned cells  |                                |                        |
|                                                | only; "front" from ignition, carried with the front and    |                                |                        |
|                                                | applied to the rate that moves it                          |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Heat flux and coupling
----------------------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.tau_residence_s**                   | Fixed residence time [s]; 0 derives it from the cell       | Real >= 0                      | 0.0                    |
|                                                | crossing time and fuel SAV                                 |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.burnout_model**                     | Fuel burnout e-folding time: the cell crossing time        | "residence", "sfire"           | "residence"            |
|                                                | floored by the particle time (residence) or WRF-SFIRE's    |                                |                        |
|                                                | burn time per fuel model / 0.8514 (sfire)                  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.burnout_times_s**                   | 13 burn times [s] for Anderson models 1-13 overriding the  | 13 Reals > 0                   | SFIRE table            |
|                                                | table (sfire)                                              |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.burnout_time_to_efold**             | Divisor turning a burn time into the e-folding time        | Real > 0                       | 0.8514                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.coupling_type**                     | Wind used by the fire and whether its heat is injected     | "passive", "lagged",           | "lagged"               |
|                                                |                                                            | "synchronous"                  |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.heat_flux_alfg**                    | E-folding height of the injected heat [m]                  | Real > 0                       | 45.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fire_atm_feedback**                 | Multiplier on the injected fluxes; 0 is one-way coupling   | Real >= 0                      | 1.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.inject_latent**                     | Inject the latent flux into the vapour equation when       | Boolean                        | true                   |
|                                                | moisture is active                                         |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.heat_flux_partition**               | Sensible flux handed to the atmosphere: the full heat      | "legacy", "cfbm"               | "legacy"               |
|                                                | release (legacy) or the CFBM dry-fuel share 1/(1+M_f)      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_heat.flux**              | Constant sensible heat flux added to the fire heat flux    | Real >= 0                      | 0.0                    |
|                                                | over a disc, whatever the fuel and front; injected like    |                                |                        |
|                                                | fire heat; 0 is off [W/m2]                                 |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_heat.center**            | Centre of the prescribed heat-flux disc [m]                | Two Reals                      | 0.0 0.0                |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_heat.radius**            | Radius of the prescribed heat-flux disc [m]                | Real > 0 when flux > 0         | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_heat.start_time**        | Time the prescribed heat flux switches on [s]              | Real                           | 0.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.prescribed_heat.end_time**          | Time it switches off [s]; negative keeps it on             | Real                           | -1.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.source_mode**                       | Replace the theta and vapour source slots (legacy) or add  | "overwrite", "add"             | "overwrite"            |
|                                                | to the rebuilt stage source. Left at the default with      |                                |                        |
|                                                | another theta source on the fire level (radiation,         |                                |                        |
|                                                | Rayleigh damping of T, custom forcing or subsidence,       |                                |                        |
|                                                | immersed forcing) the run stops: set it explicitly         |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.heat_open_fraction**                | Place injected heat only in the open part of columns with  | Boolean                        | false                  |
|                                                | structures; needs structures.enable                        |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.heat_tendency_density**             | Restore the historical density factor in the injected      | Boolean                        | false                  |
|                                                | tendency (injects rho times the flux); false is energy-    |                                |                        |
|                                                | consistent                                                 |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.heat_tendency_exner**               | Divide the rho theta tendency by the cell's Exner function | Boolean                        | false                  |
|                                                | so the column enthalpy integrates to the fire flux; false  |                                |                        |
|                                                | (WRF-SFIRE's form) injects Pi times the flux, 4.5 % short  |                                |                        |
|                                                | at 850 hPa                                                 |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.smoke_enable**                      | Add the passive smoke tracer                               | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.smoke_emission_factor**             | Smoke mass per unit fuel burned [kg/kg]                    | Real >= 0                      | 0.02                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.smoke_heat_of_comb**                | Heat of combustion used to convert flux to fuel burned     | Real > 0                       | 1.87e7                 |
|                                                | [J/kg]                                                     |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.smoke_heat_from_fuel**              | Convert the flux to fuel burned with the fuel model's own  | Boolean                        | false                  |
|                                                | heat content instead of smoke_heat_of_comb (CFBM parity)   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Spotting
--------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.spotting.enable**                   | Albini ember spotting                                      | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.I_B_min**                  | Minimum Byram intensity to loft a brand [kW/m]             | Real > 0                       | 100.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.P_base**                   | Launch probability per front cell per application          | Real 0-1                       | 0.01                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.terminal_velocity**        | Brand terminal fall velocity [m/s]                         | Real > 0                       | 0.5                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.n_traj_steps**             | Forward-Euler sub-steps along the trajectory               | Integer > 0                    | 20                     |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.launch_from**              | Cells that may launch a brand: every burned cell, or only  | "burned", "front"              | "burned"               |
|                                                | those with unburned fuel within front_band cells           |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.front_band**               | Band width for launch_from = front [fire cells]            | Integer >= 1                   | 2                      |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.spot_radius**              | Ignition disc radius at the landing point [m]              | Real > 0                       | 10.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.P_catch**                  | Probability that a landed brand ignites                    | Real 0-1                       | 1.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.reentry_fuel_thresh**      | Minimum remaining fuel fraction for a landing to ignite    | Real 0-1                       | 0.05                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.random_seed**              | Random seed; <= 0 seeds from the clock (not repeatable)    | Integer                        | 0                      |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.spotting_interval**        | Apply spotting every N fire steps (one per atmospheric     | Integer > 0                    | 1                      |
|                                                | step)                                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.spotting.fuel_system**              | Fuel system of the maximum-distance table                  | "13", "40"                     | "13"                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Crown fire
----------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.crown.enable**                      | Crown fire initiation and active crown spread              | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.canopy_base_ht**              | Canopy base height [m]                                     | Real > 0                       | 5.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.canopy_bulk_den**             | Canopy bulk density [kg/m3]                                | Real > 0                       | 0.2                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.canopy_depth**                | Canopy depth [m]                                           | Real > 0                       | 10.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.foliar_moisture**             | Foliar moisture [fraction]                                 | Real                           | 1.0                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.h_crown_BTU_lb**              | Canopy heat content [BTU/lb]                               | Real > 0                       | 8000.0                 |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.wind_10m_kmh**                | Fixed 10 m wind for the crown rate [km/h]; 0 derives it    | Real >= 0                      | 0.0                    |
|                                                | from the effective wind                                    |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.ros_model**                   | Active crown rate-of-spread model                          | "cruz", "rothermel1991",       | "cruz"                 |
|                                                |                                                            | "van_wagner_proxy"             |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.crown.use_passive_blend**           | Blend surface and crown rates through the crowning         | Boolean                        | false                  |
|                                                | fraction                                                   |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+


Diagnostics and output
----------------------

+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| Parameter                                      | Definition                                                 | Acceptable Values              | Default                |
+================================================+============================================================+================================+========================+
| **erf.fire.flame_temp_method**                 | Flame temperature estimate                                 | "byram_radiant",               | "byram_radiant"        |
|                                                |                                                            | "mcalpine_heat",               |                        |
|                                                |                                                            | "nelson_emissivity"            |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.flame_temp_T_amb**                  | Ambient temperature for the flame temperature [K]          | Real                           | 300.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.compute_flame_tilt**                | Compute the flame tilt diagnostic                          | Boolean                        | false                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.flame_tilt_T_amb**                  | Ambient temperature for the tilt buoyancy velocity [K]     | Real                           | 300.0                  |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.flame_tilt_rho_air**                | Air density for the tilt buoyancy velocity [kg/m3]         | Real                           | 1.2                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.write_fire_stats_csv**              | Append burned area, perimeter and front statistics each    | Boolean                        | true                   |
|                                                | step                                                       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.fire_stats_csv_file**               | Statistics CSV filename                                    | String                         | "fire_stats.csv"       |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.boundary_guard_cells**              | Width, in fire cells, of the band along every non-periodic | Integer >= 0                   | 2                      |
|                                                | edge of the fire grid that the boundary guard watches      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.boundary_guard_action**             | When a burning cell enters the band: "warn" prints once    | "none", "warn", "abort"        | "warn"                 |
|                                                | and records the contact time, "abort" stops the run,       |                                |                        |
|                                                | "none" checks nothing                                      |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.edge_reach_check**                  | Print once at ignition the distance to each edge against   | Boolean                        | true                   |
|                                                | the largest rate of spread times the time left in the run  |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.probes**                            | Flat list of x y points [m] whose arrival time is printed  | Reals                          | none                   |
|                                                | once                                                       |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.exposure.enable**                   | Per-structure exposure CSV and fields; needs               | Boolean                        | false                  |
|                                                | structures.enable                                          |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.exposure.file**                     | Exposure CSV filename                                      | String                         | "fire_exposure.csv"    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.exposure.interval**                 | Fire steps between exposure rows                           | Integer >= 1                   | 100                    |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.exposure.ring**                     | Width of the wall band around a footprint [fire cells]     | Integer 1-4                    | 1                      |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.suppression.enable**                | Read and apply the suppression action file (fire lines,    | Boolean                        | false                  |
|                                                | drops, hold test, burnout); see :ref:`sec:FireSuppression` |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.suppression.file**                  | The action file; required with suppression.enable          | String                         | none                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.suppression.poll_interval**         | Fire steps between modification-time checks of the file;   | Integer >= 0                   | 10                     |
|                                                | 0 reads it once at start-up                                |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.suppression.log**                   | Event log (applied, completed, expired, hold_failed,       | String                         | "suppression_log.csv"  |
|                                                | burnout, reread)                                           |                                |                        |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.plot_file**                         | Fire plotfile prefix                                       | String                         | ``plt_fire_``          |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.plot_int**                          | Steps between fire plotfiles; < 0 disables                 | Integer                        | -1                     |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
| **erf.fire.plot_per**                          | Seconds between fire plotfiles; < 0 disables               | Real                           | -1.0                   |
+------------------------------------------------+------------------------------------------------------------+--------------------------------+------------------------+
