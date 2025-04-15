import yt_dlp
import os
import whisper
from pathlib import Path
import time
import sys
import threading
from tqdm import tqdm
from datetime import datetime

class Transcriber:
    def __init__(self):
        self.running = True
        self.progress = 0

    def criar_pastas_se_nao_existirem(self):
        pastas = ["Arquivo_doc", "Arquivo_pdf", "Arquivo_txt", "Audios"]
        for pasta in pastas:
            os.makedirs(pasta, exist_ok=True)

    def configurar_cache_ytdlp(self):
        cache_dir = os.path.join(os.getcwd(), "yt_dlp_cache")
        os.makedirs(cache_dir, exist_ok=True)
        return {
            'cachedir': cache_dir,
            'no_warnings': True
        }

    def baixar_audio(self, url, pasta_salvar='Audios'):
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'wav',
                    'preferredquality': '192',
                }],
                'outtmpl': os.path.join(pasta_salvar, '%(title)s.%(ext)s'),
                'quiet': False,
                'keepvideo': False,
                'extract_audio': True,
                **self.configurar_cache_ytdlp()
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'audio_temp')
                
                time.sleep(2)
                
                arquivo_wav = os.path.join(pasta_salvar, f"{titulo}.wav")
                
                if not os.path.exists(arquivo_wav):
                    for arquivo in os.listdir(pasta_salvar):
                        if arquivo.endswith('.wav'):
                            arquivo_wav = os.path.join(pasta_salvar, arquivo)
                            break
                
                if os.path.exists(arquivo_wav):
                    print(f"\nÁudio baixado com sucesso: {arquivo_wav}")
                    return arquivo_wav, titulo
                else:
                    print("\n❌ ERRO: Não foi possível encontrar o arquivo de áudio baixado")
                    return None, None

        except Exception as e:
            print(f"\nErro ao baixar áudio: {str(e)}")
            return None, None

    def monitorar_progresso(self, duration):
        with tqdm(total=duration, desc="Transcrevendo", unit="seg") as pbar:
            while self.running and self.progress < duration:
                pbar.n = self.progress
                pbar.refresh()
                time.sleep(1)
            
            if self.progress >= duration:
                pbar.n = duration
                pbar.refresh()

    def transcrever_audio(self, caminho_audio, modelo='small', titulo=None):
        try:
            if not caminho_audio or not os.path.exists(caminho_audio):
                print("❌ Arquivo de áudio não encontrado para transcrição")
                return None
            
            print(f"\nCarregando modelo Whisper ({modelo})...")
            model = whisper.load_model(modelo)
            
            # Obter duração do áudio para a barra de progresso
            audio = whisper.load_audio(caminho_audio)
            duration = len(audio) / whisper.audio.SAMPLE_RATE  # Duração em segundos
            
            # Iniciar thread para monitorar progresso
            self.progress = 0
            progress_thread = threading.Thread(target=self.monitorar_progresso, args=(int(duration),))
            progress_thread.start()
            
            print("\nTranscrevendo áudio... (Pressione Ctrl+C para cancelar)")
            
            # Atualizar progresso periodicamente
            def update_progress():
                while self.running and self.progress < duration:
                    self.progress += 1
                    time.sleep(1)
            
            progress_updater = threading.Thread(target=update_progress)
            progress_updater.start()
            
            # Realizar transcrição
            resultado = model.transcribe(caminho_audio)
            
            # Finalizar threads
            self.running = False
            progress_thread.join()
            progress_updater.join()
            
            if titulo is None:
                titulo = Path(caminho_audio).stem
            
            self.salvar_transcricao(resultado['text'], titulo)
            
            return resultado['text']
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Transcrição cancelada pelo usuário!")
            self.running = False
            return None
        except Exception as e:
            print(f"\nErro ao transcrever: {str(e)}")
            self.running = False
            return None

    def salvar_transcricao(self, texto, titulo):
        try:
            # Obter data e hora atual no formato YYYY_MM_DD_HH_MM
            data_hora = datetime.now().strftime("%Y_%m_%d_%H_%M")
            
            # Remover caracteres inválidos para nome de arquivo e adicionar data/hora
            titulo_seguro = "".join(c for c in titulo if c.isalnum() or c in (' ', '_')).rstrip()
            nome_base = f"{titulo_seguro}_{data_hora}"
            
            # Salvar como TXT
            caminho_txt = os.path.join("Arquivo_txt", f"{nome_base}.txt")
            with open(caminho_txt, 'w', encoding='utf-8') as f:
                f.write(texto)
            print(f"\nTranscrição salva em TXT: {caminho_txt}")
            
            # Salvar como DOC
            caminho_doc = os.path.join("Arquivo_doc", f"{nome_base}.doc")
            with open(caminho_doc, 'w', encoding='utf-8') as f:
                f.write(texto)
            print(f"Transcrição salva em DOC: {caminho_doc}")
            
            # Salvar como PDF
            try:
                from fpdf import FPDF
                caminho_pdf = os.path.join("Arquivo_pdf", f"{nome_base}.pdf")
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, txt=texto)
                pdf.output(caminho_pdf)
                print(f"Transcrição salva em PDF: {caminho_pdf}")
            except ImportError:
                print("Aviso: Biblioteca FPDF não instalada. PDF não será gerado.")
                
        except Exception as e:
            print(f"\nErro ao salvar transcrição: {str(e)}")

def main():
    transcriber = Transcriber()
    print("\n=== Transcrição de Vídeos ===")
    transcriber.criar_pastas_se_nao_existirem()
    
    try:
        url = input("Cole a URL do vídeo ou caminho local: ")
        pasta_salvar = input("Digite a pasta para salvar (Enter para 'Audios'): ") or 'Audios'
        modelo = input("Escolha o modelo Whisper (tiny/base/small/medium/large): ") or 'small'
        
        print("\nBaixando áudio da URL...")
        caminho_audio, titulo = transcriber.baixar_audio(url, pasta_salvar)
        
        if caminho_audio and os.path.exists(caminho_audio):
            transcricao = transcriber.transcrever_audio(caminho_audio, modelo, titulo)
            
            if transcricao:
                print("\n✅ Transcrição concluída com sucesso!")
            else:
                print("\n❌ Falha na transcrição.")
        else:
            print("\n❌ Falha ao baixar o áudio.")
    
    except KeyboardInterrupt:
        print("\n\n⚠️ Programa encerrado pelo usuário!")
        transcriber.running = False
        sys.exit(0)

if __name__ == "__main__":
    main()