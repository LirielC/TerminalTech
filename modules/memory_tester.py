import os
import subprocess
import time
import psutil
from .utils import print_header, print_success, print_error, print_info, print_warning, run_command, get_os_type, create_table, format_bytes

class MemoryTester:
    def __init__(self):
        self.memory_info = {}
        self.test_results = {}
        self.memory_errors = []

    def get_memory_info(self):
        try:
            memory = psutil.virtual_memory()
            self.memory_info = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent,
                'free': memory.free
            }
            return True
        except Exception as e:
            print_error(f"Erro ao obter informações de memória: {e}")
            return False

    def check_memory_health_windows(self):
        try:
            print_info("Verificando saúde da memória RAM...")
            
            success, output, error = run_command("wmic memorychip get capacity,speed,manufacturer,partnumber /format:table")
            if success:
                print_info("Informações dos módulos de memória:")
                print(output)
            
            success, output, error = run_command("wmic memorychip get status /format:table")
            if success:
                print_info("Status dos módulos de memória:")
                print(output)
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar memória: {e}")
            return False

    def check_memory_health_linux(self):
        try:
            print_info("Verificando saúde da memória RAM...")
            
            success, output, error = run_command("dmidecode -t memory")
            if success:
                print_info("Informações detalhadas da memória:")
                print(output)
            
            success, output, error = run_command("cat /proc/meminfo")
            if success:
                print_info("Informações do sistema de memória:")
                print(output)
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar memória: {e}")
            return False

    def run_windows_memory_diagnostic(self):
        try:
            print_info("Iniciando Diagnóstico de Memória do Windows...")
            print_warning("O computador será reiniciado para executar o teste!")
            print_info("O teste será executado durante o boot.")
            
            choice = input("Deseja continuar? (s/n): ").strip().lower()
            if choice == 's':
                success, output, error = run_command("mdsched.exe")
                if success:
                    print_success("Diagnóstico de memória agendado")
                    print_info("O computador será reiniciado para executar o teste")
                    return True
                else:
                    print_error("Erro ao agendar diagnóstico")
                    return False
            else:
                print_info("Operação cancelada")
                return False
        except Exception as e:
            print_error(f"Erro ao executar diagnóstico: {e}")
            return False

    def run_memtester_linux(self, size_mb=100):
        try:
            print_info(f"Executando teste de memória com memtester ({size_mb}MB)...")
            
            success, output, error = run_command(f"memtester {size_mb}M 1")
            if success:
                if "FAILURE" in output:
                    print_error("⚠ Problemas detectados na memória!")
                    self.memory_errors.append("Falha no teste memtester")
                else:
                    print_success("✓ Teste de memória passou!")
                
                self.test_results['memtester'] = output
                return True
            else:
                print_error("Erro ao executar memtester")
                print_info("Instale memtester: sudo apt install memtester")
                return False
        except Exception as e:
            print_error(f"Erro no teste memtester: {e}")
            return False

    def check_memory_errors_windows(self):
        try:
            print_info("Verificando erros de memória no Event Viewer...")
            
            success, output, error = run_command('powershell "Get-WinEvent -FilterHashtable @{LogName=\'System\'; ID=1201,1202,1203,1204,1205,1206,1207,1208,1209,1210} -MaxEvents 10 | Format-Table TimeCreated,Id,Message -Wrap"')
            if success:
                if output.strip():
                    print_warning("Erros de memória encontrados:")
                    print(output)
                else:
                    print_success("✓ Nenhum erro de memória recente encontrado")
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar eventos: {e}")
            return False

    def check_memory_errors_linux(self):
        try:
            print_info("Verificando erros de memória no kernel...")
            
            success, output, error = run_command("dmesg | grep -i 'memory\|ram\|mem' | tail -10")
            if success:
                if output.strip():
                    print_warning("Mensagens relacionadas à memória:")
                    print(output)
                else:
                    print_success("✓ Nenhuma mensagem de erro de memória encontrada")
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar dmesg: {e}")
            return False

    def analyze_memory_usage(self):
        try:
            if not self.get_memory_info():
                return False
            
            print_info("Análise de uso de memória:")
            
            memory_data = [
                ["Total", format_bytes(self.memory_info['total'])],
                ["Usado", format_bytes(self.memory_info['used'])],
                ["Disponível", format_bytes(self.memory_info['available'])],
                ["Livre", format_bytes(self.memory_info['free'])],
                ["Percentual de Uso", f"{self.memory_info['percent']:.1f}%"]
            ]
            
            headers = ["Métrica", "Valor"]
            print(create_table(headers, memory_data))
            
            if self.memory_info['percent'] > 90:
                print_error("⚠ Uso de memória muito alto!")
                print_info("Recomendações:")
                print_info("- Feche programas desnecessários")
                print_info("- Reinicie o computador")
                print_info("- Considere adicionar mais RAM")
            elif self.memory_info['percent'] > 80:
                print_warning("⚠ Uso de memória alto")
                print_info("Considere fechar alguns programas")
            else:
                print_success("✓ Uso de memória normal")
            
            return True
        except Exception as e:
            print_error(f"Erro na análise: {e}")
            return False

    def get_memory_recommendations(self):
        print_header("Recomendações para Memória RAM")
        
        recommendations = [
            "Execute o diagnóstico de memória regularmente",
            "Monitore o uso de memória dos programas",
            "Feche programas desnecessários",
            "Reinicie o computador periodicamente",
            "Considere adicionar mais RAM se o uso for alto",
            "Verifique se os módulos estão bem encaixados",
            "Limpe a poeira dos slots de memória",
            "Use módulos de memória compatíveis",
            "Evite overclocking excessivo da memória",
            "Mantenha o BIOS/UEFI atualizado"
        ]
        
        for i, rec in enumerate(recommendations, 1):
            print_info(f"{i}. {rec}")
        
        return True

    def run_diagnostic(self):
        print_header("🧠 TESTE DE MEMÓRIA RAM")
        print_info("Esta ferramenta verifica:")
        print_info("• Uso atual da memória RAM")
        print_info("• Saúde dos módulos de memória")
        print_info("• Executa testes de integridade")
        print_info("• Identifica erros de memória")
        print_info("• Fornece recomendações de otimização")
        print()
        
        self.analyze_memory_usage()
        
        if get_os_type() == "windows":
            self.check_memory_health_windows()
            self.check_memory_errors_windows()
            
            print_info("\nOpções de teste:")
            print_info("1. Executar Diagnóstico de Memória do Windows")
            print_info("2. Pular teste (apenas análise)")
            
            choice = input("Escolha uma opção (1-2): ").strip()
            
            if choice == "1":
                self.run_windows_memory_diagnostic()
            
        else:
            self.check_memory_health_linux()
            self.check_memory_errors_linux()
            
            print_info("\nOpções de teste:")
            print_info("1. Executar memtester (teste básico)")
            print_info("2. Pular teste (apenas análise)")
            
            choice = input("Escolha uma opção (1-2): ").strip()
            
            if choice == "1":
                size = input("Tamanho do teste em MB (padrão: 100): ").strip()
                try:
                    size_mb = int(size) if size else 100
                    self.run_memtester_linux(size_mb)
                except ValueError:
                    print_error("Valor inválido, usando 100MB")
                    self.run_memtester_linux(100)
        
        self.get_memory_recommendations()
        return True 