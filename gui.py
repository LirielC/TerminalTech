#!/usr/bin/env python3

import sys
import threading
import queue
import re
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext, messagebox

# Importações dos módulos existentes
from modules.dns_checker import DNSChecker
from modules.disk_analyzer import DiskAnalyzer
from modules.ram_monitor import RAMMonitor
from modules.temp_cleaner import TempCleaner
from modules.speed_tester import SpeedTester
from modules.system_info import SystemInfo
from modules.driver_updater import DriverUpdater
from modules.virus_scanner import VirusScanner
from modules.memory_tester import MemoryTester
from modules.disk_checker import DiskChecker
from modules.utils import get_os_type


ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;]*m")


class QueueWriter:
    def __init__(self, log_queue: queue.Queue):
        self._log_queue = log_queue

    def write(self, message: str) -> None:
        if not message:
            return
        self._log_queue.put(message)

    def flush(self) -> None:
        pass


class TerminalTecGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("TerminalTec - GUI")
        self.geometry("1040x640")

        self._orig_stdout = sys.stdout
        self._orig_stderr = sys.stderr
        # Compatível com Python 3.7+: evitar Queue[str]
        self._log_queue: queue.Queue = queue.Queue()
        sys.stdout = QueueWriter(self._log_queue)
        sys.stderr = QueueWriter(self._log_queue)

        self.is_running = False

        # Instâncias dos módulos
        self.modules = {
            "dns": DNSChecker(),
            "disk": DiskAnalyzer(),
            "ram": RAMMonitor(),
            "temp": TempCleaner(),
            "speed": SpeedTester(),
            "system": SystemInfo(),
            "driver_updater": DriverUpdater(),
            "virus": VirusScanner(),
            "memory_tester": MemoryTester(),
            "disk_checker": DiskChecker(),
        }

        self._build_ui()
        self.after(60, self._poll_log_queue)

        self.protocol("WM_DELETE_WINDOW", self._on_close)

    def _build_ui(self) -> None:
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ttk.Frame(self, padding=8)
        sidebar.grid(row=0, column=0, sticky="ns")
        for i in range(0, 40):
            sidebar.rowconfigure(i, weight=0)

        os_label = ttk.Label(sidebar, text=f"SO: {get_os_type().capitalize()}")
        os_label.grid(row=0, column=0, sticky="w", pady=(0, 8))

        # Botões principais
        self._add_button(sidebar, 1, "Diagnóstico Completo", self._task_full_diagnostic)
        self._add_separator(sidebar, 2)

        self._add_button(sidebar, 3, "Informações do Sistema", self._task_system_info)
        self._add_button(sidebar, 4, "Diagnóstico de DNS", self._task_dns)
        self._add_button(sidebar, 5, "Análise de Disco", self._task_disk_analysis)
        self._add_button(sidebar, 6, "Verificação de Disco", self._task_disk_check)
        self._add_button(sidebar, 7, "Monitoramento de RAM", self._task_ram)
        self._add_button(sidebar, 8, "Busca de Drivers", self._task_driver_updates)
        # Backup removido
        self._add_button(sidebar, 10, "Temp: Analisar", self._task_temp_analyze)
        self._add_button(sidebar, 11, "Temp: Limpar", self._task_temp_clean)
        self._add_button(sidebar, 12, "Teste de Velocidade", self._task_speed)
        self._add_button(sidebar, 13, "Vírus e Segurança", self._task_virus_status)

        self._add_separator(sidebar, 14)
        self._add_button(sidebar, 15, "Limpar Log", self._clear_log)
        self._add_button(sidebar, 16, "Salvar Log", self._save_log)

        # Área de logs
        content = ttk.Frame(self, padding=(0, 8, 8, 8))
        content.grid(row=0, column=1, sticky="nsew")
        content.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=1)

        self.text = scrolledtext.ScrolledText(content, wrap=tk.WORD, state=tk.NORMAL)
        self.text.grid(row=0, column=0, sticky="nsew")
        self.text.insert(tk.END, "TerminalTec GUI iniciada. Selecione uma ação à esquerda.\n\n")
        self.text.configure(font=("Consolas", 10))

    def _add_button(self, parent: ttk.Frame, row: int, text: str, command) -> None:
        btn = ttk.Button(parent, text=text, command=lambda: self._run_in_thread(command))
        btn.grid(row=row, column=0, sticky="ew", pady=2)

    def _add_separator(self, parent: ttk.Frame, row: int) -> None:
        sep = ttk.Separator(parent, orient=tk.HORIZONTAL)
        sep.grid(row=row, column=0, sticky="ew", pady=6)

    def _append_log(self, raw_text: str) -> None:
        # Remove códigos ANSI de cor para exibição limpa
        text = ANSI_ESCAPE_RE.sub("", raw_text)
        self.text.insert(tk.END, text)
        self.text.see(tk.END)

    def _poll_log_queue(self) -> None:
        try:
            while True:
                msg = self._log_queue.get_nowait()
                self._append_log(msg)
        except queue.Empty:
            pass
        finally:
            self.after(60, self._poll_log_queue)

    def _clear_log(self) -> None:
        self.text.delete("1.0", tk.END)

    def _save_log(self) -> None:
        try:
            import datetime
            content = self.text.get("1.0", tk.END).strip()
            if not content:
                messagebox.showinfo("Salvar Log", "Nada para salvar.")
                return
            ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"terminaltec_log_{ts}.txt"
            with open(filename, "w", encoding="utf-8") as f:
                f.write(content)
            messagebox.showinfo("Salvar Log", f"Log salvo em {filename}")
        except Exception as e:
            messagebox.showerror("Salvar Log", f"Erro ao salvar log: {e}")

    def _run_in_thread(self, task_callable) -> None:
        if self.is_running:
            messagebox.showinfo("Em execução", "Aguarde a conclusão da tarefa atual.")
            return

        def _runner():
            try:
                self.is_running = True
                task_callable()
            except Exception as e:
                print(f"[ERRO] {e}\n")
            finally:
                self.is_running = False

        threading.Thread(target=_runner, daemon=True).start()

    # ==================== Tarefas ====================
    def _task_system_info(self) -> None:
        self.modules["system"].run_diagnostic()

    def _task_dns(self) -> None:
        self.modules["dns"].run_diagnostic()

    def _task_disk_analysis(self) -> None:
        self.modules["disk"].run_diagnostic()

    def _task_disk_check(self) -> None:
        # Mostrar diálogo para escolher tipo de verificação
        if get_os_type() == "windows":
            self._gui_disk_check_windows()
        else:
            self.modules["disk_checker"].check_disk_health_linux()

    def _gui_disk_check_windows(self) -> None:
        def run_choice(choice: str, drive: str) -> None:
            if not drive:
                drive = "C:"
            if not drive.endswith(":"):
                drive = drive + ":"
            if choice == "1":
                self.modules["disk_checker"].run_chkdsk_scan_windows(drive)
            elif choice == "2":
                self.modules["disk_checker"].run_chkdsk_fix_windows(drive)
            elif choice == "3":
                self.modules["disk_checker"].run_chkdsk_full_windows(drive)
            else:
                print("[INFO] Operação cancelada.\n")

        dialog = tk.Toplevel(self)
        dialog.title("Verificação de Disco - Windows")
        dialog.resizable(False, False)
        frm = ttk.Frame(dialog, padding=12)
        frm.grid(row=0, column=0)

        ttk.Label(frm, text="Escolha o tipo de verificação e o drive:").grid(row=0, column=0, columnspan=2, sticky="w")
        choice_var = tk.StringVar(value="1")

        ttk.Radiobutton(frm, text="1) Verificação rápida (chkdsk /scan)", variable=choice_var, value="1").grid(row=1, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(frm, text="2) Verificar e corrigir (chkdsk /F)", variable=choice_var, value="2").grid(row=2, column=0, columnspan=2, sticky="w")
        ttk.Radiobutton(frm, text="3) Completa (chkdsk /F /R) – demorada", variable=choice_var, value="3").grid(row=3, column=0, columnspan=2, sticky="w")

        ttk.Label(frm, text="Drive (ex: C):").grid(row=4, column=0, sticky="e", pady=(8,0))
        drive_var = tk.StringVar(value="C")
        ttk.Entry(frm, textvariable=drive_var, width=6).grid(row=4, column=1, sticky="w", pady=(8,0))

        btns = ttk.Frame(frm)
        btns.grid(row=5, column=0, columnspan=2, pady=(12,0))

        def on_ok():
            dialog.destroy()
            self._run_in_thread(lambda: run_choice(choice_var.get(), drive_var.get().strip()))

        def on_cancel():
            dialog.destroy()

        ttk.Button(btns, text="Executar", command=on_ok).grid(row=0, column=0, padx=(0,8))
        ttk.Button(btns, text="Cancelar", command=on_cancel).grid(row=0, column=1)

    def _task_ram(self) -> None:
        self.modules["ram"].run_diagnostic()

    def _task_driver_updates(self) -> None:
        self.modules["driver_updater"].run_diagnostic()

    # Backup removido

    def _task_temp_analyze(self) -> None:
        self.modules["temp"].analyze_temp_usage()

    def _task_temp_clean(self) -> None:
        # Executa limpeza real SEM simulação
        self.modules["temp"].run_cleanup(dry_run=False)

    def _task_speed(self) -> None:
        self.modules["speed"].run_diagnostic()

    def _task_virus_status(self) -> None:
        # Executa verificações não interativas
        if get_os_type() == "windows":
            self.modules["virus"].check_antivirus_status_windows()
        else:
            self.modules["virus"].check_antivirus_status_linux()
        self.modules["virus"].check_suspicious_processes()
        self.modules["virus"].check_startup_programs()
        self.modules["virus"].check_network_connections()

    def _task_full_diagnostic(self) -> None:
        # Fluxo completo sem prompts de input()
        self.modules["system"].run_diagnostic()
        self.modules["disk"].run_diagnostic()
        self.modules["ram"].run_diagnostic()
        self.modules["dns"].run_diagnostic()
        self.modules["temp"].analyze_temp_usage()
        self.modules["speed"].run_diagnostic()
        self.modules["driver_updater"].run_diagnostic()

        if get_os_type() == "windows":
            self.modules["virus"].check_antivirus_status_windows()
        else:
            self.modules["virus"].check_antivirus_status_linux()
        self.modules["virus"].check_suspicious_processes()
        self.modules["virus"].check_startup_programs()
        self.modules["virus"].check_network_connections()

        # Memória (sem prompts)
        self.modules["memory_tester"].analyze_memory_usage()
        if get_os_type() == "windows":
            self.modules["memory_tester"].check_memory_health_windows()
            self.modules["memory_tester"].check_memory_errors_windows()
        else:
            self.modules["memory_tester"].check_memory_health_linux()
            self.modules["memory_tester"].check_memory_errors_linux()

        # Verificação de disco (somente saúde)
        if get_os_type() == "windows":
            self.modules["disk_checker"].check_disk_health_windows()
        else:
            self.modules["disk_checker"].check_disk_health_linux()

        print("\n[OK] Diagnóstico completo (GUI) finalizado.\n")

    # ==================== Eventos ====================
    def _on_close(self) -> None:
        try:
            sys.stdout = self._orig_stdout
            sys.stderr = self._orig_stderr
        finally:
            self.destroy()


def main() -> None:
    app = TerminalTecGUI()
    app.mainloop()


if __name__ == "__main__":
    main()


