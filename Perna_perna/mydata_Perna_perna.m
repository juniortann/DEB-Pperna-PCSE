function [data, auxData, metaData, txtData, weights] = mydata_Perna_perna

%% set metaData

metaData.phylum     = 'Mollusca'; 
metaData.class      = 'Bivalvia'; 
metaData.order      = 'Mytiloida'; 
metaData.family     = 'Mytilidae';
metaData.species    = 'Perna_perna'; 
metaData.species_en = 'Brown mussel'; 
metaData.ecoCode.climate = {'MA', 'MB'};
metaData.ecoCode.ecozone = {'MA'};
metaData.ecoCode.habitat = {'0jMp', 'jiMb', 'jiMi'};
metaData.ecoCode.embryo  = {'Mp'};
metaData.ecoCode.migrate = {};
metaData.ecoCode.food    = {'biPp'};
metaData.ecoCode.gender  = {'D'};
metaData.ecoCode.reprod  = {'O'};
metaData.T_typical  = C2K(24); % K, body temp
metaData.data_0     = {'ab'; 'aj'; 'ap'; 'am'; 'Lb'; 'Lj'; 'Lp'; 'Li'; 'Wwb'; 'GSI'}; 
metaData.data_1     = {'t-L'; 'L-Ww'; 'T-JO'}; 

metaData.COMPLETE = 2.6; % using criteria of LikaKear2011

metaData.author  = {'Cristian Monaco';'Morgana Tagliarolo'; 'Valeria Montalto'; 'Gianluca Sara'; 'Christopher D. McQuaid'};    
metaData.date_subm = [2017 08 27];              
metaData.email    = {'cristianmonaco@gmail.com'};            
metaData.address  = {'Rhodes University, South Africa'};  

metaData.author_mod_1   = {'Tan Tjui Yeuw'; 'Fabio Stucchi Vannucchi'};    
metaData.date_mod_1     = [2021 06 08];              
metaData.email_mod_1    = {'tan.tjui-yeuw@unesp.br'};            
metaData.address_mod_1  = {'São Paulo State University (UNESP), Brazil'};   

metaData.curator     = {'Starrlight Augustine'};
metaData.email_cur   = {'sta@akvaplan.nuiva.no'}; 
metaData.date_acc    = [2018 10 03]; 


%% set data

% zero-variate data

data.ab = 2;      units.ab = 'd';    label.ab = 'age at birth';             bibkey.ab = 'Aara2013';   
  temp.ab = C2K(21);  units.temp.ab = 'K'; label.temp.ab = 'temperature';
data.tp = 100;    units.tp = 'd';    label.tp = 'time since birth at puberty'; bibkey.tp = 'Berr1978';
  temp.tp = C2K(24);  units.temp.tp = 'K'; label.temp.tp = 'temperature';
  comment.tp = 'estimated from the Berr1987 subtidal growth curve, assuming Lp = 29 mm';
data.am = 9 * 365; units.am = 'd';    label.am = 'life span';                bibkey.am = 'Lind1998';
  temp.am = C2K(20);  units.temp.am = 'K'; label.temp.am = 'temperature'; 
  comment.am = 'lifespan on exposed (2-3years) and sheltered (5-9 years) in south Africa';
%
data.Lb  = 0.008822; units.Lb  = 'cm';  label.Lb  = 'shell length at birth';   bibkey.Lb  = 'Aara2013';
  comment.Lb = '48 h after fertilisation the D-larvae has an initial size of 88.22 x 66.54 um';

data.Lp  = 2.9;  units.Lp  = 'cm';  label.Lp  = 'shell length at puberty'; bibkey.Lp  = 'Phil1995';
  comment.Lp = 'Intertidal South Africa 25-30mm';
  
data.Li  = 12;    units.Li  = 'cm';  label.Li  = 'ultimate shell length';   bibkey.Li  = 'Acos2009';    
data.Li_br  = 14.64;    units.Li_br  = 'cm';  label.Li_br  = 'ultimate shell length';   bibkey.Li_br  = 'HenriquesCasarini2009';
  comment.Li_br = 'Intertidal';
   
data.Wwb = 2.69e-8;   units.Wwb = 'g';   label.Wwb = 'wet weight at birth';    bibkey.Wwb = 'guess';
  comment.Wwb = 'Based on .03693*Lb^3 from HareKooy1993';
  
  
