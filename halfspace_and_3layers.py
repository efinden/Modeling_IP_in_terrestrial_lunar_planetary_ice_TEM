import empymod
import numpy as np
from scipy.special import erf
import matplotlib.pyplot as plt
import numpy.matlib as matlib
from scipy.constants import mu_0
mu0 = 4*np.pi*1e-07
e0 = 8.85e-12
from scipy.special import roots_legendre
from matplotlib.ticker import LogLocator, NullFormatter
from scipy.interpolate import InterpolatedUnivariateSpline as iuSpline
from scipy.signal import butter, lfilter, freqz, welch, cheby1
# Own modules
import dielectric_data
out = dielectric_data.data() # A tuple
import Cole_models

def pos(data):
    """Return positive data; set negative data to NaN."""
    return np.array([x if x > 0 else np.nan for x in data])

def neg(data):
    """Return -negative data; set positive data to NaN."""
    return np.array([-x if x < 0 else np.nan for x in data])

N = 801 # # points in time to compute

def halfspace_and_3layers(depth, subsurf1, subsurf2, subsurf3, radius, I, Nr, a_rec, Tx_geometry,  Rx_config, normalization, filter_ft, filter_ht, hTx, hRx, custom_LPF, output_H_or_EMF, soln_type, h_fd, s_fd, a_fd):
	# a_rec is only used if central loop. a_rec = radius of small loop.
	print('normalization = ', normalization)
	
	air_resistivity = 1.0e40
	
	f = np.logspace(-4, 7, 601)
	w = 2*np.pi*f

	
	start_time = -8
		
	Ar = np.pi*(a_rec**2) # central loop is smaller receiver and only applies circle as loop. 
		
	# Name has to be the base of the text files
	wer2001 = empymod.filters.DigitalFilter('wer2001')
	wer_101_CosSin_2020b = empymod.filters.DigitalFilter('wer_101_CosSin_2020b')
	# Load the ASCII-files
	wer2001.fromfile(path='./')
	wer_101_CosSin_2020b.fromfile(path='./')
	key101_12 = empymod.filters.key_101_CosSin_2012()
	anderson_801_1982 = empymod.filters.anderson_801_1982()
	default_ht = empymod.filters.key_201_2009()
	
	#digfilter = anderson_801_1982 # works only for htarg. 
	# For clay1 you get the same with both filters. For ice30, you get oscillations with anderson_801.

	if filter_ft == 'wer_101_CosSin_2020b':
	
		digfilter_cos = wer_101_CosSin_2020b
		print('FT-filter for custom waveform = ', 'wer_101_CosSin_2020b' )
	else:
		print('Choose a defined filter')
		
	if filter_ht =='wer2001':
		digfilter = wer2001
		print('HT-filter for custom and ideal waveforms = ', 'wer2001')
		ht_filter = 'wer'

		
	elif filter_ht == 'default':
		digfilter = default_ht
		print('HT-filter for custom and ideal waveforms = ', 'default (key_201_2009)')
		ht_filter = 'def'
	
	elif filter_ht == 'wer_101_CosSin_2020b':
		digfilter_cos = wer_101_CosSin_2020b
		ht_filter = 'cos-filter'

	else:
		print('Choose a defined filter')




	# Noise numbers for plotting..
	
	
	# Spies, p.323 says " threshold noise level detected by the system, typically reduces to 
	#  0.5 nV /m2 = 0.5e-09 V / m2, after 15 min of stacking.
	# 0.1 -- 10 nV / m2 : # Christiansen 2009 - bok.  
	noise_V_pr_m2 = 0.5e-09

	noise_V_pr_A_pr_m2 = 0.5e-09/I

									# Spies says: 
	noise_V_pr_A_pr_m4 = 1e-04*1e-12/I # Kang 2018, 2020 VTEM. Small loop trans-
					#mitter systems can further be normalized by transmitter area to obtain V/Am4
					#Spies and Frischknecht, 1991, p.357 HUSK! HAN BRUKER 200 A saa ganget opp med A blir det ikke saa lavt.
	

	# For magnetometer, typ. 1e-3 nT is the noise level p. 327 same book. 
	# In B-field, as expr. in book:
	noise_nT = 1e-3*1e-9 # [T] = [Wb/m2] = [(A H) / m2] . Req. B-field. 
	# B = mu0*H
	# Converted to H-field:
	noise_A_pr_m = noise_nT/mu0
	
	noise_BGS = 5e-11 # instantant sensitivity, we presume..
	noise_BGS_in_H_field = noise_BGS/mu0 # nT # acc to http://www.geomag.bgs.ac.uk/education/raspberry_pi_magnetometer.html, scientific level magnetometers have a sensitivty of 5e-11 T. And the cheap magnetometer controlled by Rasberry Pi, of max freq. 1 kHz has a sensitivity of 1 nT. 

	
	# TEM data, a voltage, should be normalized by current, ampl. gain, and moment of rec coil to yield units of (V / a m2) Spies p. 357. 
	
	# V/ A # Ref Kozhevnikov 2008: typical for fiels aq. system = 1e-07 # V/ A is valid only for 100 m x 100 m loop
	noise_koz = 1e-07 #V_pr_A	
	
	# ina 828 
	noise_preamp = 7e-09*((450e03)**.5) # ( 7 nV / (sqrt{Hz}) )* BW sqrt{450 kHz }. 
	noise_preamp_sqrt_n_3hours_one_sec_1e4pulses = noise_preamp/100 # ( 7 nV / (sqrt{Hz}) )* BW sqrt{450 kHz }. 

	

	### H ###

	if output_H_or_EMF == 'H':
		ylabeltext = '$H_z$ in center of loop (A/m)'
		noise = noise_A_pr_m
		noiselabel = r'Typical noise (A/m)'

	### EMF ###
	
	elif (output_H_or_EMF == 'EMF'):	
		if (normalization == 'V_pr_A') and (Rx_config == 'coincident'):
			ylabeltext = 'Norm. EMF in loop (V/A)'
