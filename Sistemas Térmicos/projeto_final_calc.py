import numpy as np
import pandas as pd
import CoolProp.CoolProp as cp

# Configurações
fluid = 'Water'

# Intervalos de variação
p2_values = np.arange(1e6, 13e6, 2e6)  # 1 MPa a 11 MPa com passo de 2 MPa

# Constantes
p1, T1 = 12e6, 480 + 273.15
T4, p6 = 480 + 273.15, 6e3
p10, p11 = p1, p1
ef_is_turb, ef_is_bomba, ef_reg_fec = 0.9, 0.8, 0.95

# Lista para armazenar os resultados
results = []

# Loop para variação de p2 e p5
for p2 in p2_values:
    p5_values = np.arange(100e3, p2, 100e3)  # p5 varia de 100 kPa até p2
    for p5 in p5_values:
        p3, p4, p7, p8, p9, p12, p13 = p2, p2, p6, p5, p5, p2, p5
        
        # Cálculos
        h1 = cp.PropsSI("H", "P", p1, "T", T1, fluid) * 1e-3
        s1 = cp.PropsSI("S", "P", p1, "T", T1, fluid)
        h2s = cp.PropsSI("H", "P", p2, "S", s1, fluid) * 1e-3
        h2 = h1 - ef_is_turb * (h1 - h2s)
        s2 = cp.PropsSI("S", "P", p2, "H", h2 * 1e3, fluid)
        h3s = cp.PropsSI("H", "P", p3, "S", s2, fluid) * 1e-3
        h3 = h2 - ef_is_turb * (h2 - h3s)
        h4 = cp.PropsSI("H", "P", p4, "T", T4, fluid) * 1e-3
        s4 = cp.PropsSI("S", "P", p4, "H", h4 * 1e3, fluid)
        h5s = cp.PropsSI("H", "P", p5, "S", s4, fluid) * 1e-3
        h5 = h4 - ef_is_turb * (h4 - h5s)
        s5 = cp.PropsSI("S", "P", p5, "H", h5 * 1e3, fluid)
        h6s = cp.PropsSI("H", "P", p6, "S", s5, fluid) * 1e-3
        h6 = h5 - ef_is_turb * (h5 - h6s)
        x6 = cp.PropsSI("Q", "P", p6, "H", h6, fluid) 
        h7 = cp.PropsSI("H", "P", p7, "Q", 0, fluid) * 1e-3
        h8s = cp.PropsSI("H", "P", p8, "S", cp.PropsSI("S", "P", p7, "H", h7 * 1e3, fluid), fluid) * 1e-3
        h8 = (h7 * (ef_is_bomba - 1) + h8s) / ef_is_bomba
        h9 = cp.PropsSI("H", "P", p9, "Q", 0, fluid) * 1e-3
        h10s = cp.PropsSI("H", "P", p10, "S", cp.PropsSI("S", "P", p9, "H", h9 * 1e3, fluid), fluid) * 1e-3
        h10 = (h9 * (ef_is_bomba - 1) + h10s) / ef_is_bomba
        T12 = cp.PropsSI("T", "P", p12, "Q", 0, fluid)
        h12 = cp.PropsSI("H", "P", p12, "Q", 0, fluid) * 1e-3
        
        # Correção no cálculo do estado 11
        p_sat_T12 = cp.PropsSI("P", "T", T12, "Q", 0, fluid)
        h11i = cp.PropsSI("H", "P", p11, "T", T12, fluid) * 1e-3 if p11 >= p_sat_T12 else cp.PropsSI("H", "P", p11, "Q", 0, fluid) * 1e-3
        h11 = h10 + ef_reg_fec * (h11i - h10)
        h13 = h12
        
        y_reg_fec = (h11 - h10) / (h2 - h12) if abs(h2 - h12) > 1e-3 else 0
        y_reg_aberto = (h9 - h8 - y_reg_fec * (h13 - h8)) / (h5 - h8) if abs(h5 - h8) > 1e-3 else 0
        
        # Cálculo de transferências de calor e potência líquida
        Q_cald = h1 - h11
        Q_reaq = (1 - y_reg_fec) * (h4 - h3)
        Q_cond = (1 - y_reg_fec - y_reg_aberto) * (h7 - h6)
        Q_reg_fec = h11 - h10
        Q_reg_aberto = (1 - y_reg_fec - y_reg_aberto) * (h9 - h8)
        P_liq = Q_cald + Q_reaq + Q_cond
        ef_ciclo = max(0, min((P_liq / (Q_cald + Q_reaq)) * 100, 100)) if (Q_cald + Q_reaq) > 1e-3 else 0
        
        # Armazenar resultados
        results.append([p2 / 1e6, p5 / 1e3, x6 * 100, y_reg_fec * 100, y_reg_aberto * 100, Q_cald, Q_reaq, Q_cond, Q_reg_aberto, Q_reg_fec, P_liq, ef_ciclo])

# Criar DataFrame
df = pd.DataFrame(results, columns=["Pressão no ponto 2 (MPa)", "Pressão no ponto 5 (kPa)", "Título na saída da turbina (%)", "Fração de extração p/ reg. fechado (%)",
                                    "Fração de extração p/ reg. aberto (%)", "Calor na caldeira (kJ/kg)", "Calor no reaquecedor (kJ/kg)", "Calor no condensador (kJ/kg)",
                                    "Calor no reg. aberto (kJ/kg)", "Calor no reg. fechado (kJ/kg)", "Potência líquida (kJ/kg)", "Eficiência do ciclo (%)"])
df.to_excel("resultados_ciclo_rankine.xlsx", index=False, engine="openpyxl")
print("Resultados salvos em 'resultados_ciclo_rankine.xlsx'")
