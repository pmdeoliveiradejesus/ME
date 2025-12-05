$title Subasta Simple - Maximizacion del Bienestar Social (LP)

* --------------------------------------------------------------------------
* 1. CONJUNTOS (SETS)
* --------------------------------------------------------------------------

SET
    I 'Generadores'             / G1*G3 /
    J 'Consumidores'            / D1*D2 /
    B 'Bloques de Generacion'   / B1*B3 /
    K 'Bloques de Demanda'      / K1*K4 /;

* --------------------------------------------------------------------------
* 2. DATOS (PARAMETERS)
* --------------------------------------------------------------------------

* Potencia máxima ofertada por Generador (i) y Bloque (b) [MW]
PARAMETER P_G_MAX(I, B)
/
    G1.B1   5,    G1.B2   12,   G1.B3   13
    G2.B1   8,    G2.B2   8,    G2.B3   9
    G3.B1   10,   G3.B2   10,   G3.B3   5
/;

* Precio de oferta de los Generadores (Costo) [$/MWh]
PARAMETER LAMBDA_G(I, B)
/
    G1.B1   1.0,  G1.B2   3.0,  G1.B3   3.5
    G2.B1   4.5,  G2.B2   5.0,  G2.B3   6.0
    G3.B1   8.0,  G3.B2   9.0,  G3.B3   10.0
/;

* Potencia máxima demandada por Consumidor (j) y Bloque (k) [MW]
PARAMETER P_D_MAX(J, K)
/
    D1.K1   8,    D1.K2   5,    D1.K3   5,    D1.K4   3
    D2.K1   7,    D2.K2   4,    D2.K3   4,    D2.K4   3
/;

* Precio de oferta de los Consumidores (Valoración) [$/MWh]
PARAMETER LAMBDA_D(J, K)
/
    D1.K1   20,   D1.K2   15,   D1.K3   7,    D1.K4   4
    D2.K1   18,   D2.K2   16,   D2.K3   11,   D2.K4   3
/;

* --------------------------------------------------------------------------
* 3. VARIABLES
* --------------------------------------------------------------------------

VARIABLES
    WS              'Bienestar Social (Funcion Objetivo) [$/h]'
    P_G(I, B)       'Potencia despachada de Generacion por bloque [MW]'
    P_D(J, K)       'Potencia despachada de Demanda por bloque [MW]';

* Declarar las variables de despacho como positivas (non-negative)
Positive Variables P_G, P_D;

* --------------------------------------------------------------------------
* 4. ECUACIONES (CONSTRAINTS)
* --------------------------------------------------------------------------

EQUATIONS
    OBJ             'Funcion Objetivo: Maximizar Bienestar Social'
    Balance_P       'Restriccion de Balance de Potencia (Generacion = Demanda)'
    Gen_Max(I, B)   'Restriccion de Potencia Maxima para Generacion'
    Dem_Max(J, K)   'Restriccion de Potencia Maxima para Demanda';

* 4.1. Función Objetivo
* Max WS = Sum(LAMBDA_D * P_D) - Sum(LAMBDA_G * P_G)
OBJ.. WS =E= SUM((J, K), LAMBDA_D(J, K) * P_D(J, K)) 
              - SUM((I, B), LAMBDA_G(I, B) * P_G(I, B));

* 4.2. Balance de Potencia
* Sum(P_G) = Sum(P_D)
Balance_P.. SUM((I, B), P_G(I, B)) =E= SUM((J, K), P_D(J, K));

* 4.3. Restricciones de Capacidad de Generación
* P_G(i, b) <= P_G_MAX(i, b)
Gen_Max(I, B).. P_G(I, B) =L= P_G_MAX(I, B);

* 4.4. Restricciones de Capacidad de Demanda
* P_D(j, k) <= P_D_MAX(j, k)
Dem_Max(J, K).. P_D(J, K) =L= P_D_MAX(J, K);

* --------------------------------------------------------------------------
* 5. MODELO Y RESOLUCIÓN
* --------------------------------------------------------------------------

MODEL SubastaSimple / ALL /;

* Resolver el problema como Programación Lineal (LP)
SOLVE SubastaSimple USING LP MAXIMIZING WS;
execute_unload 'Results M5_LP_E1.gdx';

* ------------------------------------------------