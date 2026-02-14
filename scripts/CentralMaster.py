import subprocess
import sys
import os
import time
import shutil
import threading
import re
from pathlib import Path
from datetime import datetime


# --- 1. SISTEMA DE AUTO-INSTALAÇÃO UNIVERSAL ---
def verificar_bibliotecas():
    """
    Verifica se o ambiente tem tudo o que precisa.
    Se faltar algo, instala automaticamente sem pedir permissão.
    """
    required = {
        "customtkinter": "customtkinter",
        "psutil": "psutil",
        "speedtest": "speedtest-cli",
        "yt_dlp": "yt-dlp",
        "GPUtil": "gputil",
        "requests": "requests",
        "static_ffmpeg": "static-ffmpeg",  # Correção de Vídeo/Áudio
        "PyPDF2": "PyPDF2",  # Leitor de PDF
        "pyttsx3": "pyttsx3",  # Sintetizador de Voz
        "PIL": "pillow",
    }

    faltantes = []
    print("--- [CENTRAL MASTER] Verificando integridade do sistema... ---")

    for import_name, install_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            faltantes.append(install_name)

    if faltantes:
        print(f"--- [AUTO-INSTALL] Baixando recursos: {', '.join(faltantes)} ---")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + faltantes)
            print("--- [SUCESSO] Ambiente configurado! Iniciando aplicação... ---")
            time.sleep(2)
        except Exception as e:
            print(f"[ERRO CRÍTICO] Falha na instalação: {e}")
            input("Pressione Enter para sair...")
            sys.exit()


# Executa a verificação antes de carregar o resto
verificar_bibliotecas()

# --- 2. IMPORTAÇÕES PRINCIPAIS ---
import customtkinter as ctk
import psutil
import webbrowser
import requests
import hashlib
import static_ffmpeg  # O "milagre" do vídeo
import PyPDF2
import pyttsx3

# Configuração do Driver de Vídeo (FFmpeg)
print("[SYSTEM] Carregando Codecs de Áudio e Vídeo...")
static_ffmpeg.add_paths()
FFMPEG_PATH = shutil.which("ffmpeg")  # Localiza o executável baixado automaticamente

# Importações Protegidas (Para não quebrar se o hardware não suportar)
try:
    import GPUtil
except:
    GPUtil = None
try:
    import speedtest
except:
    speedtest = None
try:
    import yt_dlp
except:
    yt_dlp = None


