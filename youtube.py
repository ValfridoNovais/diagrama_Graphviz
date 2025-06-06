import yt_dlp
import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog

def baixar_video(url, caminho_salvar=None):
    try:
        # Define o caminho padrão como uma pasta 'videos' no diretório atual
        if caminho_salvar is None:
            caminho_salvar = os.path.join(os.getcwd(), 'videos')
        
        # Cria a pasta se não existir
        os.makedirs(caminho_salvar, exist_ok=True)
        
        # Obtém a data e hora atual no formato especificado
        data_hora = datetime.now().strftime("_%Y-%m-%d-%H-%M")
        
        ydl_opts = {
            # Adiciona a data e hora ao nome do arquivo
            'outtmpl': os.path.join(caminho_salvar, f'%(title)s{data_hora}.%(ext)s'),
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"\nTítulo: {info.get('title', 'Desconhecido')}")
            print(f"Salvando em: {os.path.abspath(caminho_salvar)}")
            print("Iniciando download...")
            ydl.download([url])
            print("\nDownload concluído com sucesso!")

    except Exception as e:
        print(f"\nErro: {str(e)}")

def selecionar_pasta():
    root = tk.Tk()
    root.withdraw()  # Esconde a janela principal do tkinter
    caminho = filedialog.askdirectory(title="Selecione a pasta para salvar o vídeo")
    return caminho if caminho else None  # Retorna None se o usuário cancelar

if __name__ == "__main__":
    url = input("Cole a URL do vídeo do YouTube: ")
    print("\nSelecione a pasta para salvar o vídeo...")
    caminho = selecionar_pasta()
    
    # Se o usuário não selecionar uma pasta, usa None para acionar o padrão
    baixar_video(url, caminho)