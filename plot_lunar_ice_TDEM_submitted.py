import empymod
import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt
#plt.style.use('ggplot')
import numpy.matlib as matlib
from scipy.constants import mu_0
mu0 = 4*np.pi*1e-07
e0 = 8.85e-12
from scipy.special import roots_legendre
from matplotlib.ticker import LogLocator, NullFormatter
from scipy.interpolate import InterpolatedUnivariateSpline as iuSpline
from scipy.signal import butter, lfilter, freqz, welch, cheby1
plt.rcParams['text.usetex'] = True
import dielectric_data
out = dielectric_data.data() # A tuple
import Cole_models
from halfspace_and_3layers_tem import halfspace_and_3layers_tem
#plt.style.use('ggplot')
def pos(data):
    """Return positive data; set negative data to NaN."""
    return np.array([x if x > 0 else np.nan for x in data])
def neg(data):
    """Return -negative data; set positive data to NaN."""
    return np.array([-x if x < 0 else np.nan for x in data])

plotcolors = ['black','gray', 'silver', 'teal','C2','C3','C4','C5', 'C6', 'C7', 'C8', 'C9', 'grey',  'b', 'g', 'r', 'c', 'm', 'crimson', 'pink', 'teal', 'sandybrown']
markerspace = [ 90, 85, 105, 125, 110, 115, 99, 108, 107, 120]
mrk = ('o', 'v', '*', '<', 'd', '8', 's', 'p', '^', 'h', 'H', 'D', 'd', 'P', 'X', 'o', 'v', '*', '<', '>',)
lines = ('solid', 'dashed', 'dashdot', 'dotted')

(
Regolith, Regolith_1e10, Permafrost_from_inversion, Hundre, To_hundre, To_hundre_og_femti, Fire_hundre_og_femti, Tusen, Tre_tusen, Ti_tusen, Ti_i_tiende, air, permafrost_model_2008, permafrost_model_2008_c_0999, Fairbanks_silt_100_ice_minus_3, Fairbanks_silt_72_ice_minus_3, Fairbanks_silt_44_ice_minus_3, Fairbanks_silt_72_ice_minus_3_one_rel, Sand_ice_46_ice_181K, Sand_ice_46_ice_181K_hydrate_static_1e04_c_0_3, Sand_ice_46_ice_181K_slow, Sand_ice_46_ice_181K_slower,  Sand_ice_46_ice_100K_fake, Sand_ice_46_ice_100K_c_95, Sand_ice_46_ice_100K, Sand_ice_17_ice_100K, Sand_ice_7_ice_100K_lower_cond, Sand_ice_7_ice_100K_faster_tau, Sand_ice_7_ice_100K, Sand_ice_46_ice_100K_tau_1em1, Sand_ice_46_ice_100K_tau_1em2, Sand_ice_46_ice_100K_tau_1e4, JSC_Mars_1, Ice_0_1M_NaCl_210K, Ice_1mM_NaCl_210K, Ice_0_1M_NaCl_100K, Ice_0_1M_NaCl_198K, Ice_0_1M_NaCl_100K_099, Ice_0_1M_NaCl_100K_0999, Ice_0_1M_NaCl_100K_09999, Ice_0_1M_NaCl_100K_099999, Ice_0_1M_NaCl_100K_0999999, Ice_0_1M_NaCl_100K_05, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_210K, JSC_Mars_1_60_perc_ice_0_1M_CaCl2_198K, c_test, c_test_c_0999, num_test_c_stab_c_0999, num_test_c_stab_c_1, num_test_c_stab_c_076, Sand_ice_46_ice_100K_c075
) = out


fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True)


xlims = [1e-07, 1e-01]
ylims = [1e-10, 1e01]
ymax = 1e-07 # in symlog-plot


font = 12
titlefont = 16
legendfont = 12


saveafig = 'no'
#saveafig = 'yes'


filename = 'lunar_1m_ice_layer_at_table_01m.pdf'
filename_fd = 'lunar_1m_ice_layer_at_table_01m_fd.pdf'



ikx = 0
y = 0

MUT = []


