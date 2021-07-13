9 series: Trying gaussian instead of IDW

9.1
only SAT
exp(-(d2(j+length(n)))^2)

9.2
only SAT
0.2*exp(-(10*d2(j+length(n)))^2)

9.3
ALFA = 2;       % alfa of the IDW formula (d^alfa, BS)
bs_s_r = 0.00001;     % BS to SAT ratio on Weighting
0.2*exp(-(10*d2(j+length(n)))^2)

9.4
ALFA = 2;       % alfa of the IDW formula (d^alfa, BS)
bs_s_r = 0.00005;     % BS to SAT ratio on Weighting
0.2*exp(-(10*d2(j+length(n)))^2)

9.5
ALFA = 2;       % alfa of the IDW formula (d^alfa, BS)
bs_s_r = 0.0001;     % BS to SAT ratio on Weighting
0.2*exp(-(10*d2(j+length(n)))^2)