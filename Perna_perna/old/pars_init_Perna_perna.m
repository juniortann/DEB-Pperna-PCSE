function [par, metaPar, txtPar] = pars_init_Perna_perna(metaData)

metaPar.model = 'std'; 

%% reference parameter (not to be changed) 
par.T_ref = 293.15;   free.T_ref = 0;   units.T_ref = 'K';        label.T_ref = 'Reference temperature'; 

%% core primary parameters 
par.T_A = 8000;       free.T_A   = 0;   units.T_A = 'K';          label.T_A = 'Arrhenius temperature'; 
par.z = 2.9929;       free.z     = 1;   units.z = '-';            label.z = 'zoom factor'; 
par.F_m = 6.5;        free.F_m   = 0;   units.F_m = 'l/d.cm^2';   label.F_m = '{F_m}, max spec searching rate'; 
par.kap_X = 0.8;      free.kap_X = 0;   units.kap_X = '-';        label.kap_X = 'digestion efficiency of food to reserve'; 
par.kap_P = 0.1;      free.kap_P = 0;   units.kap_P = '-';        label.kap_P = 'faecation efficiency of food to faeces'; 
par.v = 1.4348;       free.v     = 0;   units.v = 'cm/d';         label.v = 'energy conductance'; 
par.kap = 0.9;        free.kap   = 0;   units.kap = '-';          label.kap = 'allocation fraction to soma'; 
par.kap_R = 0.95;     free.kap_R = 0;   units.kap_R = '-';        label.kap_R = 'reproduction efficiency'; 
par.p_M = 30.9514;    free.p_M   = 1;   units.p_M = 'J/d.cm^3';   label.p_M = '[p_M], vol-spec somatic maint'; 
par.p_T = 0;          free.p_T   = 0;   units.p_T = 'J/d.cm^2';   label.p_T = '{p_T}, surf-spec somatic maint'; 
par.k_J = 0.002;      free.k_J   = 0;   units.k_J = '1/d';        label.k_J = 'maturity maint rate coefficient'; 
par.E_G = 2347.7805;  free.E_G   = 0;   units.E_G = 'J/cm^3';     label.E_G = '[E_G], spec cost for structure'; 
par.E_Hb = 6.754e-06; free.E_Hb  = 0;   units.E_Hb = 'J';         label.E_Hb = 'maturity at birth'; 
par.E_Hp = 5.902e+02; free.E_Hp  = 0;   units.E_Hp = 'J';         label.E_Hp = 'maturity at puberty'; 
par.h_a = 2.321e-10;  free.h_a   = 0;   units.h_a = '1/d^2';      label.h_a = 'Weibull aging acceleration'; 
par.s_G = 0.0001;     free.s_G   = 0;   units.s_G = '-';          label.s_G = 'Gompertz stress coefficient'; 

%% other parameters 
par.T_AH = 250600;    free.T_AH  = 0;   units.T_AH = 'K';         label.T_AH = 'Arrh. temp for upper boundary'; 
par.T_AL = 55400;     free.T_AL  = 0;   units.T_AL = 'K';         label.T_AL = 'Arrh. temp for lower boundary'; 
par.T_A_Br = 8000;    free.T_A_Br = 0;   units.T_A_Br = 'K';       label.T_A_Br = 'Arrhenius temperature'; 
par.T_H = 309;        free.T_H   = 0;   units.T_H = 'K';          label.T_H = 'Upper temp boundary'; 
par.T_L = 273;        free.T_L   = 0;   units.T_L = 'K';          label.T_L = 'Lower temp boundary'; 
par.X_K = 2.24;       free.X_K   = 1;   units.X_K = '-';          label.X_K = 'half-saturation coeficient for chl-a in brazilian population'; 
par.Y_K = 103.5;      free.Y_K   = 1;   units.Y_K = '-';          label.Y_K = 'half-saturation coeficient for suspended matter in brazilian population'; 
par.c_chl = 52;       free.c_chl = 0;   units.c_chl = '-';        label.c_chl = 'Carbon / Chlorophyll ratio'; 
par.del_M = 0.32516;  free.del_M = 0;   units.del_M = '-';        label.del_M = 'shape coefficient after metam'; 
par.del_Mb = 5.0744e-25;  free.del_Mb = 0;   units.del_Mb = '-';       label.del_Mb = 'shape coefficient at birth'; 
par.f = 1;            free.f     = 0;   units.f = '-';            label.f = 'scaled functional response for fsubtidal data'; 
par.z_Br = 10.1997;   free.z_Br  = 1;   units.z_Br = '-';         label.z_Br = 'zoom factor for brazilian population'; 

%% set chemical parameters from Kooy2010 
[par, units, label, free] = addchem(par, units, label, free, metaData.phylum, metaData.class); 

%% Pack output: 
txtPar.units = units; txtPar.label = label; par.free = free; 
