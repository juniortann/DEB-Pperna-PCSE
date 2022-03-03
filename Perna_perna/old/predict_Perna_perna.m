function [prdData, info] = predict_Perna_perna(par, data, auxData)
  
  % unpack par, data, auxData
  cPar = parscomp_st(par); vars_pull(par); 
  vars_pull(cPar);  vars_pull(data);  vars_pull(auxData);
  
  if f > 1 || del_Mb < 0 || kap > 0.9 || X_K < 0.5 || Y_K < 103.5 || X_K > 2.24 || Y_K > 207 ... #X_K and Y_K half of Santos region
           || T_A_Br > 13000 || T_A_Br < 6000
       
  prdData = []; info = 0; return 
  end

  % compute temperature correction factors
  pars_TC = [T_A T_L T_H T_AL T_AH];
  
  TC_ab = tempcorr(temp.ab, T_ref, T_A);
  TC_tp = tempcorr(temp.tp, T_ref, T_A);
  TC_am = tempcorr(temp.am, T_ref, T_A);
  TC_tL = tempcorr(temp.tL, T_ref, T_A);
  
  TC_SBr = tempcorr(temp.tL_SBr, T_ref, T_A_Br); % TC for Santos, Brazil
  TC_ItaBr = tempcorr(temp.tL_ItaBr, T_ref, T_A_Br); % TC for Armação de Itapocoroy, Brazil
  TC_Uba = tempcorr(temp.tL_Uba, T_ref, T_A_Br); % TC for Ubatuba, Brazil
  TC_Flor = tempcorr(temp.Lt_Flor, T_ref, T_A_Br); % TC for Ubatuba, Brazil
  
  %% Functional responses
  
  % Armação de Itapocoroy
  Chl = 4.270207;                            % micrograms.chl-a/L, mean chlorophyll concentration in the region
  POC = 444.81046;                           % micrograms.POC/L,  mean particulate organic carbon (POC) concentration in the region
  X = Chl; 
  Y = max(0, POC - (c_chl * Chl));            % micrograms/L, POC that is not phytoplankton (using C:chl ratio for region by Bucci, 2010)
  f_ItaBr = X / (X + (X_K * (1 + Y / Y_K)));  % Estimate of functional response
  if f_ItaBr > 1                              % Constraint value of f
      prdData = []; info = 0; return
  end
  
  % Santos
  Chl = 4.4837694;                          % micrograms.chl-a/L, 2006 chlorophyll concentration in the region
  POC = 414.0;                              % micrograms.POC/L,  2006 particulate organic carbon (POC) concentration in the region
  X = Chl; 
  Y = max(0, POC - (c_chl * Chl));          % micrograms/L, POC that is not phytoplankton (using C:chl ratio for region by Bucci, 2010)
  f_SBr = X / (X + (X_K * (1 + Y / Y_K)));  % Estimate of functional response
  if f_SBr > 1                              % Constraint value of f
      prdData = []; info = 0; return
  end
  
  %% zero-variate data

  % life cycle
  pars_tp = [g; k; l_T; v_Hb; v_Hp];               % compose parameter vector
  [tau_p, tau_b, l_p, l_b, info] = get_tp(pars_tp, f); % -, scaled times & lengths at f

  % birth
  L_b = L_m * l_b;                  % cm, structural length at birth at f
  Lw_b = L_b/ del_M;                % cm, physical length at birth at f
  Ww_b = L_b^3 * (1 + f * ome);     % g, wet weight at birth at f (remove d_V for wet weight)
  aT_b = tau_b/ (k_M*TC_ab);        % d, age at birth at f and T
  
  % puberty 
  pars_tp = [g; k; l_T; v_Hb; v_Hp];  % compose parameter vector
  [tau_p, tau_b, l_p, l_b, info] = get_tp(pars_tp, f);
  L_p = L_m * l_p;                    % cm, structural length at puberty at f
  Lw_p = L_p/ del_M;                  % cm, physical length at puberty at f
  Ww_p = L_p^3 * (1 + f * ome);       % g,  wet weight at puberty
  aT_p = tau_p/ k_M / TC_tp;                   % d, age at puberty at f and T
  
 % ultimate   
  l_i = f - l_T;                    % -, scaled ultimate length at f
  L_i = L_m * l_i;                  % cm, ultimate structural length at f
  Lw_i = L_i/ del_M;                % cm, ultimate physical length at f
  Ww_i = L_i^3 * (1 + f * ome);     % g, ultimate wet weight (remove d_V for wet weight)
   
  % ultimate for Brazilian population
    
  p_Am_Br = z_Br * p_M/ kap;            % J/d.cm^2, {p_Am} spec assimilation flux  
  L_i_br = f_SBr * kap * p_Am_Br / p_M;     % cm, ultimate structural length at f
  Lw_i_br = L_i_br/ del_M;                 % cm, ultimate total length at f
   
  % life span
  pars_tm = [g; l_T; h_a/ k_M^2; s_G];  % compose parameter vector at T_ref
  t_m = get_tm_s(pars_tm, f, l_b);      % -, scaled mean life span at T_ref
  aT_m = t_m/ k_M/ TC_am;               % d, mean life span at T
  
  % pack to output
  prdData.ab = aT_b;
  prdData.tp = aT_p;
  prdData.am = aT_m;
  prdData.Lb = Lw_b;
  prdData.Lp = Lw_p;
  prdData.Li = Lw_i;
  prdData.Li_br = Lw_i_br;
  prdData.Wwb = Ww_b;
  
