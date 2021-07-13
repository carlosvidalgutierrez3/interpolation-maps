Coparative BCN interpolations;
(SQA = 0.5; SQAs = 0.1;) 

15.1 
BS:
	- Gaussian: 0.0000001*exp(-10*(100*x)^2)
	- x = distance^2
SC:
	- EAs*exp(-EBs*(100*x)^2)
	- x = distance, EAs = 0.02, EBs = 10;

15.2 (changes:)
BS: 
	- 0.0000001/x
	- x = distance^2

15.3 (changes:)
SC:
	- EAs = 0.01, EBs = 5;


15.4 (changes:)
SC:
	- EAs = 0.005, EBs = 1;

15.5 (changes:)
SC:
	- EAs = 0.005, EBs = 2;

15.6 (changes:)
SC:
	- EAs = 0.001, EBs = 20;
