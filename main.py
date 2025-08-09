#!/usr/bin/env python3

import sys
import argparse
from modules.utils import print_header, print_success, print_error, print_info, print_warning, get_user_confirmation
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

class TerminalTec:
    def __init__(self):
        self.modules = {
            'dns': DNSChecker(),
            'disk': DiskAnalyzer(),
            'ram': RAMMonitor(),
            'temp': TempCleaner(),
            'speed': SpeedTester(),
            'system': SystemInfo(),
            'driver_updater': DriverUpdater(),
            'virus': VirusScanner(),
            'memory_tester': MemoryTester(),
            'disk_checker': DiskChecker()
        }

    def show_menu(self):
        print_header("TerminalTec - Ferramenta para Técnicos")
        print("FERRAMENTAS PRINCIPAIS:")
        print("1.  Diagnostico Completo (Recomendado)")
        print("2.  Verificar Virus e Seguranca")
        print("3.  Verificar Disco (Check Disk)")
        print("4.  Testar Memoria RAM")
        print("5.  Buscar Drivers Recentes")
        print()
        print("FERRAMENTAS DE ANALISE:")
        print("6.  Diagnostico de DNS")
        print("7.  Analise de Disco")
        print("8.  Monitoramento de RAM")
        print("9.  Informacoes do Sistema")
        print("10. Teste de Velocidade")
        print()
        print("FERRAMENTAS DE MANUTENCAO:")
        print("11. Limpeza de Arquivos Temporarios")
        print()
        print("SAIR:")
        print("12. Sair do Programa")
        print()

    def run_dns_diagnostic(self):
        dns_checker = self.modules['dns']
        dns_checker.run_diagnostic()
        
        if get_user_confirmation("Deseja tentar corrigir problemas de DNS? (s/n): "):
            dns_checker.fix_dns_issues()

    def run_disk_analysis(self):
        disk_analyzer = self.modules['disk']
        disk_analyzer.run_diagnostic()
        
        if get_user_confirmation("Deseja ver sugestões de limpeza? (s/n): "):
            disk_analyzer.cleanup_suggestions()

    def run_ram_monitoring(self):
        ram_monitor = self.modules['ram']
        ram_monitor.run_diagnostic()
        
        if get_user_confirmation("Deseja otimizar o uso de memória? (s/n): "):
            ram_monitor.optimize_memory()

    def run_driver_backup(self):
        print_error("Funcionalidade de backup de drivers removida.")

    def run_temp_cleanup(self):
        temp_cleaner = self.modules['temp']
        
        print_header("LIMPEZA DE ARQUIVOS TEMPORARIOS")
        print_info("Esta ferramenta permite:")
        print_info("• Identificar arquivos temporários")
        print_info("• Simular limpeza (sem remover)")
        print_info("• Executar limpeza real")
        print_info("• Liberar espaço em disco")
        print()
        print("Opções de limpeza:")
        print("1. Simular limpeza (sem remover arquivos)")
        print("2. Executar limpeza real")
        print("3. Diagnóstico de arquivos temporários")
        
        choice = input("Escolha uma opção (1-3): ").strip()
        
        if choice == "1":
            temp_cleaner.run_cleanup(dry_run=True)
        elif choice == "2":
            if get_user_confirmation("ATENÇÃO: Isso irá remover arquivos temporários. Continuar? (s/n): "):
                temp_cleaner.run_cleanup(dry_run=False)
        elif choice == "3":
            temp_cleaner.run_diagnostic()
        else:
            print_error("Opção inválida")

    def run_speed_test(self):
        speed_tester = self.modules['speed']
        
        print("Opções de teste de velocidade:")
        print("1. Teste de velocidade de disco")
        print("2. Teste de velocidade da internet")
        print("3. Benchmark completo de disco")
        print("4. Diagnóstico completo de performance")
        
        choice = input("Escolha uma opção (1-4): ").strip()
        
        if choice == "1":
            speed_tester.run_disk_speed_test()
        elif choice == "2":
            speed_tester.run_internet_speed_test()
        elif choice == "3":
            speed_tester.benchmark_disk_performance()
        elif choice == "4":
            speed_tester.run_diagnostic()
        else:
            print_error("Opção inválida")

    def run_system_info(self):
        system_info = self.modules['system']
        system_info.run_diagnostic()

    def run_driver_updater(self):
        driver_updater = self.modules['driver_updater']
        driver_updater.run_diagnostic()

    def run_virus_scanner(self):
        virus_scanner = self.modules['virus']
        virus_scanner.run_diagnostic()

    def run_memory_tester(self):
        memory_tester = self.modules['memory_tester']
        memory_tester.run_diagnostic()

    def run_disk_checker(self):
        disk_checker = self.modules['disk_checker']
        disk_checker.run_diagnostic()

    def run_complete_diagnostic(self):
        print_header("DIAGNOSTICO COMPLETO DO SISTEMA")
        print_info("Esta ferramenta executa TODAS as verificações:")
        print_info("• Informações do sistema")
        print_info("• Análise de disco e espaço")
        print_info("• Monitoramento de RAM")
        print_info("• Diagnóstico de DNS")
        print_info("• Análise de arquivos temporários")
        print_info("• Teste de performance")
        print_info("• Verificação de drivers")
        print_info("• Verificação de vírus")
        print_info("• Teste de memória RAM")
        print_info("• Verificação de disco")
        print()
        print_warning("Este processo pode demorar varios minutos!")
        print()
        
        print_info("Iniciando diagnóstico completo...")
        
        print_info("1. Informações do Sistema...")
        self.modules['system'].run_diagnostic()
        
        print_info("2. Análise de Disco...")
        self.modules['disk'].run_diagnostic()
        
        print_info("3. Monitoramento de RAM...")
        self.modules['ram'].run_diagnostic()
        
        print_info("4. Diagnóstico de DNS...")
        self.modules['dns'].run_diagnostic()
        
        print_info("5. Análise de Arquivos Temporários...")
        self.modules['temp'].run_diagnostic()
        
        print_info("6. Teste de Performance...")
        self.modules['speed'].run_diagnostic()
        
        print_info("7. Verificação de Drivers...")
        self.modules['driver_updater'].run_diagnostic()
        
        print_info("8. Verificação de Vírus...")
        self.modules['virus'].run_diagnostic()
        
        print_info("9. Teste de Memória RAM...")
        self.modules['memory_tester'].run_diagnostic()
        
        print_info("10. Verificação de Disco...")
        self.modules['disk_checker'].run_diagnostic()
        
        print_success("Diagnóstico completo concluído!")

    def run_interactive_mode(self):
        while True:
            try:
                self.show_menu()
                choice = input("Digite sua escolha (1-13): ").strip()
                
                if choice == "1":
                    self.run_complete_diagnostic()
                elif choice == "2":
                    self.run_virus_scanner()
                elif choice == "3":
                    self.run_disk_checker()
                elif choice == "4":
                    self.run_memory_tester()
                elif choice == "5":
                    self.run_driver_updater()
                elif choice == "6":
                    self.run_dns_diagnostic()
                elif choice == "7":
                    self.run_disk_analysis()
                elif choice == "8":
                    self.run_ram_monitoring()
                elif choice == "9":
                    self.run_system_info()
                elif choice == "10":
                    self.run_speed_test()
                elif choice == "11":
                    self.run_temp_cleanup()
                elif choice == "12":
                    print_success("Saindo do TerminalTec...")
                    break
                else:
                    print_error("Opção inválida. Tente novamente.")
                
                if choice != "12":
                    input("\nPressione Enter para continuar...")
                    
            except KeyboardInterrupt:
                print("\n")
                print_info("Operação cancelada pelo usuário.")
                break
            except Exception as e:
                print_error(f"Erro inesperado: {e}")

