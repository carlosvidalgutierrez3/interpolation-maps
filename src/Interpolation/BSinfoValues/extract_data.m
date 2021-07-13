function out = extract_data()
tic
%first delete columns and lines with text (only numbers!!)
%Delete void values represented with a character (eg '-')
A = csvread('BSinfo_2.csv');
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

% save output in csv file
csvwrite('a1.csv',no2); 
toc
out = no2;