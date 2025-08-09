
import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_module(module_name, module_class):
    """Testar se um módulo pode ser importado e inicializado"""
    try:
        module = module_class()
        print(f"✅ {module_name}: OK")
        return True
    except Exception as e:
        print(f"❌ {module_name}: ERRO - {e}")
        return False

def test_compatibility():
    """Testar compatibilidade do sistema"""
    try:
        from modules.compatibility import SystemCompatibility
        compat = SystemCompatibility()
        result = compat.check_compatibility()
        
        print(f"\n🔧 COMPATIBILIDADE DO SISTEMA")
        print(f"Sistema: {result['os_type']}")
        print(f"Distribuição: {result['distribution']}")
        print(f"Versão: {result['version']}")
        
        if result['compatible']:
            print("✅ Sistema compatível")
        else:
            print("❌ Sistema com problemas de compatibilidade")
            for issue in result['issues']:
                print(f"   ❌ {issue}")
        
        if result['warnings']:
            print("⚠️  Avisos:")
            for warning in result['warnings']:
                print(f"   ⚠️  {warning}")
        
        return result['compatible']
    except Exception as e:
        print(f"❌ Teste de compatibilidade: ERRO - {e}")
        return False

def main():
    print("TESTE DE MODULOS - TerminalTec")
    print("=" * 50)
    
    compatibility_ok = test_compatibility()
    
    modules_to_test = [
        ('DNS Checker', 'modules.dns_checker', 'DNSChecker'),
        ('Disk Analyzer', 'modules.disk_analyzer', 'DiskAnalyzer'),
        ('RAM Monitor', 'modules.ram_monitor', 'RAMMonitor'),
        ('Temp Cleaner', 'modules.temp_cleaner', 'TempCleaner'),
        ('Speed Tester', 'modules.speed_tester', 'SpeedTester'),
        ('System Info', 'modules.system_info', 'SystemInfo'),
        ('Driver Updater', 'modules.driver_updater', 'DriverUpdater'),
        ('Virus Scanner', 'modules.virus_scanner', 'VirusScanner'),
        ('Memory Tester', 'modules.memory_tester', 'MemoryTester'),
        ('Disk Checker', 'modules.disk_checker', 'DiskChecker'),
    ]
    
    successful = 0
    total = len(modules_to_test)
    
    for name, module_path, class_name in modules_to_test:
        try:
            module = __import__(module_path, fromlist=[class_name])
            module_class = getattr(module, class_name)
            
            if test_module(name, module_class):
                successful += 1
                
        except ImportError as e:
            print(f"❌ {name}: ERRO DE IMPORTACAO - {e}")
        except Exception as e:
            print(f"❌ {name}: ERRO GERAL - {e}")
    
    print("=" * 50)
    print(f"Resultado: {successful}/{total} modulos funcionando")
    
    if successful < total or not compatibility_ok:
        print("\n💡 Dicas para resolver problemas:")
        print("1. Execute como administrador")
        print("2. Verifique se todas as dependências estão instaladas")
        print("3. Execute: pip install -r requirements.txt")
        print("4. Verifique se o Python tem permissões adequadas")
        
        if not compatibility_ok:
            print("\n🔧 Para problemas de compatibilidade:")
            print("1. Verifique a versão do seu sistema operacional")
            print("2. Atualize o sistema se necessário")
            print("3. Instale dependências específicas do sistema")

if __name__ == "__main__":
    main() 