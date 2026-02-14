import subprocess
import sys
import os
import time
import shutil


# --- AUTO-INSTALAÇÃO DE BIBLIOTECAS ---
def verificar_bibliotecas():
    required = {
        "customtkinter": "customtkinter",
        "psutil": "psutil",
        "speedtest": "speedtest-cli",
        "yt_dlp": "yt-dlp",
        "GPUtil": "gputil",
        "requests": "requests",
        "static_ffmpeg": "static-ffmpeg",
    }
    faltantes = []
    for import_name, install_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            faltantes.append(install_name)

    if faltantes:
        print(f"--- [AUTO-INSTALL] Baixando: {', '.join(faltantes)} ---")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + faltantes)
        except Exception as e:
            print(f"[ERRO] {e}")
            sys.exit()


verificar_bibliotecas()

# --- INÍCIO DO PROGRAMA ---
import customtkinter as ctk
import psutil
import webbrowser
import threading
import re
import requests
import hashlib
import static_ffmpeg
from pathlib import Path
from datetime import datetime

# CONFIGURAÇÃO DE DRIVERS DE VÍDEO
print("[SYSTEM] Configurando Drivers de Vídeo...")
static_ffmpeg.add_paths()
FFMPEG_PATH = shutil.which("ffmpeg")

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