% uni-variate data
%
% t-L data Subtidal South Africa
data.tL =   [ ...    % time settlement (months), shell length (mm)
    1.116188276	7.521696341
    2.106273435	22.92744028
    3.615411519	31.42345889
    4.664253703	35.66341594
    5.586211945	46.47400913
    6.440043271	52.68945155
    7.289580063	51.68113089
    8.343692811	64.78661537
    9.385702782	57.53422206
    10.37051738	64.07443858
    11.28798588	67.33291581
    12.27123883	71.24630939
    13.2554678	76.8014673
    14.23891596	81.04321374
    15.28580608	81.99964212
    16.72779328	87.54227431
    17.7135839	95.72425517
    18.49772666	94.7177239
    19.48156523	99.61617608];
data.tL(:,1)  = data.tL(:,1) * 30;  % convert time to d
data.tL(:,2)  = data.tL(:,2) / 10;  % convert shell length to cm
units.tL   = {'d', 'cm'};  label.tL = {'time since settlement', 'shell length'};  
temp.tL    = C2K(24);  units.temp.tL = 'K'; label.temp.tL = 'temperature';
bibkey.tL = 'Berr1978';
comment.tL = 'Subtidal population Durban, South Africa';
%
% t-L Santos Bay, Brazil
data.tL_SBr =   [ ...    % time settlement (months), shell length (mm)
0.04	0.71
0.32	3.81
0.62	6.78
0.97	10.30
1.40	14.81
1.72	17.77
2.13	21.72
2.55	25.67
2.99	29.62
3.54	32.86
4.20	38.78
4.77	43.86
5.44	48.37
5.70    50.00
6.04	52.46
6.40	54.86
6.96	57.82
7.42	61.35
7.87	64.03
8.41	67.41
8.89	69.53
9.42	72.35
9.86	74.89
10.44	77.99
10.87	79.41
11.13	80.68
11.48	82.79
11.94	84.06
12.36	85.76
12.69	87.45
13.09	89.57
13.68	91.97
14.29	93.52
14.77	95.78
15.34	96.91
15.92	98.89
16.72	100.72
17.18	102.42
17.67	103.27
17.95	104.68
18.06	105.52
];
data.tL_SBr(:,1)  = data.tL_SBr(:,1) * 30;  % convert time to d
data.tL_SBr(:,2)  = data.tL_SBr(:,2) / 10;  % convert shell length to cm
units.tL_SBr   = {'d', 'cm'};  label.tL_SBr = {'time since settlement', 'shell length'};  
temp.tL_SBr    = C2K(24);  units.temp.tL_SBr = 'K'; label.temp.tL_SBr = 'temperature';
bibkey.tL_SBr = 'HenriquesCasarini2009';
comment.tL_SBr = 'Intertidal population Santos Bay, Brazil';
%
% t-L Armação do Itapocoroy, Brazil
data.tL_ItaBr =   [ ...    % time settlement (months), shell length (cm)
0.02	0.06
1.02	2.64
2.02	3.99
3.03	5.02
4.05	5.82
5.00	6.26
6.01	6.55
7.04	6.79
8.00	6.85
9.05	6.89
];
data.tL_ItaBr(:,1)  = data.tL_ItaBr(:,1) * 30;  % convert time to d
units.tL_ItaBr   = {'d', 'cm'};  label.tL_ItaBr = {'time since settlement', 'shell length'};  
temp.tL_ItaBr    = C2K(22.8);  units.temp.tL_ItaBr = 'K'; label.temp.tL_ItaBr = 'temperature';
bibkey.tL_ItaBr = 'MarenziBranco2005';
comment.tL_ItaBr = 'Armação do Itapocoroy farmed mussels, Santa Catarina, Brasil';
%
% t-W Armação do Itapocoroy, Brazil
data.tW_ItaBr =   [ ...    % Time (months), Weight (g)
0.01	0.07
1.00	1.28
2.01	4.45
2.96	7.98
3.97	12.57
5.02	17.15
6.05	20.96
7.08	24.70
8.49	27.46
];
data.tW_ItaBr(:,1)  = data.tW_ItaBr(:,1) * 30;  % convert time to d
units.tW_ItaBr   = {'d', 'g'};  label.tW_ItaBr = {'time since settlement', 'Wet Weight'};  
temp.tW_ItaBr    = C2K(22.8);  units.temp.tW_ItaBr = 'K'; label.temp.tW_ItaBr = 'temperature';
bibkey.tW_ItaBr = 'MarenziBranco2005';
comment.tW_ItaBr = 'Armação do Itapocoroy farmed mussels, Santa Catarina, Brasil';
%
% tL Ubatuba, Brazil
data.tL_Uba = [ ... % time settlement (months), length (mm)
    3.3012, 4.2864, 5.1984, 6.2244, 7.1736, 8.2032, 9.2244, 10.2468, 11.1624, 12.2208, 13.17, 14.1948, 15.144, 16.2024, 2.7792, 3.846, 4.8384, 5.8308, 6.8232, 7.8156, 8.8092, 9.7284, 10.794, 11.7864, 12.7428, 4.0272, 4.8336, 5.8608, 6.8136, 7.914, 8.8308, 9.822, 10.7388, 11.8392, 12.8652, 13.746, 14.7732, 15.7992, 16.68, 17.7804
    9.92, 9.7085, 9.8727, 13.7723, 13.5618, 22.1342, 21.735, 21.8964, 25.7988, 25.7724, 26.1226, 29.8354, 29.8117, 29.9723, 5.8847, 5.7094, 9.8728, 18.3759, 18.3884, 22.1744, 26.5266, 26.3494, 22.2119, 22.2244, 26.7647, 9.8356, 10.1273, 9.737, 14.0647, 18.2018, 22.1525, 21.9514, 22.1285, 25.6996, 25.8754, 25.8643, 30.0023, 29.612, 30.3557, 29.9645
    ]';