#			noise = (noise_V_pr_m2*Ar*Nr)/I
			noise = noise_koz
			noiselabel = r'Typical noise (V/A)'

		elif (normalization == 'V_pr_A_pr_m2') and (Rx_config == 'coincident'):
			ylabeltext = 'Norm. EMF in coincident loop (V/A m$^2$)'
			noise = noise_V_pr_A_pr_m2
			noiselabel = r'Typical noise (V/Am$^2$)'
						
		elif (normalization == 'V_pr_m2') and (Rx_config == 'coincident'):
			ylabeltext = 'Norm. EMF in coincident loop (V/m$^2$)'
			noise = noise_V_pr_m2
			noiselabel = r'Typical noise (V/m$^2$)'			
			
		elif (normalization == 'none') and (Rx_config == 'coincident'):
			ylabeltext = 'EMF in loop (V)'
			#noise = noise_preamp # assumed 1 uV
#			noiselabel = r' Preamp noise @ 450 kHz BW (4.7 $\mu$V)'
			noise = noise_preamp_sqrt_n_3hours_one_sec_1e4pulses
			noiselabel = r'3h averaged preamp noise @ 450 kHz BW (4.7 $\mu$V)'
		
		
		elif (normalization == 'V_pr_A_pr_m2') and (Rx_config == 'central'):
			ylabeltext = 'Normalized receiver voltage (V/A m$^2$)'
			noise = noise_V_pr_A_pr_m2
			noiselabel = r'Typical noise'		
		
			
		elif (normalization == 'none') and (Rx_config == 'central'):
			ylabeltext = 'EMF in loop (V)'
			#noise = noise_preamp # assumed 1 uV
#			noiselabel = r' Preamp noise @ 450 kHz BW (4.7 $\mu$V)'
			noiselabel = r'3h averaged preamp noise @ 450 kHz BW (4.7 $\mu$V)'
			noise = noise_preamp_sqrt_n_3hours_one_sec_1e4pulses



	# t = [ tid 0 fdtd - fast neg tid empymod  , 
	#tid 1 fdtd - fast neg tid empymod  
	#, .. ]
	
	# Standard step-off
	
	#waveform_times = np.array([
	#0.0000000e+00 -1.041E-03, 
	#5.6000000e-04 -1.041E-03, 
	#1.0410000e-03 -1.041E-03, 
	#1.0450000e-03 -1.041E-03 # WalkTEM
	#])
	#waveform_current = np.r_[0.0, 1.0, 1.0, 0.0]
	
	
	# Step-off slik den var
	
	waveform_times = np.array([ 
	5.6000000e-04 -1.041E-03, 
	1.0410000e-03 -1.041E-03, 
	1.0450000e-03 -1.041E-03 # WalkTEM # 4 us
##	1.0950000e-03 -1.041E-03 # WalkTEM # 54 us
#	1.250000e-03 -1.041E-03 # WalkTEM # 209 us
	])



	# Test med 0 der den har rampet helt ned (før LPF)