class CentralMaster(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CENTRAL MASTER V5.2 - ESTÁVEL")
        self.geometry("1100x850")
        self.configure(fg_color="#000000")
        self.base_path = Path(__file__).parent
        self.monitors = {}
        self.last_net_io = psutil.net_io_counters()
        self.last_time = datetime.now()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.setup_sidebar()
        self.setup_main_frame()
        self.show_dashboard()

    def setup_sidebar(self):
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

        menu = [
            ("DASHBOARD", self.show_dashboard),
            ("LINKS TRABALHO", self.show_links),
            ("WI-FI HACKER", self.show_wifi_hacker),
            ("SPEEDTEST", self.show_speedtest),
            ("YOUTUBE DOWNLOAD", self.show_youtube),
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
        self.monitors = {}
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def executar_comando_silencioso(self, comando, titulo_botao):
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
                    textbox.insert("end", f"\n[INFO]:\n{stderr}")
            except Exception as e:
                textbox.insert("end", f"\nErro: {e}")

        threading.Thread(target=run).start()

    # --- YOUTUBE DOWNLOAD (CORRIGIDO PARA NÃO TRAVAR AO MUDAR DE ABA) ---
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

        # Função Segura para Atualizar a Interface
        def safe_update(text, color, progress=None):
            try:
                # Verifica se o widget ainda existe antes de tentar mexer nele
                if self.yt_status.winfo_exists():
                    self.yt_status.configure(text=text, text_color=color)
                if progress is not None and self.yt_progress.winfo_exists():
                    self.yt_progress.set(progress)
            except:
                pass  # Se a janela fechou, apenas ignora o erro silenciosamente

        def baixar():
            link = url_entry.get()
            if not link:
                return

            safe_update("Iniciando conexão...", "#D4AF37", 0)

            def process():
                if not yt_dlp:
                    safe_update("Erro: yt-dlp não instalado.", "red")
                    return
                try:
                    path = str(self.base_path / "Downloads")
                    if not os.path.exists(path):
                        os.makedirs(path)

                    def progress_hook(d):
                        if d["status"] == "downloading":
                            try:
                                total = d.get("total_bytes") or d.get(
                                    "total_bytes_estimate"
                                )
                                downloaded = d.get("downloaded_bytes", 0)
                                if total:
                                    percent = downloaded / total
                                    # Chama a atualização segura
                                    if self.yt_progress.winfo_exists():
                                        self.yt_progress.set(percent)

                                speed_raw = d.get("speed")
                                speed_str = (
                                    f"{speed_raw/1024/1024:.1f} MB/s"
                                    if speed_raw
                                    else "-- MB/s"
                                )
                                eta = d.get("eta")
                                eta_str = f"{eta}s" if eta else "--"

                                msg = f"Baixando: {percent*100:.1f}%  |  Vel: {speed_str}  |  Falta: {eta_str}"
                                safe_update(msg, "#D4AF37")
                            except:
                                pass

                        elif d["status"] == "finished":
                            safe_update(
                                "Download concluído! Processando conversão...",
                                "#00BFFF",
                                1,
                            )

                    opts = {
                        "outtmpl": f"{path}/%(title)s.%(ext)s",
                        "quiet": True,
                        "ffmpeg_location": FFMPEG_PATH,  # Usa o caminho detectado do FFmpeg
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

                    safe_update(f"SUCESSO! Salvo na pasta Downloads.", "#00FF00")
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
            height=45,
        ).pack(pady=10)

    # --- DEMAIS FUNÇÕES (DASHBOARD, ETC) ---
    def show_dashboard(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="MONITORAMENTO",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=15)
        self.monitors = {
            "CPU": self.create_monitor("CPU"),
            "GPU": self.create_monitor("GPU"),
            "RAM": self.create_monitor("RAM"),
            "DISK": self.create_monitor("DISCO"),
            "BATT": self.create_monitor("BATERIA", "#00FF00"),
            "NET": self.create_monitor("REDE", "#00BFFF"),
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
            return
        try:
            cpu = psutil.cpu_percent()
            self.monitors["CPU"]["bar"].set(cpu / 100)
            self.monitors["CPU"]["lbl"].configure(text=f"CPU: {cpu}%")
            ram = psutil.virtual_memory().percent
            self.monitors["RAM"]["bar"].set(ram / 100)
            self.monitors["RAM"]["lbl"].configure(text=f"RAM: {ram}%")
            disk = psutil.disk_usage("/").percent
            self.monitors["DISK"]["bar"].set(disk / 100)
            self.monitors["DISK"]["lbl"].configure(text=f"DISCO: {disk}%")
            if GPUtil and GPUtil.getGPUs():
                self.monitors["GPU"]["bar"].set(GPUtil.getGPUs()[0].load)
                self.monitors["GPU"]["lbl"].configure(
                    text=f"GPU: {GPUtil.getGPUs()[0].load*100:.0f}%"
                )
            batt = psutil.sensors_battery()
            if batt:
                self.monitors["BATT"]["bar"].set(batt.percent / 100)
                self.monitors["BATT"]["lbl"].configure(text=f"BAT: {batt.percent}%")
            net = psutil.net_io_counters()
            now = datetime.now()
            dt = (now - self.last_time).total_seconds()
            if dt > 0:
                up = (net.bytes_sent - self.last_net_io.bytes_sent) / 1024 / dt
                self.monitors["NET"]["bar"].set(min(up / 2000, 1.0))
                self.monitors["NET"]["lbl"].configure(text=f"UP: {up:.1f} KB/s")
                self.last_net_io, self.last_time = net, now
        except:
            pass
        self.after(2000, self.update_stats)

    def show_wifi_hacker(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="RECUPERADOR WI-FI",
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
            try:
                cmd = subprocess.check_output(
                    ["netsh", "wlan", "show", "profiles"],
                    encoding="cp850",
                    errors="ignore",
                )
                for p in re.findall(r"Todos os Usu.rios\s*:\s(.*)", cmd):
                    try:
                        key = subprocess.check_output(
                            [
                                "netsh",
                                "wlan",
                                "show",
                                "profile",
                                p.strip(),
                                "key=clear",
                            ],
                            encoding="cp850",
                            errors="ignore",
                        )
                        s = re.search(r"Conte.do da Chave\s*:\s(.*)", key)
                        passw = s.group(1) if s else "[SEM SENHA]"
                        textbox.insert(
                            "end", f"REDE: {p.strip():<20} | SENHA: {passw}\n"
                        )
                    except:
                        pass
            except:
                textbox.insert("end", "Erro ao escanear.")

        ctk.CTkButton(
            self.main_frame,
            text="ESCANEAR",
            command=run,
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=10)

    def show_speedtest(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="SPEEDTEST",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)
        lbl = ctk.CTkLabel(self.main_frame, text="Pronto...", text_color="gray")
        lbl.pack()

        def run():
            if not speedtest:
                return
            lbl.configure(text="Testando...", text_color="#D4AF37")
            try:
                st = speedtest.Speedtest()
                st.get_best_server()
                lbl.configure(
                    text=f"DL: {st.download()/1e6:.1f} Mbps | UL: {st.upload()/1e6:.1f} Mbps | Ping: {st.results.ping:.0f} ms",
                    text_color="#00FF00",
                )
            except:
                lbl.configure(text="Erro de conexão", text_color="red")

        ctk.CTkButton(
            self.main_frame,
            text="INICIAR",
            command=lambda: threading.Thread(target=run).start(),
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=20)

    def show_maintenance(self):
        self.clear_frame()
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
        ctk.CTkButton(
            self.main_frame,
            text="CANCELAR SHUTDOWN",
            command=lambda: os.system("shutdown -a"),
            fg_color="#8B0000",
            text_color="white",
        ).pack(pady=20, fill="x", padx=40)

    def show_security_native(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="VERIFICAR VAZAMENTO",
            text_color="#D4AF37",
            font=("Roboto", 20),
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
                        self.main_frame, text="VAZADA!", text_color="red"
                    ).pack()
                else:
                    ctk.CTkLabel(
                        self.main_frame, text="SEGURA.", text_color="green"
                    ).pack()
            except:
                pass

        ctk.CTkButton(
            self.main_frame,
            text="VERIFICAR",
            command=check,
            fg_color="#D4AF37",
            text_color="black",
        ).pack()

        def cripto():
            path = ctk.filedialog.askopenfilename()
            if path:
                self.executar_comando_silencioso(
                    f'python seguranca.py enc "{path}"', "Criptografando"
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
import customtkinter as ctk
import psutil
import os
import subprocess
import webbrowser
import threading
from pathlib import Path
from datetime import datetime

# Tenta importar bibliotecas opcionais
try:
    import GPUtil
except ImportError:
    GPUtil = None


class CentralMaster(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO VISUAL ---
        self.title("CENTRAL MASTER V3.0 - ULTIMATE")
        self.geometry("1100x850")
        self.configure(fg_color="#000000")
        self.base_path = Path(__file__).parent

        # Variáveis
        self.monitors = {}
        self.last_net_io = psutil.net_io_counters()
        self.last_time = datetime.now()

        # Layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_frame()
        self.show_dashboard()

    def setup_sidebar(self):
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

        # Menu Completo (Sem .bat)
        menu = [
            ("DASHBOARD", self.show_dashboard),
            ("LINKS TRABALHO", self.show_links),
            ("MANUTENÇÃO PC", self.show_maintenance),
            ("REDE / INTERNET", self.show_network),
            ("SEGURANÇA", self.show_security_native),
            ("ANDROID (ADB)", self.show_android),
            ("PROGRAMAS", self.show_programs),
            ("RECURSOS", self.show_resources),
        ]

        for text, cmd in menu:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=cmd,
                fg_color="transparent",
                text_color="#D4AF37",
                hover_color="#1A1A1A",
                anchor="w",
                font=("Roboto", 13, "bold"),
                height=40,
            )
            btn.pack(fill="x", padx=15, pady=5)

    def setup_main_frame(self):
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#000000")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def clear_frame(self):
        self.monitors = {}
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- FUNÇÃO AUXILIAR: Executar comandos sem abrir janela preta ---
    def executar_comando_silencioso(self, comando, titulo_botao):
        # Cria uma janela de log dentro da interface
        log_window = ctk.CTkToplevel(self)
        log_window.title(f"Executando: {titulo_botao}")
        log_window.geometry("600x400")
        log_window.configure(fg_color="#000000")

        textbox = ctk.CTkTextbox(
            log_window, fg_color="#0A0A0A", text_color="#D4AF37", font=("Consolas", 12)
        )
        textbox.pack(fill="both", expand=True, padx=10, pady=10)
        textbox.insert("0.0", f"--- INICIANDO {titulo_botao} ---\nWait...\n")

        def run():
            try:
                # Executa o comando e captura a saída
                process = subprocess.Popen(
                    comando,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                stdout, stderr = process.communicate()

                textbox.insert("end", stdout)
                if stderr:
                    textbox.insert("end", f"\n[ERROS]:\n{stderr}")
                textbox.insert("end", "\n--- PROCESSO CONCLUÍDO ---\n")
            except Exception as e:
                textbox.insert("end", f"\nErro Crítico: {e}")

        # Roda em thread separada para não travar a interface
        threading.Thread(target=run).start()

    # --- PÁGINA: DASHBOARD ---
    def show_dashboard(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="MONITORAMENTO DO SISTEMA",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=15)

        self.monitors = {
            "CPU": self.create_monitor("PROCESSADOR (CPU)"),
            "GPU": self.create_monitor("PLACA DE VÍDEO (GPU)"),
            "RAM": self.create_monitor("MEMÓRIA RAM"),
            "DISK": self.create_monitor("ARMAZENAMENTO (C:)"),
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
            return
        try:
            cpu = psutil.cpu_percent()
            self.monitors["CPU"]["lbl"].configure(text=f"CPU: {cpu}%")
            self.monitors["CPU"]["bar"].set(cpu / 100)

            ram = psutil.virtual_memory().percent
            self.monitors["RAM"]["lbl"].configure(text=f"RAM: {ram}%")
            self.monitors["RAM"]["bar"].set(ram / 100)

            disk = psutil.disk_usage("/").percent
            self.monitors["DISK"]["lbl"].configure(text=f"DISCO: {disk}%")
            self.monitors["DISK"]["bar"].set(disk / 100)

            if GPUtil:
                gpus = GPUtil.getGPUs()
                if gpus:
                    self.monitors["GPU"]["lbl"].configure(
                        text=f"GPU: {gpus[0].load*100:.1f}%"
                    )
                    self.monitors["GPU"]["bar"].set(gpus[0].load)

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

    # --- PÁGINA: LINKS ---
    def show_links(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="LINKS DE TRABALHO",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)
        urls = [
            (
                "Portal WFM",
                "https://portalwfm.hapvida.com.br/sisqualIdentityServer/core/login?signin=ef11be1cd5fb328f715cf7a9bc18f826",
            ),
            ("Beedoo", "https://hapvidandi.beedoo.io/feed"),
            ("Busca Bat-System", "https://th3exe.github.io/bat-system/busca.html"),
            ("Teams", "https://teams.microsoft.com/v2/"),
            ("GitHub", "https://github.com"),
        ]

        def abrir_todas():
            for _, u in urls:
                webbrowser.open(u)

        ctk.CTkButton(
            self.main_frame,
            text="ABRIR TODAS AS ABAS",
            command=abrir_todas,
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=10, fill="x", padx=20)

        for n, u in urls:
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=lambda x=u: webbrowser.open(x),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: MANUTENÇÃO (NATIVA) ---
    def show_maintenance(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="LIMPEZA E OTIMIZAÇÃO",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        cmds = [
            ("LIMPAR ARQUIVOS TEMPORÁRIOS", 'del /q /f /s "%temp%\\*.*"'),
            (
                "LIMPAR CACHE DO CHROME",
                'del /q /f /s "%LocalAppData%\\Google\\Chrome\\User Data\\Default\\Cache\\*.*"',
            ),
            ("VERIFICAR INTEGRIDADE (SFC)", "sfc /scannow"),
        ]

        for nome, comando in cmds:
            ctk.CTkButton(
                self.main_frame,
                text=nome,
                command=lambda c=comando, n=nome: self.executar_comando_silencioso(
                    c, n
                ),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: REDE (NATIVA) ---
    def show_network(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="FERRAMENTAS DE REDE",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        cmds = [
            ("FLUSH DNS (LIMPAR CACHE)", "ipconfig /flushdns"),
            ("RENOVAR IP", "ipconfig /release && ipconfig /renew"),
            ("RESETAR WINSOCK", "netsh winsock reset"),
        ]

        for nome, comando in cmds:
            ctk.CTkButton(
                self.main_frame,
                text=nome,
                command=lambda c=comando, n=nome: self.executar_comando_silencioso(
                    c, n
                ),
                fg_color="#1A1A1A",
                text_color="#00BFFF",
                border_color="#00BFFF",
                border_width=1,
            ).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: SEGURANÇA (NATIVA - SEM CONSOLE PRETO) ---
    def show_security_native(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="SEGURANÇA INTEGRADA",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        # Área de Input para Senha
        self.pass_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Digite a senha para verificar vazamento...",
            show="*",
        )
        self.pass_entry.pack(fill="x", padx=20, pady=10)

        def verificar_vazamento():
            senha = self.pass_entry.get()
            if not senha:
                return
            import hashlib, requests

            sha1 = hashlib.sha1(senha.encode("utf-8")).hexdigest().upper()
            prefix, suffix = sha1[:5], sha1[5:]
            try:
                res = requests.get(
                    f"https://api.pwnedpasswords.com/range/{prefix}", verify=False
                )
                if suffix in res.text:
                    ctk.CTkLabel(
                        self.main_frame,
                        text="[PERIGO] Essa senha vazou!",
                        text_color="red",
                    ).pack()
                else:
                    ctk.CTkLabel(
                        self.main_frame, text="[OK] Senha segura.", text_color="green"
                    ).pack()
            except:
                ctk.CTkLabel(
                    self.main_frame, text="Erro de conexão.", text_color="orange"
                ).pack()

        ctk.CTkButton(
            self.main_frame,
            text="VERIFICAR AGORA",
            command=verificar_vazamento,
            fg_color="#D4AF37",
            text_color="black",
        ).pack(pady=5)

        # Criptografia de Arquivo (Visual)
        def criptografar():
            path = ctk.filedialog.askopenfilename()
            if path:
                self.executar_comando_silencioso(
                    f'python seguranca.py enc "{path}"', "Criptografando"
                )

        ctk.CTkButton(
            self.main_frame,
            text="CRIPTOGRAFAR ARQUIVO",
            command=criptografar,
            fg_color="#1A1A1A",
            border_color="#D4AF37",
            border_width=1,
            text_color="#D4AF37",
        ).pack(pady=20, fill="x", padx=20)

    # --- PÁGINA: ANDROID (ADB) ---
    def show_android(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="CONTROLE ANDROID (ADB)",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)

        cmds = [
            ("VERIFICAR DISPOSITIVOS", "adb devices"),
            ("LIMPAR CACHE APPS", "adb shell pm trim-caches 999G"),
            ("REINICIAR CELULAR", "adb reboot"),
        ]

        for nome, comando in cmds:
            ctk.CTkButton(
                self.main_frame,
                text=nome,
                command=lambda c=comando, n=nome: self.executar_comando_silencioso(
                    c, n
                ),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: PROGRAMAS ---
    def show_programs(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="PROGRAMAS",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)
        progs = [
            ("VS CODE", "code ."),
            ("EXPLORER", f'explorer "{self.base_path}"'),
            ("CALCULADORA", "calc"),
            ("TECLADO VIRTUAL", "osk"),
        ]
        for n, c in progs:
            ctk.CTkButton(
                self.main_frame,
                text=n,
                command=lambda x=c: os.system(x),
                fg_color="#1A1A1A",
                text_color="#D4AF37",
                border_color="#D4AF37",
                border_width=1,
            ).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: RECURSOS ---
    def show_resources(self):
        self.clear_frame()
        ctk.CTkLabel(
            self.main_frame,
            text="SEUS PROJETOS",
            font=("Roboto", 24, "bold"),
            text_color="#D4AF37",
        ).pack(pady=20)
        recursos = [
            ("BUSCA PRESTADOR", "busca_de_prestador/inicio.html"),
            ("SISTEMA HAPVIDA", "http://sistemas.hapvida.com.br/planos"),
            ("PROJETO SEMEADORES", "semeadores"),
            ("NOTAS", "procedimentos.txt"),
        ]
        for n, p in recursos:
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
            ).pack(pady=5, fill="x", padx=20)


if __name__ == "__main__":
    app = CentralMaster()
    app.mainloop()

