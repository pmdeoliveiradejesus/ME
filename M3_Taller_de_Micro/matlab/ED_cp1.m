%Clearing the market (1 producer - 1 demand)
% cp: perfect competition
mO1=15;pmax=100;mD=20;p1min=5
B=[-p1min; -pmax; 0];
Acp=[mO1 0 -1; 
     0  -mD -1; 
     -1  1 0];
Solcp=inv(Acp)*B
PSP = 0.5*Solcp(1)*(pmax-Solcp(3))
CSP = 0.5*Solcp(1)*(Solcp(3)-p1min) 
SW=PSP+CSP
%Elasticity at equilibrium point
Past=Solcp(3);
Qast=Solcp(1);
DP=(pmax-Solcp(3));
DQ=0-Solcp(1);
e=(DQ/Qast)/(DP/Past)