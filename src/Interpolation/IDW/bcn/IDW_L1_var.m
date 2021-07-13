function out = IDW_L1()
% IDW for the L1 sources at 0.001 resolution (bcn)
% (!)THE ANOTATIONS ARE NOT A GUIDE, THEY ARE NOTES FOR THE PROGRAMMER
ALFA = 2;               % alfa of the IDW formula (d^alfa, BS)
% bs_s_r = 0.0001;     % BS to SAT ratio on Weighting
% (!) adjust SQA to alfa for faster execution. (i.e: if ALFA is big, SQA
% can be smaller and we obtain the same output)
SQA = 0.5;      % area of the square for nearby BS's
SQAs = 0.1;     % area of the square for nearby SC's
EAs = 0.02;     % var A of Exp() SC
EBs = 10;    % var B of Exp() SC
% EA = 0.025;       % BS
% EB = 1000;

% select BS/SC inside grid area:
grid = csvread('bcn_L1_grid.csv');   % grid w/ 0's
BS = csvread("BS_bcn_synth.csv");
BSr = round(BS,3);
SC = csvread("scoots_11_12.csv");

tic
%copy each data value to the correspondent position in the grid
% for i=1:length(BSr) 
%    row = find(grid(:,1)==BSr(i,1) & grid(:,2)==BSr(i,2));
%    grid(row,3) = BSr(i,3);
% end

% IDW 
for i=1:length(grid)           % for each cell of the grid:
    if grid(i,3)==0            % only with cells equal 0
        % Find BS's/SC's in a SQA degree square area centered on the point
        n = find(BS(:,2)<(grid(i,2)+SQA/2) & BS(:,2)>(grid(i,2)-SQA/2) & BS(:,1)>(grid(i,1)-SQA/2) & BS(:,1)<(grid(i,1)+SQA/2));
        ns = find(SC(:,2)<(grid(i,2)+SQAs/2) & SC(:,2)>(grid(i,2)-SQAs/2) & SC(:,1)>(grid(i,1)-SQAs/2) & SC(:,1)<(grid(i,1)+SQAs/2));
        
        d2 = zeros(length(n)+length(ns),1);         % array of squared distances
        divider = 0;
        
        for j=1:length(n)     % for list of BS's nearby
            d2(j) =  ((grid(i,1)-BS(n(j),1))^2 + (grid(i,2)-BS(n(j),2))^2)^(ALFA/2);    % Square distance to each BS
            % divider = divider + bs_s_r*1/d2(j);
            divider = divider + 0.0000001*exp(-10*(100*d2(j))^2);
        end
        
        for j=1:length(ns)     % for list of SC's nearby
            d2(j+length(n)) =  ((grid(i,1)-SC(ns(j),1))^2 + (grid(i,2)-SC(ns(j),2))^2)^(1/2);    % distance to each SC
            divider = divider + EAs*exp(-EBs*(100*d2(j+length(n)))^2);
        end
        
        for j=1:length(n)
            % w = bs_s_r*1/(d2(j)*divider);               % weight of each BS
            w = 0.0000001*exp(-10*(100*d2(j))^2)/divider;
            grid(i,3) = grid(i,3) + w*BS(n(j),3);       % pollution on the point
        end
        for j=1:length(ns)
            w = EAs*exp(-EBs*(100*d2(j+length(n)))^2)/divider;       % weight of each SC
            grid(i,3) = grid(i,3) + w*SC(ns(j),3);              % pollution on the point
        end
        
    end
end

toc

csvwrite('bcn_L1_int_var.csv',grid);
out = grid;