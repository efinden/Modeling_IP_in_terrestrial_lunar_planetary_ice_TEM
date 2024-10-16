import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
from PIL import Image

plotcolors = ['black','C2','C3','C4','C5', 'C6', 'C7', 'C8', 'C9', 'grey', 'gold', 'b', 'g', 'r', 'c', 'm', 'crimson', 'pink', 'teal', 'sandybrown']

mrk = ('o', 'v', '*', '<', '>', '8', 's', 'p', '^', 'h', 'H', 'D', 'd', 'P', 'X')
lines = ('solid', 'dashed', 'dashdot', 'dotted')


import dielectric_data
out = dielectric_data.data() # A tuple

(
Regolith, Regolith_1e10, Permafrost_from_inversion, Hundre, To_hundre, To_hundre_og_femti, Fire_hundre_og_femti, Tusen, Tre_tusen, Ti_tusen, Ti_i_tiende, air, permafrost_model_2008, permafrost_model_2008_c_0999, Fairbanks_silt_100_ice_minus_3, Fairbanks_silt_72_ice_minus_3, Fairbanks_silt_44_ice_minus_3, Fairbanks_silt_72_ice_minus_3_one_rel, Sand_ice_46_ice_181K, Sand_ice_46_ice_181K_hydrate_static_1e04_c_0_3, Sand_ice_46_ice_181K_slow, Sand_ice_46_ice_181K_slower,  Sand_ice_46_ice_100K_fake, Sand_ice_46_ice_100K_c_95, Sand_ice_46_ice_100K, Sand_ice_17_ice_100K, Sand_ice_7_ice_100K_lower_cond, Sand_ice_7_ice_100K_faster_tau, Sand_ice_7_ice_100K, Sand_ice_46_ice_100K_tau_1em1, Sand_ice_46_ice_100K_tau_1em2, Sand_ice_46_ice_100K_tau_1e4, JSC_Mars_1, Ice_0_1M_NaCl_210K, Ice_1mM_NaCl_210K, Ice_0_1M_NaCl_100K, Ice_0_1M_NaCl_198K, Ice_0_1M_NaCl_100K_099, Ice_0_1M_NaCl_100K_0999, Ice_0_1M_NaCl_100K_09999, Ice_0_1M_NaCl_100K_099999, Ice_0_1M_NaCl_100K_0999999, Ice_0_1M_NaCl_100K_05, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_210K, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_198K, c_test, c_test_c_0999, num_test_c_stab_c_0999, num_test_c_stab_c_1, num_test_c_stab_c_076, Sand_ice_46_ice_100K_c075
) = out



font = 12
titlefont = 14
legendfont = 10

xlim_min = 1e-06

#saveafig = 'yes'
saveafig = 'no'

#filename = 'fairbanks-72-one-rel.pdf'

filename = 'dielectric__planetary_ices.pdf'



#eta = np.load('etaH.npy')
#freq = np.load('freq.npy')


mu0 = 4*np.pi*1e-07
e0 = 8.85*1e-12
f = np.logspace(-9,6,601)
w = 2*np.pi*f


f_max = 300e03
k0 = (	e0*mu0*(2*np.pi*f_max)	)**0.5
print('k0', k0)


y = 0


#subsurfs = [Sand_ice_46_ice_100K, Sand_ice_46_ice_100K_c_95, Sand_ice_46_ice_100K_c075, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_198K, Ice_1mM_NaCl_210K, Fairbanks_silt_72_ice_minus_3]
subsurfs = [Sand_ice_46_ice_100K, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_198K, Ice_1mM_NaCl_210K, Fairbanks_silt_72_ice_minus_3]




#cond_DC = np.full( (1, len(subsurfs)), np.nan)

#tau_1 = np.full( (1, len(subsurfs)), np.nan)
#eperm0_1 = np.full( (1, len(subsurfs)), np.nan)
#c1 = np.full( (1, len(subsurfs)), np.nan)

