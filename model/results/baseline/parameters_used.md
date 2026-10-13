# Parameters used

| Name | Value | Unit | Ref | Source |
|---|---|---|---|---|
| cargo_outbound | 5,000 | kg | A-01 | Study assumption; close to the 5.4 t of Rimani et al. (2020) |
| cargo_return | 500.0 | kg | A-02 | Study assumption; Explore2040 p.14 return need |
| design_life | 15.0 | years | A-03 | Study assumption |
| end_time_per_round_trip | 60.0 | days | A-18 | Study assumption: rendezvous, refuelling, capture and hand-over at both ends |
| dv_per_leg_base | 2,400 | m/s | A-06 | Rimani et al. (2020), GTO to NRHO |
| dv_margin | 0.1 | - | A-06 | Study assumption |
| dv_per_leg_sensitivity_base | 3,100 | m/s | A-06 | McGuire et al. (2024), Gateway PPE sub-GTO to NRHO; margin applied on top |
| return_dv_ratio | 1.000 | - | A-07 | Study assumption: return leg delta-v equal to outbound |
| leo_to_geo_dv | 6,000 | m/s | D-02 | Loghry et al. (2017), LEO (28.5 deg) to GEO with 20-50 kW SEP |
| thrust | 1.050 | N | A-17 | Rimani et al. (2020) operating point, reproduced by own check |
| isp | 2,100 | s | A-17 | Rimani et al. (2020) |
| thruster_efficiency | 0.6 | - | A-19 | Own estimate, typical Hall thruster total efficiency (jet power / electrical input power); read as PPU x thruster (D-22) |
| duty_cycle | 0.85 | - | A-17 | Gateway PPE: 319 of 383 days thrusting (McGuire et al. 2024), rounded |
| dry_mass | 5,900 | kg | A-10 | Parametric value from Rimani et al. (2020); kept as the baseline after the bottom-up mass budget (D-32) |
| launcher_gto_capacity | 11,500 | kg | C-1 | ArianeGroup, Ariane 64 to GTO |
| launcher_lto_capacity | 8,600 | kg | D-09 | Ariane 6 published capability to lunar transfer orbit (97.4 deg reference) |
| llo_altitude | 100.0 | km | D-10 | Study assumption for the excluded LLO case |
| thruster_rated_life | 23,000 | hours | §5.2 | Shastry et al. (2024), AEPS 12 kW Hall thruster life target |
| thruster_unit_power | 12,000 | W | §5.2 | Own estimate, AEPS-class operating point (TBC against Shastry et al.) |
| thruster_unit_isp | 2,600 | s | §5.2 | Own estimate, AEPS-class operating point (TBC against Shastry et al.) |
| thruster_unit_efficiency | 0.63 | - | §5.2 | Own estimate, AEPS-class operating point (TBC against Shastry et al.) |
| rimani_initial_mass | 13,600 | kg | §6.1 | Rimani et al. (2020): 13.6 t tug (5.4 t cargo, 5.9 t dry) |
| rimani_dv | 2,400 | m/s | §6.1 | Rimani et al. (2020), GTO to NRHO (no margin) |
| rimani_isp | 2,100 | s | §6.1 | Rimani et al. (2020) |
| rimani_thrust | 1.050 | N | §6.1 | Own check: total thrust that reproduces the Rimani et al. (2020) transfer |
| rimani_transfer_time | 364.0 | days | §6.1 | Rimani et al. (2020) |
| ppe_transfer_time | 383.0 | days | §6.1 | McGuire et al. (2024) |
| ppe_thrusting_time | 319.0 | days | §6.1 | McGuire et al. (2024) |
| smart1_launch_mass | 367.0 | kg | §6.1 | eoPortal SMART-1 page (TBC) |
| smart1_xenon_used | 82.0 | kg | §6.1 | Estublier et al., ESA Bulletin 129 |
| smart1_dv | 3,700 | m/s | §6.1 | Estublier et al., ESA Bulletin 129 |
| smart1_isp | 1,540 | s | §6.1 | Estublier et al., ESA Bulletin 129 |
| ep_specific_mass | 25.0 | kg/kW | A-23 | Own estimate: added dry mass per extra kW of EP power (arrays, PPUs, thrusters, radiators, structure); swept 15-40 kg/kW |
| platform_power | 2,000 | W | A-21 | Own estimate (system analysis), TBC in the logical architecture |
| european_thruster_unit_power | 5,000 | W | A-24 | PPS 5000 class, 5 kW (public catalogue listing, satcatalog.com); flown European Hall thruster class |
| european_thruster_rated_life | 15,000 | hours | A-24 | PPS 5000 class, about 15,000 h operating life (public catalogue listing, satcatalog.com) |
| design_ep_power | 25,000 | W | D-16 | Trade-offs decision: EP power at the PPU inputs at end of life |
| staging_perigee_altitude | 250.0 | km | D-02 | Ariane 6 reference GTO, 250 x 35,786 km (TBC against the user's manual) |
| staging_apogee_altitude | 35,786 | km | D-02 | Ariane 6 reference GTO, 250 x 35,786 km (TBC against the user's manual) |
| design_eclipse | 2.500 | hours | A-28 | Own choice: CALC-29 (2.2 h at GTO-class apogee) rounded up; NRHO eclipses are under 1 h and avoidable (Zimovan-Spreen, Howell, Davis, AAS 20-562); longer eclipses avoided by trajectory phasing (D-26) |
| ppu_efficiency | 0.95 | - | A-29 | ESA ARTES project on the PPS 5000 thruster and PPU: high-power PPU breadboard measured 95 % at 5 kW |
| thruster_anode_efficiency | 0.63 | - | A-29 | Own estimate, same value as the 12 kW-class unit (thruster_unit_efficiency) |
| power_margin | 0.2 | - | A-30 | Own convention for Phase 0/A: 20 % on nominal power estimates |
| distribution_efficiency | 0.95 | - | A-30 | Own estimate: array regulation, distribution and harness losses |
| battery_dod | 0.6 | - | A-31 | Own estimate: Li-ion battery cycled a few thousand times over 15 years |
| battery_efficiency | 0.95 | - | A-31 | Own estimate: discharge efficiency, also used for charge |
| array_eol_bol_ratio | 0.75 | - | A-32 | Own estimate: 15 years with two radiation-belt crossings per round trip; TBC by the dose analysis of PWR-02 |
| xenon_transfer_time | 21.0 | days | A-26 | ESPRIT refuelling allows up to about 3 weeks for a xenon transfer (NASA, IAC 2024) |
| propellant_module_dry_mass | 500.0 | kg | A-25 | Own estimate: tank, structure and docking target, about 20 % of the xenon load |
| mass_system_margin | 0.2 | - | A-35 | ESA margin philosophy for science assessment studies (SRE-PA/2011.097, issue 1.3): 20 % system margin on nominal dry mass |
| direct_carrier_dry_mass | 1,200 | kg | A-36 | Own estimate: expendable carrier with structure, GNC, chemical propulsion, power and an IBDM-class port (< 325 kg); swept 800-1,600 kg |
| direct_transfer_dv | 100.0 | m/s | A-36 | Ballistic lunar transfer to NRHO: 17-41 m/s deterministic (Parrish et al., NASA); rounded up for navigation and margin |
| direct_carrier_isp | 300.0 | s | A-36 | Own estimate, bipropellant |
| thruster_rated_life_alt | 20,000 | hours | A-38 | PPS 5000 operating life about 20,000 h per the Safran representative's product page; 15,000 h per satcatalog (A-24 baseline) |
