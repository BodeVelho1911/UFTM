import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import square

# Programa para aplicação prática da Transformada Discreta de Fourier na mudança de domínio do tempo
# para o dominio da frequência de um sinal digital (Discretizado) harmônico e periódico
 
# Parâmetros de amostragem (Escolhe 2 e calcula o restante)
dt = 2e-3 # Resolução no tempo [s]
T = 1 # Tempo total [s]
fs = 1 / dt # Frequência de aquisição [Hz]
N = T / dt # Número de pontos
df = fs / N # Resolução em frequência [Hz]
tempo = np.arange(0, (N-1)*dt, dt) # Vetor de tempo

# Sinal harmônico
A1 = 1 # Amplitude [V]
f1 = 10 # Frequência [Hz]
harm = A1 * np.sin(2 * np.pi * f1 * tempo)

# Sinal periódico (Quadrado)
A2 = 1 # Amplitude [V]
f2 = 5 # Frequência [Hz]
period = A2 * square(2 * np.pi * f2 * tempo)

# Espectro do sinal harmônico (Domínio da frequência)
freq = np.arange(0, (N-1)*df, df) # Vetor de frequência
espectro_harm = np.fft.fft(harm) * 2 / N
N_metade = int(N // 2)

# Espectro do sinal periódico (Quadrado)
espectro_period = np.fft.fft(period) * 2 / N

# Gráficos
fig, axs = plt.subplots(2, 2, figsize=(10, 8))
linecolor = "#509000"
plt.rcParams['font.family'] = 'Times New Roman'  # Fonte
plt.rcParams['font.size'] = 12  # Tamanho da fonte
plt.rcParams['font.weight'] = 'bold'  # Peso da fonte

# Gráfico do sinal harmônico no tempo
axs[0, 0].plot(tempo, harm, marker="o", markersize=2, color=linecolor)  
axs[0, 0].set_xlabel('Tempo [s]')
axs[0, 0].set_ylabel('Amplitude [V]')
axs[0, 0].set_title('Sinal harmônico no domínio do tempo')
axs[0, 0].grid()

# Gráfico do espectro do sinal harmônico (Domínio da frequência)
axs[0, 1].plot(freq[1:N_metade],                 # Plota apenas metade dos pontos, pois a FFT 
            abs(espectro_harm[1:N_metade]),      # espelha os dados ao redor de Fmáx = fs / 2
            marker="o",                          # É utilizada a função abs() para o módulo dos complexos da FFT
            markersize=2, 
            color=linecolor) 
axs[0, 1].set_xlabel('Frequência [Hz]')
axs[0, 1].set_ylabel('Amplitude [V]')
axs[0, 1].set_title('Espectro do sinal harmônico (FFT)')
axs[0, 1].grid()

# Gráfico do sinal periódico no tempo
axs[1, 0].plot(tempo, period, marker="o", markersize=2, color=linecolor)  
axs[1, 0].set_xlabel('Tempo [s]')
axs[1, 0].set_ylabel('Amplitude [V]')
axs[1, 0].set_title('Sinal periódico no domínio do tempo')
axs[1, 0].grid()

# Gráfico do espectro do sinal periódico (Domínio da frequência)
axs[1, 1].plot(freq[1:N_metade],                 # Plota apenas metade dos pontos, pois a FFT 
            abs(espectro_period[1:N_metade]),    # espelha os dados ao redor de Fmáx = fs / 2.
            marker="o",                          # É utilizada a função abs() para o módulo dos complexos da FFT
            markersize=2, 
            color=linecolor)
axs[1, 1].set_xlabel('Frequência [Hz]')
axs[1, 1].set_ylabel('Amplitude [V]')
axs[1, 1].set_title('Espectro do sinal periódico (FFT)')
axs[1, 1].grid()

plt.tight_layout()
plt.show()
