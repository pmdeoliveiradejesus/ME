%Clearing the market (1 producer - 1 demand)
% cp: perfect competition
mO1=15;pmax=100;mD=20;p1min=5
B=[-p1min; -pmax; 0];
Acp=[mO1 0 -1; 
     0  -mD -1; 
     -1  1 0];
Solcp=inv(Acp)*B
Past=Solcp(3);
Qast=Solcp(1);
CSP = 0.5*Qast*(pmax-Past) % Area bajo la curva superior
CSPx=  pmax*Qast-0.5*mD*Qast*Qast-Past*Qast 
PSPx= Past*Qast-p1min*Qast-0.5*mO1*Qast*Qast
PSP = 0.5*Qast*(Past-p1min) % Area bajo la curva inferior 
SW=PSP+CSP
%Elasticity at equilibrium point
DP=(pmax-Past);
DQ=0-Qast;
e=(DQ/Qast)/(DP/Past)
OPEX=p1min*Qast+0.5*mO1*Qast*Qast
CAPEX= 100;
CostosTotales=OPEX+CAPEX
Ingreso= Past*Qast
