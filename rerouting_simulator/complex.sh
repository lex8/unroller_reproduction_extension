#!/bin/bash
python3 sim.py -f routing_tables/complex/complex.txt
python3 sim_plotter.py reroute_curr_complex_14L_results.csv
python3 sim_plotter.py reroute_src_complex_14L_results.csv
