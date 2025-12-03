%Clearing the market (2 producers - 1 demand)
% cp: perfect competition
mO1=15;mO2=0;pmax=100;mD=20;p1min=5;p2min=-5;
B=[-p1min; -p2min; -pmax; 0];
Acp=[mO1 0 0 -1; %bombeo
     0 mO2 0 -1; 
     0 0 -mD -1; 
     -1 -1 1 0];
Solcp=inv(Acp)*B
Past=Solcp(4);
Qast1=Solcp(1);
Qast2=Solcp(2);
Qast=Solcp(3);
PSP1=Past*Qast1-p1min*Qast1-0.5*mO1*Qast1*Qast1
PSP2=Past*Qast2-p2min*Qast2-0.5*mO2*Qast2*Qast2
PSP=PSP1+PSP2
CSP = pmax*Qast-0.5*mD*Qast*Qast-Past*Qast 
SW=PSP+CSP
%Elasticity at equilibrium point
DP=(pmax-Past);
DQ=0-Qast;
e=(DQ/Qast)/(DP/Past)

 