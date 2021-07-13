% Position generator

% Reads matrix with the following format:
% lat,long_min,long_max
% Generates positions within the read values at a certain resolution
function out = generate_positions(A)

%A = csvread('peninsula_1d.txt');
k = 1;

for i=1:length(A)
    for j=A(i,2):A(i,3)
        B(k,:) = [A(i,1),j,0];  %zero values for test
        k = k+1;
    end
end
% --------------------------------------------- Adjust to resolution
B = B/10;     %0.1 resolution -> x10
%-------------------------------------------------------------------
csvwrite('a2.csv',B);

out = B;
