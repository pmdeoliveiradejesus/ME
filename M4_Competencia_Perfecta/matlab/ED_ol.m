%Economic Dispatch
% cp: perfect competition
% 0l: oligopoly
mO1=15;mO2=10;pmax=100;mD=20;p1min=5;p2min=10;
B=[-p1min; -p2min; -pmax; 0];
Acp=[mO1 0 0 -1; 
     0 mO2 0 -1; 
     0 0 -mD -1; 
     -1 -1 1 0];
Aol=[mO1+mD 0 0 -1; 
     0 mO2+mD 0 -1; 
     0 0 -mD -1;
     -1 -1 1 0];
Solcp=inv(Acp)*B
Solol=inv(Aol)*B
