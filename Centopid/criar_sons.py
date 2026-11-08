
import os
import wave
import math
import struct

os.makedirs("sons", exist_ok=True)

def criar_som(nome, frequencias, duracao):
    taxa = 44100
    amostras = []

    for i in range(int(taxa * duracao)):
        tempo = i / taxa
        progresso = i / (taxa * duracao)

        indice = min(int(progresso * len(frequencias)), len(frequencias) - 1)
        frequencia = frequencias[indice]

        volume = 0.4 * (1 - progresso)
        valor = volume * math.sin(2 * math.pi * frequencia * tempo)

        amostras.append(int(valor * 32767))

    with wave.open(f"sons/{nome}.wav", "w") as arquivo:
        arquivo.setnchannels(1)
        arquivo.setsampwidth(2)
        arquivo.setframerate(taxa)
        arquivo.writeframes(
            b"".join(struct.pack("<h", amostra) for amostra in amostras)
        )

criar_som("comida", [500, 700, 900], 0.2)
criar_som("fim", [500, 350, 200], 0.8)

print("Sons criados com sucesso!")
