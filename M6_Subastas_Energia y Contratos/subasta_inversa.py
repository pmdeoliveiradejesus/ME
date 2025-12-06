#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  6 18:17:15 2025

@author: pm.deoliveiradejes
"""

import pulp

# --- 1. Definición de Datos ---

# Capacidad Requerida Total (MW)
C_req = 500
# Energía Anual Equivalente por MW (MWh/MW-año)
E_MW = 5000
# Restricciones de Balance (%)
R_min = 0.50
T_min = 0.50

# Datos de las Ofertas
# (Capacidad [MW], Tipo [R/T], Precio Energía [USD/MWh], Precio Potencia [USD/MW-mes])
ofertas_data = {
    1: (100, 'R', 45.00, 6000),  # Vendedor A (Eólica)
    2: (150, 'T', 70.00, 15000), # Vendedor B (Gas Natural)
    3: (200, 'R', 42.50, 5500),  # Vendedor C (Solar)
    4: (50, 'T', 85.00, 18000),  # Vendedor D (Diesel)
    5: (100, 'T', 72.00, 14000), # Vendedor B (Gas Natural)
    6: (50, 'R', 43.00, 5800)   # Vendedor C (Solar)
}

# --- 2. Creación del Modelo de Optimización ---

modelo = pulp.LpProblem("Subasta_Inversa_PPA", pulp.LpMinimize)

# Variables de Decisión (Binarias)
X = pulp.LpVariable.dicts("Oferta", ofertas_data.keys(), lowBound=0, upBound=1, cat=pulp.LpInteger)

# --- 3. Función Objetivo ---

# Costo Anual Total = Sum(X_i * [ (P^E_i * E_MW * C_i) + (P^P_i * 12 * C_i) ])
costo_total_anual = 0
for i, (C_i, T_i, PE_i, PP_i) in ofertas_data.items():
    # Costo Anual de Energía
    costo_energia = PE_i * E_MW * C_i
    # Costo Anual de Potencia (mensual * 12)
    costo_potencia = PP_i * 12 * C_i
    
    costo_total_anual += X[i] * (costo_energia + costo_potencia)

modelo += costo_total_anual, "Costo_Total_Anual"

# --- 4. Restricciones ---

# 1. Restricción de Capacidad Total Requerida (500 MW)
capacidad_adjudicada = pulp.lpSum([X[i] * ofertas_data[i][0] for i in ofertas_data])
modelo += capacidad_adjudicada == C_req, "Capacidad_Total_Requerida"

# 2. Restricción de Balance Tecnológico (Renovable >= 50%)
capacidad_renovable = pulp.lpSum([X[i] * ofertas_data[i][0] for i in ofertas_data if ofertas_data[i][1] == 'R'])
modelo += capacidad_renovable >= R_min * C_req, "Min_Renovable"

# 3. Restricción de Balance Tecnológico (Térmico >= 50%)
capacidad_termica = pulp.lpSum([X[i] * ofertas_data[i][0] for i in ofertas_data if ofertas_data[i][1] == 'T'])
modelo += capacidad_termica >= T_min * C_req, "Min_Termico"

# --- 5. Solución del Modelo ---

modelo.solve()

# --- 6. Impresión de Resultados ---

print(f"\n## Resultados de la Subasta Inversa ##")
print(f"Estado de la solución: {pulp.LpStatus[modelo.status]}")
print(f"Costo Total Anual Mínimo Adjudicado: ${modelo.objective.value():,.2f}")

cap_ren_adj = 0
cap_ter_adj = 0
costo_ren_adj = 0
costo_ter_adj = 0

print("\n--- Adjudicación por Oferta ---")
for i in ofertas_data:
    if X[i].varValue == 1.0:
        cap_i, tipo_i, pe_i, pp_i = ofertas_data[i]
        costo_anual_i = (pe_i * E_MW * cap_i) + (pp_i * 12 * cap_i)
        
        print(f"Oferta {i} (Tipo: {tipo_i}, Cap: {cap_i} MW): **ADJUDICADA** (Costo Anual: ${costo_anual_i:,.2f})")
        
        if tipo_i == 'R':
            cap_ren_adj += cap_i
            costo_ren_adj += costo_anual_i
        else:
            cap_ter_adj += cap_i
            costo_ter_adj += costo_anual_i

print("\n--- Resumen de Adjudicación ---")
print(f"Capacidad Total Adjudicada: {capacidad_adjudicada.value():.0f} MW")
print(f"Capacidad Renovable Adjudicada: {cap_ren_adj:.0f} MW ({(cap_ren_adj/C_req)*100:.2f}%)")
print(f"Capacidad Térmica Adjudicada: {cap_ter_adj:.0f} MW ({(cap_ter_adj/C_req)*100:.2f}%)")
print(f"Costo Anual Renovable: ${costo_ren_adj:,.2f}")
print(f"Costo Anual Térmico: ${costo_ter_adj:,.2f}")