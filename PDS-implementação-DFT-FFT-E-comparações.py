import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.fft import fft

#gerando um sinal cosenoidal
def function(n, A=1):# n vetor de amostras A amplitude
    return A * np.cos(2 * np.pi * n / 10)

#implementação da DFT usando multiplicação matricial
def DFT(x, n):
    wn = np.exp(-1j * 2 * np.pi / n)  # Raiz da unidade,base da exponencial complexa usada para calcular os coeficientes da DFT.
    w = np.zeros((n, n), dtype=complex)  # Matriz W (armazenaremos os fatores exponenciais)

    for i in range(n):
        for j in range(n):
            w[i, j] = wn ** (i * j)  # Preenchimento da matriz W com os fatores exponenciais

    zp = np.pad(x, (0, n - len(x)), 'constant')  # Aplicação do zero-padding para ajuta o tamanho prechendo com zero
    return np.dot(w, zp)  # Multiplicação matricial para calcular a DFT


# Número de pontos
N = 64
k = np.arange(N)#cria um vetor de índices de 0 a 63, usado para representar o tempo ou frequência.
x = function(k) #gera o sinal cosenoidal de comprimento N.

# Calculo da DFT usando a implementação própria
Xd = DFT(x, N) #computa a DFT do sinal x.

# Calcula a magnitude dos coeficiente da DFT
magnitude = np.abs(Xd)

# Plotagem dos resultados
plt.figure(figsize=(12, 6))

# Plot do sinal original
plt.subplot(2, 1, 1)
plt.stem(k, x)
plt.title('Sinal Original')
plt.xlabel('Tempo (n)')
plt.ylabel('Amplitude')

# Plot do espectro da DFT (magnetude)
plt.subplot(2, 1, 2)
plt.stem(k, magnitude)
plt.title('Magnitude da DFT')
plt.xlabel('Frequência (k)')
plt.ylabel('Magnitude')

plt.tight_layout()
plt.show()




#função utilizada na implementação da fft
def butterfly(a, b):  #combina os resultados das sub-FFT's em termos de soma e diferença.
    return a + b, a - b

#implementação recursisa da FFT
def FFT(x):  #divide o problema em partes menores (pares e ímpares) até que o tamanho do problema seja 1 (caso base).
    N = len(x)
    if N == 1:
        return x    #caso a FFT de um único ponto é ele mesmo
    else:
        Wn = np.exp(-1j * 2 * np.pi * np.arange(N // 2) / N)  #fatores de rotação
        par = FFT(x[0::2])  #FFT dos termos de índice pares
        impar = FFT(x[1::2])  #FFT dos termos índice ímpares
        X = butterfly(par, Wn * impar)  #combinação dos resultados utilizando o butterfly
        return np.concatenate(X)   #combina os resultados

#implementação básica do algoritmo Cooley-Tukey


# Amplitude
A = 1

# Número de pontos
N = 128

# Gerando o sinal. Gera um sinal cosenoidal com o comprimento N = 128.
k = np.arange(0, N)
x = function(k, A)

#cálculo da FFT usando a implementação própria
sinal = FFT(x)

#calculo da magnetude dos coeficientes da FFT, Calcula a magnitude da FFT, que mostra as intensidades das frequências no sinal.
magnitude = np.abs(sinal)

# Plotagem dos resultados
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.stem(k, x, label='x(n)')
plt.title('Sinal Original')
plt.xlabel('tempo(n)')
plt.ylabel('Amplitude')

# Plotagem do espectro da FFT (magnitude)
plt.subplot(2, 1, 2)
plt.stem(k, magnitude)
plt.title('Sinal de Saida')
plt.xlabel('Frequência (k)')
plt.ylabel('Magnitude da FFT')
plt.tight_layout()
plt.show()

# Comparação de tempos de execução entre DFT, FFT implementada e FFT do Python
p = np.zeros(10)  # Vetor para armazenar potências de 2
t1 = np.zeros(10)  # Tempos de execução da DFT implementada
t2 = np.zeros(10)  # Tempos de execução da FFT implementada
t3 = np.zeros(10)  # Tempos de execução da FFT do Python

for i in range(len(p)):
    p[i] = 2 ** i     # Potência de 2 para o tamanho do sinal
    N = int(p[i])
    x = np.pad(np.linspace(1, 1, N), 0, 'constant')  # Testando o sinal com uma constante

    # DFT implementada
    start = time.time()
    Xd = DFT(x, N)
    end = time.time()
    t1[i] = end - start

    # FFT implementada
    start = time.time()
    Xf = FFT(x)
    end = time.time()
    t2[i] = end - start

    # FFT do Python
    start = time.time()
    X = fft(x, N)
    end = time.time()
    t3[i] = end - start    # Tempo de execução da FFT do Python

# Plotagem dos tempos de execução
plt.figure(figsize=(12, 6))
plt.plot(p, t1, label='DFT implementada')
plt.plot(p, t2, label='FFT implementada')
plt.plot(p, t3, label='FFT do python')
plt.xlabel('Valor de N')
plt.ylabel('Tempo de execução (s)')
plt.legend(fontsize=12)
plt.grid()
plt.show()