data.tL_Uba(:,1)  = data.tL_Uba(:,1) * 30;  % convert months to days
data.tL_Uba(:,2)  = data.tL_Uba(:,2) / 10;  % convert mm to cm
units.tL_Uba   = {'d', 'cm'};  label.tL_Uba = {'days', 'shell length'};  
temp.tL_Uba    = C2K(18.8);  units.temp.tL_Uba = 'K'; label.temp.tL_Uba = 'temperature';
comment.tL_Uba = 'Field data from Ubatuba, Brazil (Marques et al, 1991)';
bibkey.tL_Uba = 'Marq1991'; 
%
% Growth for 180 days in Florianopolis, Brazil
data.Lt_Flor = [... % initial length (mm), final length (mm)
    180.0, 180.0, 180.0, 180.0, 180.0, 180.0,
    66.27, 61.86, 64.64, 64.34, 59.43, 62.72]';
data.Lt_Flor(:,2) = data.Lt_Flor(:,2) / 10; % convert mm to cm
units.Lt_Flor   = {'d', 'mm'}; label.Lt_Flor = {'time', 'shell length'};  
temp.Lt_Flor    = C2K(21);  units.temp.Lt_Flor = 'K'; label.temp.Lt_Flor = 'temperature';
comment.Lt_Flor = 'Length at time zero and time 180 for Florianópolis, Brazil in 2008 (-27.483333, -48.516667)';
bibkey.Lt_Flor  = 'Muga2010'; 
%
% L-W data
data.LW = [ ...
    3.053	3.174	3.279	3.557	3.57	3.506	4.485	4.826	4.226	4.932	4.274	4.503	4.257	4.007	6.565	5.646	6.202	4.258	6.987	4.207	4.767	7.879	3.814	5.661	4.639	6.172	4.069	5.33	4.239	5.405	3.364	7.211	4.392	4.411	8.55	5.123	3.798	4.76	4.354	7.759	3.529	8.832	3.592	7.577	3.625	2.969	5.951	4.207	6.798	6.219	3.757	5.267	9.619	7.163	4.303	6.832	9.527	2.984	4.418	4.411	4.225	3.83	3.705	4.578	4.571	5.88	6.412	5.052	5.368	4.138	5.7	4.741	7.229	8.434	8.105	5.694	7.412	6.299	2.824	3.091	4.049	3.988	3.52	3.279	3.532	3.127	6.294	3.352	2.948	3.465	3.404	4.239	3.922	4.763	6.647	8.84	4.049	3.702	4.153	4.512	4.85	8.795	8.327	4.779	7.484	5.848	6.412	7.016	6.927	6.86	8.808	9.542	9.582	7.489	10.106	8.22	9.696	8.214	8.408	11.165	3.149	3.437	3.554	3.561	3.312	3.602	3.676	3.789	3.822	3.51	3.391	3.953	3.803	7.942	7.933	4.212	4.488	4.263	4.093	4.879	4.522	4.656	5.421	6.217	6.075	5.478	4.858	6.654	7.61	7.817	4.475	5.271	10.539	6.805	5.471	6.412	9.056	5.696	5.954	4.656	5.957	4.977	6.025	5.919	9.879	3.408	4.086	3.677	3.599	7.073	5.03	4.037	4.433	4.798	3.931	4.471	3.821	4.052	4.039	8.607	4.108	4.066	4.105	4.56	4.033	5.172	5.196	5.006	5.914	5.896	5.465	5.817	6.78	5.698	3.959	3.054	3.209	3.335	3.699	3.779	3.743	3.384	3.744	3.719	3.576	3.541	3.404	6.873	7.882	9.029	4.542	4.645	3.549	3.871	4.05	5.022	3.549	4.956	4.13	4.19	4.659	3.358	4.526	4.545	6.173	4.884	3.063	5.271	3.874	5.905	7.121	7.345	4.31	3.688	7.574	4.008	3.083	3.091	4.641	8.812	4.439	4.162	4.695	5.446	5.337	5.903	9.083	7.671	8.566	10.498	3.497	3.295	4.364	4.024	3.444	2.99	3.358	4.551	8.966	7.71	8.802	6.199	6.92	4.57	6.257	3.049	3.96	4.424	4.951	5.723	8.328	6.311	7.951	5.961	4.3	3.666	4.872	4.575	4.097	5.195	3.933	4.184	4.069	4.232	5.834	8.335	6.519	5.909	5.522	4.987	5.903	2.977	3.495	3.205	6.485	4.353	3.232	3.943	3.434	3.241	5.943	6.741	5.469	3.4	4.061	8.456	6.364	5.04	4.434	8.343	7.761	4.932	3.991	4.077	5.151	4.418	3.623	3.375	5.055	6.529	6.088	4.932	5.61	5.33	8.051	10.673	9.915	3.277	3.812	4.81	7.147	5.466	4.042	3.317	5.423	3.385	5.71	5.525	6.223	4.119	6.446	5.681	5.127	5.294	4.538	4.274	3.686	5.029	7.329	6.381	4.622	3.441	3.694	3.714	3.737	3.238	3.314	2.995	7.743	9.363	5.75	3.953	5.007	4.137	7.535	3.686	3.342	3.488	6.419	3.758	7.09	4.112	4.03	5.733	6.97	3.006	4.904	2.975	8.295	3.345	5.075	4.289	5.981	5.145	3.011	3.175	5.62	7.634	10.095	5.086	4.011	5.887	4.732	4.739	3.593	6.045	4.263	6.229	4.077	6.31	4.641	5.315	3.505	3.546	3.407	5.541	3.891	4.809	6.905	3.843	4.448	8.527	3.173	3.458	7.864	6.336	3.713	4.971	4.887	4.176	5.126	11.281	5.806	6.293	3.847	4.352	4.107	3.941	4.173	4.881	3.437	7.293	6.809	9.99	4.955	6.008	9.573	9.046	7.111	3.768	4.622	3.399	5.932	5.666	5.361	3.997	3.647	5.803	9.903
    0.1186	0.1157	0.1146	0.1863	0.1936	0.1612	0.2852	0.402	0.3541	0.3437	0.2675	0.3748	0.4155	0.3076	0.7526	0.6164	0.6893	0.2319	0.7737	0.3068	0.381	1.1784	0.2632	0.6005	0.4199	0.5919	0.2826	0.4077	0.2791	0.43	0.1072	0.8519	0.3775	0.3032	1.1946	0.4586	0.2221	0.3059	0.2736	1.0202	0.1366	1.8617	0.1809	1.3975	0.2066	0.137	0.6745	0.3669	0.7952	0.9602	0.2133	0.5482	3.0815	0.7696	0.2419	0.7619	1.8703	0.0982	0.3156	0.3776	0.2129	0.2052	0.224	0.2306	0.3384	0.4458	0.6304	0.3141	0.4104	0.2601	0.4405	0.3071	0.6369	1.0839	0.872	0.4321	0.9781	0.6438	0.0845	0.0669	0.2063	0.1488	0.2069	0.1544	0.1988	0.1724	0.4873	0.1238	0.1045	0.1389	0.1457	0.2396	0.2181	0.3391	0.3913	1.3221	0.3251	0.158	0.216	0.3	0.4535	1.2347	1.2968	0.3905	0.9002	0.6646	0.4798	0.7434	1.0491	0.4699	1.2475	3.0577	1.4057	0.8126	3.3411	1.1673	1.1688	0.8005	1.3346	2.8257	0.1616	0.2626	0.2338	0.2049	0.1942	0.2545	0.2051	0.2738	0.2391	0.2027	0.2443	0.3264	0.3174	1.0939	1.1917	0.3181	0.4474	0.3926	0.3458	0.5511	0.3815	0.4926	0.6092	0.8299	0.7181	0.4644	0.4974	0.9147	0.4904	1.4704	0.3006	0.5506	1.7657	1.0489	0.6474	0.9995	1.3859	0.5526	0.723	0.4943	0.4182	0.5203	0.7857	0.6401	1.5451	0.1913	0.2889	0.2437	0.1928	0.8789	0.5441	0.267	0.2848	0.5107	0.2294	0.3868	0.2743	0.3127	0.228	1.7874	0.2421	0.23	0.3313	0.2875	0.2111	0.4505	0.463	0.471	0.689	0.5644	0.089	0.4273	0.6648	0.4813	0.1976	0.1359	0.1492	0.1382	0.1643	0.2028	0.1731	0.145	0.1808	0.0397	0.1592	0.1638	0.1532	0.8299	0.5439	1.9456	0.2853	0.3567	0.1306	0.1789	0.1768	0.3343	0.1293	0.4327	0.2147	0.2371	0.268	0.1267	0.2638	0.2939	0.6693	0.3357	0.1214	0.3862	0.1765	0.6683	0.9608	0.8848	0.269	0.1669	0.9842	0.2054	0.0875	0.1213	0.279	1.573	0.247	0.1993	0.2802	0.4457	0.3355	0.5193	1.3856	1.1699	1.2659	2.2408	0.1307	0.0926	0.2387	0.2066	0.1332	0.0683	0.0993	0.2309	1.5619	0.7639	1.0733	0.4199	0.6924	0.2808	0.4355	0.1189	0.1594	0.1903	0.2928	0.443	1.1244	0.6389	1.2109	0.7553	0.3795	0.2343	0.4457	0.366	0.2674	0.648	0.2399	0.2813	0.2678	0.253	0.69	1.3016	0.8443	0.7738	0.7547	0.3551	0.5372	0.1122	0.2464	0.1183	0.8085	0.2951	0.127	0.2461	0.1503	0.1421	0.7148	0.919	0.5726	0.1527	0.2817	1.6967	0.9132	0.6502	0.3138	1.4336	1.4912	0.4081	0.237	0.2685	0.5691	0.2335	0.202	0.1298	0.4001	0.9304	0.6471	0.4716	0.4665	0.4537	1.4966	2.4208	2.0794	0.0976	0.2118	0.4263	0.9927	0.713	0.2907	0.1804	0.9428	0.2302	0.7972	0.988	0.6187	0.3487	0.9249	0.8393	0.5691	0.5842	0.448	0.3062	0.2574	0.4088	1.082	0.813	0.3179	0.2203	0.2557	0.1855	0.2836	0.1828	0.2022	0.1486	1.4236	2.3118	0.7682	0.2514	0.45	0.2595	1.2265	0.203	0.1747	0.1963	0.6793	0.2097	0.6258	0.2783	0.2512	0.5108	0.8585	0.1785	0.4316	0.1116	1.4175	0.171	0.5737	0.3097	0.9405	0.6074	0.1016	0.1419	0.4595	1.2659	1.6645	0.5915	0.372	0.8322	0.5033	0.4077	0.2334	0.7314	0.3801	0.837	0.3639	0.8246	0.3771	0.613	0.3106	0.1789	0.2873	0.8211	0.3474	0.5387	1.1814	0.2386	0.5372	2.9991	0.2044	0.1973	2.1445	0.9654	0.3184	0.5696	0.5435	0.3064	0.5417	3.6033	0.9068	0.7561	0.3448	0.3596	0.4056	0.2349	0.345	0.5771	0.1623	1.3569	1.0992	2.8545	0.6753	0.9449	2.0072	1.9238	1.597	0.1917	0.3456	0.2472	0.8766	0.5619	0.5824	0.2387	0.2149	0.73	2.8483
    ]';