#	waveform_times = np.array([ 
#	5.600e-04 -1.045e-03, 
#	1.041e-03 -1.045e-03, 
#	1.045e-03 -1.045e-03 # WalkTEM # 54 us
#	])

	print('waveform_times = ', waveform_times)

	waveform_current = np.r_[1.0, 1.0, 0.0]
	
	
	off_time = np.logspace(start_time, 1, N) # Hvis du ikke skal sample saa tidlig folger det ikke saa hoy frekvens! Tidlig losning krever hoy frekvens!
	
	
	def waveform(times, resp, times_wanted, wave_time, wave_amp, nquad=3):
		"""Apply a source waveform to the signal.
		
		Parameters
		----------
		times : ndarray
			Times of computed input response; should start before and end after `times_wanted`.
		
		resp : ndarray
			EM-response corresponding to `times`.
		
		times_wanted : ndarray
			Wanted times.
		
		wave_time : ndarray
			Time steps of the wave.
		
		wave_amp : ndarray
			Amplitudes of the wave corresponding to `wave_time`, usually in the range of [0, 1].
		
		nquad : int
			Number of Gauss-Legendre points for the integration. Default is 3.
		
		Returns
		-------
		resp_wanted : ndarray
			EM field for `times_wanted`.
		"""
		# Interpolate on log.
		PP = iuSpline(np.log10(times), resp)
	# Wave time steps.
		dt = np.diff(wave_time)
		dI = np.diff(wave_amp)
		dIdt = dI/dt
	# Gauss-Legendre Quadrature; 3 is generally good enough.
	# (Roots/weights could be cached.)
		g_x, g_w = roots_legendre(nquad)
	
	# Pre-allocate output.
		resp_wanted = np.zeros_like(times_wanted)
	
	    # Loop over wave segments.
		for i, cdIdt in enumerate(dIdt):
			# We only have to consider segments with a change of current.
			if cdIdt == 0.0:
				continue
			# If wanted time is before a wave element, ignore it.
			ind_a = wave_time[i] < times_wanted
			if ind_a.sum() == 0:
				continue
				
			# If wanted time is within a wave element, we cut the element.
			ind_b = wave_time[i+1] > times_wanted[ind_a]
		
			# Start and end for this wave-segment for all times.
			ta = times_wanted[ind_a]-wave_time[i]
			tb = times_wanted[ind_a]-wave_time[i+1]
			tb[ind_b] = 0.0  # Cut elements
		
			# Gauss-Legendre for this wave segment. See
			# https://en.wikipedia.org/wiki/Gaussian_quadrature#Change_of_interval
			# for the change of interval, which makes this a bit more complex.
			logt = np.log10(np.outer((tb-ta)/2, g_x)+(ta+tb)[:, None]/2)
			fact = (tb-ta)/2*cdIdt
			resp_wanted[ind_a] += fact*np.sum(np.array(PP(logt)*g_w), axis=1)
		
		return resp_wanted
	    
	def get_time(time, r_time):
		"""Additional time for ramp.
		
		Because of the arbitrary waveform, we need to compute some times before and
		after the actually wanted times for interpolation of the waveform.
		
		Some implementation details: The actual times here don't really matter. We
		create a vector of time.size+2, so it is similar to the input times and
		accounts that it will require a bit earlier and a bit later times. Really
		important are only the minimum and maximum times. The Fourier DLF, with
		`pts_per_dec=-1`, computes times from minimum to at least the maximum,
		where the actual spacing is defined by the filter spacing. It subsequently
		interpolates to the wanted times. Afterwards, we interpolate those again to
		compute the actual waveform response.
		
		Note: We could first call `waveform`, and get the actually required times
		from there. This would make this function obsolete. It would also
		avoid the double interpolation, first in `empymod.model.time` for the
		Fourier DLF with `pts_per_dec=-1`, and second in `waveform`. Doable.
		Probably not or marginally faster. And the code would become much
		less readable.
		
		Parameters
		----------
		time : ndarray
			Desired times
		
		r_time : ndarray
			Waveform times
		
		Returns
		-------
		time_req : ndarray
			Required times
		"""
		tmin = np.log10(max(time.min()-r_time.max(), 1e-10))
		tmax = np.log10(time.max()-r_time.min())
		return np.logspace(tmin, tmax, time.size+2)
		
	
	if ht_filter == 'cos-filter':
	
		def walktem(src, rec, depth, epermH, ftarg, strength, mrec, verb, a, Nt, I, eta_model):  # for htarg
		#def walktem(src, rec, depth, epermH, ht, ft, strength ,mrec, verb, a, Nt, I, eta_model): #for qwe 
		#def walktem(src, rec, depth, epermH, ftarg, strength ,mrec, verb, a, Nt, I, eta_model): # for ftarg
			"""Custom wrapper of empymod.model.bipole.
			
			Here, we compute WalkTEM data using the ``empymod.model.bipole`` routine as
			an example. We could achieve the same using ``empymod.model.dipole`` or
			``empymod.model.loop``.
			
			We model the big source square loop by computing only half of one side of
			the electric square loop and approximating the finite length dipole with 3
			point dipole sources. The result is then multiplied by 8, to account for
			all eight half-sides of the square loop.
		
			The implementation here assumes a central loop configuration, where the
			receiver (1 m2 area) is at the origin, and the source is a 40x40 m electric
			loop, centered around the origin.
	
			Parameters
			----------
		
			Returns
			-------
			WalkTEM : EMArray
				WalkTEM response (dB/dt).
			"""
			
		# === GET REQUIRED TIMES ===
			time = get_time(off_time, waveform_times)
	#		print('len(time) = ', len(time))
	#		print('first index of time', time[0])
	#		print('last index of time', time[-1])
	
	#		print('len(off_time) = ', len(off_time))
	#		print('first index of off_time', off_time[0])
	#		print('last index of off_time', off_time[-1])
	
	#		print('len (waveform_times)', len(waveform_times))
	
	
		# === GET REQUIRED FREQUENCIES ===
		#    time, freq, ft, ftarg = empymod.utils.check_time(
			time, freq, ft, ftarg = empymod.utils.check_time(
				time=time,          # Required times
				signal=-1,           # Switch-off/on response
	#        ft='qwe',           # Use DLF
	#        ftarg= {'rtol': 1e-08},  #
				ft='dlf',           # Use DLF
				ftarg={'dlf': digfilter_cos},  #
				verb=0,                 # 
				)
	
	
		# === COMPUTE FREQUENCY-DOMAIN RESPONSE ===
		# We only define a few parameters here. You could extend this for any
		# parameter possible to provide to empymod.model.bipole.
	
			EM = empymod.model.bipole(res=eta_model,
			freqtime=freq, 
			srcpts=3,
			**model_walktem          # Approx. the finite dip. with 3 points.
			)
		
		# Multiply the frequecny-domain result with
		# i\omega for H->dH/dt.
		
			if output_H_or_EMF == 'H':
				pass
			elif output_H_or_EMF == 'EMF':
				EM *= 2j*np.pi*freq # If commented, shows H-field. If uncommented, computes dH/dt. 
	
		# === Butterworth-type filter (implemented from simpegEM1D.Waveforms.py)===
		# Note: Here we just apply one filter. But it seems that WalkTEM can apply
		#       two filters, one before and one after the so-called front gate
		#       (which might be related to ``delay_rst``, I am not sure about that
		#       part.)
		
		# Skal vi filtrere her etter dH/dt eller over, da vi bare har H?
		
			cutofffreq = custom_LPF  # changed
			h = (1+1j*freq/cutofffreq)**-1   # First order type
			h *= (1+1j*freq/3e5)**-1
			
			EM *= h # Means EM = EM*h

	
			# === CONVERT TO TIME DOMAIN ===
			delay_rst = 1.8e-7               # As stated in the WalkTEM manual
	
			EM, _ = empymod.model.tem(EM[:, None], np.array([1]), freq, time+delay_rst, 1, ft, ftarg)
			EM = np.squeeze(EM)
	
			# === APPLY WAVEFORM ===
			return waveform(time, EM, off_time, waveform_times, waveform_current) 
	

	
	else:
	
		def walktem(src, rec, depth, epermH, htarg, strength, mrec, verb, a, Nt, I, eta_model):  # for htarg
		#def walktem(src, rec, depth, epermH, ht, ft, strength ,mrec, verb, a, Nt, I, eta_model): #for qwe 
		#def walktem(src, rec, depth, epermH, ftarg, strength ,mrec, verb, a, Nt, I, eta_model): # for ftarg
			"""Custom wrapper of empymod.model.bipole.
			
			Here, we compute WalkTEM data using the ``empymod.model.bipole`` routine as
			an example. We could achieve the same using ``empymod.model.dipole`` or
			``empymod.model.loop``.
			
			We model the big source square loop by computing only half of one side of
			the electric square loop and approximating the finite length dipole with 3
			point dipole sources. The result is then multiplied by 8, to account for
			all eight half-sides of the square loop.
		
			The implementation here assumes a central loop configuration, where the
			receiver (1 m2 area) is at the origin, and the source is a 40x40 m electric
			loop, centered around the origin.
	
			Parameters
			----------
		
			Returns
			-------
			WalkTEM : EMArray
				WalkTEM response (dB/dt).
			"""
			
		# === GET REQUIRED TIMES ===
			time = get_time(off_time, waveform_times)
			print('')
			print('len(time) = ', len(time))
			print('first index of time', time[0])
			print('last index of time', time[-1])
			print('')
	
	#		print('len(off_time) = ', len(off_time))
	#		print('first index of off_time', off_time[0])
	#		print('last index of off_time', off_time[-1])
	
	#		print('len (waveform_times)', len(waveform_times))
	
	
		# === GET REQUIRED FREQUENCIES ===
		#    time, freq, ft, ftarg = empymod.utils.check_time(
			time, freq, ft, ftarg = empymod.utils.check_time(
				time=time,          # Required times
				signal=-1,           # Switch-off/on response
	#        ft='qwe',           # Use DLF
	#        ftarg= {'rtol': 1e-08},  #
				ft='dlf',           # Use DLF
				ftarg={'dlf': digfilter_cos},  #
				verb=0,                 # 
				)
	
	
		# === COMPUTE FREQUENCY-DOMAIN RESPONSE ===
		# We only define a few parameters here. You could extend this for any
		# parameter possible to provide to empymod.model.bipole.
	
			EM = empymod.model.bipole(res=eta_model,
			freqtime=freq, 
			srcpts=3,
			**model_walktem          # Approx. the finite dip. with 3 points.
			)
		
		# Multiply the frequecny-domain result with
		# i\omega for H->dH/dt.
		
			if output_H_or_EMF == 'H':
				pass
			elif output_H_or_EMF == 'EMF':
				EM *= 2j*np.pi*freq # If commented, shows H-field. If uncommented, computes dH/dt. 
	
		# === Butterworth-type filter (implemented from simpegEM1D.Waveforms.py)===
		# Note: Here we just apply one filter. But it seems that WalkTEM can apply
		#       two filters, one before and one after the so-called front gate
		#       (which might be related to ``delay_rst``, I am not sure about that
		#       part.)
		
		# Skal vi filtrere her etter dH/dt eller over, da vi bare har H?
		
			cutofffreq = custom_LPF  # changed
			h = (1+1j*freq/cutofffreq)**-1   # First order type
			h *= (1+1j*freq/3e5)**-1
			
			EM *= h # Means EM = EM*h

	#    plt.figure(22)
	#    plt.plot(freq, np.abs(h), '-d',  label = 'empymod filter' )
	#    plt.legend()
	#    plt.xlabel('Frequency (Hz)')
	#    plt.xscale('log')
	#    plt.yscale('symlog')
	#    plt.xticks([ 1e-6, 7.35e-05, 1e-2, 1e2, 1e3,1e4,1e5 ,1e6, 1e10, 1e12 ])
	#   # plt.xlim([10,1e08])
	#    plt.grid(True)
	#    plt.show()
	
	
			# === CONVERT TO TIME DOMAIN ===
			delay_rst = 1.8e-7               # As stated in the WalkTEM manual
	
			EM, _ = empymod.model.tem(EM[:, None], np.array([1]), freq, time+delay_rst, 1, ft, ftarg)
			EM = np.squeeze(EM)
	
			# === APPLY WAVEFORM ===
			return waveform(time, EM, off_time, waveform_times, waveform_current) 
	
	########################################
	# DIELECTRIC 
	
	res_0 = np.array([air_resistivity, 1/subsurf1.cond_dc, 1/subsurf2.cond_dc, 1/subsurf3.cond_dc], dtype='float64')		
