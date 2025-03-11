import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

# Carregar os dados
file_path = "resultados_ciclo_rankine.xlsx"
df = pd.read_excel(file_path)

# Verificar nome exato da coluna
coluna_fra_extr = next((col for col in df.columns if "Fração" in col and "reg. aberto" in col), None)
if coluna_fra_extr is None:
    print("Aviso: Coluna de fração de extração para o regenerador aberto não encontrada. Verifique os nomes das colunas no arquivo.")
    print("Colunas disponíveis:", df.columns.tolist())
    raise KeyError("Coluna de fração de extração para o regenerador aberto não encontrada.")

# Definição das variáveis para os gráficos
variables = df.columns[2:]
title_names = [
    "Título na saída da turbina",
    "Fração de ext. p/ reg. fechado",
    "Fração de ext. p/ reg. aberto",
    "Calor na caldeira",
    "Calor no reaquecedor",
    "Calor no condensador",
    "Calor no regenerador aberto",
    "Calor no regenerador fechado",
    "Potência líquida",
    "Eficiência do ciclo"
]
current_index = 0

# Criar figura e eixo
fig, ax = plt.subplots(figsize=(8, 6))
plt.subplots_adjust(bottom=0.2)

# Função para atualizar o gráfico
def update_graph(index):
    ax.clear()
    var = variables[index]
    title = title_names[index]
    
    unique_p2 = df["Pressão no ponto 2 (MPa)"].unique()
    default_colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
    color_map = {p2: default_colors[i % len(default_colors)] for i, p2 in enumerate(unique_p2)}
    legend_handles = {}
    
    for p2 in unique_p2:
        subset = df[df["Pressão no ponto 2 (MPa)"] == p2]
        subset_sorted = subset.sort_values("Pressão no ponto 5 (kPa)")
        
        prev_color = None
        for i in range(len(subset_sorted) - 1):
            fra_extr = subset_sorted.iloc[i][coluna_fra_extr]
            cor = "black" if fra_extr < 0 else color_map[p2]
            
            if cor != prev_color or prev_color is None:
                if cor != "black" and p2 not in legend_handles:
                    legend_handles[p2] = ax.plot([], [], color=color_map[p2], label=f"{p2} MPa")[0]
            
            ax.plot(
                [subset_sorted.iloc[i]["Pressão no ponto 5 (kPa)"], subset_sorted.iloc[i + 1]["Pressão no ponto 5 (kPa)"]],
                [subset_sorted.iloc[i][var], subset_sorted.iloc[i + 1][var]],
                color=cor
            )
            prev_color = cor
    
    ax.set_xlabel("Pressão no ponto 5 (kPa)")
    ax.set_ylabel(var)
    ax.set_title(title)
    ax.legend(handles=legend_handles.values(), title='Pressão no ponto 2', loc='lower right', framealpha=0.5)
    ax.grid()
    fig.canvas.draw()

# Função para avançar
def next_graph(event):
    global current_index
    current_index = (current_index + 1) % len(variables)
    update_graph(current_index)

# Função para voltar
def prev_graph(event):
    global current_index
    current_index = (current_index - 1) % len(variables)
    update_graph(current_index)

# Botões de navegação
axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
bnext = Button(axnext, 'Próximo')
bprev = Button(axprev, 'Anterior')
bnext.on_clicked(next_graph)
bprev.on_clicked(prev_graph)

# Inicializar gráfico
update_graph(current_index)
plt.show()