def main():
    parser = argparse.ArgumentParser(description="TerminalTec - Ferramenta para Técnicos de Computadores")
    parser.add_argument("--dns", action="store_true", help="Executar diagnóstico de DNS")
    parser.add_argument("--disk", action="store_true", help="Executar análise de disco")
    parser.add_argument("--ram", action="store_true", help="Executar monitoramento de RAM")
    # Removido: backup de drivers
    parser.add_argument("--clean-temp", action="store_true", help="Executar limpeza de arquivos temporários")
    parser.add_argument("--speed-test", action="store_true", help="Executar teste de velocidade")
    parser.add_argument("--internet-test", action="store_true", help="Executar teste de velocidade da internet")
    parser.add_argument("--system-info", action="store_true", help="Exibir informações do sistema")
    parser.add_argument("--driver-update", action="store_true", help="Buscar drivers recentes")
    parser.add_argument("--virus-scan", action="store_true", help="Verificar vírus")
    parser.add_argument("--memory-test", action="store_true", help="Testar memória RAM")
    parser.add_argument("--disk-check", action="store_true", help="Verificar disco (check disk)")
    parser.add_argument("--all", action="store_true", help="Executar diagnóstico completo")
    
    args = parser.parse_args()
    
    terminal_tec = TerminalTec()
    
    if any([args.dns, args.disk, args.ram, args.clean_temp, 
            args.speed_test, args.internet_test, args.system_info, args.driver_update,
            args.virus_scan, args.memory_test, args.disk_check, args.all]):
        
        if args.dns:
            terminal_tec.run_dns_diagnostic()
        if args.disk:
            terminal_tec.run_disk_analysis()
        if args.ram:
            terminal_tec.run_ram_monitoring()
        # Backup de drivers removido
        if args.clean_temp:
            terminal_tec.run_temp_cleanup()
        if args.speed_test:
            terminal_tec.run_speed_test()
        if args.internet_test:
            terminal_tec.modules['speed'].run_internet_speed_test()
        if args.system_info:
            terminal_tec.run_system_info()
        if args.driver_update:
            terminal_tec.run_driver_updater()
        if args.virus_scan:
            terminal_tec.run_virus_scanner()
        if args.memory_test:
            terminal_tec.run_memory_tester()
        if args.disk_check:
            terminal_tec.run_disk_checker()
        if args.all:
            terminal_tec.run_complete_diagnostic()
    else:
        terminal_tec.run_interactive_mode()

if __name__ == "__main__":
    main() 