#		res_0 = np.array([2e14, 1/subsurf.cond_dc])
	
	eperm_0 = e0*np.array([1, subsurf1.perm0, subsurf2.perm0, subsurf3.perm0], dtype='float64')	
#		eperm_0 = e0*np.array([1, subsurf.perm0])
#		eperm_8 = e0*np.array([1, subsurf.perm8])
	eperm_8 = e0*np.array([1, subsurf1.perm8, subsurf2.perm8, subsurf3.perm8], dtype='float64')


		
#		tau = [0, 1/(subsurf.f_r*2*np.pi)]
	tau = np.array([0, 1/(subsurf1.f_r*2*np.pi), 1/(subsurf2.f_r*2*np.pi), 1/(subsurf3.f_r*2*np.pi)], dtype='float64')

#		c = [0, subsurf.c]
	c = np.array([1, subsurf1.c, subsurf2.c, subsurf3.c], dtype='float64')

	
#		eperm_0_2 = e0*np.array([1, subsurf.perm0_2])
	eperm_0_2 = e0*np.array([1, subsurf1.perm0_2, subsurf2.perm0_2, subsurf3.perm0_2], dtype='float64')

#		eperm_8_2 = e0*np.array([1, subsurf.perm8_2]) # Denne blir lagt til som HF-ledd i Cole-Cole. I Dielectric data er det den med storst rel. 
	eperm_8_2 = e0*np.array([1, subsurf1.perm8_2, subsurf2.perm8_2, subsurf3.perm8_2], dtype='float64') # Denne blir lagt til som HF-ledd i Cole-Cole. I Dielectric data er det den med storst rel. 

		
