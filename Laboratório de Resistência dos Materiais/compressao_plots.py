import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import simpson
    
"""Programa que analisa os dados obtidos em um ensaio de compressão
Trocar o caminho do arquivo dos dados (.csv) em 'file_path'."""
    
# Caminho para arquivo
file_path = "./Dados - Compressão/aluminio_compressao.csv"

# Lê e transforma em DataFrame
data = pd.read_csv(file_path)
df = pd.DataFrame(data)

# Dados iniciais
L0 = np.mean([19.68, 19.68, 19.68, 19.68, 19.68, 19.67, 19.67, 19.67, 19.67]) 
d = np.mean([9.47, 9.47, 9.47, 9.48, 9.48, 9.48, 9.48, 9.48, 9.48, 9.49]) # Diâmetro do CDP [mm]
A = (np.pi * d ** 2) / 4 # Área da seção do CDP [mm]

# Adicionando colunas para calculo de outras grandezas do CDP
df["Load (N)"] = df["Load (kN)"] * 1e3 # Força em [N]
df["Rel. Defor."] = df["Defor (mm)"] / L0 # Deformação relativa []
df["Stress (MPa)"] = df["Load (N)"] / A

# Limite de resistência à compressão
Sut = max(df["Stress (MPa)"])

# Separa um intervalo de deformação elástica
ind = (df["Rel. Defor."] - 0.017).abs().idxmin() # Index final da fase elástica
deform = df["Rel. Defor."].iloc[:ind]
stress = df["Stress (MPa)"].iloc[:ind]

# Tendência da fase elástica
a, b = np.polyfit(deform, stress, 1)

# Módulo de Young [GPa]
E = a * 1e-3

# Linha paralela à fase elástica (0.2% transladada)
def reta_paral(x, a, b):
    return a * (x - 0.002) + b

df["Paralel Line [MPa]"] = reta_paral(df["Rel. Defor."], a, b)
line_ind = df["Paralel Line [MPa]"].abs().idxmin() # Index de limite inferior
line_ind2 = (df["Paralel Line [MPa]"] - 300).abs().idxmin() # Index de limite superior
line_deform = df["Rel. Defor."].iloc[line_ind:line_ind2]
line_stress = df["Stress (MPa)"].iloc[line_ind:line_ind2]

# Tensão Limite de Escoamento
df["Diference from Line"] = df["Stress (MPa)"] - df["Paralel Line [MPa]"]
sigma_ind = df["Diference from Line"].abs().idxmin()
sigma_e = df.at[sigma_ind, "Stress (MPa)"]

# Resiliência [J/m³]
res = ((sigma_e * 1e6) ** 2) / (2 * E * 1e9)

# Tenacidade
ten = simpson(df["Stress (MPa)"] * 1e6, df["Rel. Defor."])
    
# Interalo total do ensaio
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(df["Rel. Defor."], df["Stress (MPa)"], color="green")
plt.plot(line_deform, df["Paralel Line [MPa]"].iloc[line_ind:line_ind2], ls="--", color="r")
plt.title(label="Ensaio de compressão - Alumínio")
plt.xlabel("Deformação Relativa []")
plt.ylabel("Tensão Normal [MPa]")
plt.grid()

# Fase elástica
plt.subplot(1, 2, 2)
plt.plot(deform, stress, label=f"Tendência: {a:.1f}x + {b:.1f}", color="green")
plt.title(label="Alumínio - Fase elástica")
plt.xlabel("Deformação Relativa []")
plt.ylabel("Tensão Normal [MPa]")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Propriedades do material
print(f"Limite de Resistência à Compressão: {Sut:.2f} MPa")
print(f"Módulo de Young: {E:.2f} GPa")
print(f"Limite de Escoamento: {sigma_e:.2f} MPa")
print(f"Resiliência: {res * 1e-3:.1f} kJ/m³")
print(f"Tenacidade: {ten * 1e-3:.1f} kJ/m³")