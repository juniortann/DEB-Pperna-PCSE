import numpy as np

def C2K(T):
    """Transform Celcius to Kelvin"""
    K = T + 273.15
    return K

def K2C(T):
    """Transform Kelvin to Celcius"""
    C = T - 273.15
    return C

def tempcorr(T, pars_T): # T_A, T_L, T_H, T_AL, T_AH, T_ref
    """Arrhenius temperature correction factor"""
    T_A  = pars_T[0] #Arrh. temp
    T_L  = pars_T[1]  # Lower temp boundary
    T_H  = pars_T[2]  # Upper temp boundary
    T_AL = pars_T[3]  # Arrh. temp for lower boundary
    T_AH = pars_T[4]  # Arrh. temp for upper boundary
    T_ref = pars_T[5] # Reference temp

    TC = np.exp(T_A/ T_ref - T_A / T) * \
    (1 + np.exp(T_AL / T_ref - T_AL/ T_L) + np.exp(T_AH/ T_H - T_AH / T_ref)) / \
	(1 + np.exp(T_AL / T     - T_AL/ T_L) + np.exp(T_AH/ T_H - T_AH / T    ))
    return TC

def func(par, Chlor):
    """Functional response function"""
    return par[0] * (Chlor / (Chlor + par[1])) #9.95 is Max IR

def residuals(par, Chlor, PLP, error):        #The residual is the actual function to minimize
    """Residual function"""
    return (PLP - func(par, Chlor))/error

def nmfunc(par, Chlor, PLP, error):
    """Get sum squares of residuals"""
    residuals = (PLP - func(par, Chlor))/error
    objective = (residuals**2).sum()
    return objective

def read_resultsMyPet(file):

    """
    Loads results_mypet.mat, returns a DataFrame for checking results
    and a dictionary with parameters and values
    file: results_mypet.mat location

    example: pars, df = read_resultsMyPet(file)
    """

    from scipy.io import loadmat
    from pandas import DataFrame

    pars_dict = loadmat(file, simplify_cells=True)
    par = pars_dict['par']
    del par['free']

    df = DataFrame(pars_dict['txtPar']['label'], index=[0])
    df = df.append(pars_dict['par'], ignore_index=True)
    df = df.append(pars_dict['txtPar']['units'], ignore_index=True)
    return par, df

def parscomp(pars):
    """
    Extracts some compound parameters for growth simulation from pars.
    input:
        - pars = [z, p_M, kap, kap_X, v, E_G, k_J, p_T]
    output:
        - dictionary with parscomp
        - parscomp = dict(p_Am, p_Xm, E_m, k_M, k, g, L_m, L_T, l_T)

    Example:
    pars = [z, p_M, kap, kap_X, v, E_G, k_J, p_T]
    parscomp = parscomp(pars)
    """
    z, p_M, kap, kap_X, v, E_G, k_J, p_T = pars
    # Feeding
    p_Am = z*p_M/kap # J/d.cm^2, {p_Am}, spec assimilation flux
    p_Xm = p_Am/ kap_X # J/d.cm^2, max spec feeding power
    # Reserve
    E_m = p_Am/ v # J/cm^3 [E_m], reserve capacity
    # Maintenence
    k_M = p_M/E_G # 1/d, somatic maintenance rate coefficient
    k = k_J/k_M # no dimension, maintenance ratio
    # Growth
    g = E_G/ kap/ E_m # -, energy investment ratio

    L_m = v/ k_M/ g # cm, maximum length
    L_T = p_T/ p_M # cm, heating length (also applies to osmotic work)

    l_T = L_T/ L_m # - , scaled heating length

    # Pack parscomp
    parscomp = dict(p_Am=p_Am, p_Xm=p_Xm, E_m=E_m, k_M=k_M, k=k,
                    g=g, L_m=L_m, L_T=L_T, l_T=l_T)

    return parscomp


def get_pars(file):
    """
    Extract parameters and compound parameters related to growth from
    results_mypet.mat file.
    Input: string with file name
    """
    # Extract parameters
    pars, df = read_resultsMyPet(file)  # Extracting variables

    # Extract compound parameters from base parameters
    p_parscomp = [pars['z'], pars['p_M'], pars['kap'], pars['kap_X'], pars['v'], pars['E_G'], pars['k_J'], pars['p_T']]
    comp = parscomp(p_parscomp)

    pars = {**pars, **comp} # Merge the two

    return pars

def f_POC(X, Y, X_K, Y_K, C_chl):
    """
    Functional response taking POC into account.
    See Kooijman, 2006 (Pseudofaeces production in bivalves).
    Input:
     - X: Food availability
     - Y: POC particles
     - X_K: Food Half-saturation coeficient
     - Y_K: Particle saturation coeficient
     - C_chl: Carbon to chl ratio
    """
    Ycorrected = Y - (C_chl * X)             # Remove chl contribution to POC
    X_K_app = X_K * (1 + (Ycorrected / Y_K)) # Kooijman, 2006
    f = X / (X + X_K_app)

    return f

