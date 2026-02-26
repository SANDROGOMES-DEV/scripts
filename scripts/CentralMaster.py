import subprocess
import sys
import os
import time
import shutil
import threading
import re
import hashlib
import webbrowser
import requests
import asyncio
import ssl
from pathlib import Path
from datetime import datetime

# =====================================================================
# 1. PROTEÇÕES DE AMBIENTE E REDE CORPORATIVA (CRÍTICO PARA O .EXE)
# =====================================================================
# Ignora bloqueios de certificado SSL para a biblioteca requests
requests.packages.urllib3.disable_warnings()
os.environ['CURL_CA_BUNDLE'] = ''

# PATCH GLOBAL: Força o Python inteiro a ignorar firewalls corporativos (Resolve o erro do Edge-TTS)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# Evita o erro "NoneType object has no attribute 'fileno'" no PyInstaller --windowed
if sys.stdout is None: sys.stdout = open(os.devnull, "w")
if sys.stderr is None: sys.stderr = open(os.devnull, "w")

def resource_path(relative_path):
    """ Retorna o caminho absoluto para recursos internos do executável """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# =====================================================================
# 2. AUTO-INSTALAÇÃO INTELIGENTE (ANTI-FORK BOMB)
# =====================================================================
def verificar_bibliotecas():
    if getattr(sys, 'frozen', False):
        return

    required = {
        "customtkinter": "customtkinter", 
        "psutil": "psutil",
        "speedtest": "speedtest-cli", 
        "yt_dlp": "yt-dlp",
        "static_ffmpeg": "static-ffmpeg", 
        "PyPDF2": "PyPDF2",
        "edge_tts": "edge-tts",
        "GPUtil": "gputil"
    }
    
    for imp, inst in required.items():
        try: 
            __import__(imp)
        except ImportError:
            try:
                subprocess.check_call([
                    sys.executable, "-m", "pip", "install", inst, 
                    "--trusted-host", "pypi.org", 
                    "--trusted-host", "files.pythonhosted.org"
                ])
            except Exception:
                pass 

verificar_bibliotecas()

# =====================================================================
# 3. IMPORTAÇÕES PÓS-VERIFICAÇÃO
# =====================================================================
import customtkinter as ctk
import psutil
import static_ffmpeg
import PyPDF2
import edge_tts

try:
    static_ffmpeg.add_paths()
    FFMPEG_PATH = shutil.which("ffmpeg")
except:
    FFMPEG_PATH = None

try: import yt_dlp
except: yt_dlp = None
try: import speedtest
except: speedtest = None
try: import GPUtil
except: GPUtil = None

