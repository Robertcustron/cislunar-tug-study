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
| thruster_efficiency | 0.6 | - | §6.3 | Own estimate, typical Hall thruster anode efficiency (not yet in Appendix A: propose A-19) |
| duty_cycle | 0.85 | - | A-17 | Gateway PPE: 319 of 383 days thrusting (McGuire et al. 2024), rounded |
| dry_mass | 5,900 | kg | A-10 | Placeholder from Rimani et al. (2020); to be replaced by Step 4/6 mass model |
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
