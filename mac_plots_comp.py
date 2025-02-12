import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
    
"""Programa que analisa os dados obtidos em um ensaio de compressão
Trocar o caminho do arquivo dos dados (.csv) em 'file_path'."""
    
# Caminho para arquivo
n = 5 # Nro da Macadâmia 
file_path = f"./Dados - Compressão/macad_{n}_compressao.csv"

# Lê e transforma em DataFrame
data = pd.read_csv(file_path)
df = pd.DataFrame(data)

# Dados iniciais
m = 10.733 # Massa [g]
d = np.mean([26.54, 26.32, 26.61, 26.27, 28.64]) # Diâmetro da macadâmia [mm]
v = (4 / 3) * np.pi * (d / 20) ** 3 # Volume [cm³]
rho = m / v # Massa específica [g/cm³]

# Adicionando colunas para calculo de outras grandezas do CDP
df["Load (N)"] = df["Load (kN)"] * 1e3 # Força em [N]

# Limite de resistência à compressão
Suc = max(df["Load (N)"])

# Separa um intervalo de deformação elástica
init_ind = (df["Defor (mm)"] - 0.1).abs().idxmin() # Index inicial da fase elástica 
end_ind = (df["Defor (mm)"] - 1.4).abs().idxmin() # Index final da fase elástica
deform = df["Defor (mm)"].iloc[init_ind:end_ind]
stress = df["Load (N)"].iloc[init_ind:end_ind]

# Tendência da fase elástica
a, b = np.polyfit(deform, stress, 1)

# Rigidez [N/mm]
E = a 

# Máxima deformação
max_def = max(df["Defor (mm)"])

# Linha paralela à fase elástica (0.2% transladada)
def reta_paral(x, a, b):
    return a * (x - 0.002 * d) + b

df["Paralel Line"] = reta_paral(df["Defor (mm)"], a, b)
line_ind = df["Paralel Line"].abs().idxmin() # Index de limite inferior
line_ind2 = (df["Paralel Line"] - 2700).abs().idxmin() # Index de limite superior
line_deform = df["Defor (mm)"].iloc[line_ind:line_ind2]
line_stress = df["Load (N)"].iloc[line_ind:line_ind2]

# Tensão Limite de Escoamento (Correção do método)
df["Diference from Line"] = df["Load (N)"] - df["Paralel Line"]

# Encontrar o primeiro ponto onde ocorre a mudança de sinal
crossing_indices = np.where(np.diff(np.sign(df["Diference from Line"])))[0]

if len(crossing_indices) > 0:
    sigma_ind1 = crossing_indices[0]  # Primeiro ponto antes da interseção
    sigma_ind2 = sigma_ind1 + 1  # Primeiro ponto depois da interseção

    # Pegamos os valores de deformação e carga nos dois pontos
    x1, y1 = df.loc[sigma_ind1, "Defor (mm)"], df.loc[sigma_ind1, "Load (N)"]
    x2, y2 = df.loc[sigma_ind2, "Defor (mm)"], df.loc[sigma_ind2, "Load (N)"]
    
    # Pegamos as diferenças nos dois pontos
    diff1 = df.loc[sigma_ind1, "Diference from Line"]
    diff2 = df.loc[sigma_ind2, "Diference from Line"]

    # Interpolação linear para encontrar o ponto exato onde Diference from Line = 0
    x_intersec = x1 - (diff1 * (x2 - x1)) / (diff2 - diff1)
    sigma_e = y1 + (x_intersec - x1) * (y2 - y1) / (x2 - x1)

else:
    sigma_e = np.nan  # Retorna NaN se não houver interseção

# Propriedades do material
print(f"Carga Máxima: {Suc:.2f} N")
print(f"Rigidez: {E:.2f} N/mm")
print(f"Limite de Resistência: {sigma_e:.2f} N")
print(f"Diâmetro médio: {d:.2f} mm")
print(f"Massa específica média: {rho:.5f} g/cm³")

# Interalo total do ensaio
plt.figure(figsize=(16, 6))
plt.subplot(1, 2, 1)
plt.plot(df["Defor (mm)"], df["Load (N)"], color="green", label="Curva experimental")
plt.plot(line_deform, df["Paralel Line"].iloc[line_ind:line_ind2], ls="--", color="r", label="Tendência transladada em 0,2 %")
plt.title(label=f"Ensaio de compressão - Macadâmia {n}")
plt.xlabel("Deformação [mm]")
plt.ylabel("Carga [N]")
plt.legend()
plt.grid()

# Fase elástica
plt.subplot(1, 2, 2)
plt.plot(deform, stress, label=f"Tendência: {a:.1f}x + {b:.1f}", color="green")
plt.title(label=f"Macadâmia {n} - Fase elástica")
plt.xlabel("Deformação [mm]")
plt.ylabel("Carga [N]")
plt.legend()
plt.grid()
plt.tight_layout()
plt.show()

# Dados em txt
with open(f"./Gráficos - Compressão/macad_{n}_prop.txt", "w") as file:
    file.write(f"Carga Msxima: {Suc:.2f} N\n")
    file.write(f"Rigidez: {E:.2f} N/mm\n")
    file.write(f"Limite de Resistencia: {sigma_e:.2f} N\n")
    file.write(f"Diametro medio: {d:.2f} mm\n")
    file.write(f"Massa especifica media: {rho:.5f} g/cm³")