#		tau_2 = [0, 1/(subsurf.f_r_2*2*np.pi)]
#		c_2 = [0, subsurf.c_2]
	tau_2 = np.array([0, 1/(subsurf1.f_r_2*2*np.pi), 1/(subsurf2.f_r_2*2*np.pi), 1/(subsurf3.f_r_2*2*np.pi)], dtype='float64')
	c_2 = np.array([1, subsurf1.c_2, subsurf2.c_2, subsurf3.c_2], dtype='float64')



	cole_perm_model_2 = {'res': res_0, 'rho_0': res_0, 'eperm_0': eperm_0, 'eperm_8': eperm_8, 
	'tau': tau, 'c': c, 'eperm_0_2': eperm_0_2, 'eperm_8_2': eperm_8_2, 'tau_2': tau_2, 'c_2': c_2, 'func_eta': Cole_models.cole_perm_2}

	cole_perm_model_2_diff = {'res': res_0, 'rho_0': res_0, 'eperm_0': eperm_0, 'eperm_8': eperm_8, 
	'tau': tau, 'c': c, 'eperm_0_2': eperm_0_2, 'eperm_8_2': eperm_8_2, 'tau_2': tau_2, 'c_2': c_2, 'func_eta': Cole_models.cole_perm_2_diff}

	
	

	########################################
		# FDEM - model start:

	I_fd = 1
	N_t_fd = 100

	hTx_fd = h_fd + s_fd
	hRx_fd = h_fd
	hRxRef_fd = h_fd + s_fd + s_fd
	area_fd = np.pi*(a_fd**2)

	src_fd = [a_fd, 0, -hTx_fd, 90, 0]
	rec_fd = [0, 0, -hRx_fd, 0, 90]
	rec_ref_fd = [0, 0, -hRxRef_fd, 0, 90]
	
	strength_fd = 2*np.pi*a_fd*I_fd*N_t_fd		

	sigma_theta = 1 # To verify model with GEM-5 from Huang, 2005
	theta = ((sigma_theta*mu0*0.5)**0.5)*s_fd*((2*np.pi*f)**0.5) # OK
	