def vB_abj(f, T, t, pars, pars_TC):
    """
    Simulates von Bertalanffy growth for abj DEB model.
    Input:
        - f: funcional response
        - T: Temperature (Celcius)
        - t: time points for simulation
        - pars = [p_Am, p_M, E_Hb, E_Hj, kap, g, k_M, v, L_m, l_T, del_M]
        - pars_TC = [T_A, T_L, T_H, T_AL, T_AH, T_ref]
    Output: array with length per time values

    Example:
    pars = [p_Am, p_M, E_Hb, E_Hj, kap, g, k_M, v, L_m, l_T, del_M]
    L = vB_abj(f, TC, pars)
    """
    # Unpack pars
    p_Am, p_M, E_Hb, E_Hj, kap, g, k_M, v, L_m, l_T, del_M = pars

    # Temperature correction
    TC = tempcorr(C2K(T), pars_TC)

    ### Acceleration for abj model
    # Acceleration is important in abj, because if you try to simulate growth
    # without it, L_i will be underestimated. You can't use all std equations in abj parameters.
    U_Hb = E_Hb/ p_Am; v_Hb = (U_Hb / (1-kap)) * g**2 * k_M**3/ v**2
    U_Hj = E_Hj/ p_Am; v_Hj = (U_Hj / (1-kap)) * g**2 * k_M**3/ v**2
    l_b = v_Hb**(1/3);    l_j = v_Hj**(1/3);
    s_M = l_j/ l_b # Acceleration factor

    # Dependent on f
    #l_i_scaled = f * kap * (p_Am/p_M) # scalel ultimate length L_m = L_i if f=1. Only works for std.
    l_i = f * s_M - l_T # Ultimate scaled structural length
    l_is = l_i * L_m # Unscaling to get ultimate structural length

    # r_B_scaled = (p_M / 3) / (1 + (f / g)) # This overestimates r_B
    r_B_scaled =(1/ 3/ (1 + f/ g))
    r_B = r_B_scaled * k_M * TC # von Bertalanffy growth rate

    # von Bertalanffy simulation
    l =  l_is - (l_is - 1) * np.exp(-r_B * t)
    L = l/del_M # converting structural to physical length
    return L

def get_rb(f, TC, pars):
    """
    Simulates von Bertalanffy growth for abj DEB model.
    Input:
        - f: funcional response
        - TC: temperature correction factor
        - pars: a list with parameters [p_M, g, k_M]
    Output: value or r_B in given conditions

    Example:
    L = vB_abj(f, TC, pars)
    """
    # Unpack pars
    p_M, g, k_M = pars

    # r_B_scaled = (p_M / 3) / (1 + (f / g)) # This overestimates r_B
    r_B_scaled = (1/ 3/ (1 + f/ g))
    r_B = r_B_scaled * k_M * TC # von Bertalanffy growth rate

    return r_B

def get_li(f, pars):
    """
    Simulates von Bertalanffy growth for abj DEB model.
    Input:
        - f: funcional response
        - TC: temperature correction factor
        - pars: a list with parameters [p_Am, p_M, E_Hb, E_Hj, kap, g, k_M, v, L_m, l_T, del_M]
        - t: time points for simulation
    Output: array with length per time values

    Example:
    pars = [p_Am, p_M, E_Hb, E_Hj, kap, g, k_M, v, L_m, l_T, del_M]
    L = vB_abj(f, TC, pars)
    """
    # Unpack pars
    p_Am, p_M, E_Hb, E_Hj, kap, g, k_M, v, L_m, l_T, del_M = pars

    ### Acceleration for abj model
    # Acceleration is important in abj, because if you try to simulate growth
    # without it, L_i will be underestimated. You can't use all std equations in abj parameters.
    U_Hb = E_Hb/ p_Am; v_Hb = (U_Hb / (1-kap)) * g**2 * k_M**3/ v**2
    U_Hj = E_Hj/ p_Am; v_Hj = (U_Hj / (1-kap)) * g**2 * k_M**3/ v**2
    l_b = v_Hb**(1/3);    l_j = v_Hj**(1/3);
    s_M = l_j/ l_b # Acceleration factor

    # Dependent on f
    #l_i_scaled = f * kap * (p_Am/p_M) # scalel ultimate length L_m = L_i if f=1. Only works for std.
    l_i = f * s_M - l_T # Ultimate scaled structural length
    l_is = l_i * L_m # Unscaling to get ultimate structural length
    L_i = l_is / del_M
    return L_i

def rb_li(f, T, p):
    """
    Estimates value for von Bertalanffy growth rate (r_B) and ultimate physical assymptotic length (L_i)
    Input:
     - f = functional response
     - T = Temperature in Celcius
     - p = dictionary with species parameters (see get_pars)
    Output:
     list(r_B, L_i)
    Example:
    r_B, L_i = rb_li(f, T, p)
    """
    #Temperature correction
    T = C2K(T)
    pars_T = [p['T_A'], p['T_L'], p['T_H'], p['T_AL'], p['T_AH'], p['T_ref']]
    TC = tempcorr(T, pars_T)

    # Get r_B
    pars_rb = [p['p_M'], p['g'], p['k_M']]
    r_B = get_rb(f, TC, pars_rb)

    # Get L_i
    pars_li = [p['p_Am'], p['p_M'], p['E_Hb'], p['E_Hj'], p['kap'], p['g'], p['k_M'], p['v'], p['L_m'], p['l_T'], p['del_M']]
    L_i = get_li(f, pars_li)

    return r_B, L_i

def OverallError(Y_pred, Y_obs):
    """
    Overall Error equation.
    "The overall error computed for each comparison aims to quantify the
    difference between model estimation and real data. A null value of E is assumed
    to be a perfect match be tween the model and the observed data and increasing
    values represent increasing errors (Saraiva et al. 2011)"

    Input:
        - Y_Pred: array with predicted values
        - Y_obs: array with observed values
    """
    eps = np.sqrt(np.log(np.array(Y_pred)/np.array(Y_obs))**2)

    E = np.exp(np.var(eps))-1

    return E
