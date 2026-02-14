import customtkinter as ctk
import psutil
import os
import subprocess
import webbrowser
from pathlib import Path
from datetime import datetime

# Tenta importar o módulo de segurança GUI
try:
    from seguranca_gui import SubMenuSeguranca
except ImportError:
    SubMenuSeguranca = None

# Tenta importar GPUtil para dados de GPU
try:
    import GPUtil
except ImportError:
    GPUtil = None

class CentralMaster(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÕES DA JANELA ---
        self.title("CENTRAL MASTER V3.0 - ULTIMATE EDITION")
        self.geometry("1100x850")
        self.configure(fg_color="#000000")
        self.base_path = Path(__file__).parent
        
        # Monitoramento
        self.last_net_io = psutil.net_io_counters()
        self.last_time = datetime.now()
        self.monitors = {}

        # Layout Principal
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.setup_sidebar()
        self.setup_main_frame()
        self.show_dashboard()

    def setup_sidebar(self):
        """Menu lateral Dourado com todas as classes do .BAT"""
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color="#0A0A0A", border_color="#D4AF37", border_width=1)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        ctk.CTkLabel(self.sidebar, text="MASTER", font=("Impact", 38), text_color="#D4AF37").pack(pady=30)

        # Mapeamento completo do Menu .BAT
        menu_items = [
            ("DASHBOARD", self.show_dashboard),
            ("LINKS TRABALHO", self.show_links),          # Classe 1
            ("MANUTENÇÃO PC", self.show_maintenance),     # Classes 2, 3 e 4
            ("ANDROID (ADB)", self.show_android),         # Classe 6
            ("SEGURANÇA", self.show_security),            # Classe 8
            ("PROGRAMAS / HÍBRIDO", self.show_programs),  # Classe 5 e 9
            ("RECURSOS / ARQUIVOS", self.show_resources)  # Classe 10
        ]

        for text, cmd in menu_items:
            btn = ctk.CTkButton(self.sidebar, text=text, command=cmd, fg_color="transparent", 
                                text_color="#D4AF37", hover_color="#1A1A1A", anchor="w", 
                                font=("Roboto", 13, "bold"), height=40)
            btn.pack(fill="x", padx=15, pady=5)

    def setup_main_frame(self):
        self.main_frame = ctk.CTkScrollableFrame(self, fg_color="#000000")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)

    def clear_frame(self):
        self.monitors = {}
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # --- PÁGINA: DASHBOARD ---
    def show_dashboard(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="MONITORAMENTO DO SISTEMA", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=15)
        
        self.monitors = {
            "CPU": self.create_unified_monitor("PROCESSADOR (CPU)"),
            "GPU": self.create_unified_monitor("PLACA DE VÍDEO (GPU)"),
            "RAM": self.create_unified_monitor("MEMÓRIA RAM"),
            "DISK": self.create_unified_monitor("ARMAZENAMENTO (C:)"),
            "NET": self.create_unified_monitor("REDE (UPLOAD)", "#00BFFF")
        }
        self.update_stats()

    def create_unified_monitor(self, title, color="#D4AF37"):
        frame = ctk.CTkFrame(self.main_frame, fg_color="#0A0A0A", border_color="#D4AF37", border_width=1)
        frame.pack(fill="x", pady=8, padx=10)
        lbl = ctk.CTkLabel(frame, text=f"{title}: --", text_color=color, font=("Roboto", 15, "bold"))
        lbl.pack(pady=5, padx=20, anchor="w")
        bar = ctk.CTkProgressBar(frame, progress_color=color, fg_color="#1A1A1A", height=12)
        bar.set(0)
        bar.pack(fill="x", padx=20, pady=10)
        return {"lbl": lbl, "bar": bar}

    def update_stats(self):
        if not self.monitors: return
        try:
            cpu = psutil.cpu_percent()
            cpu_temp = cpu * 0.5 + 35
            self.monitors["CPU"]["lbl"].configure(text=f"CPU: {cpu}%  |  ESTIMADA: {cpu_temp:.1f}°C")
            self.monitors["CPU"]["bar"].set(cpu / 100)

            ram = psutil.virtual_memory().percent
            self.monitors["RAM"]["lbl"].configure(text=f"RAM: {ram}%")
            self.monitors["RAM"]["bar"].set(ram / 100)

            disk = psutil.disk_usage('/').percent
            self.monitors["DISK"]["lbl"].configure(text=f"DISCO: {disk}%")
            self.monitors["DISK"]["bar"].set(disk / 100)

            gpu_u, gpu_t = 0, 0
            if GPUtil:
                try:
                    gpus = GPUtil.getGPUs()
                    if gpus: gpu_u, gpu_t = gpus[0].load * 100, gpus[0].temperature
                except: pass
            self.monitors["GPU"]["lbl"].configure(text=f"GPU: {gpu_u:.1f}%" + (f" | {gpu_t}°C" if gpu_t else ""))
            self.monitors["GPU"]["bar"].set(gpu_u / 100)

            net = psutil.net_io_counters()
            now = datetime.now()
            dt = (now - self.last_time).total_seconds()
            if dt > 0:
                up = (net.bytes_sent - self.last_net_io.bytes_sent) / 1024 / dt
                self.monitors["NET"]["lbl"].configure(text=f"UPLOAD: {up:.1f} KB/s")
                self.monitors["NET"]["bar"].set(min(up / 2000, 1.0))
                self.last_net_io, self.last_time = net, now
        except: pass
        self.after(2000, self.update_stats)

    # --- PÁGINA: LINKS (Classe 1) ---
    def show_links(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="FERRAMENTAS DE TRABALHO (CLASSE 1)", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        
        urls = [
            ("Portal WFM", "https://portalwfm.hapvida.com.br/sisqualIdentityServer/core/login?signin=ef11be1cd5fb328f715cf7a9bc18f826"),
            ("Beedoo Hapvida", "https://hapvidandi.beedoo.io/feed"),
            ("Busca Bat-System", "https://th3exe.github.io/bat-system/busca.html"),
            ("Microsoft Teams", "https://teams.microsoft.com/v2/"),
            ("Google Docs (Base)", "https://docs.google.com/document/d/1z3eFgQkzXhO8INNo6mkiN2CO8_LAu9h1CYLuQoV0USc/edit?tab=t.0"),
            ("GitHub", "https://github.com"),
            ("Python W3Schools", "https://www.w3schools.com/python/")
        ]

        def abrir_todas():
            for _, u in urls: webbrowser.open(u)

        ctk.CTkButton(self.main_frame, text="ABRIR TODAS AS ABAS", command=abrir_todas, 
                      fg_color="#D4AF37", text_color="#000000", font=("Roboto", 14, "bold"), height=50).pack(pady=10, fill="x", padx=20)

        for n, u in urls:
            ctk.CTkButton(self.main_frame, text=n, command=lambda x=u: webbrowser.open(x),
                          fg_color="#1A1A1A", text_color="#D4AF37", border_color="#D4AF37", border_width=1).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: MANUTENÇÃO (Classes 2, 3, 4) ---
    def show_maintenance(self):
        self.clear_frame()
        
        # OTIMIZAÇÃO (Classe 2)
        ctk.CTkLabel(self.main_frame, text="OTIMIZAÇÃO E LIMPEZA", font=("Roboto", 20, "bold"), text_color="#D4AF37").pack(pady=10)
        cmds_opt = [
            ("LIMPAR TEMP DO WINDOWS", 'del /q /f /s "%temp%\\*.*" & del /q /f /s "C:\\Windows\\Temp\\*.*"'),
            ("LIMPAR CACHE CHROME", 'del /q /f /s "%LocalAppData%\\Google\\Chrome\\User Data\\Default\\Cache\\*.*"')
        ]
        for n, c in cmds_opt:
            ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: os.system(x),
                          fg_color="#1A1A1A", text_color="#D4AF37", border_color="#D4AF37", border_width=1).pack(pady=5, fill="x", padx=40)

        # REDE (Classe 3)
        ctk.CTkLabel(self.main_frame, text="CONFIGURAÇÃO DE REDE", font=("Roboto", 20, "bold"), text_color="#D4AF37").pack(pady=(20, 10))
        cmds_net = [
            ("FLUSH DNS (Limpar Cache)", "ipconfig /flushdns"),
            ("RENOVAR IP (Release/Renew)", "ipconfig /release & ipconfig /renew"),
            ("RESETAR WINSOCK", "netsh winsock reset")
        ]
        for n, c in cmds_net:
            ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: os.system(x),
                          fg_color="#1A1A1A", text_color="#00BFFF", border_color="#00BFFF", border_width=1).pack(pady=5, fill="x", padx=40)

        # SISTEMA (Classe 4)
        ctk.CTkLabel(self.main_frame, text="FERRAMENTAS DE SISTEMA", font=("Roboto", 20, "bold"), text_color="#D4AF37").pack(pady=(20, 10))
        ctk.CTkButton(self.main_frame, text="VERIFICADOR DE ARQUIVOS (SFC SCAN)", command=lambda: os.system("sfc /scannow"),
                      fg_color="#1A1A1A", text_color="red", border_color="red", border_width=1).pack(pady=5, fill="x", padx=40)

    # --- PÁGINA: ANDROID (Classe 6) ---
    def show_android(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="GERENCIADOR ADB (ANDROID)", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        
        cmds = [
            ("VERIFICAR DISPOSITIVOS", "adb devices"),
            ("LIMPAR CACHE (TRIM 999G)", "adb shell pm trim-caches 999G"),
            ("REINICIAR CELULAR", "adb reboot")
        ]
        for n, c in cmds:
            ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: os.system(x),
                          fg_color="#1A1A1A", text_color="#D4AF37", border_color="#D4AF37", border_width=1, height=45).pack(pady=5, fill="x", padx=20)
        
        # Função especial para Desativar Bloatware com Input
        def desativar_app():
            dialog = ctk.CTkInputDialog(text="Digite o nome do pacote (ex: com.facebook.katana):", title="Desativar App")
            pacote = dialog.get_input()
            if pacote:
                os.system(f"adb shell pm disable-user --user 0 {pacote}")

        ctk.CTkButton(self.main_frame, text="DESATIVAR BLOATWARE (Disable User)", command=desativar_app,
                      fg_color="#1A1A1A", text_color="orange", border_color="orange", border_width=1, height=45).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: PROGRAMAS (Classe 5 e 9) ---
    def show_programs(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="PROGRAMAS E HÍBRIDO", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        
        # Híbrido (Classe 5)
        ctk.CTkLabel(self.main_frame, text="AUTOMACAO PYTHON", font=("Roboto", 16, "bold"), text_color="gray").pack(pady=5)
        ctk.CTkButton(self.main_frame, text="EXECUTAR AUTOMACAO.PY", command=lambda: subprocess.Popen(["python", "automacao.py"], creationflags=subprocess.CREATE_NEW_CONSOLE),
                      fg_color="#1A1A1A", text_color="#00FF00", border_color="#00FF00", border_width=1, height=50).pack(pady=5, fill="x", padx=20)

        # Programas (Classe 9)
        ctk.CTkLabel(self.main_frame, text="ACESSO RÁPIDO", font=("Roboto", 16, "bold"), text_color="gray").pack(pady=5)
        progs = [
            ("VS CODE (Projeto Atual)", "code ."),
            ("EXPLORER (Pasta Scripts)", f'explorer "{self.base_path}"'),
            ("TECLADO VIRTUAL", "osk"),
            ("PAINEL DE CONTROLE", "control"),
            ("CALCULADORA", "calc")
        ]
        for n, c in progs:
            ctk.CTkButton(self.main_frame, text=n, command=lambda x=c: os.system(x),
                          fg_color="#1A1A1A", text_color="#D4AF37", border_color="#D4AF37", border_width=1).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: RECURSOS (Classe 10) ---
    def show_resources(self):
        self.clear_frame()
        ctk.CTkLabel(self.main_frame, text="RECURSOS UNIVERSAIS", font=("Roboto", 24, "bold"), text_color="#D4AF37").pack(pady=20)
        
        # Mapeamento Inteligente (Prioriza caminho relativo para ser Universal)
        recursos = [
            ("BUSCA DE PRESTADOR", "busca_de_prestador/index.html"),
            ("SISTEMA SIGO (HAPVIDA)", "http://sistemas.hapvida.com.br/planos"),
            ("NOTAS (procedimentos.txt)", "procedimentos.txt"),
            ("PASTA SEMEADORES", "semeadores"),
            ("EXECUTAR ABRIR_ARQUIVOS.PY", "abrir_arquivos.py")
        ]

        for nome, alvo in recursos:
            def acao(t=alvo):
                if t.startswith("http"):
                    webbrowser.open(t)
                elif t.endswith(".py"):
                    subprocess.Popen(["python", t], creationflags=subprocess.CREATE_NEW_CONSOLE)
                else:
                    path = self.base_path / t
                    if path.exists():
                        os.startfile(path)
                    else:
                        print(f"Arquivo não encontrado: {path}")

            ctk.CTkButton(self.main_frame, text=nome, command=acao,
                          fg_color="#1A1A1A", text_color="#D4AF37", border_color="#D4AF37", border_width=1, height=45).pack(pady=5, fill="x", padx=20)

    # --- PÁGINA: SEGURANÇA (Classe 8) ---
    def show_security(self):
        self.clear_frame()
        if SubMenuSeguranca:
            submenu = SubMenuSeguranca(self.main_frame)
            submenu.pack(fill="both", expand=True)
        else:
            ctk.CTkLabel(self.main_frame, text="ERRO: seguranca_gui.py não encontrado!", text_color="red").pack()

if __name__ == "__main__":
    app = CentralMaster()
    app.mainloop()