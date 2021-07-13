Tests for L1 

11.1 scooters (Use 10.2 for BS, and 7.2 for SAT)

11.2 BS

11.4  
- only SC
SQAs = 0.01;     % area of the square for nearby SC's
EAs = 2;     % var A of Exp() SC
EBs = 10;    % var B of Exp() SC
EAs*exp(-EBs*(100*d2(j+length(n)))^2)

11.5
ALFA = 2;               % alfa of the IDW formula (d^alfa, BS)
bs_s_r = 0.0001;     % BS to SAT ratio on Weighting
SQA = 0.1;      % area of the square for nearby BS's
SQAs = 0.1;     % area of the square for nearby SC's
EAs = 2;     % var A of Exp() SC
EBs = 10;    % var B of Exp() SC
EA = 0.2;       % BS
EB = 10;
divider = divider + bs_s_r*1/d2(j);
EAs*exp(-EBs*(100*d2(j+length(n)))^2)

11.6
- same as 11.4, but w/ out zeros

11.7
SQA = 0.01;      % area of the square for nearby BS's
SQAs = 0.01;     % area of the square for nearby SC's
EAs = 0.02;     % var A of Exp() SC
EBs = 10;    % var B of Exp() SC
EA = 0.025;       % BS
EB = 1000;

11.8
- same as 11.7 but w/ synth. BS