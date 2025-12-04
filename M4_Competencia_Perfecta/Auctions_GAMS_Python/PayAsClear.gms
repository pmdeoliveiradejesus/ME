Sets
    g       Generators      / PlantA, PlantB /
    s       Scenarios       / Scen1, Scen2 /;

Parameters
    Bid(g)       Bid Price ($ per MWh)
    Cap(g)       Capacity (MW)
    Demand       Total Demand (MW) / 100 /;

* Define Prices
Bid('PlantA') = 20;
Bid('PlantB') = 80;

* Define Variables
Positive Variable x(g);
Variable z;
Equation
* Define Equations
    CostObj      Objective
    BalEq        Supply Demand Balance
    CapLim(g)    Capacity Limit;

CostObj..    z =e= sum(g, Bid(g) * x(g));
BalEq..      sum(g, x(g)) =e= Demand;
CapLim(g)..  x(g) =l= Cap(g);

Model Auction /all/;

* Reporting Parameter
Parameter Report(s, *);

* --- SCENARIO 1: Plant A restricted to 50MW ---
Cap('PlantA') = 100;
Cap('PlantB') = 100;

Solve Auction using lp minimizing z

*Report('Scen1', 'Gen_A') = x.l('PlantA');
*Report('Scen1', 'Gen_B') = x.l('PlantB');
*Report('Scen1', 'ClearingPrice') = BalEq.m 

* --- SCENARIO 2: Plant A full 100MW ---
* Note: To strictly ensure the price drops to 20 in LP, 
* we assume A has margin or is the marginal unit.
*Cap('PlantA') = 100;
*Cap('PlantB') = 100;

*Solve Auction using lp minimizing z;

*Report('Scen2', 'Gen_A') = x.l('PlantA');
*Report('Scen2', 'Gen_B') = x.l('PlantB');
*Report('Scen2', 'ClearingPrice') = BalEq.m;

*Display Report;