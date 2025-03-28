import yt_dlp  # Note o underscore (_) em vez do hífen (-)
import os

def baixar_video(url, caminho_salvar='./'):
    try:
        ydl_opts = {
            'outtmpl': os.path.join(caminho_salvar, '%(title)s.%(ext)s'),
            'quiet': False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Título: {info.get('title', 'Desconhecido')}")
            print("Iniciando download...")
            ydl.download([url])
            print("Download concluído!")

    except Exception as e:
        print(f"Erro: {str(e)}")

if __name__ == "__main__":
    url = input("Cole a URL do vídeo do YouTube: ")
    caminho = input("Digite o caminho para salvar (deixe em branco para diretório atual): ") or './'
    baixar_video(url, caminho)