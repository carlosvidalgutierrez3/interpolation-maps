function out = extract_data()

%first delete columns and lines with text (only numbers!!)
%Delete void values represented with a character (eg '-')
A = csvread('BS_eur.csv');
%choose columns depending on pollutant:
no2zeros = A(:,1:3);
j=1;

%extact values that equal 0:
for i=1:length(no2zeros)
   if no2zeros(i,3)~=0
      no2(j,:) = no2zeros(i,:);
      j = j+1;
   end
end

% Spain: lon € [27.7636,43.5792], lat € [-17.9216,4.259]
 
 out = no2;