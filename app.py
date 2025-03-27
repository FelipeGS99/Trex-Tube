from flask import Flask, render_template, request, flash, send_file
import validators  # Biblioteca para validar URL
import yt_dlp  # Biblioteca para download de vídeos
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretkey'  # Chave secreta para usar flash messages
app.config['UPLOAD_FOLDER'] = 'downloads'  # Pasta para armazenar os downloads
COOKIES_PATH = "cookies.txt"

# Certifique-se de que a pasta de downloads exista
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        url = request.form.get("url")
        format = request.form.get("format")
        
        # Validar URL
        if not validators.url(url):
            flash("URL inválida, por favor insira uma URL válida.", "error")
            return render_template("index.html")
        
        try:
            # Configurações do yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best' if format == 'mp3' else 'bestvideo+bestaudio/best',
                'outtmpl': os.path.join(app.config['UPLOAD_FOLDER'], '%(title)s.%(ext)s'),
                "cookiefile": COOKIES_PATH
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info_dict)
            
            # Enviar o arquivo para o usuário
            return send_file(filename, as_attachment=True)
        
        except Exception as e:
            flash(f"Erro ao tentar baixar: {str(e)}", "error")
            return render_template("index.html")
        
    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)