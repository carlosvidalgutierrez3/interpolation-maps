function out = IDW_2s_g()
%The variation in this one: SAT with gaussian, not idw
%(!)THE ANOTATIONS ARE NOT A GUIDE, THEY ARE NOTES FOR THE PROGRAMMER
ALFA = 2;       % alfa of the IDW formula (d^alfa, BS)
bs_s_r = 0.0001;     % BS to SAT ratio on Weighting
% (!) adjust SQA to alfa for faster execution. (i.e: if ALFA is big, SQA
% can be smaller and we obtain the same output)
SQA = 1;        % area of the square for nearby BS's
SQAs = 1;     % area of the square for nearby SAT's


% select BS inside grid area:
cat = csvread('cat_L2_grid.csv');
% BS = extract_data();
BS = csvread("BS_25_no2.csv");
BSr = round(BS,2);
SAT = csvread("SAT_25_no2.csv");

tic
% lat
BSr(BSr(:,1)>44,:) = []; %lat max 44
BSr(BSr(:,1)<39,:) = []; %lat min 39
SAT(SAT(:,1)>44,:) = []; %lat max 44
SAT(SAT(:,1)<39,:) = []; %lat min 39

% long
BSr(BSr(:,2)<-1,:) = []; %long min -1
BSr(BSr(:,2)>5,:) = []; %long max 5
SAT(SAT(:,2)<-1,:) = []; %long min -1
SAT(SAT(:,2)>5,:) = []; %long max 5

% copy each data value to the corresponent position in the grid
for i=1:length(BSr) 
   row = find(cat(:,1)==BSr(i,1) & cat(:,2)==BSr(i,2));
   cat(row,3) = BSr(i,3);
end


% IDW 
for i=1:length(cat)           % for each cell of the grid:
    if cat(i,3)==0            % only with cells equal 0
        % Find BS's in a SQA degree square area centered on the point
        n = find(BS(:,2)<(cat(i,2)+SQA/2) & BS(:,2)>(cat(i,2)-SQA/2) & BS(:,1)>(cat(i,1)-SQA/2) & BS(:,1)<(cat(i,1)+SQA/2));
        ns = find(SAT(:,2)<(cat(i,2)+SQAs/2) & SAT(:,2)>(cat(i,2)-SQAs/2) & SAT(:,1)>(cat(i,1)-SQAs/2) & SAT(:,1)<(cat(i,1)+SQAs/2));
        
        d2 = zeros(length(n)+length(ns),1);         % array of squared distances
        divider = 0;
        
        for j=1:length(n)     % for list of BS's nearby
            d2(j) =  ((cat(i,1)-BS(n(j),1))^2 + (cat(i,2)-BS(n(j),2))^2)^(ALFA/2);    % Square distance to each BS
            divider = divider + bs_s_r*1/d2(j);
        end
        
        for j=1:length(ns)     % for list of SAT's nearby
            d2(j+length(n)) =  ((cat(i,1)-SAT(ns(j),1))^2 + (cat(i,2)-SAT(ns(j),2))^2)^(1/2);    % distance to each BS
            divider = divider + 0.2*exp(-(10*d2(j+length(n)))^2);
        end
        
        for j=1:length(n)
            w = bs_s_r*1/(d2(j)*divider);            % weight of each BS
            cat(i,3) = cat(i,3) + w*BS(n(j),3);      % pollution on the point
        end
        for j=1:length(ns)
            w = 0.2*exp(-(10*d2(j+length(n)))^2)/divider;         % weight of each SAT
            cat(i,3) = cat(i,3) + w*SAT(ns(j),3);    % pollution on the point
        end
        
    end
end
toc

csvwrite('cat_L2_int.csv',cat);
out = cat;