units.LW   = {'cm', 'g'};  label.LW = {'shell length', 'soma dry weight'};  
comment.LW = 'data collected from individuals at different shore levels. South coast of South Africa';
bibkey.LW = 'Mona2016';


%% set weights for all real data
  weights = setweights(data, []);
   weights.tL = 0 * weights.tL;
   weights.LW = 0 * weights.LW;
 
%   weights.tL_SBr = 5 * weights.tL_SBr;
%   weights.tL_ItaBr = 5 * weights.tL_ItaBr;
  weights.tW_ItaBr = 0 * weights.tW_ItaBr;
%   weights.tL_Uba = 3 * weights.tL_Uba;
%   weights.Lt_Flor = 5 * weights.Lt_Flor;
 
%% set pseudodata and respective weights
[data, units, label, weights] = addpseudodata(data, units, label, weights);

%% pack auxData and txtData for output
auxData.temp = temp;
txtData.units = units;
txtData.label = label;
txtData.bibkey = bibkey;
txtData.comment = comment;


%% Facts
F1 = 'An eariler version of this entry was by TaglMcQu2016';
metaData.bibkey.F1 = 'TaglMcQu2016';  
metaData.facts = struct('F1',F1);

%% Discussion
D1 = 'This version assumes that metamorphosis coincides with settlement';
D2 = 'Weight zero is given to Lb because the shape is probably different from that of post-settlement individuals.';
D3 = 'Brazilian population is assumed to be different from South African by P_Am';
metaData.discussion = struct('D1',D1,'D2',D2,'D3',D3);

