from gtts import gTTS
import os
import csv
import re


from pydub import AudioSegment

async def text_to_audio(texto, arquivo_saida):
    # Cria um objeto gTTS com o texto fornecido
    tts = gTTS(text=texto, lang='pt', tld='com.br', slow=False)

    # Salva o arquivo de áudio temporário
    arquivo_temp = "temp_audio.mp3"
    tts.save(arquivo_temp)

    # Carrega o arquivo de áudio temporário com o pydub
    audio = AudioSegment.from_mp3(arquivo_temp)

    # Altera a velocidade do áudio (1.5x mais rápido)
    audio = audio.speedup(playback_speed=1.25)

    # Exporta o áudio modificado para um arquivo MP3
    audio.export(arquivo_saida, format="mp3")

    # Remove o arquivo de áudio temporário
    os.remove(arquivo_temp)

async def get_movie(mensagem):
    padrao = r'\b[A-Z][a-zA-Z\'~\d]+\b(?:\s+[A-Z][a-zA-Z\'~\d]+\b)*(?:\s+\d+)?[.?,]|$'

    correspondencias = re.findall(padrao, mensagem)

    filmes = []

    for match in correspondencias:
        # Remove pontuação do final do nome do filme
        filme = re.sub(r'[.?,]', '', match)
        filmes.append(filme.strip())
    
    return filmes[0]

async def get_itens(mensagem):
    mensagem = mensagem.replace('*', '')
    titulos = re.findall(r'(?:Nome do filme|Nome da série|Nome da música): (.+)', mensagem)
    return titulos

async def get_itens_bold(mensagem):
    padrao = r"\*\*(.*?)\*\*"
    nomes = re.findall(padrao, mensagem)
    return nomes

async def verifica_itens(string):
    itens = ['filme', 'filmes', 'série', 'séries', 'música', 'músicas']
    return any(item in string for item in itens)