#	inp_fd = {'src': src_fd, 'rec': rec_fd, 'depth': depth, 'ftarg': {'dlf': digfilter_cos}, #'dlf': 'key_401_2009', # 'htarg': {'dlf': digfilter}
#	'freqtime': f, 'strength': strength_fd, 'mrec': True,  
#	'verb': 1}

	inp_fd = {'src': src_fd, 'rec': rec_fd, 'depth': depth, 'htarg': {'dlf': digfilter}, #'dlf': 'key_401_2009', # 'htarg': {'dlf': digfilter}
	'freqtime': f, 'strength': strength_fd, 'mrec': True,  
	'verb': 1}


# 'anderson_801_1982'

#	inpRef_fd = {'src': src_fd, 'rec': rec_ref_fd, 'depth': depth,  'ftarg' : {'dlf': digfilter_cos}, #'dlf': 'key_401_2009',
#	'freqtime': f, 'strength': strength_fd, 'mrec': True, 
#	'verb': 1}

	inpRef_fd = {'src': src_fd, 'rec': rec_ref_fd, 'depth': depth,  'htarg' : {'dlf': digfilter}, #'dlf': 'key_401_2009',
	'freqtime': f, 'strength': strength_fd, 'mrec': True, 
	'verb': 1}


	fHz = empymod.bipole(res= [air_resistivity, sigma_theta, sigma_theta, sigma_theta], **inp_fd) # For verification with Huang-paper. 
	fHz_Ref = empymod.bipole(res= [air_resistivity, sigma_theta, sigma_theta, sigma_theta], **inpRef_fd) # For Huang-reprod. 

	# Full model	
	fHz_c = empymod.bipole(	  res=cole_perm_model_2, **inp_fd)
	fHz_Ref_c = empymod.bipole( res=cole_perm_model_2, **inpRef_fd)

	# Diff model
	fHz_c_diff = empymod.bipole(	  res=cole_perm_model_2_diff, **inp_fd)
	fHz_Ref_c_diff = empymod.bipole( res=cole_perm_model_2_diff, **inpRef_fd)


	Ippm = np.real(  ((fHz - fHz_Ref )/( fHz_Ref ))	)*1e06 # Huang GEM-5 replica with induction number..
	Qppm = np.imag(  ((fHz - fHz_Ref )/( fHz_Ref ))	)*1e06

	Ippm_c = np.real(  ((fHz_c - fHz_Ref_c )/( fHz_Ref_c ))	)*1e06 # Cole-Cole FD modeling
	Qppm_c = np.imag(  ((fHz_c - fHz_Ref_c )/( fHz_Ref_c ))	)*1e06

	Ippm_c_diff = np.real(  ((fHz_c_diff - fHz_Ref_c_diff )/( fHz_Ref_c_diff ))	)*1e06 # Cole-Cole FD modeling
	Qppm_c_diff = np.imag(  ((fHz_c_diff - fHz_Ref_c_diff )/( fHz_Ref_c_diff ))	)*1e06


		# FDEM - model end:
