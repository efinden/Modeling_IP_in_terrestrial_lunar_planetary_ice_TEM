# Python library with dielectric data
import numpy as np
e0 = 8.85e-12
# Cole-Cole conductivity data can be converted to complex permittivity data if the jwe0e8 term is excluded. 
# first, obtain the infinite freq. conductivity (if not given):
#sigma0 = 0.01
#m = 0.1
#sigma8 = sigma0/(1-m)
#tau = 0.01
# Then set perm8 = 0 since, only delta epsilon matters, then , and jwe0e8 must be zero. 
#eperm0 = () becomes freq. dependendt if c is not 1. 

def data():

	class Dielectric:
		def __init__(self, name, T, perm0, perm8, f_r, cond_dc, c, perm0_2, perm8_2, f_r_2, c_2):
			self.name = name
			self.T = T
			self.perm0 = perm0
			self.perm8 = perm8
			self.f_r = f_r
			self.cond_dc = cond_dc
			self.c = c
			
			self.perm0_2 = perm0_2
			self.perm8_2 = perm8_2
			self.f_r_2 = f_r_2
			self.c_2 = c_2

				      # name, T, perm0, perm8, f_r, cond_dc, c, perm0_2, perm8_2, f_r_2, c_2
	Regolith = Dielectric('Regolith', -173, 3, 3, 1, 1e-12, 1, 3, 3, 1, 1) #. Lunar sourcebook. 
	 
	Hundre = Dielectric(r'Purely resistive. $\rho=100~\Omega$m', 10, 3, 3, 1, 1/100, 1, 3, 3, 1, 1) # typical terrestrial value
	To_hundre = Dielectric('200 $\Omega$m', 10, 3.1, 3.1, 1, 1/200, 1, 3.1, 3.1, 1, 1) # typical terrestrial value
	To_hundre_og_femti = Dielectric('250 $\Omega$m', 10, 3.1, 3.1, 1, 1/250, 1, 3.1, 3.1, 1, 1) # typical terrestrial value
	Fire_hundre_og_femti = Dielectric('450 $\Omega$m', 10, 3.1, 3.1, 1, 1/450, 1, 3.1, 3.1, 1, 1) # typical terrestrial value
	Tusen = Dielectric('1 k$\Omega$m', -3, 3, 3, 1, 1/1000, 1, 3, 3, 1, 1) # typical frost terrestrial value
	Tre_tusen = Dielectric('3 k$\Omega$m', -3, 3, 3, 1, 1/3000, 0, 3, 3, 1, 0) # typical frost terrestrial value
	Ti_tusen = Dielectric('10 k$\Omega$m', -3, 3, 3, 1, 1/10000, 1, 3, 3, 1, 1) # typical frost terrestrial value
					# name,   T,   perm0, perm8, f_r, cond_dc, c, perm0_2, perm8_2, f_r_2, c_2
	Ti_i_tiende = Dielectric('1e10 $\Omega$m', -3, 3,     3,     1,   1e-10,   1, 3,       3,       1,     1)
	air = Dielectric('Air', 273, 1, 1, 1, 1/2e14, 1, 1, 1, 1, 1) # Stillmann and Grimm 2008. Perm0, perm8 from Nurge 2012. 

						# name,   T, perm0, perm8, f_r, cond_dc,  c,  perm0_2, perm8_2,     f_r_2,            
	Fairbanks_silt_100_ice_minus_3 = Dielectric(r'Fairbanks silt w/ 100\% ice', -3, 150.1, 3.1,  2.8e02, 1/(1.5e06), .7, 176, 3.1, 0.98e04, 1) # Grimm and Stillman 2015
	Fairbanks_silt_72_ice_minus_3 = Dielectric(r'Fairbanks silt w/ 72\% ice', -3, 3.99e03, 3.1, 2.6e02, 1/(1.6e04), .78, 265, 3.1, 0.98e04, 1) # Grimm and Stillman 2015
	Fairbanks_silt_44_ice_minus_3 = Dielectric(r'Fairbanks silt w/ 44\% ice', -3, 750.1, 3.1, 2.8e02, 1/(1.1e04), .7, 196, 3.1, 0.98e04, 1) # Grimm and Stillman 2015
	Sand_ice_46_ice_100K_fake = Dielectric(r'Artificial ice ($\tau_{2}=10$ s)', 100-273, (1000), 4,  1/(2*np.pi*1e47), 1e-40, .7, (58), 4, 1/(2*np.pi*1e01), 0.76) # Grimm and Stillman 2010, 2011, perm. from Nurge 2012
	Sand_ice_46_ice_100K_c_95 = Dielectric(r'Artificial ice ($c_{2}=1.0$)', 100-273, (1000), 4,  1/(2*np.pi*1e47), 1e-40, .7, (58), 4, 1/(2*np.pi*1e04), 1.0) # Grimm and Stillman 2010,
	Sand_ice_46_ice_100K = Dielectric(r'Fine sand w/ 46\% ice', 100-273, (1000), 4,  1/(2*np.pi*1e47), 1e-40, .7, (58), 4, 1/(2*np.pi*1e04), 0.76) # Grimm and Stillman 2010, 2011, perm. from Nurge 2012
	Sand_ice_17_ice_100K = Dielectric(r'Fine sand w/ 17.9\% ice', 100-273, (1000), 3,  1/(2*np.pi*1e47), 1e-40, .7, (14.1), 3, 1/(2*np.pi*3e03), 0.76) # Grimm and Stillman 2010, 2011, perm. from Nurge 2012
	Sand_ice_7_ice_100K = Dielectric(r'Fine sand w/ 7.4\% ice', 100-273, (1000), 3,  1/(2*np.pi*1e47), 1e-40, .7, (6.3), 3, 1/(2*np.pi*2e03), 0.76) # Grimm and Stillman 2010, 2011, perm. from Nurge 20
	Sand_ice_46_ice_100K_c075 = Dielectric(r'Artificial c=0.99 (Sand w/ 46\% ice)', 100-273, (1000), 4,  1/(2*np.pi*1e47), 1e-40, .7, (58), 4, 1/(2*np.pi*1e04), 0.99) # Grimm and Stillman 2010, 2011, perm. from Nurge 2012
	JSC_Mars_1 = Dielectric(r'JSC Mars 1', 210-273, 2.4,   2.4,   1,   1e-10,   1, 2.4,     2.4,     1,     1) # Data frin Simoes 2004, (also in agreement with Grimm 2007).
	Ice_0_1M_NaCl_210K = Dielectric(r'100\% ice w/ 0.1 M NaCl', 210-273, 3.1, 3.1, 1, 5e-11, 1, 125, 3.1, 1/(2*np.pi*1e-04), 1.0) # Grimm 2008, Petrenko withworth 1999; and ref therein.
	Ice_1mM_NaCl_210K = Dielectric(r'100\% ice w/ 1 mM NaCl', 210-273, 3.1, 3.1, 1, 1e-11, 1, 125, 3.1, 1/(2*np.pi*9e-04), 1.0) # Grimm 2008, Petrenko withworth 1999; and ref therein.
	Ice_0_1M_NaCl_198K = Dielectric(r'100\% ice w/ 0.1 M NaCl', 198-273, 3.1, 3.1, 1, 3e-12, 1, 133, 3.1, 1/(2*np.pi*3e-04), 1.0) # Grimm 2008, Petrenko withworth 1999; and ref
	JSC_Mars_1_60_perc_ice_0_1M_CaCl2_198K = Dielectric(r'JSC Mars 1 w/ 60\% ice', 198-273, 1.2e03, 5, 1/(2*np.pi*1), 2e-10, .64, 110, 5, 1/(2*np.pi*0.0011), .73) # Data frin Simoes 2004, (also in agreement with Grimm 2007).  w/ 0.1 M CaCl$_2$
	JSC_Mars_1_60_perc_ice_0_1M_CaCl2_210K = Dielectric(r'JSC Mars 1 w/ 60\% ice', 210-273, 1000, 5, 1/(2*np.pi*0.0333), 2e-9, .75, 125, 5, 1/(2*np.pi*3.33e-04), .75) # Data frin Simoes 2004, (also in agreement with Grimm 2007).  w/ 0.1 M CaCl$_2$

			#	name,          T,     perm0, perm8, f_r, cond_dc, c, perm0_2, perm8_2, f_r_2, c_2


	return Regolith, Hundre, To_hundre, To_hundre_og_femti, Fire_hundre_og_femti, Tusen, Tre_tusen, Ti_tusen, Ti_i_tiende, air, Fairbanks_silt_100_ice_minus_3, Fairbanks_silt_72_ice_minus_3, Fairbanks_silt_44_ice_minus_3, Sand_ice_46_ice_100K_fake, Sand_ice_46_ice_100K_c_95, Sand_ice_46_ice_100K, Sand_ice_17_ice_100K, Sand_ice_7_ice_100K, JSC_Mars_1, Ice_0_1M_NaCl_210K, Ice_1mM_NaCl_210K, Ice_0_1M_NaCl_198K, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_210K, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_198K, Sand_ice_46_ice_100K_c075



	
			
			
			