#tau_2 = np.full( (1, len(subsurfs)), np.nan)
#eperm0_2 = np.full( (1, len(subsurfs)), np.nan)
#c2 = np.full( (1, len(subsurfs)), np.nan)

eperm_HF = np.full( (len(f), len(subsurfs)), np.nan)


eperm_1 = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')
eperm_2 = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')
eperm_dc = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')
e_tot = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')

e_tot_diffusive = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')



cond = np.full( (len(f), len(subsurfs)), np.nan,  dtype='G')
rho = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')
rho_phase = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')

cond_diffusive = np.full( (len(f), len(subsurfs)), np.nan,  dtype='G')
rho_diffusive = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')
rho_phase_diffusive = np.full( (len(f), len(subsurfs)), np.nan, dtype='G')


plt.rc('legend',fontsize=10)

# Figure 4 x 4

fig, axs = plt.subplots(2, 2, figsize=(10,6))

plt.suptitle(r'Cole-Cole models of ice-rich planetary and lunar subsurfaces', fontsize=titlefont)
ax =  axs[1,0]  # imag perm
ax2 = axs[0,1] # cond
ax4 = axs[0,0] # real perm
ax3 = axs[1,1] # phase



# Figure 2 x 2 : Permittivity

#fig, axs = plt.subplots(2, 2, figsize=(10,6))

#plt.suptitle(r'Cole-Cole model of planetary subsurfaces', fontsize=10)
#ax =  axs[1,0]  # imag perm
#ax4 = axs[0,0] # real perm





for subsurf1 in subsurfs:
	print('#######################################################')
	print('subsurf', subsurf1.name)

	#cond_DC[y] = subsurf1.cond_dc
	cond_DC = subsurf1.cond_dc
	print('cond_DC', cond_DC)


	# 4: Salt hydrate : 

#	tau_1[y] = 1/(2*np.pi*subsurf1.f_r)
	tau_1 = 1/(2*np.pi*subsurf1.f_r)
	print('tau_1', tau_1)

#	eperm0_1[y] = subsurf1.perm0
	eperm0_1 = subsurf1.perm0
	print('eperm0_1', eperm0_1)

#	c1[y] = subsurf1.c
	c1 = subsurf1.c
	print('c1', c1)

	
	# 2: ICE 

#	tau_2[y] = 1/(2*np.pi*subsurf1.f_r_2)
	tau_2 = 1/(2*np.pi*subsurf1.f_r_2)
	print('tau_2', tau_2)


#	eperm0_2[y] = subsurf1.perm0_2 
	eperm0_2 = subsurf1.perm0_2 
	print('eperm0_2', eperm0_2)

#	c2[y] =  subsurf1.c_2
	c2 =  subsurf1.c_2
	print('c2', c2)


#	eperm_HF[y] = subsurf1.perm0_2 
	eperm_HF[:] = subsurf1.perm8_2
	print('eperm_8', eperm_HF)



#	eperm_1[:,y]  =  (eperm0_1[y] - eperm_HF[y])/(1+(1j*w*tau_1[y])**c1[y]) # rel. 
#	eperm_2[:,y]  = (eperm0_2[y] - eperm_HF[y])/(1+(1j*w*tau_2[y])**c2[y]) # Rel. 
#	eperm_dc[:,y]  = cond_DC[y]/(1j*w*e0) # rel. 

	eperm_1[:,y]  =  (eperm0_1 - eperm_HF[0, y])/(1+(1j*w*tau_1)**c1) # rel. 
	eperm_2[:,y]  = (eperm0_2 - eperm_HF[0, y])/(1+(1j*w*tau_2)**c2) # Rel. 
	eperm_dc[:,y]  = np.clongdouble(cond_DC/(1j*w*e0)) # rel. 


	e_tot[:,y]  = eperm_dc[:,y] + (eperm_1[:,y]) + (eperm_2[:,y]) + eperm_HF[:,y] # rel.
	e_tot_diffusive[:,y]  = eperm_dc[:,y] + (eperm_1[:,y]) + (eperm_2[:,y])# rel.

	# alt til cond over:
	cond[:,y]  = 1j*w*e0*e_tot[:,y]
	cond_diffusive[:,y]  = 1j*w*e0*e_tot_diffusive[:,y]

	rho[:,y]  = 1/cond[:,y]  # Just inverse
	rho_diffusive[:,y]  = 1/cond_diffusive[:,y]  # Just inverse

	rho_phase[:,y]  = np.rad2deg( np.arctan2( np.imag(rho[:,y]), np.real(rho[:,y])) ) 
	rho_phase_diffusive[:,y]  = np.rad2deg( np.arctan2( np.imag(rho_diffusive[:,y]), np.real(rho_diffusive[:,y])) ) 


