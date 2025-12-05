#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  4 19:12:46 2025

@author: pm.deoliveiradejes
"""

import pulp
import numpy as np
import matplotlib.pyplot as plt

# =============================================================================
# 1. DATOS DEL PROBLEMA
# =============================================================================

# Ofertas de los Generadores (Oferta)
P_G_max = np.array([
    [5, 12, 13],  # G1
    [8, 8, 9],    # G2
    [10, 10, 5]   # G3
])

# Lambda_G [$/MWh]: Precios ofertados por los generadores
Lambda_G = np.array([
    [1, 3, 3.5],   # G1
    [4.5, 5, 6],   # G2
    [8, 9, 10]     # G3
])

# Ofertas de los Consumidores (Demanda)
P_D_max = np.array([
    [8, 5, 5, 3],  # D1
    [7, 4, 4, 3]   # D2
])

# Lambda_D [$/MWh]: Precios ofertados por los consumidores (valoración)
Lambda_D = np.array([
    [20, 15, 7, 4], # D1
    [18, 16, 11, 3] # D2
])

N_G, N_B_G = P_G_max.shape
N_D, N_B_D = P_D_max.shape

Generators = range(N_G)
Demanders = range(N_D)
Blocks_G = range(N_B_G)
Blocks_D = range(N_B_D)


# =============================================================================
# 2. FORMULACIÓN Y SOLUCIÓN DEL PROBLEMA LP
# =============================================================================

# Crear el problema de maximización del Bienestar Social
prob = pulp.LpProblem("Maximizacion_Bienestar_Social", pulp.LpMaximize)

# Variables de decisión (potencia despachada por bloque)
P_G = pulp.LpVariable.dicts("P_G", ((i, b) for i in Generators for b in Blocks_G), lowBound=0)
P_D = pulp.LpVariable.dicts("P_D", ((j, k) for j in Demanders for k in Blocks_D), lowBound=0)

# FUNCIÓN OBJETIVO: Max W^S = Sum(Lambda_D * P_D) - Sum(Lambda_G * P_G)
prob += (
    pulp.lpSum(Lambda_D[j, k] * P_D[(j, k)] for j in Demanders for k in Blocks_D)
    - pulp.lpSum(Lambda_G[i, b] * P_G[(i, b)] for i in Generators for b in Blocks_G),
    "Bienestar_Social"
)

# RESTRICCIONES DE CAPACIDAD
for i in Generators:
    for b in Blocks_G:
        prob += P_G[(i, b)] <= P_G_max[i, b], f"Capacidad_Generador_{i+1}_Bloque_{b+1}"
        
for j in Demanders:
    for k in Blocks_D:
        prob += P_D[(j, k)] <= P_D_max[j, k], f"Capacidad_Demanda_{j+1}_Bloque_{k+1}"

# RESTRICCIÓN DE BALANCE DE POTENCIA (Generación = Demanda)
prob += (
    pulp.lpSum(P_G[(i, b)] for i in Generators for b in Blocks_G)
    == pulp.lpSum(P_D[(j, k)] for j in Demanders for k in Blocks_D),
    "Balance_Potencia"
)

# Solución del Problema
prob.solve()

# =============================================================================
# 3. EXTRACCIÓN Y RESUMEN DE RESULTADOS DEL DESPACHO
# =============================================================================

Shadow_Price = prob.constraints["Balance_Potencia"].pi
Equilibrium_Price = Shadow_Price if Shadow_Price is not None else 0.0

P_G_despacho = np.array([[P_G[(i, b)].varValue for b in Blocks_G] for i in Generators])
P_D_despacho = np.array([[P_D[(j, k)].varValue for k in Blocks_D] for j in Demanders])

Total_Power = P_G_despacho.sum()
Max_WS = pulp.value(prob.objective)

print("="*60)
print("## ✅ 1. RESULTADOS DEL DESPACHO ÓPTIMO (LP)")
print("="*60)
print(f"Estado de la Solución: {pulp.LpStatus[prob.status]}")
print(f"Bienestar Social Máximo (W^S): {Max_WS:.2f} $/h")
print(f"Potencia Total Despachada (Balance): {Total_Power:.2f} MW")
print(f"Precio Marginal del Mercado (CMP): {Equilibrium_Price:.2f} $/MWh")

print("\n### Despacho de Generación P_G (MW):")
print(P_G_despacho)
print("\n### Despacho de Demanda P_D (MW):")
print(P_D_despacho)


# =============================================================================
# 4. LIQUIDACIÓN PAY-AS-CLEAR (PAC)
# =============================================================================

Ingresos_G_PAC = P_G_despacho.sum(axis=1) * Equilibrium_Price
Egresos_D_PAC = P_D_despacho.sum(axis=1) * Equilibrium_Price

print("\n" + "="*60)
print("## 💰 2. LIQUIDACIÓN PAY-AS-CLEAR (PAC)")
print("="*60)
print(f"Precio de Liquidación (CMP): {Equilibrium_Price:.2f} $/MWh")

print("\n### Ingresos de los Generadores:")
for i in Generators:
    print(f"Unidad {i+1}: {P_G_despacho[i].sum():.0f} MW x {Equilibrium_Price:.2f} $/MWh = {Ingresos_G_PAC[i]:.1f} $/h")
print(f"-> Ingresos Totales Generadores: {Ingresos_G_PAC.sum():.1f} $/h")

print("\n### Egresos de los Consumidores:")
for j in Demanders:
    print(f"Demanda {j+1}: {P_D_despacho[j].sum():.0f} MW x {Equilibrium_Price:.2f} $/MWh = {Egresos_D_PAC[j]:.1f} $/h")
print(f"-> Egresos Totales Consumidores: {Egresos_D_PAC.sum():.1f} $/h")


# =============================================================================
# 5. LIQUIDACIÓN PAY-AS-BID (PAB)
# =============================================================================

Ingresos_G_PAB = (P_G_despacho * Lambda_G).sum()
Egresos_D_PAB = (P_D_despacho * Lambda_D).sum()

print("\n" + "="*60)
print("## 💸 3. LIQUIDACIÓN PAY-AS-BID (PAB)")
print("="*60)

print("### Ingresos de los Generadores (PAB):")
for i in Generators:
    ingreso_i = (P_G_despacho[i] * Lambda_G[i]).sum()
    print(f"Unidad {i+1}: {ingreso_i:.1f} $/h")
print(f"-> Ingresos Totales Generadores: {Ingresos_G_PAB:.1f} $/h")

print("\n### Egresos de los Consumidores (PAB):")
for j in Demanders:
    egreso_j = (P_D_despacho[j] * Lambda_D[j]).sum()
    print(f"Demanda {j+1}: {egreso_j:.1f} $/h")
print(f"-> Egresos Totales Consumidores: {Egresos_D_PAB:.1f} $/h")


# =============================================================================
# 6. GRÁFICO DE CASACIÓN DE CURVAS
# =============================================================================

def plot_auction_curves(P_G_max, Lambda_G, P_D_max, Lambda_D, Total_Power, Equilibrium_Price):
    
    # --- Preparación de la Curva de Oferta (Generación) ---
    offers = []
    for i in Generators:
        for b in Blocks_G:
            offers.append((P_G_max[i, b], Lambda_G[i, b]))
    offers.sort(key=lambda x: x[1]) # Ordenar por Precio ascendente
    
    P_G_cumulative = np.cumsum([o[0] for o in offers])
    P_G_prices = [o[1] for o in offers]
    
    P_G_plot = np.insert(P_G_cumulative, 0, 0)
    P_G_prices_plot = np.insert(P_G_prices, 0, P_G_prices[0])

    # --- Preparación de la Curva de Demanda (Consumo) ---
    demands = []
    for j in Demanders:
        for k in Blocks_D:
            demands.append((P_D_max[j, k], Lambda_D[j, k]))
    demands.sort(key=lambda x: x[1], reverse=True) # Ordenar por Precio descendente
    
    P_D_cumulative = np.cumsum([d[0] for d in demands])
    P_D_prices = [d[1] for d in demands]
    
    P_D_plot = np.insert(P_D_cumulative, 0, 0)
    P_D_prices_plot = np.insert(P_D_prices, 0, P_D_prices[0])


    # --- Dibujar la Casación ---
    plt.figure(figsize=(10, 6))
    
    # Curva de Oferta (Step up)
    plt.step(P_G_plot, P_G_prices_plot, where='post', label='Oferta Agregada', color='red', linewidth=2)
    
    # Curva de Demanda (Step down)
    plt.step(P_D_plot, P_D_prices_plot, where='post', label='Demanda Agregada', color='blue', linewidth=2)
    
    # Punto de Equilibrio (CMP)
    plt.plot(Total_Power, Equilibrium_Price, 'o', color='green', markersize=8, 
             label=f'CMP: ({Total_Power:.1f} MW, {Equilibrium_Price:.1f} $/MWh)')
    plt.axvline(Total_Power, color='green', linestyle='--', alpha=0.6)
    plt.axhline(Equilibrium_Price, color='green', linestyle='--', alpha=0.6)
    
    # Rellenar el área de Bienestar Social (visualización conceptual)
    idx_d = np.searchsorted(P_D_plot, Total_Power)
    P_D_fill = P_D_plot[:idx_d+1]
    P_D_prices_fill = P_D_prices_plot[:idx_d+1]
    P_D_fill = np.append(P_D_fill, Total_Power)
    P_D_prices_fill = np.append(P_D_prices_fill, Equilibrium_Price)
    
    idx_g = np.searchsorted(P_G_plot, Total_Power)
    P_G_fill = P_G_plot[:idx_g+1]
    P_G_prices_fill = P_G_prices_plot[:idx_g+1]
    P_G_fill = np.append(P_G_fill, Total_Power)
    P_G_prices_fill = np.append(P_G_prices_fill, Equilibrium_Price)
    
    # Área bajo la demanda y sobre la oferta hasta el CMP
    plt.fill_between(P_D_fill, P_D_prices_fill, Equilibrium_Price, 
                     where=P_D_fill <= Total_Power, color='lightblue', alpha=0.3, step='post')
    
    plt.fill_between(P_G_fill, Equilibrium_Price, P_G_prices_fill, 
                     where=P_G_fill <= Total_Power, color='pink', alpha=0.3, step='post')

    
    # Títulos y Etiquetas
    plt.title('Casación de Curvas de Oferta y Demanda (Subasta Simple)')
    plt.xlabel('Potencia (MW)')
    plt.ylabel('Precio ($/MWh)')
    plt.legend()
    plt.grid(True, linestyle='--')
    plt.ylim(0, max(P_D_prices_plot) + 2)
    plt.xlim(0, max(P_G_plot[-1], P_D_plot[-1]) + 5)
    plt.xticks(sorted(list(set(np.concatenate((P_G_plot, P_D_plot, [Total_Power]))))))
    plt.yticks(sorted(list(set(np.concatenate((P_G_prices_plot, P_D_prices_plot, [Equilibrium_Price]))))))
    
    plt.show()

# Ejecutar la función de gráfico
plot_auction_curves(P_G_max, Lambda_G, P_D_max, Lambda_D, Total_Power, Equilibrium_Price)