# --- 3. CLASSE PRINCIPAL ---
class CentralMaster(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configurações da Janela
        self.title("CENTRAL MASTER V6.0 - ULTIMATE")
        self.geometry("1100x850")
        self.configure(fg_color="#000000")  # Tema Black
        self.base_path = Path(__file__).parent

        # Variáveis Globais
        self.monitors = {}
        self.last_net_io = psutil.net_io_counters()
        self.last_time = datetime.now()

        # Layout (Grid 2 colunas)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_frame()

        # Inicia na Dashboard
        self.show_dashboard()

    def setup_sidebar(self):
        """Menu Lateral Dourado"""
        self.sidebar = ctk.CTkFrame(
            self,
            width=240,
            corner_radius=0,
            fg_color="#0A0A0A",
            border_color="#D4AF37",
            border_width=1,
        )
        self.sidebar.grid(row=0, column=0, sticky="nsew")

        ctk.CTkLabel(
            self.sidebar, text="MASTER", font=("Impact", 38), text_color="#D4AF37"
        ).pack(pady=30)
        ctk.CTkLabel(
            self.sidebar, text="V6.0 FULL", font=("Roboto", 10), text_color="gray"
        ).pack(pady=(0, 20))

        # Lista de Módulos
        menu = [
            ("DASHBOARD", self.show_dashboard),
            ("LINKS TRABALHO", self.show_links),
            ("WI-FI HACKER", self.show_wifi_hacker),
            ("SPEEDTEST", self.show_speedtest),
            ("YOUTUBE DOWNLOAD", self.show_youtube),
            ("CRIAR AUDIOBOOK", self.show_pdf_audio),  # Novo!
            ("MANUTENÇÃO PC", self.show_maintenance),
            ("SEGURANÇA", self.show_security_native),
            ("ANDROID (ADB)", self.show_android),
            ("PROGRAMAS", self.show_programs),
            ("RECURSOS", self.show_resources),
        ]

        for text, cmd in menu:
            ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd,
                fg_color="transparent",
                text_color="#D4AF37",
                hover_color="#1A1A1A",
                anchor="w",
                font=("Roboto", 13, "bold"),
                height=40,
            ).pack(fill="x", padx=15, pady=5)

    def setup_main_frame(self):
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#000000")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def clear_frame(self):
        """Limpa a tela e reseta variáveis de monitoramento"""
        self.monitors = {}
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def executar_comando_silencioso(self, comando, titulo_botao):
        """Executa comandos do CMD sem abrir janelas pretas"""
        log_window = ctk.CTkToplevel(self)
        log_window.title(f"Executando: {titulo_botao}")
        log_window.geometry("600x400")
        log_window.configure(fg_color="#000000")

        textbox = ctk.CTkTextbox(
            log_window, fg_color="#0A0A0A", text_color="#D4AF37", font=("Consolas", 12)
        )
        textbox.pack(fill="both", expand=True, padx=10, pady=10)

        def run():
            try:
                # Configuração para ocultar janela do CMD
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW

                process = subprocess.Popen(
                    comando,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    startupinfo=startupinfo,
                    encoding="cp850",
                    errors="ignore",
                )
                stdout, stderr = process.communicate()

                textbox.insert("end", stdout)
                if stderr:
                    textbox.insert("end", f"\n[INFO/ERRO]:\n{stderr}")
                textbox.insert("end", "\n--- PROCESSO CONCLUÍDO ---\n")
            except Exception as e:
                textbox.insert("end", f"\nErro Crítico: {e}")

        threading.Thread(target=run).start()

    # =========================================================================
    # MODULO 1: DASHBOARD (Monitoramento)
    # =========================================================================
    def show_dashboard(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="MONITORAMENTO GLOBAL",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=15)

        self.monitors = {
            "CPU": self.create_monitor("PROCESSADOR (CPU)"),
            "GPU": self.create_monitor("PLACA DE VÍDEO (GPU)"),
            "RAM": self.create_monitor("MEMÓRIA RAM"),
            "DISK": self.create_monitor("ARMAZENAMENTO (C:)"),
            "BATT": self.create_monitor("BATERIA", "#00FF00"),
            "NET": self.create_monitor("REDE (UPLOAD)", "#00BFFF"),
        }
        self.update_stats()

    def create_monitor(self, title, color="#D4AF37"):
        frame = ctk.CTkFrame(
            self.main_frame, fg_color="#0A0A0A", border_color="#D4AF37", border_width=1
        )
        frame.pack(fill="x", pady=8, padx=10)
        lbl = ctk.CTkLabel(
            frame, text=f"{title}: --", text_color=color, font=("Roboto", 15, "bold")
        )
        lbl.pack(pady=5, padx=20, anchor="w")
        bar = ctk.CTkProgressBar(
            frame, progress_color=color, fg_color="#1A1A1A", height=12
        )
        bar.set(0)
        bar.pack(fill="x", padx=20, pady=10)
        return {"lbl": lbl, "bar": bar}

    def update_stats(self):
        if not self.monitors:
            return  # Para se mudar de aba
        try:
            # CPU
            cpu = psutil.cpu_percent()
            self.monitors["CPU"]["lbl"].configure(text=f"CPU: {cpu}%")
            self.monitors["CPU"]["bar"].set(cpu / 100)

            # RAM
            ram = psutil.virtual_memory().percent
            self.monitors["RAM"]["lbl"].configure(text=f"RAM: {ram}%")
            self.monitors["RAM"]["bar"].set(ram / 100)

            # DISCO
            disk = psutil.disk_usage("/").percent
            self.monitors["DISK"]["lbl"].configure(text=f"DISCO: {disk}%")
            self.monitors["DISK"]["bar"].set(disk / 100)

            # BATERIA
            batt = psutil.sensors_battery()
            if batt:
                plug = "Carregando" if batt.power_plugged else "Uso"
                self.monitors["BATT"]["lbl"].configure(
                    text=f"BATERIA: {batt.percent}% | {plug}"
                )
                self.monitors["BATT"]["bar"].set(batt.percent / 100)
            else:
                self.monitors["BATT"]["lbl"].configure(text="BATERIA: AC / Desktop")

            # GPU
            if GPUtil:
                gpus = GPUtil.getGPUs()
                if gpus:
                    self.monitors["GPU"]["lbl"].configure(
                        text=f"GPU: {gpus[0].load*100:.1f}%"
                    )
                    self.monitors["GPU"]["bar"].set(gpus[0].load)

            # REDE
            net = psutil.net_io_counters()
            now = datetime.now()
            dt = (now - self.last_time).total_seconds()
            if dt > 0:
                up = (net.bytes_sent - self.last_net_io.bytes_sent) / 1024 / dt
                self.monitors["NET"]["lbl"].configure(text=f"UPLOAD: {up:.1f} KB/s")
                self.monitors["NET"]["bar"].set(min(up / 2000, 1.0))
                self.last_net_io, self.last_time = net, now
        except:
            pass
        self.after(2000, self.update_stats)

    # =========================================================================
    # MODULO 2: YOUTUBE PRO (Download + Progresso)
    # =========================================================================
    def show_youtube(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="YOUTUBE DOWNLOADER PRO",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        url_entry = ctk.CTkEntry(
            self.main_frame, placeholder_text="Cole o link do vídeo aqui...", width=500
        )
        url_entry.pack(pady=10)

        tipo_var = ctk.StringVar(value="video")
        opt_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        opt_frame.pack(pady=5)
        ctk.CTkRadioButton(
            opt_frame,
            text="MP4 (Vídeo Completo)",
            variable=tipo_var,
            value="video",
            text_color="#D4AF37",
        ).pack(side="left", padx=20)
        ctk.CTkRadioButton(
            opt_frame,
            text="MP3 (Apenas Áudio)",
            variable=tipo_var,
            value="audio",
            text_color="#D4AF37",
        ).pack(side="left", padx=20)

        # Elementos de Progresso
        self.yt_progress = ctk.CTkProgressBar(
            self.main_frame, width=500, progress_color="#D4AF37"
        )
        self.yt_progress.set(0)
        self.yt_progress.pack(pady=(20, 5))

        self.yt_status = ctk.CTkLabel(
            self.main_frame,
            text="Aguardando link...",
            text_color="gray",
            font=("Consolas", 12),
        )
        self.yt_status.pack(pady=5)

        # Função de atualização segura (Evita crash se mudar de aba)
        def safe_update(text, color, progress=None):
            try:
                if self.yt_status.winfo_exists():
                    self.yt_status.configure(text=text, text_color=color)
                if progress is not None and self.yt_progress.winfo_exists():
                    self.yt_progress.set(progress)
            except:
                pass

        def baixar():
            link = url_entry.get()
            if not link:
                return

            safe_update("Inicializando...", "#D4AF37", 0)

            def process():
                if not yt_dlp:
                    safe_update("Erro: Biblioteca yt-dlp não carregou.", "red")
                    return
                try:
                    path = str(self.base_path / "Downloads")
                    if not os.path.exists(path):
                        os.makedirs(path)

                    # Hook de progresso
                    def progress_hook(d):
                        if d["status"] == "downloading":
                            try:
                                total = d.get("total_bytes") or d.get(
                                    "total_bytes_estimate"
                                )
                                downloaded = d.get("downloaded_bytes", 0)
                                if total:
                                    percent = downloaded / total
                                    if self.yt_progress.winfo_exists():
                                        self.yt_progress.set(percent)

                                speed = d.get("speed")
                                speed_str = (
                                    f"{speed/1024/1024:.1f} MB/s"
                                    if speed
                                    else "-- MB/s"
                                )
                                eta = d.get("eta")
                                eta_str = f"{eta}s" if eta else "--"

                                safe_update(
                                    f"{percent*100:.1f}% | Vel: {speed_str} | Falta: {eta_str}",
                                    "#D4AF37",
                                )
                            except:
                                pass
                        elif d["status"] == "finished":
                            safe_update(
                                "Download finalizado. Convertendo...", "#00BFFF", 1
                            )

                    # Configuração do YT-DLP
                    opts = {
                        "outtmpl": f"{path}/%(title)s.%(ext)s",
                        "quiet": True,
                        "ffmpeg_location": FFMPEG_PATH,  # O segredo do sucesso
                        "noplaylist": True,
                        "progress_hooks": [progress_hook],
                    }

                    if tipo_var.get() == "audio":
                        opts["format"] = "bestaudio/best"
                        opts["postprocessors"] = [
                            {
                                "key": "FFmpegExtractAudio",
                                "preferredcodec": "mp3",
                                "preferredquality": "192",
                            }
                        ]
                    else:
                        opts["format"] = "bestvideo+bestaudio/best"
                        opts["merge_output_format"] = "mp4"

                    with yt_dlp.YoutubeDL(opts) as ydl:
                        ydl.download([link])

                    safe_update("SUCESSO! Arquivo salvo em Downloads.", "#00FF00")
                    os.startfile(path)
                except Exception as e:
                    safe_update(f"Erro: {e}", "red")

            threading.Thread(target=process).start()

        ctk.CTkButton(
            self.main_frame,
            text="BAIXAR AGORA",
            command=baixar,
            fg_color="red",
            text_color="white",
        ).pack(pady=10)

    # =========================================================================
    # MODULO 3: PDF PARA AUDIOBOOK
    # =========================================================================
    def show_pdf_audio(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="CRIADOR DE AUDIOBOOKS",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        lbl_info = ctk.CTkLabel(
            self.main_frame,
            text="Converta livros PDF em MP3 para ouvir onde quiser.",
            text_color="gray",
        )
        lbl_info.pack(pady=10)

        def converter():
            pdf_path = ctk.filedialog.askopenfilename(filetypes=[("PDF", "*.pdf")])
            if not pdf_path:
                return

            lbl_info.configure(text="Lendo PDF... Aguarde...", text_color="#D4AF37")

            def run_conversion():
                try:
                    reader = PyPDF2.PdfReader(pdf_path)
                    engine = pyttsx3.init()

                    # Tenta selecionar voz brasileira
                    for voice in engine.getProperty("voices"):
                        if (
                            "brazil" in voice.id.lower()
                            or "portuguese" in voice.name.lower()
                        ):
                            engine.setProperty("voice", voice.id)
                            break

                    full_text = ""
                    for page in reader.pages:
                        full_text += page.extract_text() + " "

                    output = os.path.splitext(pdf_path)[0] + ".mp3"
                    lbl_info.configure(
                        text="Convertendo texto em voz...", text_color="#00BFFF"
                    )

                    engine.save_to_file(full_text, output)
                    engine.runAndWait()

                    lbl_info.configure(
                        text=f"Pronto! Salvo: {output}", text_color="#00FF00"
                    )
                    os.startfile(output)
                except Exception as e:
                    lbl_info.configure(text=f"Erro: {e}", text_color="red")

            threading.Thread(target=run_conversion).start()

        ctk.CTkButton(
            self.main_frame,
            text="SELECIONAR PDF",
            command=converter,
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=20)

    # =========================================================================
    # MODULO 4: WI-FI HACKER
    # =========================================================================
    def show_wifi_hacker(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="RECUPERADOR DE SENHAS WI-FI",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        textbox = ctk.CTkTextbox(
            self.main_frame,
            width=700,
            height=400,
            fg_color="#0A0A0A",
            text_color="#00FF00",
            font=("Consolas", 14),
        )
        textbox.pack(pady=10, fill="both", expand=True)

        def run():
            textbox.delete("0.0", "end")
            textbox.insert("end", "--- ESCANEANDO REDES ---\n")
            try:
                # Usa cp850 para compatibilidade com CMD em PT-BR
                cmd = subprocess.check_output(
                    ["netsh", "wlan", "show", "profiles"],
                    encoding="cp850",
                    errors="ignore",
                )

                # Regex para pegar nomes (PT e EN)
                perfis = re.findall(r"Perfil de Todos os Usu.rios\s*:\s(.*)", cmd)
                if not perfis:
                    perfis = re.findall(r"All User Profile\s*:\s(.*)", cmd)

                for p in perfis:
                    try:
                        p_clean = p.strip()
                        key = subprocess.check_output(
                            ["netsh", "wlan", "show", "profile", p_clean, "key=clear"],
                            encoding="cp850",
                            errors="ignore",
                        )

                        s = re.search(r"Conte.do da Chave\s*:\s(.*)", key)
                        if not s:
                            s = re.search(r"Key Content\s*:\s(.*)", key)

                        passw = s.group(1) if s else "[SEM SENHA]"
                        textbox.insert("end", f"REDE: {p_clean:<25} | SENHA: {passw}\n")
                        textbox.insert("end", "-" * 60 + "\n")
                    except:
                        pass
            except:
                textbox.insert("end", "Erro ao executar comando netsh.")

        ctk.CTkButton(
            self.main_frame,
            text="REVELAR SENHAS",
            command=run,
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=10)

    # =========================================================================
    # MODULO 5: SPEEDTEST
    # =========================================================================
    def show_speedtest(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="SPEEDTEST PRO",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)
        lbl = ctk.CTkLabel(
            self.main_frame, text="Pronto para iniciar.", text_color="gray"
        )
        lbl.pack()

        def run():
            if not speedtest:
                return
            lbl.configure(text="Conectando aos servidores...", text_color="#D4AF37")
            try:
                st = speedtest.Speedtest()
                st.get_best_server()
                lbl.configure(text="Testando Download...", text_color="#00BFFF")
                dl = st.download() / 1e6
                lbl.configure(text="Testando Upload...", text_color="#FF4500")
                ul = st.upload() / 1e6
                lbl.configure(
                    text=f"DL: {dl:.1f} Mbps  |  UL: {ul:.1f} Mbps  |  Ping: {st.results.ping:.0f} ms",
                    text_color="#00FF00",
                    font=("Roboto", 18, "bold"),
                )
            except:
                lbl.configure(text="Erro de conexão.", text_color="red")

        ctk.CTkButton(
            self.main_frame,
            text="INICIAR TESTE",
            command=lambda: threading.Thread(target=run).start(),
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=20)

    # =========================================================================
    # OUTROS MODULOS (Links, Android, Manutenção, etc.)
    # =========================================================================
    def show_maintenance(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="MANUTENÇÃO",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)
        for n, c in [
            ("LIMPAR TEMP", 'del /q /f /s "%temp%\\*.*"'),
            ("SFC SCAN", "sfc /scannow"),
        ]:
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=lambda x=c, y=n: self.executar_comando_silencioso(x, y),
                fg_color="#1A1A1A",
                border_color="#D4AF37",
                border_width=1,
                text_color="#D4AF37",
            ).pack(pady=5, fill="x", padx=40)

        # Shutdown Timer
        grid = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        grid.pack(fill="x", padx=40, pady=20)
        for n, s in [("30 Min", 1800), ("1 Hora", 3600), ("2 Horas", 7200)]:
            ctk.CTkButton(
                grid,
                text=n,
                command=lambda t=s: os.system(f"shutdown -s -t {t}"),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(side="left", expand=True, padx=5)
        ctk.CTkButton(
            self.main_frame,
            text="CANCELAR SHUTDOWN",
            command=lambda: os.system("shutdown -a"),
            fg_color="#8B0000",
            text_color="white",
        ).pack(pady=5, fill="x", padx=40)

    def show_security_native(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame, text="SEGURANÇA", text_color="#D4AF37", font=("Roboto", 20)
        ).pack(pady=20)
        e = ctk.CTkEntry(self.main_frame, show="*")
        e.pack(pady=10)

        def check():
            s = hashlib.sha1(e.get().encode()).hexdigest().upper()
            try:
                if (
                    s[5:]
                    in requests.get(
                        f"https://api.pwnedpasswords.com/range/{s[:5]}"
                    ).text
                ):
                    ctk.CTkLabel(
                        self.main_frame, text="SENHA VAZADA!", text_color="red"
                    ).pack()
                else:
                    ctk.CTkLabel(
                        self.main_frame, text="SENHA SEGURA.", text_color="green"
                    ).pack()
            except:
                pass

        ctk.CTkButton(
            self.main_frame,
            text="VERIFICAR VAZAMENTO",
            command=check,
            fg_color="#D4AF37",
            text_color="black",
        ).pack()

        def cripto():
            p = ctk.filedialog.askopenfilename()
            if p:
                self.executar_comando_silencioso(
                    f'python seguranca.py enc "{p}"', "Criptografando"
                )

        ctk.CTkButton(
            self.main_frame,
            text="CRIPTOGRAFAR ARQUIVO",
            command=cripto,
            fg_color="#1A1A1A",
            border_color="#D4AF37",
            border_width=1,
            text_color="#D4AF37",
        ).pack(pady=20, fill="x", padx=40)

    def show_links(self):
        self.clear_frame()
        for n, u in [
            ("WFM", "https://portalwfm.hapvida.com.br/"),
            ("GITHUB", "https://github.com"),
        ]:
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=lambda x=u: webbrowser.open(x),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=40)

    def show_android(self):
        self.clear_frame()
        for n, c in [("Listar", "adb devices"), ("Reiniciar", "adb reboot")]:
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=lambda x=c, y=n: self.executar_comando_silencioso(x, y),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=40)

    def show_programs(self):
        self.clear_frame()
        for n, c in [
            ("VS Code", "code ."),
            ("Explorer", f'explorer "{self.base_path}"'),
        ]:
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=lambda x=c: os.system(x),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=40)

    def show_resources(self):
        self.clear_frame()
        for n, p in [
            ("BUSCA PRESTADOR", "busca_de_prestador/index.html"),
            ("SIGO", "http://sistemas.hapvida.com.br/planos"),
        ]:
            cmd = lambda path=p: (
                webbrowser.open(path)
                if "http" in path
                else os.startfile(self.base_path / path)
            )
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=cmd,
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=40)


if __name__ == "__main__":
    app = CentralMaster()
    app.mainloop()
