function [C,Ceq]= myfun(X);
global mo pmin pgmin pgmax md pmax n
% min -SW = SC = sum_1^ (pmin*Pg+ 0.5*mo*Pg^2)-(pmax*Pd-0.5*md*Pd^2) 
% st
% rho=pmax-md*Pd
% sum Pg = Pd
Ceq=sum(X)-2*X(n+1);
C=[];