########################################		



	times = np.logspace(start_time, 1, N)

	out_custom = np.full( (2, np.size(radius), len(off_time)), np.nan)
	out_step_off = np.full( (2, np.size(radius), len(times)), np.nan)
	
	idx = 0
	for a in radius:
		print('a',a)
	
		if a < 1.1:
			Nt = 9
			print('Nt=',Nt)

		elif (a > 1) and (a < 2.001):
			Nt = 9 # e.g. SkyTEM har 12.5 m x 12.5 m og 4 turns
#			Nt = 1


		elif (a > 2.01) and (a < 9.98):
			Nt = 4 # e.g. SkyTEM har 12.5 m x 12.5 m og 4 turns
#			Nt = 1

			print('Nt=',Nt)
		elif a > 9.99:
			Nt = 1
			print('Nt=',Nt)


			# tTEM 2019 ref, Rx coil is 0.56 x 0.56 m with area 5 m2. 
			# skyTEM is 31.4 m2. 

		if Tx_geometry == 'loop':
			src = [a, 0, -hTx, 90, 0] # sirkel loop #
			strength= 2*np.pi*a*Nt*I # circular loop,
			At = np.pi*(a**2)

		
		elif Tx_geometry == 'square':
			src=[a, a, 0, a,  -hTx, -hTx]  # El. bipole source; half of one side. #
			strength= 8*Nt*I # 4-kantloop,                   # To account for 4 sides of square loop. # 7
			At = (2*a)*(2*a) 


		rec = [0, 0, -hRx, 0, 90] # neg. z is above ground. 
#		depth = 0        # Depth-model, adding air-interface.




#	model_td_00 = {... 'ftarg': {'dlf': digfilter}, ...}
#	model_td_00 = {... 'htarg': {'dlf': digfilter} ...

