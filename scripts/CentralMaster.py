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