#	ax1.plot(f, out_step_off[x, i, :], '-', linewidth=2, color = plotcolors[i+ikx+y], marker=mrk[i+ikx+y] ,markevery=50, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))  )
		
#	ax2.plot(f, out_step_off[x, i, :], '-', linewidth=2, color = plotcolors[i+ikx+y], marker=mrk[i+ikx+y] ,markevery=50, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T  + 273 ) )  )
		

	ax.plot(f,  -np.imag(e_tot[:,y]), '-', linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=50, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 )))#, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))  )
	ax.plot(f,  -np.imag(e_tot_diffusive[:,y]), '-', linewidth=2, color = plotcolors[y])#, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))  )

#	a1, = ax.plot(f,  -np.imag(e_tot[:,y]), '-', linewidth=2, color = plotcolors[i+ikx+y], marker=mrk[i+ikx+y] ,markevery=50, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))  )
#	a3, = ax.plot(f,  -np.imag(eperm_dc[:,y]), ':', color = 'orange')
#	a2, = ax.plot(f,  -np.imag(eperm_1[:,y]), ':', color = 'green')
#	a4, = ax.plot(f,  -np.imag(eperm_2[:,y]), ':', color = 'blue')

	#ax.legend((a1, a3, a2, a4), 
	#(r'Total imag. permittivity', 
	#r' $\frac{\sigma_{DC}}{ j\omega \varepsilon_0}$', 
	#r' Salt hydrate relaxation',
	#r' Ice relaxation'))
	ax.legend(frameon=False)
	ax.set_xlim([xlim_min, 1e06])
	ax.set_ylim([1e-10,1e08])

	ax.semilogy()
	ax.semilogx()
#	ax.set_yticks([1e-01,1e-00, 1e01, 1e02, 1e03, 1e04, 1e05, 1e06, 1e07])
	ax.set_xlabel(r'Frequency (Hz)', fontsize=10)
	ax.set_ylabel(r"$\varepsilon$''", fontsize=10)
	#ax.set_title(r'Imaginary permittivity', fontsize=10)
	#ax2.text(1e02,1e02, tex, fontsize=8, va='top')

	b1 = ax2.plot(f, np.abs(cond[:,y]), '-',  linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=50)#, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 )))
	b2 = ax2.plot(f, np.abs(cond_diffusive[:,y]), '--',  linewidth=2, color = plotcolors[y])#, label = r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))) 
#	b3 = ax2.plot(freq, np.abs(cond), '-', color='blue', linewidth=2, label = 'Cole-Cole conductivity: Diffusive model')
#	b4 = ax2.plot(freq, np.abs((eta[:,1])), '-', color='blue', linewidth=2, label = 'eta (conductivity) from inside empymod.model.bipole.py')
	ax2.legend()
	ax2.semilogx()
	ax2.semilogy()
	ax2.set_xlim([xlim_min, 1e06])
	ax2.set_ylim([1e-15,1e-03])
