import os
import sys
import platform
import subprocess
import ctypes
from colorama import init, Fore, Back, Style
from tabulate import tabulate

init(autoreset=True)

class TerminalColors:
    HEADER = Fore.CYAN + Style.BRIGHT
    SUCCESS = Fore.GREEN + Style.BRIGHT
    WARNING = Fore.YELLOW + Style.BRIGHT
    ERROR = Fore.RED + Style.BRIGHT
    INFO = Fore.BLUE + Style.BRIGHT
    RESET = Style.RESET_ALL

def print_header(title):
    print(f"\n{TerminalColors.HEADER}{'='*60}")
    print(f"{title:^60}")
    print(f"{'='*60}{TerminalColors.RESET}\n")

def print_success(message):
    print(f"{TerminalColors.SUCCESS}[OK] {message}{TerminalColors.RESET}")

def print_warning(message):
    print(f"{TerminalColors.WARNING}[!] {message}{TerminalColors.RESET}")

def print_error(message):
    print(f"{TerminalColors.ERROR}[ERRO] {message}{TerminalColors.RESET}")

def print_info(message):
    print(f"{TerminalColors.INFO}[INFO] {message}{TerminalColors.RESET}")

def get_os_type():
    return platform.system().lower()

def is_windows():
    return get_os_type() == "windows"

def is_linux():
    return get_os_type() == "linux"

def is_macos():
    return get_os_type() == "darwin"

def run_command(command, shell=True):
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return False, "", "Comando expirou"
    except Exception as e:
        return False, "", str(e)

def format_bytes(bytes_value):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"

def format_percentage(value, total):
    if total == 0:
        return "0.00%"
    return f"{(value / total) * 100:.2f}%"

def create_table(headers, data):
    return tabulate(data, headers=headers, tablefmt="grid")

def get_user_confirmation(message="Deseja continuar? (s/n): "):
    while True:
        response = input(message).lower().strip()
        if response in ['s', 'sim', 'y', 'yes']:
            return True
        elif response in ['n', 'não', 'nao', 'no']:
            return False
        print("Por favor, responda com 's' para sim ou 'n' para não.")

def ensure_directory_exists(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        return True
    return False

def get_safe_filename(filename):
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename 

def is_admin():
    try:
        if is_windows():
            try:
                return ctypes.windll.shell32.IsUserAnAdmin() != 0
            except Exception:
                return False
        else:
            return os.geteuid() == 0  # type: ignore[attr-defined]
    except Exception:
        return False