% uni-variate data
  
  % time-length 1 - Subtidal Durban, South Africa
  TC = TC_tL;
  L_b = L_m * get_lb([g; k; v_Hb], f); L_i = L_m * f;
  rT_B = TC * k_M/ 3/ (1 + f/ g);               % 1/d, von Bert growth rate 
  L = L_i - (L_i - L_b) * exp(-rT_B * tL(:,1)); % cm, struct length
  ELw_subt = L/ del_M;                          % cm, total length
  
  % length-weight
  EWd_L = (LW(:,1) * del_M).^3 * d_V * (1 + f * w); % g, dry weight
   
  
  %% pars_tp for Brazil
  p_Am_Br = z_Br * p_M/ kap;               % J/d.cm^2, {p_Am} spec assimilation flux
  E_m_Br = p_Am_Br/ v;                     % J/cm^3, reserve capacity [E_m]
  g_Br = E_G/ (kap* E_m_Br);               % -, energy investment ratio
  m_Em_Br = y_E_V * E_m_Br/ E_G;           % mol/mol, reserve capacity 
  w_Br = m_Em_Br * w_E/ w_V;               % -, contribution of reserve to weight
  L_m_Br = v/ k_M/ g_Br;                   % cm, max struct length
  pars_tp_Br = [g_Br; k; l_T; v_Hb; v_Hp];       % parameter vector like pars_tp, but for brazilian population
   
  % time-length - Santos Bay, Brazil
  
  [t_p, t_b, l_p, l_b, info] = get_tp(pars_tp_Br, f_SBr);  
  L_b = L_m_Br * l_b; L_i = L_m_Br * f_SBr; %cm, struct lengths
  rT_B = TC_SBr * k_M/ 3/ (1 + f_SBr/ g_Br);     % 1/d, von Bert growth rate 
  %
  L = L_i - (L_i - L_b) * exp(-rT_B * tL_SBr(:,1)); % cm, struct length
  ELw_SBr = L/ del_M;                          % cm, total length
  
  % t-L Armação do Itapocoroy, Brazil
  [t_p, t_b, l_p, l_b, info] = get_tp(pars_tp_Br, f_ItaBr);  
  L_b = L_m_Br * l_b; L_i = L_m_Br * f_ItaBr; %cm, struct lengths
  rT_B = TC_ItaBr * k_M/ 3/ (1 + f_ItaBr/ g_Br);     % 1/d, von Bert growth rate 
  %
  L = L_i - (L_i - L_b) * exp(-rT_B * tL_ItaBr(:,1)); % cm, struct length
  ELw_ItaBr = L/ del_M;                          % cm, total length
  
  % t-W Armação do Itapocoroy, Brazil
   EWw_ItaBr = (L_i - (L_i - L_b) * exp( - rT_B * (tW_ItaBr(:,1)))).^3 * (1 + f_ItaBr * w); % g, wet weight

  % t-L Ubatuba, Brazil
  Chl =  1.4290122;                            % micrograms.chl-a/L, mean chlorophyll concentration in the region
  POC = 280.92624;                             % micrograms.POC/L,  mean particulate organic carbon (POC) concentration in the region
  X = Chl; 
  Y = max(0, POC - (c_chl * Chl));            % micrograms/L, POC that is not phytoplankton (using C:chl ratio for region by Bucci, 2010)
  f_estim = X / (X + (X_K * (1 + Y / Y_K)));  % Estimate of functional response
  if f_estim > 1                              % Constraint value of f
      prdData = []; info = 0; return
  end  
  
  
  [t_p, t_b, l_p, l_b, info] = get_tp(pars_tp_Br, f_estim);  
  L_b = L_m_Br * l_b; L_i = L_m_Br * f_estim;             %cm, struct lengths
  rT_B = TC_Uba * k_M/ 3/ (1 + f_estim/ g_Br);       % 1/d, von Bert growth rate 
  %
  L = L_i - (L_i - L_b) * exp(-rT_B * tL_Uba(:,1));  % cm, struct length
  ELw_Uba = L/ del_M;                                % cm, total length
   
  % L-t Florianópolis, Brazil
  Chl =  6.3641295;                        % micrograms.chl-a/L, 2008 chlorophyll concentration in the region
  POC = 514.0;                             % micrograms.POC/L,  mean particulate organic carbon (POC) concentration in the region
  X = Chl; 
  Y = max(0, POC - (c_chl * Chl));          % micrograms/L, POC that is not phytoplankton (using C:chl ratio for region by Bucci, 2010)
  f_Flor = X / (X + (X_K * (1 + Y / Y_K))); % Estimate of functional response  
  if f_Flor > 1                             % Constraint value of f
      prdData = []; info = 0; return
  end
  
  L_0 = [26.61, 27.55, 21.57, 26.61, 27.55, 21.57]/ 10; % cm, mean initial sizes at experiment
  L_0_mean = mean(L_0);
  
  L_i = L_m_Br * f_Flor;                         %cm, ultimate struct length
  rT_B = TC_Flor * k_M/ 3/ (1 + f_Flor/ g_Br);   % 1/d, von Bert growth rate 

  L = L_i - (L_i - L_0_mean) * exp( -rT_B * Lt_Flor(:,1));
  ELw_Flor = L/ del_M;
  
  % pack to output
  prdData.tL = ELw_subt;
  prdData.LW = EWd_L;
  prdData.tL_SBr = ELw_SBr;
  prdData.tL_ItaBr = ELw_ItaBr;
  prdData.tW_ItaBr = EWw_ItaBr;
  prdData.tL_Uba = ELw_Uba;
  prdData.Lt_Flor = ELw_Flor;