depth=[0, 0.1, 1.1]  # Husk! *Nedre lag er under siste oppgitte dybde.
#depth=[0, 0.001, 1.0]  # Husk! *Nedre lag er under siste oppgitte dybde.




for subsurf2 in [Regolith, Sand_ice_7_ice_100K,  Sand_ice_17_ice_100K,  Sand_ice_46_ice_100K, Sand_ice_46_ice_100K_fake, Sand_ice_46_ice_100K_c_95]: 
#for subsurf2 in [Regolith, Sand_ice_7_ice_100K,  Sand_ice_17_ice_100K,  Sand_ice_46_ice_100K, Sand_ice_46_ice_100K_fake, Sand_ice_46_ice_100K_c_95, Sand_ice_46_ice_100K_c075]: 




#	subsurf1 = subsurf2 # for halfspace, set subsurf2 and 3 = subsurf1
#	subsurf3 = subsurf2

	subsurf1 = Regolith # for halfspace, set subsurf2 and 3 = subsurf1
	subsurf3 = Regolith


#	soln_type = ['Full', 'Diff']
	soln_type = ['Diff']
#	soln_type = ['Full']


#	radius = np.array([2, 3,5, 6]) # or siden length 

#	radius = np.array([.1, 1,  5, 10, 100, 500, 1000]) # or siden length 
	radius = np.array([2]) # or siden length 



#	Rx_config = 'coincident'
	Rx_config = 'central'	

#	normalization = 'none' 
	normalization = 'V_pr_A_pr_m2'
#	normalization = 'V_pr_A'



	Tx_geometry = 'loop'
#	Tx_geometry = 'square'

	output_H_or_EMF = 'EMF'
#	output_H_or_EMF = 'H'

	I = 10
	Nr = 500
	a_rec = 0.5
	
	noise_mars = (1e-12*10)/I # V/(A m2) * 10 A / (I som er brukt i denne koden) fordi 10 A er brukt i utledningen av tallet 1e-12. 
	
	hTx = .01 # Når du setter positiv her blir det over bakken, siden du setter en minus foran hTx og hRx i src og rec, siden minus høyde er over bakken i 	empymod. 
	hRx = .01



	custom_LPF = 450e03

	filter_ft = 'wer_101_CosSin_2020b'

	filter_ht = 'wer2001' # (Lunar) Regolith maa ha dette filteret!!!
#	filter_ht = 'wer_101_CosSin_2020b'
#	filter_ht = 'default'
	


	Name =  r'%.35s' %(subsurf1.name)#, subsurf1.T+273)
	Name2 =  r'%.35s' %(subsurf2.name)#, subsurf1.T+273)
	Name3 =  r'%.35s' %(subsurf3.name)#, subsurf1.T+273)
	MUT = np.append(MUT, Name2)

	off_time, times, out_custom, out_step_off, radius, rampdown_end, Ar, Nr, I, soln_type,  ylabeltext, noise, noiselabel = halfspace_and_3layers_tem(depth, subsurf1, subsurf2, subsurf3, radius, I, Nr, a_rec, Tx_geometry,  Rx_config, normalization, filter_ft, filter_ht, hTx, hRx, custom_LPF, output_H_or_EMF, soln_type)


	for i in range (len(radius)):
		print ('i=',i)

		for x in range (len(soln_type)):


			plt.figure(2)
			plt.plot(times, pos(out_step_off[x, i,:]),'-', color = plotcolors[i+ikx+y], label=r'Step-off. %.45s-soln. %.45s at %.1d$^\circ$C, a = %.2f m' %(soln_type[x], subsurf2.name, subsurf1.T, radius[i])  )
			plt.plot(times, neg(out_step_off[x, i,:]),'--', color = plotcolors[i+ikx+y], label=r'Step-off. %.45s-soln. %.45s at %.1d$^\circ$C, a = %.2f m' %(soln_type[x], subsurf2.name, subsurf1.T, radius[i])  )
	
			plt.plot(off_time,  pos(out_custom[x, i,:]), '-', color = plotcolors[i+ikx+y+1], label=r'Ramp-off. %.45s-soln. %.45s at %.1d$^\circ$C, a = %.2f m' %(soln_type[x], subsurf2.name, subsurf1.T, radius[i]) )
			plt.plot(off_time,  neg(out_custom[x, i,:]), '--', color = plotcolors[i+ikx+y+1], label=r'Ramp-off. %.45s-soln. %.45s at %.1d$^\circ$C, a = %.2f m' %(soln_type[x], subsurf2.name, subsurf1.T, radius[i]) )
	#plt.text(1.5e-05,1e-12, cond_model_tex, fontsize=14)#, va='top')
	#	Data = (
	#	r'$\sigma_{DC}=$ %.2e S/m, \newline $~~~~~\varepsilon_{\infty} = %.2f$, \newline $~~~~~\varepsilon_{0} = %.2f$, \newline $~~~~~f_r=$%.3f Hz, 	\newline $~~~~~c=$%.1f' %(subsurf.cond_dc, subsurf.perm8, subsurf.perm0, subsurf.f_r, subsurf.c)
	#	)
	#plt.text(1e-02,0, Name, fontsize=14)#, va='top')
	#plt.text(1e-02,-1e-18, Data, fontsize=12)#, va='top')	
			plt.xlabel(r'Time (s)', fontsize = font)

		#plt.yticks(fontsize=font)
		#plt.xticks(fontsize=font)
			plt.ylabel(r'%.45s' %(ylabeltext), rotation='vertical', fontsize = font)
		#plt.yticks([1e-10, 1e-9, 1e-8,  1e-7, 1e-6,  1e-5, 1e-4,  1e-3, 1e-2,  1e-1, 1e0])


		####################

		# Figure with symlog
		
		# The first (figure 1 called above loop) plot with subplots-routine
