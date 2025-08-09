import os
import subprocess
import time
from .utils import print_header, print_success, print_error, print_info, print_warning, run_command, get_os_type, create_table, is_admin

class DiskChecker:
    def __init__(self):
        self.check_results = {}
        self.disk_errors = []

    def run_chkdsk_windows(self, drive="C:"):
        try:
            print_info(f"Executando CHKDSK em {drive}...")
            print_warning("Esta operação pode demorar!")
            
            success, output, error = run_command(f"chkdsk {drive} /F /R")
            if success:
                print_success("CHKDSK executado com sucesso")
                print(output)
                self.check_results['chkdsk'] = output
                return True
            else:
                print_error("Erro ao executar CHKDSK")
                return False
        except Exception as e:
            print_error(f"Erro no CHKDSK: {e}")
            return False

    def run_chkdsk_scan_windows(self, drive="C:"):
        try:
            print_info(f"Executando verificação rápida em {drive} (/scan)...")
            if not is_admin():
                print_warning("Permissões elevadas recomendadas para chkdsk. Execute como Administrador.")
            try:
                result = subprocess.run(
                    f"chkdsk {drive} /scan",
                    shell=True,
                    capture_output=True,
                    text=True,
                    timeout=300
                )
                if result.returncode == 0:
                    print_success("Verificação rápida concluída")
                    print(result.stdout)
                    return True
                else:
                    print_warning("Falha no chkdsk /scan; tentando chkdsk simples (somente leitura)")
                    ok, out, err = run_command(f"chkdsk {drive}")
                    if ok:
                        print_success("Verificação concluída")
                        print(out)
                        return True
                    # Mostrar stderr se houver
                    if err:
                        print_error(err)
                    print_error("Erro ao verificar disco (sem privilégios ou volume bloqueado)")
                    return False
            except subprocess.TimeoutExpired:
                print_warning("Verificação /scan demorou demais e foi interrompida")
                return False
        except Exception as e:
            print_error(f"Erro no chkdsk /scan: {e}")
            return False

    def run_chkdsk_fix_windows(self, drive="C:"):
        try:
            print_warning("Executando chkdsk /F (pode agendar para o próximo boot)")
            if not is_admin():
                print_warning("Sem administrador, o Windows pode apenas AGENDAR a correção para o próximo boot.")
            result = subprocess.run(
                f"chkdsk {drive} /F",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_success("Verificação /F concluída/agendada")
                print(result.stdout)
                return True
            else:
                print_error("Erro ao executar chkdsk /F")
                print(result.stdout or result.stderr)
                return False
        except Exception as e:
            print_error(f"Erro no chkdsk /F: {e}")
            return False

    def run_chkdsk_full_windows(self, drive="C:"):
        try:
            print_warning("Executando chkdsk /F /R (muito demorado; verifica setores defeituosos)")
            if not is_admin():
                print_warning("Sem administrador, o Windows deve AGENDAR esta verificação para o próximo boot.")
            result = subprocess.run(
                f"chkdsk {drive} /F /R",
                shell=True,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                print_success("Verificação /F /R concluída/agendada")
                print(result.stdout)
                return True
            else:
                print_error("Erro ao executar chkdsk /F /R")
                print(result.stdout or result.stderr)
                return False
        except Exception as e:
            print_error(f"Erro no chkdsk /F /R: {e}")
            return False

    def run_fsck_linux(self, device="/dev/sda1"):
        try:
            print_info(f"Verificando sistema de arquivos em {device}...")
            print_warning("Esta operação requer que a partição esteja desmontada!")
            
            success, output, error = run_command(f"fsck -f {device}")
            if success:
                print_success("Verificação concluída")
                print(output)
                self.check_results['fsck'] = output
                return True
            else:
                print_error("Erro na verificação")
                return False
        except Exception as e:
            print_error(f"Erro no fsck: {e}")
            return False

    def check_disk_health_windows(self):
        try:
            print_info("Verificando saúde do disco...")

            # Preferir PowerShell (mais confiável/rápido) e fazer fallback para WMIC
            ps_health = (
                'powershell -NoProfile -ExecutionPolicy Bypass '
                '"Get-PhysicalDisk | Select-Object FriendlyName, HealthStatus, Size, MediaType | Format-Table -AutoSize"'
            )
            success, output, error = run_command(ps_health)
            if success and output.strip():
                print_info("Status (Get-PhysicalDisk):")
                print(output)
            else:
                success2, output2, error2 = run_command("wmic diskdrive get model,size,status /format:table")
                if success2:
                    print_info("Informações dos discos (WMIC):")
                    print(output2)
                else:
                    print_warning("Não foi possível obter status via PowerShell/WMIC")

            return True
        except Exception as e:
            print_error(f"Erro ao verificar saúde: {e}")
            return False

    def check_disk_health_linux(self):
        try:
            print_info("Verificando saúde do disco...")
            
            success, output, error = run_command("smartctl -a /dev/sda")
            if success:
                print_info("Informações SMART do disco:")
                print(output)
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar saúde: {e}")
            return False

    def run_diagnostic(self):
        print_header("VERIFICACAO DE DISCO (CHECK DISK)")
        print_info("Esta ferramenta verifica:")
        print_info("• Saúde física dos discos")
        print_info("• Integridade do sistema de arquivos")
        print_info("• Corrige erros de disco")
        print_info("• Identifica setores danificados")
        print()
        
        if get_os_type() == "windows":
            self.check_disk_health_windows()
            
            print_info("\nOpções de verificação:")
            print_info("1. Verificação rápida (chkdsk /scan)")
            print_info("2. Verificar e corrigir (chkdsk /F)")
            print_info("3. Verificação completa (chkdsk /F /R) – demorada")
            print_info("4. Pular verificação")
            
            choice = input("Escolha uma opção (1-4): ").strip()
            
            if choice in {"1", "2", "3"}:
                drive = input("Drive para verificar (padrão: C:): ").strip() or "C:"
                if not drive.endswith(":"):
                    drive = drive + ":"
                if choice == "1":
                    # chkdsk /scan é mais rápido e não bloqueia volume
                    try:
                        print_info(f"Executando: chkdsk {drive} /scan")
                        result = subprocess.run(
                            f"chkdsk {drive} /scan",
                            shell=True,
                            capture_output=True,
                            text=True,
                            timeout=300
                        )
                        if result.returncode == 0:
                            print_success("Verificação rápida concluída")
                            print(result.stdout)
                        else:
                            print_warning("Falha no chkdsk /scan; tentando chkdsk simples")
                            ok, out, err = run_command(f"chkdsk {drive}")
                            if ok:
                                print_success("Verificação concluída")
                                print(out)
                            else:
                                print_error("Erro ao verificar disco")
                    except subprocess.TimeoutExpired:
                        print_warning("Verificação /scan demorou demais e foi interrompida")
                elif choice == "2":
                    # Correção de erros (/F) – pode agendar no próximo boot
                    try:
                        print_warning("Isso pode exigir agendamento e reinicialização")
                        result = subprocess.run(
                            f"chkdsk {drive} /F",
                            shell=True,
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            print_success("Verificação /F concluída/agenda realizada")
                            print(result.stdout)
                        else:
                            print_error("Erro ao executar chkdsk /F")
                            print(result.stdout or result.stderr)
                    except Exception as e:
                        print_error(f"Erro: {e}")
                elif choice == "3":
                    # Completa (/F /R) – MUITO demorada
                    print_warning("/R verifica setores defeituosos, pode levar horas")
                    try:
                        result = subprocess.run(
                            f"chkdsk {drive} /F /R",
                            shell=True,
                            capture_output=True,
                            text=True
                        )
                        if result.returncode == 0:
                            print_success("Verificação completa concluída/agendada")
                            print(result.stdout)
                        else:
                            print_error("Erro ao executar chkdsk /F /R")
                            print(result.stdout or result.stderr)
                    except Exception as e:
                        print_error(f"Erro: {e}")
            
        else:
            self.check_disk_health_linux()
            
            print_info("\nOpções de verificação:")
            print_info("1. Executar fsck (requer desmontar)")
            print_info("2. Verificar apenas")
            print_info("3. Pular verificação")
            
            choice = input("Escolha uma opção (1-3): ").strip()
            
            if choice == "1":
                device = input("Dispositivo para verificar (padrão: /dev/sda1): ").strip() or "/dev/sda1"
                self.run_fsck_linux(device)
            elif choice == "2":
                device = input("Dispositivo para verificar (padrão: /dev/sda1): ").strip() or "/dev/sda1"
                success, output, error = run_command(f"fsck -n {device}")
                if success:
                    print_success("Verificação concluída")
                    print(output)
        
        return True 