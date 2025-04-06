import yt_dlp
import os
from datetime import datetime
import numpy as np
import librosa
from pydub import AudioSegment
import soundfile as sf
import re

def baixar_audio(url, caminho_salvar=None):
    """Baixa o áudio com nome temporário fixo"""
    try:
        if caminho_salvar is None:
            caminho_salvar = os.path.join(os.getcwd(), 'videos')
        
        os.makedirs(caminho_salvar, exist_ok=True)
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(caminho_salvar, 'processar_audio'),  # Nome fixo
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'wav',
            }],
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            caminho_temp = os.path.join(caminho_salvar, 'processar_audio.wav')
            
            if os.path.exists(caminho_temp):
                print("\nÁudio baixado temporariamente como 'processar_audio.wav'")
                return caminho_temp, info.get('title', 'audio_baixado')
            else:
                raise FileNotFoundError("Arquivo temporário não foi criado")

    except Exception as e:
        print(f"\nErro ao baixar áudio: {str(e)}")
        return None, None

def modificar_voz(caminho_audio, titulo_original, efeito='deep'):
    """Processa e só depois renomeia com nome final"""
    try:
        if not caminho_audio or not os.path.exists(caminho_audio):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_audio}")
        
        # Processa o áudio
        y, sr = librosa.load(caminho_audio, sr=None)
        
        if efeito == 'deep':
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=-5)
            y = librosa.effects.time_stretch(y, rate=0.8)
        elif efeito == 'fast':
            y = librosa.effects.pitch_shift(y, sr=sr, n_steps=4)
            y = librosa.effects.time_stretch(y, rate=1.3)
        elif efeito == 'robot':
            y_ft = np.fft.fft(y)
            y_ft[::10] = 0
            y = np.fft.ifft(y_ft).real

        # Define nome final
        data_hora = datetime.now().strftime("_%Y-%m-%d-%H-%M")
        titulo_seguro = re.sub(r'[^\w\-_\. ]', '', titulo_original)
        nome_final = f"{titulo_seguro}{data_hora}_{efeito}.mp3"
        caminho_final = os.path.join(os.path.dirname(caminho_audio), nome_final)

        # Salva temporariamente
        temp_path = os.path.join(os.path.dirname(caminho_audio), f"temp_{efeito}.wav")
        sf.write(temp_path, y, sr)
        
        # Converte e renomeia
        AudioSegment.from_wav(temp_path).export(caminho_final, format='mp3')
        os.remove(temp_path)  # Remove o arquivo WAV temporário
        
        print(f"\n✅ Áudio modificado salvo como: {nome_final}")
        return caminho_final

    except Exception as e:
        print(f"\n❌ Erro ao processar áudio: {str(e)}")
        return None

def main():
    print("=== MODIFICADOR DE VOZ ===")
    url = input("\nCole a URL do YouTube: ").strip()
    
    # Baixa com nome temporário
    audio_path, titulo = baixar_audio(url)
    
    if audio_path:
        while True:
            print("\nEfeitos de voz:")
            print("1 - Voz Profunda")
            print("2 - Voz Acelerada")
            print("3 - Efeito Robótico")
            print("4 - Sair")
            
            escolha = input("Escolha (1-4): ").strip()
            
            if escolha in ['1', '2', '3']:
                efeito = ['deep', 'fast', 'robot'][int(escolha)-1]
                modificar_voz(audio_path, titulo, efeito)
            elif escolha == '4':
                # Remove o arquivo temporário ao sair
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                print("\nSaindo...")
                break
            else:
                print("\nOpção inválida!")

if __name__ == "__main__":
    main()