%% Links
metaData.links.id_CoL = '550e68bd80ea1046404db3659e71ffee'; % Cat of Life
metaData.links.id_EoL = '468743'; % Ency of Life
metaData.links.id_Wiki = 'Perna_perna'; % Wikipedia
metaData.links.id_ADW = 'Perna_perna'; % ADW
metaData.links.id_WoRMS = '140483'; % WoRMS
metaData.links.id_molluscabase = '541374'; % MolluscaBase

%% References
bibkey = 'Wiki'; type = 'Misc'; bib = ...
'howpublished = {\url{http://en.wikipedia.org/wiki/Perna_perna}}';
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Kooy2010'; type = 'Book'; bib = [ ...  % used in setting of chemical parameters and pseudodata
'author = {Kooijman, S.A.L.M.}, ' ...
'year = {2010}, ' ...
'title  = {Dynamic Energy Budget theory for metabolic organisation}, ' ...
'publisher = {Cambridge Univ. Press, Cambridge}, ' ...
'pages = {Table 4.2 (page 150), 8.1 (page 300)}, ' ...
'howpublished = {\url{../../../bib/Kooy2010.html}}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Acos2009'; type = 'Article'; bib = [ ...  
'author = {Vanessa Acosta and Mar\''{i}a E. Glem and Yolimar Natera and Trinidad Urbano and John H. Himmelman and Manuel Rey-M\''{e}ndez and C\''{e}sar Lodeiros}, ' ...
'year = {2009}, ' ...
'title  = {Differential growth of the mussels \emph{Perna perna} and \emph{Perna viridis} (Bivalvia: Mytilidae) in suspended culture in the {G}olfo de {C}ariaco, {V}enezuela}, ' ...
'journal = {Journal of the World Aquaculture Society}, ' ...
'volume = {40}, ' ...
'pages = {226--235}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'HenriquesCasarini2009'; type = 'Article'; bib = [ ...  
'author = {Marcelo Barbosa Henriques and Luiz Miguel Casarini}, ' ...
'year = {2009}, ' ...
'title  = {Growth evaluation of brown mussel Perna perna and invasive bivalve Isognomon bicolor of a natural bed in Palmas Island, Santos Bay, Sao Paulo state, Brazil}, ' ...
'journal = {Boletim do Instituto de Pesca}, ' ...
'volume = {35}, ' ...
'pages = {577-586}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'MarenziBranco2005'; type = 'Article'; bib = [ ...  
'author = {Adriano W. C. Marenzi and Joaquim O. Branco}, ' ...
'year = {2005}, ' ...
'title  = {O mexilhão Perna perna (Linnaeus) (Bivalvia, Mytilidae) em cultivo na Armação do Itapocoroy, Santa Catarina, Brasil}, ' ...
'journal = {Revista Brasileira de Zoologia}, ' ...
'volume = {22}, ' ...
'pages = {394-399}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Aara2013'; type = 'Article'; bib = [ ...  
'author = {Lahoussine Aarab and Alejandro Prez-Camacho and Mara del Pino Viera-Toledo and Gercende Courtois de Viose and Hiplito Fernndez-Palacios and Lucia Molina}, ' ...
'year = {2013}, ' ...
'title  = {Embryonic development and influence of egg density on early veliger larvae and effects of dietary microalgae on growth of brown mussel \emph{Perna perna} (L. 1758) larvae under laboratory conditions}, ' ...
'journal = {Aquaculture International}, ' ...
'volume = {21}, ' ...
'pages = {1065-1076}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Berr1978'; type = 'techreport'; bib = [ ...  
'author = {Patrick F Berry}, ' ...
'year = {1978}, ' ...
'title  = {Reproduction, growth and production in the mussel, \emph{Perna perna} ({L}innaeus), on the east coast of {S}outh {A}frica}, ' ...
'institution = {Oceanographic Research Institute}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Lind1998'; type = 'Book'; bib = [ ...  % used in setting of chemical parameters and pseudodata
'author = {Tracey Lynn Lindsay}, ' ...
'year = {1998}, ' ...
'title  = {Population dynamics and growth rate of the brown mussel (\emph{Perna perna}) on wave exposed and wave sheltered shores of {S}outh {A}frica}, ' ...
'publisher = {Rhodes University}, ' ...
'pages = {195}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'TaglMcQu2016'; type = 'Article'; bib = [ ...
'author = {Morgana Tagliarolo, Christopher D. McQuaid}, ' ... 
'year = {2015}, ' ...
'title = {Sub-lethal and sub-specific temperature effects are better predictors of mussel distribution than thermal tolerance.}, ' ...
'journal = {Marine Ecology Progress Series}, ' ...
'volume = {535}, ' ...
'pages = {145--159}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Mona2016'; type = 'unpublished'; bib = [ ...
'author = {Cristian Monaco}, ' ... 
'year = {2016}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Phil1995'; type = 'Book'; bib = [ ...  
'author = {Tracey Elizabeth Phillips}, ' ...
'year = {1995}, ' ...
'title  = {Dispersal, settlement and recruitment: their influence on the population dynamics of intertidal mussels}, ' ...
'publisher = {Rhodes University}, ' ...
'pages = {261}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'HareKooy1993'; type = 'Article'; bib = [ ... 
'author = {Haren, R. van and Kooijman, S. A. L. M.}, ' ... 
'year = {1993}, ' ...
'title = {Application of a {D}ynamic {E}nergy {B}udget model to \emph{Mytilus edulis} ({L}.)}, ' ...
'journal = {Neth. J. Sea Res.}, ' ...
'volume = {31}, ' ...
'doi  = {10.1016/0077-7579(93)90002-a}, '...
'pages = {119–-133}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Marq1991'; type = 'Article'; bib = [ ... 
'author = {Marques, H.L.A. and Pereira, R.T.L. and Correa, B.C.}, ' ... 
'year = {1991}, ' ...
'title = {CRESCIMENTO DE MEXILH{\~O}ES Perna perna (LINNAEUS, 1758) EM POPULA{\c{C}}{\~O}ES NATURAIS NO LITORAL DE UBATUBA (SP), BRASIL.}, ' ...
'journal = {Boletim do Instituto de Pesca}, ' ...
'volume = {18}, ' ...
'pages = {61-72}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'Muga2010'; type = 'Dissertation'; bib = [ ... 
'author = {Mugabe, E. D. and Ferreira, J. F.}, ' ... 
'year = {1991}, ' ...
'title = {Efeito de sementes obtidas por diferentes métodos no crescimento do mexilhão Perna perna (Bivalvia:Mytilidae) em cultivo no sul do Brasil}, ' ...
'pages = {61-72}'];
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
% bibkey = 'Resgalla2007'; type = 'Article'; bib = [ ... 
% 'author = {Charrid Resgalla and Elisângela De Souza Brasil and Luis Carlos Salomão}, ' ... 
% 'year = {2007}, ' ...
% 'title = {The effect of temperature and salinity on the physiological rates of the mussel Perna perna (Linnaeus 1758)}, ' ...
% 'journal = {Brazilian Archives of Biology and Technology}, ' ...
% 'volume = {50}, ' ...
% 'pages = {543-556}'];
% metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
%
bibkey = 'guess'; type = 'Misc'; bib = ... 
'howpublished = {\url{guess}}'; 
metaData.biblist.(bibkey) = ['''@', type, '{', bibkey, ', ' bib, '}'';'];