# =====================================================================
# 4. CLASSE PRINCIPAL DO SISTEMA
# =====================================================================
class CentralMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CENTRAL MASTER V9.5 - FIREWALL BYPASS")
        self.geometry("1100x850")
        self.configure(fg_color="#000000")
        
        self.monitors = {}
        self.last_net_io = psutil.net_io_counters()
        self.last_time = datetime.now()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        self.setup_sidebar()
        self.setup_main_frame()
        self.show_dashboard()

    def setup_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#0A0A0A", border_color="#D4AF37", border_width=1)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        ctk.CTkLabel(self.sidebar, text="MASTER", font=("Impact", 42), text_color="#D4AF37").pack(pady=35)
        
        menu = [
            ("DASHBOARD", self.show_dashboard),
            ("LINKS TRABALHO", self.show_links),
            ("WI-FI HACKER", self.show_wifi_hacker),
            ("SPEEDTEST", self.show_speedtest),
            ("YOUTUBE DOWNLOAD", self.show_youtube),
            ("AUDIOBOOK NEURAL", self.show_pdf_audio),
            ("MANUTENÇÃO PC", self.show_maintenance),
            ("SEGURANÇA", self.show_security_native),
            ("ANDROID (ADB)", self.show_android),
            ("PROGRAMAS", self.show_programs),
            ("RECURSOS", self.show_resources)
        ]

        for text, cmd in menu:
            ctk.CTkButton(self.sidebar, text=text, command=cmd, fg_color="transparent", 
                          text_color="#D4AF37", hover_color="#1A1A1A", anchor="w", 
                          font=("Roboto", 13, "bold"), height=40).pack(fill="x", padx=15, pady=4)

    def setup_main_frame(self):
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#000000")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def clear_frame(self):
        self.monitors = {}
        for widget in self.main_frame.winfo_children(): widget.destroy()

    def safe_update(self, widget, **kwargs):
        try:
            if widget.winfo_exists(): widget.configure(**kwargs)
        except: pass

    def executar_cmd_silencioso(self, comando):
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        subprocess.run(comando, shell=True, startupinfo=startupinfo)

    # =====================================================================
    # MÓDULOS DA APLICAÇÃO
    # =====================================================================

    def show_dashboard(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="MONITORAMENTO GLOBAL", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=15)
        self.monitors = {
            "CPU": self.create_monitor("PROCESSADOR (CPU)"),
            "RAM": self.create_monitor("MEMÓRIA RAM"),
            "DISK": self.create_monitor("DISCO LOCAL (C:)"),
            "BATT": self.create_monitor("BATERIA", "#00FF00"),
            "NET": self.create_monitor("REDE (UPLOAD)", "#00BFFF"),
            "GPU": self.create_monitor("PLACA DE VÍDEO")
        }
        self.update_stats()

    def create_monitor(self, title, color="#D4AF37"):
        f = ctk.CTkFrame(self.main_frame, fg_color="#0A0A0A", border_color="#D4AF37", border_width=1)
        f.pack(fill="x", pady=5, padx=10)
        lbl = ctk.CTkLabel(f, text=f"{title}: --", text_color=color, font=("Roboto", 15, "bold"))
        lbl.pack(pady=5, padx=20, anchor="w")
        bar = ctk.CTkProgressBar(f, progress_color=color, fg_color="#1A1A1A", height=12)
        bar.set(0); bar.pack(fill="x", padx=20, pady=10)
        return {"lbl": lbl, "bar": bar}

    def update_stats(self):
        if not self.monitors: return
        try:
            cpu = psutil.cpu_percent(); self.monitors["CPU"]["lbl"].configure(text=f"CPU: {cpu}%"); self.monitors["CPU"]["bar"].set(cpu/100)
            ram = psutil.virtual_memory().percent; self.monitors["RAM"]["lbl"].configure(text=f"RAM: {ram}%"); self.monitors["RAM"]["bar"].set(ram/100)
            disk = psutil.disk_usage('/').percent; self.monitors["DISK"]["lbl"].configure(text=f"DISCO: {disk}%"); self.monitors["DISK"]["bar"].set(disk/100)
            
            batt = psutil.sensors_battery()
            if batt: 
                self.monitors["BATT"]["lbl"].configure(text=f"BATERIA: {batt.percent}%")
                self.monitors["BATT"]["bar"].set(batt.percent/100)
                
            if GPUtil and GPUtil.getGPUs():
                gpu = GPUtil.getGPUs()[0]
                self.monitors["GPU"]["lbl"].configure(text=f"GPU: {gpu.load*100:.0f}% | Temp: {gpu.temperature}°C")
                self.monitors["GPU"]["bar"].set(gpu.load)

            net = psutil.net_io_counters(); now = datetime.now(); dt = (now - self.last_time).total_seconds()
            if dt > 0:
                up = (net.bytes_sent - self.last_net_io.bytes_sent) / 1024 / dt
                self.monitors["NET"]["bar"].set(min(up/2000, 1.0)); self.monitors["NET"]["lbl"].configure(text=f"UP: {up:.1f} KB/s")
                self.last_net_io, self.last_time = net, now
        except: pass
        self.after(2000, self.update_stats)

    def show_youtube(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="YOUTUBE DOWNLOADER PRO", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        
        url_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Cole o link do vídeo aqui...", width=550)
        url_entry.pack(pady=10)
        
        tipo_var = ctk.StringVar(value="video")
        opt_f = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        opt_f.pack(pady=5)
        ctk.CTkRadioButton(opt_f, text="MP4 Vídeo", variable=tipo_var, value="video", text_color="#D4AF37").pack(side="left", padx=20)
        ctk.CTkRadioButton(opt_f, text="MP3 Áudio", variable=tipo_var, value="audio", text_color="#D4AF37").pack(side="left", padx=20)
        
        progress_bar = ctk.CTkProgressBar(self.main_frame, width=550, progress_color="#D4AF37")
        progress_bar.set(0); progress_bar.pack(pady=(20, 5))
        
        status_lbl = ctk.CTkLabel(self.main_frame, text="Aguardando link...", text_color="gray", font=("Consolas", 12))
        status_lbl.pack(pady=5)

        def baixar():
            link = url_entry.get()
            if not link: return
            self.safe_update(status_lbl, text="Iniciando...", text_color="#D4AF37")
            
            def run():
                try:
                    path = resource_path("Downloads")
                    if not os.path.exists(path): os.makedirs(path)

                    def hook(d):
                        if d['status'] == 'downloading':
                            p = d.get('downloaded_bytes', 0) / (d.get('total_bytes') or d.get('total_bytes_estimate', 1))
                            speed = d.get('speed', 0)
                            speed_mb = f"{speed/1024/1024:.1f} MB/s" if speed else "0 MB/s"
                            msg = f"Baixando: {p*100:.1f}% | Vel: {speed_mb}"
                            self.safe_update(status_lbl, text=msg)
                            self.safe_update(progress_bar, progress=p)
                        elif d['status'] == 'finished':
                            self.safe_update(status_lbl, text="Convertendo mídia (Aguarde)...", text_color="#00BFFF")

                    opts = {
                        'outtmpl': f'{path}/%(title)s.%(ext)s', 
                        'quiet': True,
                        'nocheckcertificate': True, 
                        'ffmpeg_location': FFMPEG_PATH, 
                        'progress_hooks': [hook], 
                        'noplaylist': True
                    }
                    if tipo_var.get() == "audio":
                        opts.update({'format': 'bestaudio/best', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]})
                    else:
                        opts.update({'format': 'bestvideo+bestaudio/best', 'merge_output_format': 'mp4'})

                    with yt_dlp.YoutubeDL(opts) as ydl: ydl.download([link])
                    self.safe_update(status_lbl, text="Sucesso! Arquivo salvo em Downloads.", text_color="#00FF00")
                    os.startfile(path)
                except Exception as e: 
                    self.safe_update(status_lbl, text=f"Erro: {e}", text_color="red")

            threading.Thread(target=run, daemon=True).start()

        ctk.CTkButton(self.main_frame, text="BAIXAR AGORA", command=baixar, fg_color="red", text_color="white", height=45).pack(pady=15)

    def show_pdf_audio(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="AUDIOBOOK PRO (VOZ NEURAL NATIVA)", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        lbl = ctk.CTkLabel(self.main_frame, text="Selecione um PDF. O Firewall foi neutralizado.", text_color="gray")
        lbl.pack(pady=10)
        
        voz_escolhida = "pt-BR-FranciscaNeural" 
        
        def conv():
            pdf_path = ctk.filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
            if not pdf_path: return
            
            def run():
                out_mp3 = pdf_path.replace(".pdf", ".mp3")
                
                try:
                    self.safe_update(lbl, text="1/3: Extraindo texto do PDF...", text_color="#D4AF37")
                    text = "".join([p.extract_text() for p in PyPDF2.PdfReader(pdf_path).pages])
                    
                    self.safe_update(lbl, text="2/3: Conectando à IA Neural (Bypass Ativo)...", text_color="#00BFFF")
                    
                    async def gerar_audio():
                        communicate = edge_tts.Communicate(text, voz_escolhida)
                        await communicate.save(out_mp3)
                    
                    asyncio.run(gerar_audio())
                        
                    self.safe_update(lbl, text="3/3: Audiobook gerado com sucesso!", text_color="#00FF00")
                    os.startfile(out_mp3)
                    
                except Exception as e:
                    self.safe_update(lbl, text=f"Erro na conversão: {e}", text_color="red")

            threading.Thread(target=run, daemon=True).start()
        
        ctk.CTkButton(self.main_frame, text="SELECIONAR E CONVERTER", command=conv, fg_color="#D4AF37", text_color="black").pack(pady=20)

    def show_wifi_hacker(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="REVELADOR WI-FI", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        box = ctk.CTkTextbox(self.main_frame, width=700, height=400, fg_color="#0A0A0A", text_color="#00FF00", font=("Consolas", 13))
        box.pack(pady=10)
        def scan():
            box.delete("0.0", "end")
            try:
                cmd = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'], encoding='cp850', errors='ignore')
                for p in re.findall(r"Usu.rios\s*:\s(.*)", cmd):
                    p = p.strip()
                    res = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', p, 'key=clear'], encoding='cp850', errors='ignore')
                    pwd = re.search(r"Chave\s*:\s(.*)", res) or re.search(r"Content\s*:\s(.*)", res)
                    box.insert("end", f"SSID: {p:<20} | SENHA: {pwd.group(1) if pwd else '---'}\n")
            except: box.insert("end", "Erro ao escanear redes.")
        ctk.CTkButton(self.main_frame, text="REVELAR SENHAS", command=scan, fg_color="#D4AF37", text_color="black").pack(pady=10)

    def show_speedtest(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="SPEEDTEST PRO", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        lbl = ctk.CTkLabel(self.main_frame, text="Aguardando...", font=("Roboto", 18), text_color="gray"); lbl.pack(pady=30)
        def run():
            if not speedtest: return
            self.safe_update(lbl, text="Testando...", text_color="#D4AF37")
            try:
                st = speedtest.Speedtest(); st.get_best_server()
                self.safe_update(lbl, text=f"Download: {st.download()/1e6:.1f} Mbps\nUpload: {st.upload()/1e6:.1f} Mbps\nPing: {st.results.ping:.0f} ms", text_color="#00FF00")
            except: self.safe_update(lbl, text="Erro de rede.", text_color="red")
        ctk.CTkButton(self.main_frame, text="INICIAR TESTE", command=lambda: threading.Thread(target=run, daemon=True).start(), fg_color="#D4AF37", text_color="black").pack()

    def show_maintenance(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="MANUTENÇÃO", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        for n, c in [("LIMPAR TEMP", 'del /q /f /s "%temp%\\*.*"'), ("SFC SCAN", "sfc /scannow")]:
            ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: self.executar_cmd_silencioso(x), fg_color="#1A1A1A", border_width=1, border_color="#D4AF37").pack(pady=5, fill="x", padx=100)
        ctk.CTkButton(self.main_frame, text="CANCELAR DESLIGAMENTO", command=lambda: self.executar_cmd_silencioso("shutdown -a"), fg_color="red", text_color="white").pack(pady=20)

    def show_security_native(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="VERIFICADOR DE VAZAMENTOS", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        e = ctk.CTkEntry(self.main_frame, show="*", placeholder_text="Digite a senha..."); e.pack(pady=20, fill="x", padx=100)
        def check():
            h = hashlib.sha1(e.get().encode()).hexdigest().upper()
            try:
                r = requests.get(f"https://api.pwnedpasswords.com/range/{h[:5]}", verify=False)
                msg = "ALERTA: Senha Vazada!" if h[5:] in r.text else "SEGURO: Senha OK."
                ctk.CTkLabel(self.main_frame, text=msg, text_color="red" if "Vazada" in msg else "green", font=("Roboto", 16, "bold")).pack(pady=10)
            except: pass
        ctk.CTkButton(self.main_frame, text="VERIFICAR", command=check, fg_color="#D4AF37", text_color="black").pack()

    def show_links(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="LINKS ÚTEIS", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        for n, u in [("WFM", "https://portalwfm.hapvida.com.br/"), ("Teams", "https://teams.microsoft.com/v2/"), ("GitHub", "https://github.com")]:
             ctk.CTkButton(self.main_frame, text=n, command=lambda x=u: webbrowser.open(x), fg_color="#1A1A1A", border_width=1, border_color="#D4AF37").pack(pady=5, fill="x", padx=100)

    def show_android(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="ADB ANDROID", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        for n, c in [("Listar ADB", "adb devices"), ("Reiniciar ADB", "adb reboot")]:
             ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: self.executar_cmd_silencioso(x), fg_color="#1A1A1A", border_width=1, border_color="#D4AF37").pack(pady=5, fill="x", padx=100)

    def show_programs(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="LANÇADOR DE PROGRAMAS", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        for n, c in [("VS Code", "code ."), ("Calculadora", "calc"), ("Teclado Virtual", "osk")]:
             ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: self.executar_cmd_silencioso(x), fg_color="#1A1A1A", border_width=1, border_color="#D4AF37").pack(pady=5, fill="x", padx=100)

    def show_resources(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="RECURSOS LOCAIS", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        recursos = [
            ("BUSCA PRESTADOR", "busca_de_prestador/index.html"), 
            ("NOTAS PROCEDIMENTOS", "procedimentos.txt"), 
            ("SISTEMA SIGO", "http://sistemas.hapvida.com.br/planos")
        ]
        for n, p in recursos:
            cmd = lambda x=p: webbrowser.open(x) if "http" in x else os.startfile(resource_path(x))
            ctk.CTkButton(self.main_frame, text=n, command=cmd, fg_color="#1A1A1A", border_width=1, border_color="#D4AF37").pack(pady=5, fill="x", padx=100)

if __name__ == "__main__":
    app = CentralMaster()
    app.mainloop()