#		ax1.plot(off_time,  out_custom[i,:], '-', linewidth=2, color = plotcolors[i+ikx], linestyle=lines[i+ikx], label=r'Ramp-off. %.45s at %.1d K, a = %.2f m' %(subsurf.name, (subsurf.T  + 273) , radius[i]) )
#		ax2.plot(off_time,  out_custom[i,:], '-', linewidth=2, color = plotcolors[i+ikx], linestyle=lines[i+ikx], label=r'Ramp-off. %.45s at %.1d K, a = %.2f m' %(subsurf.name, (subsurf.T  + 273 ) , radius[i]) )
			ax1.plot(times, out_step_off[x, i,:], '-', linewidth=2, markersize=8, color = plotcolors[i+ikx+y*np.int(len(radius))], marker=mrk[i+ikx+y], markevery=markerspace[y+i+ikx], label=r'%.55s' %(subsurf2.name)  )
		
			ax2.plot(times, out_step_off[x, i,:], '-', linewidth=2, markersize=8, color = plotcolors[i+ikx+np.int(y*len(radius))], marker=mrk[i+ikx+y],  markevery=markerspace[y+i+ikx], label=r'%.55s' %(subsurf2.name)  )
		
			if x > 0:
				y=y+1
	
	
	
	
	
	ikx=ikx+1



plt.rcParams['text.usetex'] = True
fig.suptitle(r'TDEM response of lunar ice layers', fontsize = titlefont)
#fig.subplots_adjust(hspace=0.08)  # adjust space between axes
fig.subplots_adjust(hspace=0.03)  # adjust space between axes
# plot the same data on both axes
# zoom-in / limit the view to different portions of the data

#ax1.plot(rampdown_end, 3e-03, 'd', color='c', markersize=8, label = 'Ramp-off end (before LPF)')
ax1.axvline(x=rampdown_end, color='black')
# Add a vertical span to the left of the line filled with transparent light red color
ax1.axvspan(xmin=times[0], xmax=rampdown_end, color='lightcoral', alpha=0.3)
ax2.axvline(x=rampdown_end, color='black')
# Add a vertical span to the left of the line filled with transparent light red color
ax2.axvspan(xmin=times[0], xmax=rampdown_end, color='lightcoral', alpha=0.3)




