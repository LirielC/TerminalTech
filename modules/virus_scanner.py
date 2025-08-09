import os
import subprocess
import time
from .utils import print_header, print_success, print_error, print_info, print_warning, run_command, get_os_type, create_table

class VirusScanner:
    def __init__(self):
        self.scan_results = {}
        self.antivirus_status = {}
        self.threats_found = []

    def check_antivirus_status_windows(self):
        try:
            print_info("Verificando status do antivírus...")
            
            antivirus_services = [
                "WinDefend",
                "McAfeeFramework",
                "McAfeeEngine",
                "McAfeeDLPAgent",
                "McAfeeVSEForShield",
                "McAfeeVSEForShield64",
                "Symantec AntiVirus",
                "Norton AntiVirus",
                "Avast Antivirus",
                "AVG Antivirus"
            ]
            
            active_antivirus = []
            
            for service in antivirus_services:
                success, output, error = run_command(f"sc query {service}")
                if success and "RUNNING" in output:
                    active_antivirus.append(service)
                    print_success(f"✓ {service} - Ativo")
                else:
                    print_warning(f"✗ {service} - Inativo")
            
            if not active_antivirus:
                print_warning("Nenhum antivírus ativo detectado!")
                print_info("Recomendações:")
                print_info("1. Ative o Windows Defender")
                print_info("2. Instale um antivírus de terceiros")
                print_info("3. Mantenha o sistema atualizado")
            
            self.antivirus_status = {'active': active_antivirus}
            return True
        except Exception as e:
            print_error(f"Erro ao verificar antivírus: {e}")
            return False

    def check_antivirus_status_linux(self):
        try:
            print_info("Verificando antivírus no Linux...")
            
            antivirus_commands = [
                ("clamscan", "ClamAV"),
                ("sophos", "Sophos"),
                ("avast", "Avast"),
                ("eset", "ESET"),
                ("kaspersky", "Kaspersky")
            ]
            
            active_antivirus = []
            
            for command, name in antivirus_commands:
                success, output, error = run_command(f"{command} --version")
                if success:
                    active_antivirus.append(name)
                    print_success(f"✓ {name} - Instalado")
                else:
                    print_warning(f"✗ {name} - Não instalado")
            
            if not active_antivirus:
                print_warning("Nenhum antivírus instalado!")
                print_info("Recomendações:")
                print_info("1. Instale ClamAV: sudo apt install clamav")
                print_info("2. Configure varreduras automáticas")
                print_info("3. Mantenha o sistema atualizado")
            
            self.antivirus_status = {'active': active_antivirus}
            return True
        except Exception as e:
            print_error(f"Erro ao verificar antivírus: {e}")
            return False

    def run_quick_scan_windows(self):
        try:
            print_info("Iniciando varredura rápida com Windows Defender...")
            
            success, output, error = run_command('powershell "Start-MpScan -ScanType QuickScan"')
            if success:
                print_success("Varredura rápida iniciada")
                print_info("A varredura está sendo executada em segundo plano")
                print_info("Verifique os resultados no Windows Security")
                return True
            else:
                print_error("Erro ao iniciar varredura")
                return False
        except Exception as e:
            print_error(f"Erro na varredura: {e}")
            return False

    def run_full_scan_windows(self):
        try:
            print_info("Iniciando varredura completa com Windows Defender...")
            print_warning("Esta operação pode demorar várias horas!")
            
            success, output, error = run_command('powershell "Start-MpScan -ScanType FullScan"')
            if success:
                print_success("Varredura completa iniciada")
                print_info("A varredura está sendo executada em segundo plano")
                print_info("Verifique os resultados no Windows Security")
                return True
            else:
                print_error("Erro ao iniciar varredura completa")
                return False
        except Exception as e:
            print_error(f"Erro na varredura: {e}")
            return False

    def run_clamav_scan_linux(self, path="/"):
        try:
            print_info(f"Iniciando varredura com ClamAV em {path}...")
            
            success, output, error = run_command(f"clamscan -r --infected {path}")
            if success:
                if "Infected files: 0" in output:
                    print_success("✓ Nenhuma ameaça encontrada!")
                else:
                    print_error("⚠ Ameaças encontradas!")
                    print(output)
                
                self.scan_results['clamav'] = output
                return True
            else:
                print_error("Erro ao executar ClamAV")
                print_info("Instale ClamAV: sudo apt install clamav")
                return False
        except Exception as e:
            print_error(f"Erro na varredura ClamAV: {e}")
            return False

    def check_suspicious_processes(self):
        try:
            print_info("Verificando processos suspeitos...")
            
            if get_os_type() == "windows":
                success, output, error = run_command('powershell "Get-Process | Where-Object {$_.CPU -gt 50} | Select-Object Name,CPU,WorkingSet | Format-Table"')
                if success:
                    print_info("Processos com alto uso de CPU:")
                    print(output)
                
                success, output, error = run_command('powershell "Get-Process | Where-Object {$_.WorkingSet -gt 500MB} | Select-Object Name,CPU,WorkingSet | Format-Table"')
                if success:
                    print_info("Processos com alto uso de memória:")
                    print(output)
            else:
                success, output, error = run_command("ps aux --sort=-%cpu | head -10")
                if success:
                    print_info("Top 10 processos por CPU:")
                    print(output)
                
                success, output, error = run_command("ps aux --sort=-%mem | head -10")
                if success:
                    print_info("Top 10 processos por memória:")
                    print(output)
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar processos: {e}")
            return False

    def check_startup_programs(self):
        try:
            print_info("Verificando programas de inicialização...")
            
            if get_os_type() == "windows":
                success, output, error = run_command('powershell "Get-CimInstance Win32_StartupCommand | Select-Object Name,Location,Command | Format-Table"')
                if success:
                    print_info("Programas de inicialização:")
                    print(output)
            else:
                success, output, error = run_command("systemctl list-unit-files --type=service --state=enabled")
                if success:
                    print_info("Serviços habilitados:")
                    print(output)
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar inicialização: {e}")
            return False

    def check_network_connections(self):
        try:
            print_info("Verificando conexões de rede suspeitas...")
            
            if get_os_type() == "windows":
                success, output, error = run_command("netstat -ano | findstr ESTABLISHED")
                if success:
                    print_info("Conexões estabelecidas:")
                    print(output)
            else:
                success, output, error = run_command("netstat -tuln")
                if success:
                    print_info("Conexões de rede:")
                    print(output)
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar rede: {e}")
            return False

    def run_diagnostic(self):
        print_header("VERIFICACAO DE VIRUS E SEGURANCA")
        print_info("Esta ferramenta verifica:")
        print_info("• Status do antivírus instalado")
        print_info("• Executa varredura de malware")
        print_info("• Analisa processos suspeitos")
        print_info("• Verifica programas de inicialização")
        print_info("• Monitora conexões de rede")
        print()
        
        if get_os_type() == "windows":
            self.check_antivirus_status_windows()
            print_info("\nOpções de varredura:")
            print_info("1. Varredura rápida (recomendado)")
            print_info("2. Varredura completa (demora mais)")
            
            choice = input("Escolha uma opção (1-2) ou Enter para pular: ").strip()
            
            if choice == "1":
                self.run_quick_scan_windows()
            elif choice == "2":
                self.run_full_scan_windows()
            
            print_info("\nVerificações adicionais:")
            self.check_suspicious_processes()
            self.check_startup_programs()
            self.check_network_connections()
            
        else:
            self.check_antivirus_status_linux()
            
            if "ClamAV" in self.antivirus_status.get('active', []):
                choice = input("Executar varredura com ClamAV? (s/n): ").strip().lower()
                if choice == 's':
                    self.run_clamav_scan_linux()
            
            print_info("\nVerificações adicionais:")
            self.check_suspicious_processes()
            self.check_startup_programs()
            self.check_network_connections()
        
        return True

    def get_security_recommendations(self):
        print_header("Recomendações de Segurança")
        
        recommendations = [
            "Mantenha o sistema operacional sempre atualizado",
            "Use um antivírus confiável e mantenha-o atualizado",
            "Não abra anexos de emails suspeitos",
            "Não clique em links suspeitos",
            "Use senhas fortes e únicas",
            "Ative a autenticação de dois fatores quando possível",
            "Faça backup regular dos seus dados",
            "Use firewall e mantenha-o ativo",
            "Evite usar redes Wi-Fi públicas sem VPN",
            "Monitore regularmente as atividades do sistema"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print_info(f"{i}. {rec}")
        
        return True 