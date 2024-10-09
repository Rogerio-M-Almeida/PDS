import numpy as np
import scipy.io.wavfile as wav
import serial
import matplotlib.pyplot as plt  # Importação do Matplotlib
import scipy.signal as signal

#engenheiro, foi feito pra resolve problema,
# engenheiro que cria problema não serve pra porra nenhuma.

#audio ja filtro por proma externo.



# Função para fazer a FFT do áudio
def process_audio(file_path):
    # Lê o arquivo de áudio
    sample_rate, data = wav.read(file_path)

    # Se o áudio for estéreo, usa apenas um canal
    if len(data.shape) > 1:
       # data = data[:, 0]
        data = np.mean(data, axis=1)  # Média dos canais



    # Aplica a FFT
    fft_data = np.fft.fft(data)
    freqs = np.fft.fftfreq(len(fft_data), 1 / sample_rate)

    # Filtra apenas as frequências positivas
    freqs = freqs[:len(freqs) // 2]
    fft_data = np.abs(fft_data[:len(fft_data) // 2])

    # Filtro passa-baixa ( 300 Hz) não deu certo de tal sorte que o audio ja foi filtrado
    cutoff_freq = 300  # Frequência de corte do filtro
    nyquist = 0.5 * sample_rate
    normal_cutoff = cutoff_freq / nyquist
    b, a = signal.butter(4, normal_cutoff, btype='low')  # Filtro de Butterworth de 4ª ordem
    filtered_fft_data = signal.filtfilt(b, a, fft_data)  # Aplica o filtro

    # Identifica a frequência dominante do espectro filtrado
    dominant_freq = freqs[np.argmax(filtered_fft_data)]


    # Plota o espectro de frequências
    plt.plot(freqs, fft_data)
    plt.xlabel('Frequência (Hz)')
    plt.ylabel('Magnitude')
    plt.title('Espectro de Frequências')
    plt.xlim(0, 1000)  # Ajuste conforme necessário
    plt.show()

    return dominant_freq


# Função para identificar gênero com base na frequência dominante
def identify_gender(freq):
    if 85 <= freq <= 180:  # Faixa de voz masculina
        return "male"
    elif 181 <= freq <= 300:  # Faixa de voz feminina
        return "female"
    else:
        return "unknown"

import time

# Envia sinal para o Arduino
def send_to_arduino(gender):
    # Configuração da comunicação serial
    arduino = serial.Serial('COM6', 9600)  # Modifique a porta conforme necessário
    time.sleep(2)  # Aguarde 2 segundos para estabelecer a conexão


    if gender == "male":

        print("Enviando sinal de gênero masculino")

        arduino.write(b'1')  # Sinal para voz masculina
    elif gender == "female":

        print("Enviando sinal de gênero masculino")

        arduino.write(b'2')  # Sinal para voz feminina
    else:
        print("Enviando sinal indefinido")

        arduino.write(b'3')  # Sinal para indefinido

    arduino.close()  # Fecha a porta serial após enviar o dado

# Processo completo
def main(audio_file):
    dominant_freq = process_audio(audio_file)
    gender = identify_gender(dominant_freq)
    send_to_arduino(gender)
    print(f"Frequência dominante: {dominant_freq} Hz")
    print(f"Gênero identificado: {gender}")


# Chame o código com o caminho do arquivo de áudio
main(r"C:\Users\Acer\Downloads\audiofema.wav")

