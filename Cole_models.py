import numpy as np

# Ved wrong shape feil!
# NB! H	vis du skal ha bare et lag med jord, maa du endre np.ones (4) til np.ones (2)

def cole_perm(inp, p_dict):
    """ Cole and Cole (1941). Finden"""
    iotc = np.outer(2j*np.pi*p_dict['freq'], inp['tau'])**inp['c']
    jw = np.outer(2j*np.pi*p_dict['freq'], np.ones(4  ))
    # Compute the complex admittivity described by a
    # constant (DC) conductivity + the Cole-Cole permittivity
    epsilonH = inp['eperm_8'] + (inp['eperm_0']-inp['eperm_8'])/(1 + iotc)
    epsilonV = epsilonH/p_dict['aniso']**2
    etaH = 1/inp['rho_0'] + jw*epsilonH
    etaV = 1/inp['rho_0'] + jw*epsilonV
    return etaH, etaV




def cole_perm_2(inp, p_dict):
    """ Cole and Cole (1941). Finden"""
    iotc = np.outer(2j*np.pi*p_dict['freq'], inp['tau'])**inp['c']
    iotc_2 = np.outer(2j*np.pi*p_dict['freq'], inp['tau_2'])**inp['c_2']
    jw = np.outer(2j*np.pi*p_dict['freq'], np.ones(4  ))
    # Compute the complex admittivity described by a
    # constant (DC) conductivity + the Cole-Cole permittivity
    epsilonH = inp['eperm_8_2'] + (inp['eperm_0']-inp['eperm_8_2'])/(1 + iotc) + ((inp['eperm_0_2']-inp['eperm_8_2'])/(1 + iotc_2)) # PS! HF-leddene eperm_8 og eperm_8_2 skal vaere like. 
    epsilonV = epsilonH/p_dict['aniso']**2
    etaH = 1/inp['rho_0'] + jw*epsilonH
    etaV = 1/inp['rho_0'] + jw*epsilonV
    return etaH, etaV

def cole_perm_2_diff(inp, p_dict):
    """ Cole and Cole (1941). Finden"""
    iotc = np.outer(2j*np.pi*p_dict['freq'], inp['tau'])**inp['c']
    iotc_2 = np.outer(2j*np.pi*p_dict['freq'], inp['tau_2'])**inp['c_2']
    jw = np.outer(2j*np.pi*p_dict['freq'], np.ones(4 ) )
    # Compute the complex admittivity described by a
    # constant (DC) conductivity + the Cole-Cole permittivity

    epsilonH = (inp['eperm_0']-inp['eperm_8_2'])/(1 + iotc) + ((inp['eperm_0_2']-inp['eperm_8_2'])/(1 + iotc_2)) # PS! HF-leddene eperm_8 og eperm_8_2 skal vaere like. 

#    epsilonH =  (inp['eperm_0']-inp['eperm_8_2'])/(1 + iotc) + ((inp['eperm_0_2']-inp['eperm_8_2'])/(1 + iotc_2)) # PS! HF-leddene eperm_8 og eperm_8_2 skal vaere like. 

    epsilonV = epsilonH/p_dict['aniso']**2
    etaH = 1/inp['rho_0'] + jw*epsilonH
    etaV = 1/inp['rho_0'] + jw*epsilonV
    return etaH, etaV
    



def cole_perm_2_4layers(inp, p_dict):
    """ Cole and Cole (1941). Finden"""
    iotc = np.outer(2j*np.pi*p_dict['freq'], inp['tau'])**inp['c']
    iotc_2 = np.outer(2j*np.pi*p_dict['freq'], inp['tau_2'])**inp['c_2']
    jw = np.outer(2j*np.pi*p_dict['freq'], np.ones(5  ))
    # Compute the complex admittivity described by a
    # constant (DC) conductivity + the Cole-Cole permittivity
    epsilonH = inp['eperm_8_2'] + (inp['eperm_0']-inp['eperm_8_2'])/(1 + iotc) + ((inp['eperm_0_2']-inp['eperm_8_2'])/(1 + iotc_2)) # PS! HF-leddene eperm_8 og eperm_8_2 skal vaere like. 
    epsilonV = epsilonH/p_dict['aniso']**2
    etaH = 1/inp['rho_0'] + jw*epsilonH
    etaV = 1/inp['rho_0'] + jw*epsilonV
    return etaH, etaV

def cole_perm_2_diff_4layers(inp, p_dict):
    """ Cole and Cole (1941). Finden"""
    iotc = np.outer(2j*np.pi*p_dict['freq'], inp['tau'])**inp['c']
    iotc_2 = np.outer(2j*np.pi*p_dict['freq'], inp['tau_2'])**inp['c_2']
    jw = np.outer(2j*np.pi*p_dict['freq'], np.ones(5 ) )
    # Compute the complex admittivity described by a
    # constant (DC) conductivity + the Cole-Cole permittivity

    epsilonH = (inp['eperm_0']-inp['eperm_8_2'])/(1 + iotc) + ((inp['eperm_0_2']-inp['eperm_8_2'])/(1 + iotc_2)) # PS! HF-leddene eperm_8 og eperm_8_2 skal vaere like. 

#    epsilonH =  (inp['eperm_0']-inp['eperm_8_2'])/(1 + iotc) + ((inp['eperm_0_2']-inp['eperm_8_2'])/(1 + iotc_2)) # PS! HF-leddene eperm_8 og eperm_8_2 skal vaere like. 

    epsilonV = epsilonH/p_dict['aniso']**2
    etaH = 1/inp['rho_0'] + jw*epsilonH
    etaV = 1/inp['rho_0'] + jw*epsilonV
    return etaH, etaV
        





def cole_cole(inp, p_dict):
	"""Cole and Cole (1941). Werthemuller"""
	# Compute complex conductivity from Cole-Cole
	iotc = np.outer(2j*np.pi*p_dict['freq'], inp['tau'])**inp['c']
	condH = inp['cond_8'] + (inp['cond_0']-inp['cond_8'])/(1+iotc)
	condV = condH/p_dict['aniso']**2
	# Add electric permittivity contribution
	etaH = condH + 1j*p_dict['etaH'].imag
	etaV = condV + 1j*p_dict['etaV'].imag
	return etaH, etaV

