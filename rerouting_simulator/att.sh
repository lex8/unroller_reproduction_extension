#!/bin/bash
python sim.py -f routing_tables/att/19L/att_metadata.txt
python sim_plotter.py reroute_curr_att_19L_results.csv
python sim_plotter.py reroute_src_att_19L_results.csv