#	digfilter_cos = wer_101_CosSin_2020b
#		ht_filter = 'cos-filter

		if ht_filter == 'cos-filter':

			model_walktem = {'src': src, 'rec': rec, 'depth': depth, 'epermH': [0,0,0,0], 'ftarg': {'dlf': digfilter_cos}, 'strength': strength, 'mrec': True, 'verb': 0}
					
		else:
			model_walktem = {'src': src, 'rec': rec, 'depth': depth, 'epermH': [0,0,0,0], 'htarg': {'dlf': digfilter}, 'strength': strength, 'mrec': True, 'verb': 0}
	
	
	# For the built - in ideal step-off fcn.:
	
		if output_H_or_EMF == 'H':
		
			if ht_filter == 'cos-filter':

				model_td_step_off = {'src': src, 'rec': rec, 'depth': depth, 'epermH': [0,0,0,0], 'ftarg': {'dlf': digfilter_cos}, 'freqtime': times, 'strength': strength, 'mrec': True, 'signal': -1, 'verb': 0}

			else:
				model_td_step_off = {'src': src, 'rec': rec, 'depth': depth, 'epermH': [0,0,0,0], 'htarg': {'dlf': digfilter}, 'freqtime': times, 'strength': strength, 'mrec': True, 'signal': -1, 'verb': 0}
			
			EMF =  1 # just for to do nothing


		elif output_H_or_EMF == 'EMF':

			if ht_filter == 'cos-filter':

				model_td_step_off = {'src': src, 'rec': rec, 'depth': depth, 'epermH': [0,0,0,0], 'ftarg': {'dlf': digfilter_cos}, 'freqtime': times, 'strength': strength, 'mrec': True, 'signal': 0, 'verb': 0}

			else:
		
				model_td_step_off = {'src': src, 'rec': rec, 'depth': depth, 'epermH': [0,0,0,0], 'htarg': {'dlf': digfilter}, 'freqtime': times, 'strength': strength, 'mrec': True, 'signal': 0, 'verb': 0}


			if Rx_config == 'coincident':

				Ar = At
				Nr = Nt
				print('normalization (inside norm statement) =', normalization)

				if normalization == 'V_pr_A':
					norm = 1/I
				elif normalization == 'V_pr_m2': # pr. eff. rec. area (moment of rec. coil as Spies says p.357)
					norm = 1/(Ar*Nr)
				elif normalization == 'V_pr_A_pr_m2': # # pr. eff. rec. area (moment of rec. coil as Spies says p.357) pr. A
					norm = 1/(I*Ar*Nr)
				elif normalization == 'V_pr_A_pr_m4': # # pr. eff. rec. area and tx moment. 
					norm = 1/(I*Ar*Nr*Ar*Nr)

				elif normalization == 'none':
					norm = 1
				else:
					print('')
					print('Choose a normalization for coincident loop!')
			
				EMF =  mu0*Ar*Nr*norm
	
			elif Rx_config == 'central':

				if normalization == 'V_pr_A':
					norm = 1/I
				elif normalization == 'V_pr_A_pr_m2':
					norm = 1/(I*Ar*Nr)
				elif normalization == 'V_pr_A_pr_m4': # pr. eff. rec. area and tx moment. 
					norm = 1/(I*Ar*Nr*At*Nt)

				elif normalization == 'none':
					norm = 1
				else:
					print('')
					print('Choose a normalization for central loop!')
					
				

				EMF = mu0*Ar*Nr*norm

	#	print('EMF = ', EMF)
		kx = 0
		for x in soln_type:
		
			if x == 'Diff': # # Custom waveform
				walktem_perm = EMF*walktem(a=a, Nt=Nt, I=I, eta_model=cole_perm_model_2_diff, **model_walktem)  # # Diff soln.
				tdem_step_off = EMF*empymod.bipole(res=cole_perm_model_2_diff, **model_td_step_off) # # Diff soln.

			elif x == 'Full': # # Built in step-off (ideal) waveform
				walktem_perm = EMF*walktem(a=a, Nt=Nt, I=I, eta_model=cole_perm_model_2, **model_walktem) # # Full soln.
				tdem_step_off = EMF*empymod.bipole(res=cole_perm_model_2, **model_td_step_off) # # Full soln.


			out_custom[kx, idx, :] = walktem_perm
			out_step_off[kx, idx, :] = tdem_step_off
			
			
			kx = kx + 1


		idx = idx + 1
		





	return off_time, times, out_custom, out_step_off, radius, waveform_times[-1], Ar, Nr, I, soln_type,f, Ippm, Qppm, Ippm_c, Qppm_c, Ippm_c_diff, Qppm_c_diff, I_fd, N_t_fd, theta, ylabeltext, noise, noiselabel

# copy: off_time, times, out_custom, out_step_off, radius, waveform_times[-1], Ar, Nr, I, soln_type



