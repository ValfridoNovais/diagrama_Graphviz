import yt_dlp
import os
from datetime import datetime
import openai
import re

# Configuração
openai.api_key = 'sua-chave'  # Substitua pela sua chave OpenAI

def baixar_audio(url):
    """Baixa áudio com nome temporário"""
    try:
        caminho_salvar = os.path.join(os.getcwd(), 'videos')
        os.makedirs(caminho_salvar, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(caminho_salvar, 'temp_audio'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            caminho_temp = os.path.join(caminho_salvar, 'temp_audio.mp3')
            return caminho_temp, info.get('title', 'audio')
    
    except Exception as e:
        print(f"Erro no download: {str(e)}")
        return None, None

def transformar_voz(arquivo_entrada, titulo):
    """Usa OpenAI para transformar em voz feminina"""
    try:
        data_hora = datetime.now().strftime("_%Y-%m-%d-%H-%M")
        nome_final = re.sub(r'[^\w\-_\. ]', '', titulo) + data_hora + "_feminina.mp3"
        caminho_final = os.path.join(os.path.dirname(arquivo_entrada), nome_final)

        with open(arquivo_entrada, "rb") as audio_file:
            resposta = openai.Audio.create(
                file=audio_file,
                model="whisper-1",
                voice="nova",  # Voz feminina
                response_format="mp3"
            )
        
        with open(caminho_final, "wb") as f:
            f.write(resposta.content)
        
        print(f"Voz feminina gerada: {nome_final}")
        return caminho_final
    
    except Exception as e:
        print(f"Erro na transformação: {str(e)}")
        return None

if __name__ == "__main__":
    url = input("URL do vídeo: ")
    audio_path, titulo = baixar_audio(url)
    
    if audio_path:
        transformar_voz(audio_path, titulo)
        os.remove(audio_path)  # Remove o temporário