import pandas as pd
from io import StringIO
"""Converte o arquivo .txt gerado pela máquina universal de ensaios em arquivo .csv,
extrai os dados, excluindo o cabeçalho e o rodapé.
Trocar o caminho 'file_path' pelo caminho do arquivo .txt."""

# Caminho do arquivo .txt
file_path = "./Dados - Compressão/P2 - Mac 05.txt"

# Caminho do arquivo .csv
output_path = "./Dados - Compressão/macad_5_compressao.csv"

# Abrindo o arquivo para identificar a linha onde os dados começam
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# Encontrando a linha onde começa a tabela de dados
start_index = next(i for i, line in enumerate(lines) if "index" in line)

# Extraindo os dados a partir da linha identificada
data = lines[start_index+1:]  # Pulamos a linha do cabeçalho textual

# Filtrando apenas linhas que começam com números
data = [line for line in data if line.strip() and line.strip()[0].isdigit()]

# Criando um DataFrame com os dados numéricos
df = pd.read_csv(
    StringIO("\n".join(data)),  
    delim_whitespace=True,  
    usecols=[0, 1, 2],  
    names=["Index", "Load (kN)", "Defor (mm)"]
)

# Converter 'Index' para inteiro de forma segura
df["Index"] = pd.to_numeric(df["Index"], errors='coerce')  
df["Load (kN)"] = pd.to_numeric(df["Load (kN)"], errors='coerce')
df["Defor (mm)"] = pd.to_numeric(df["Defor (mm)"], errors='coerce')

# Remover quaisquer linhas com valores NaN, garantindo que apenas números fiquem no DataFrame
df = df.dropna().astype({"Index": int, "Load (kN)": float, "Defor (mm)": float})

# Filtrar novamente para garantir que os índices estejam em ordem crescente (removendo possíveis erros no final)
df = df[df["Index"] >= 0]  # Mantém apenas valores válidos de índice

# Salvando o DataFrame filtrado
df.to_csv(output_path, index=False)

print(f"Arquivo salvo com sucesso em: {output_path}")
