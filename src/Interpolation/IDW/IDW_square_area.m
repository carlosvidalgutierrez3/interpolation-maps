function out = IDW_square_area()
%(!)THE ANOTATIONS ARE NOT A GUIDE, THEY ARE NOTES FOR THE PROGRAMMER
% "cat" is the grid
% "BSr" is the BS list rounded
tic
% select BS inside squared area:
% lat
cat = csvread('cat_L2.csv');
BS = extract_data();
BSr = round(BS,2);

BSr(BSr(:,1)>44,:) = []; %lat max 44
BSr(BSr(:,1)<39,:) = []; %lat min 39

% long
BSr(BSr(:,2)<-1,:) = []; %long min -1
BSr(BSr(:,2)>5,:) = []; %long max 5


% copy each BS value to the corresponent position in the grid
for i=1:length(BSr)
   row = find(cat(:,1)==BSr(i,1) & cat(:,2)==BSr(i,2));
   cat(row,3) = BSr(i,3);
end

% IDW with squares

for i=1:length(cat)           % for each cell of the grid:
   if cat(i,3)==0             % only with cells equal 0
      divider = 0;
      % Find BS's in a 1 degree square area centered on the point
      n = find(BS(:,2)<(cat(i,2)+0.5) & BS(:,2)>(cat(i,2)-0.5) & BS(:,1)>(cat(i,1)-0.5) & BS(:,1)<(cat(i,1)+0.5));  
      
      % Find BS's in a 1 degree radius
      d2 = zeros(length(n),1);
        
      if ~isempty(n)            % only if there is at least 1 BS inside
          k = 1;
          for j=1:length(n)
              d2(j) =  (cat(i,1)-BS(n(j),1))^2 + (cat(i,2)-BS(n(j),2))^2;    % Square distance to each BS
              if d2(j)<0.5
                  d2_2(k) = d2(j);
                  divider = divider + 1/d2_2(k);
                  k = k+1;
              end
          end
          
         w = zeros(length(n),1);
         for j=1:length(n)
            w(j) = 1/(d2(j)*divider);                   % weight of each BS  
            cat(i,3) = cat(i,3) + w(j)*BS(n(j),3);      % pollution on the point
         end
         
      end
   end
end
toc

csvwrite('cat_L2_int.csv',cat);
out = cat;