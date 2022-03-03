load DEBmatrix_mean
load std_li_corr
load std_rb_corr

Li = L_i_corr;
rB = r_B_corr;
std_li = std_Li_corr;
std_rb = std_rB_corr;

P = Li.*rB ./ ( 1 + (std_li .* std_rb)./(Li.*rB) );

save('P_coefficient.mat', 'P')
