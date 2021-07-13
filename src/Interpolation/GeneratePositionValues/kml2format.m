% With this script we will obtain the shore coordinates in the desired
% format for the next script.

% Copy coordinate values from .kml file to a .txt file
function out = kml2format()

%A = importdata("red_cat.txt");     % All data in a string:
%B = strsplit(A{1});                % Separate by positions (lat,long,height) each cell)

id = fopen('iberia_red.txt');
txt = textscan(id,'%s');        % One position (lat,long,h) per row in 1 column
B = string(txt{1});             % Convert to string

% arrange by rows
for i=1:length(B)
   C(i,:) = strsplit(B{i},',');
end

C(:,3) = [];        % delete 3rd row (height)
D = str2double(C);  % convert to double
% --------------------------------------------- Adjust to resolution
D = 100*D;     %0.1 resolution -> x10
%-------------------------------------------------------------------
F = round(D);       % round values

%F(length(F),:) = [];               % delete the last "\n" (NaN)-----------------ONLY if copied!!!
[G,I] = sort(F(:,2),'descend');     % Organize descendent lat and save indexes in I

% Organize correspondant long by I
for i=1:length(F)
   G(i,2) = F(I(i),1); 
end

% arrange to desired format:
i = 1;
H = 0;
M = [];
while i<length(G)
    j = i;
    i = i+1;
    %To find number (i-j) of lat's equal
    %---------------------
    if G(i,1)==G(j,1)
        equal = 1;
    end
    
    while equal == 1
        i = i+1;
        if i <= length(G)
            if G(i,1)==G(j,1)
                equal = 1;
            else
                equal = 0;
            end
        else
            equal = 0;
        end
    end
    %----------------------
    H(:) = [];
    H(1:i-j) = G(j:(i-1),2);
    H = sort(H);
    k = 1;
    
    while k < (i-j)
       M(size(M,1)+1,:) = [G(j,1),H(k),H(k+1)];
       k = k+2;
    end
end

out = M;