#	ax2.set_yticks([1e-11, 1e-10, 1e-09, 1e-08, 1e-07, 1e-06, 1e-05, 1e-04, 1e-03, 1e-02, 1e-01, 1e00,])
	#ax2.set_xlabel(r'$f$ (Hz)', fontsize=10)
	ax2.set_ylabel(r'Conductivity $|\sigma^*|$ (S/m)', fontsize=10)



	gd2 = ax4.plot(f, np.real(e_tot[:,y]), '-' , linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=50)#, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 )))
	gd3 = ax4.plot(f, np.real(e_tot_diffusive[:,y]), '--' , linewidth=2, color = plotcolors[y])#, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T +
	ax4.legend()
	ax4.semilogx()
	ax4.semilogy()
	ax4.set_xlim([xlim_min ,1e06])
	ax4.set_ylim([1e0,1e04])
#	ax4.set_yticks([1e-00, 1e01, 1e02, 1e03, 1e04, 1e05])
	#ax4.set_xlabel(r'$f$ (Hz)', fontsize=10)
	ax4.set_ylabel(r"$\varepsilon$'", fontsize=10)


	gd1 = ax3.plot(f, rho_phase[:,y], '-',  linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=50)
	gd2 = ax3.plot(f, rho_phase_diffusive[:,y], '--',  linewidth=2, color = plotcolors[y])#, label=r'Diff. %.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 )))

	ax3.legend()
	ax3.semilogx()
	ax3.set_yticks([-90,-80,-70,-60,-50,-40,-30,-20,-10,0])
	ax3.set_xlim([xlim_min, 1e06])
	ax3.set_ylim([-90,2])
	ax3.set_xlabel(r'Frequency (Hz)', fontsize=10)
	ax3.set_ylabel(r'Phase $\phi$ ($^{\circ}$)', fontsize=10)
	plt.tight_layout()









# Single figures 

# PHASE
	plt.figure(100)
	plt.plot(f, rho_phase[:,y], '-',  linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=50, label=r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 )))
	
	plt.legend()
	plt.semilogx()
	plt.yticks([-90,-80,-70,-60,-50,-40,-30,-20,-10,0])
	plt.xlim([1e-07,1e06])
	plt.ylim([-90,2])
	plt.xlabel(r'$f$ (Hz)', fontsize=10)
	plt.ylabel(r'Phase $\phi$ ($^{\circ}$)', fontsize=10)


# ABS COND

	plt.figure(101)
	plt.plot(f, np.imag(cond[:,y]), '-',  linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=30, label = r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))) 
	plt.plot(f, np.imag(cond_diffusive[:,y]), '--',  linewidth=2, color = plotcolors[y], marker=mrk[y] ,markevery=30, label = r'%.45s at %.1d K' %(subsurf1.name, (subsurf1.T + 273 ))) 
	plt.legend()
	plt.semilogx()
	plt.semilogy()
	plt.xlim([1e-07,1e06])
	plt.ylim([1e-15,1e-03])
	plt.xlabel(r'$f$ (Hz)', fontsize=10)
	plt.ylabel(r'Im Conductivity $\sigma^*$ (S/m)', fontsize=10)




	y=y+1


#


#plt.suptitle(r'Cole-Cole model of cold ice', fontsize=10)
plt.tight_layout()


if saveafig == 'yes':
	fig.savefig(filename, format='pdf') # Must come before plt.show()
	fig.savefig('4x4_dielectrics_HR.png', format='png', dpi=1200) # Must come before plt.show()
else:
	pass



plt.figure(100)
plt.title(r'Complex conductivity of planetary ices', fontsize=14)
plt.tight_layout()
plt.savefig("phase_HR.png", dpi=1200)



plt.figure(101)
plt.title(r'Complex conductivity of planetary ices', fontsize=14)
plt.tight_layout()
plt.savefig("abs_cond_HR.png", dpi=1200)



plt.show()