ax1.set_ylim(1e-18, ymax)
ax1.set_yscale('symlog', linthresh=1e-22 )
ax2.set_yscale('symlog', linthresh=1e-22 )
ax2.set_ylim(-ymax, -1e-18)
ax1.set_xscale('log')
ax2.set_xscale('log')
ax2.set_xlabel(r'Time (s)', fontsize = font)
ax1.set_xlim(xlims)
ax2.set_xlim(xlims)
ax1.tick_params(axis='both', which='major', labelsize=font)
ax2.tick_params(axis='both', which='major', labelsize=font)
#ax1.set_ylabel(r'%.45s' %(ylabeltext), rotation='vertical', fontsize = font)
fig.supylabel(r'%.45s' %(ylabeltext), rotation='vertical', fontsize = font, ha='center')
#ax1.plot(rampdown_end, -10, 's', label = 'Ideal rampdown end here (before LPF)')

# Noise
ax1.plot(off_time, np.ones(len(off_time))*noise_mars, ':', color='gray', linewidth=2) # , label = noiselabel
ax2.plot(off_time, -np.ones(len(off_time))*noise_mars, ':', color='gray', linewidth=2)

ax1.legend(loc = 'upper right', fontsize = legendfont, frameon = False)

# hide the spines between ax and ax2
ax1.spines.bottom.set_visible(False)
ax2.spines.top.set_visible(False)
ax1.xaxis.tick_top()
ax1.tick_params(labeltop=False)  # don't put tick labels at the top
ax2.xaxis.tick_bottom()
#ax1.set_yticks([1e-10, 1e-8, 1e-6, 1e-4, 1e-2, 1e0]) # den oppe skal være rett tall
#ax2.set_yticks([-1e0, -1e-2, -1e-4, -1e-6,  -1e-8, -1e-10, -1e-12])
#ax2.set_yticklabels([r'$-10^{0}$', r'$-10^{-2}$', r'$-10^{-4}$', r'$-10^{-6}$',  r'$-10^{-8}$', r'$10^{-10}$', r'$\pm10^{-12}$'  ])
# Upstairs
ax1.set_yticks([1e-16, 1e-14, 1e-12, 1e-10, 1e-8]) # den oppe skal være rett tall
# Downstairs
ax2.set_yticks([ -1e-8, -1e-10, -1e-12, -1e-14, -1e-16,  -1e-18 ])
ax2.set_yticklabels([r'$-10^{-8}$', r'$-10^{-10}$', r'$-10^{-12}$', r'$-10^{-14}$', r'$-10^{-16}$', r'$\pm10^{-18}$'  ])
plt.tight_layout()

xlayer_text = 1e-04
if subsurf1 == subsurf2:
	ax1.text(xlayer_text,1e-10, r'Halfspace',	 fontsize=font)
else:
	ax2.text(xlayer_text,-2e-11, r'Layer 1 (0 - %.1f m): %.45s'%(depth[1], Name ), 				fontsize=legendfont)

#	ax2.text(xlayer_text,-1e-4, r'Layer 2 (%.1f m - %.1f m) %.45s ' %(depth[1], depth[2], Name2),		fontsize=font)
	ax2.text(xlayer_text,-5e-10, r'Layer 2 (%.1f m - %.1f m): %.45s' %(depth[1], depth[2], 'MUT'),		fontsize=legendfont)

#	ax2.text(xlayer_text,-1e-3, r'Layer 2 (%.2f m - %.1f m): %.45s or %.45s' %(depth[1], depth[2], MUT[0], MUT[1]),		fontsize=legendfont)
	ax2.text(xlayer_text,-1e-8, r'Layer 3 (%.1f m - $\infty$): %.45s ' %(depth[2], Name3 ),	 fontsize=legendfont)

if saveafig == 'yes':
	fig.savefig(filename, format='pdf') # Must come before plt.show()
else:
	pass







plt.figure(2)
plt.title(r'Instrument response', fontsize = titlefont )
plt.plot(rampdown_end, 1e-04, 's', label = 'Ideal rampdown end here (before LPF)')
plt.plot(off_time, np.ones(len(off_time))*noise, ':', color='gray', linewidth=3, label = noiselabel)
plt.legend(loc='best', fontsize = font) # frameon = False, 
plt.xscale('log')
plt.yscale('log')
plt.tight_layout()
#plt.show()










plt.close(2)

#plt.close(4)

plt.show()



	




