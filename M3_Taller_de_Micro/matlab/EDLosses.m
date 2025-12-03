% Economic Dispatch Program,De Oliveira De Jesus UNIANDES. August 2017
% With Transmission
% No Output limits
% 
% cp: perfect competition
%  
clc
clear all
close all
global mo pmin pgmin pgmax md pmax n Bloss Loss flagx Loss2


%% Generation cost structure
%   alpha ($/h) beta ($/MWh) gamma ($/MW2h) Pmin (MW) Pmax (MW)
PG=[%0  10 5 0 5 .6;
%      0 15 0 2 5 0;
%      0 5 30 2 10 0;
%      0 0 50 2 10 0;
%     0 15 5 2 10 0;
%     0 7.5 25 2 100 0;
   0 5 7.5 0 5 0.05;
];
%% Demand cost structure
md=20;
pmax=100;%$/MWh
Pdmax=4;%MW
% 
Bloss=PG(:,6);
n=size(PG,1);for k=1:n
    mo(k)=PG(k,3)*2;
    pmin(k)=PG(k,2);
    Pgmin(k)=PG(k,4);
    Pgmax(k)=PG(k,5);    
end


% min -SW = SC = sum pmin*Pg+ 0.5*mo*Pg^2-(pmax*Pd-0.5*md*Pd^2) 
% st
% rho=pmax-md*Pd
% sum Pg = Pd

% Solution approach 2 (Interior Point)
x0=zeros(1,n+1); 
LB=zeros(1,n+1);
UB=ones(1,n+1)*100000;
A=[];
Bx=[];
Aeq=[];
Beq=[];
tol1=1e-8;
tol2=1e-8;
tol3=1e-8;
options=optimset('Display','iter','LargeScale','on','ActiveConstrTol',1,'TolFun',tol1,'TolCon',tol2,'TolX',tol3,'MaxIter',250000,'MaxFunEvals',2500000000)
[X,FVAL,EXITFLAG,OUTPUT,LAMBDA] = fmincon('obj',x0,A,Bx,Aeq,Beq,LB,UB,'restrloss')
EXITFLAG
LAMBDA
% Solution approach 2 (Langrange)

X
-LAMBDA.eqnonlin

