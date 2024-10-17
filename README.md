This repository contains the files neccesarry to use the open source tool empymod to reproduce the modeling results of the paper "Induced polarization in the transient electromagnetic method for detection of subsurface ice on Earth, Mars, and the Moon submitted to Planetary and Space Sciences".

In order to apply these files, empymod must be installed. Please see https://empymod.emsig.xyz/en/stable/ for installation manual and guide on useage. 

The model applies many elements from the examples in the empymod-website. 

The files are: 

dielectric_data.py - which is a python library containg data with estimated electrical parameters for different ices, based on published results available in the open literature.

halfspace_and_3layers.py - is a function including the computation of the model. 

Cole_model.py - A custom Cole-Cole function file, based on the examples in the empymod wesite. 

dielectric_plots.py - creates a plot of the permittivity and conducitivity (Figure 2).

The *txt -files are digital filters needed for the transforms of empymod. 

The rest of the files creates plots of TEM-responses for lunar, martian and terretrial subsurface ice, and reproduce Figure 4-9, dependent on depth settings in the files. 

plot_lunar_ice_TDEM.py (Fig. 9)

plot_martian_ice_TDEM.py (Fig. 5-8)

plot_permafrost_ice_TDEM_loops.py (Fig. 4)

Please see empymod-documentation for application manual. Specific to this code is the library where you can select the material in each layer from dielectric_data.py, and the extended Cole-Cole models. 



