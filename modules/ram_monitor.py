import psutil
import time
from .utils import print_header, print_success, print_error, print_info, print_warning, format_bytes, format_percentage, create_table

class RAMMonitor:
    def __init__(self):
        self.memory_info = None
        self.swap_info = None
        self.memory_processes = []

    def get_memory_info(self):
        try:
            self.memory_info = psutil.virtual_memory()
            self.swap_info = psutil.swap_memory()
            return True
        except Exception as e:
            print_error(f"Erro ao obter informações de memória: {e}")
            return False

    def get_top_memory_processes(self, limit=10):
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
                try:
                    proc_info = proc.info
                    if proc_info['memory_info']:
                        processes.append({
                            'pid': proc_info['pid'],
                            'name': proc_info['name'],
                            'memory': proc_info['memory_info'].rss
                        })
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            processes.sort(key=lambda x: x['memory'], reverse=True)
            self.memory_processes = processes[:limit]
            return True
        except Exception as e:
            print_error(f"Erro ao obter processos: {e}")
            return False

    def check_memory_pressure(self):
        if not self.memory_info:
            return "Unknown"
        
        percent = self.memory_info.percent
        
        if percent > 90:
            return "CRÍTICO"
        elif percent > 80:
            return "ALTO"
        elif percent > 70:
            return "MODERADO"
        else:
            return "NORMAL"

    def analyze_memory_fragmentation(self):
        if not self.memory_info:
            return "Unknown"
        
        available = self.memory_info.available
        total = self.memory_info.total
        
        if available < total * 0.1:
            return "ALTA"
        elif available < total * 0.2:
            return "MODERADA"
        else:
            return "BAIXA"

    def get_memory_usage_trend(self, duration=60):
        usage_trend = []
        start_time = time.time()
        
        while time.time() - start_time < duration:
            try:
                memory = psutil.virtual_memory()
                usage_trend.append({
                    'timestamp': time.time(),
                    'percent': memory.percent,
                    'used': memory.used,
                    'available': memory.available
                })
                time.sleep(5)
            except KeyboardInterrupt:
                break
            except Exception:
                break
        
        return usage_trend

    def optimize_memory(self):
        print_info("Otimizando uso de memória...")
        
        if not self.get_top_memory_processes(5):
            return False
        
        print_info("Processos consumindo mais memória:")
        for i, proc in enumerate(self.memory_processes[:5], 1):
            print_info(f"{i}. {proc['name']} (PID: {proc['pid']}) - {format_bytes(proc['memory'])}")
        
        print_info("Sugestões de otimização:")
        print_info("1. Feche aplicações desnecessárias")
        print_info("2. Reinicie aplicações que consomem muita memória")
        print_info("3. Verifique vazamentos de memória em aplicações")
        print_info("4. Considere aumentar a memória virtual")
        
        return True

    def run_diagnostic(self):
        print_header("MONITORAMENTO DE RAM")
        print_info("Esta ferramenta verifica:")
        print_info("• Uso atual de memória")
        print_info("• Processos consumindo mais RAM")
        print_info("• Otimizações possíveis")
        print_info("• Recomendações de performance")
        print()
        
        if not self.get_memory_info():
            return False

        if not self.get_top_memory_processes():
            return False

        print_info("Informações Gerais de Memória:")
        memory_data = [
            ["Total", format_bytes(self.memory_info.total)],
            ["Disponível", format_bytes(self.memory_info.available)],
            ["Usado", format_bytes(self.memory_info.used)],
            ["Percentual de Uso", f"{self.memory_info.percent:.1f}%"],
            ["Pressão de Memória", self.check_memory_pressure()],
            ["Fragmentação", self.analyze_memory_fragmentation()]
        ]
        
        headers = ["Métrica", "Valor"]
        print(create_table(headers, memory_data))

        if self.swap_info:
            print_info("Informações de Swap:")
            swap_data = [
                ["Total", format_bytes(self.swap_info.total)],
                ["Usado", format_bytes(self.swap_info.used)],
                ["Livre", format_bytes(self.swap_info.free)],
                ["Percentual", f"{self.swap_info.percent:.1f}%"]
            ]
            print(create_table(headers, swap_data))

        print_info("Top 10 Processos por Uso de Memória:")
        process_data = []
        for i, proc in enumerate(self.memory_processes, 1):
            process_data.append([
                i,
                proc['name'][:30],
                proc['pid'],
                format_bytes(proc['memory']),
                format_percentage(proc['memory'], self.memory_info.total)
            ])
        
        headers = ["#", "Processo", "PID", "Memória", "% do Total"]
        print(create_table(headers, process_data))

        print_info("Análise de Performance:")
        pressure = self.check_memory_pressure()
        if pressure == "CRÍTICO":
            print_error("Memória em estado crítico - ação imediata necessária")
        elif pressure == "ALTO":
            print_warning("Uso de memória alto - considere otimizar")
        else:
            print_success("Uso de memória normal")

        fragmentation = self.analyze_memory_fragmentation()
        if fragmentation == "ALTA":
            print_warning("Fragmentação de memória alta detectada")
        elif fragmentation == "MODERADA":
            print_info("Fragmentação de memória moderada")
        else:
            print_success("Fragmentação de memória baixa")

        return True

    def monitor_realtime(self, duration=300):
        print_header("Monitoramento em Tempo Real")
        print_info(f"Monitorando por {duration} segundos... (Ctrl+C para parar)")
        
        try:
            start_time = time.time()
            while time.time() - start_time < duration:
                if self.get_memory_info():
                    percent = self.memory_info.percent
                    available = format_bytes(self.memory_info.available)
                    
                    print(f"\rUso: {percent:.1f}% | Disponível: {available}", end="", flush=True)
                
                time.sleep(2)
            
            print()
            print_success("Monitoramento concluído")
            
        except KeyboardInterrupt:
            print()
            print_info("Monitoramento interrompido pelo usuário")
        
        return True 