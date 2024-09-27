This repository contains the files neccesarry to use the open source tool empymod to reproduce the modeling results of the paper "Induced polarization in the transient electromagnetic method may enable detection of
subsurface ice on Earth, Mars, and the Moon to be submitted for Planetary and Space Sciences".

In order to apply these files, empymod must be installed. Please see https://empymod.emsig.xyz/en/stable/ for installation manual. 

The files are: 

dielectric_data.py - which is a python library containg data with estimated electrical parameters for different ices, based on published results available in the open literature.
halfspace_and_3layers.py - is a function that do the computation of the model. 

dielectric_plots.py - create a plot of the permittivity and conducitivity (Figure 2).

The rest of the files creates plots of TEM-responses for lunar, martian and terretrial subsurface ice, and reproduce Figure 4-9, dependent on depth settings in the files. 

plot_lunar_ice_FDEM_TDEM.py
plot_martian_ice_FDEM_TDEM.py
plot_permafrost_ice_FDEM_TDEM_loops.py

