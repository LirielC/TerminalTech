import os
import psutil
import shutil
import time
from .utils import print_header, print_success, print_error, print_info, print_warning, format_bytes, format_percentage, create_table, run_command, get_os_type

class DiskAnalyzer:
    def __init__(self):
        self.disk_partitions = []
        self.disk_usage = {}
        self.disk_health = {}

    def get_disk_partitions(self):
        try:
            partitions = psutil.disk_partitions()
            self.disk_partitions = [p for p in partitions if p.device and p.mountpoint]
            return True
        except Exception as e:
            print_error(f"Erro ao obter partições: {e}")
            return False

    def analyze_disk_usage(self):
        self.disk_usage = {}
        
        for partition in self.disk_partitions:
            try:
                usage = psutil.disk_usage(partition.mountpoint)
                self.disk_usage[partition.device] = {
                    'mountpoint': partition.mountpoint,
                    'total': usage.total,
                    'used': usage.used,
                    'free': usage.free,
                    'percent': usage.percent
                }
            except Exception as e:
                print_warning(f"Erro ao analisar {partition.device}: {e}")

    def check_disk_health(self):
        self.disk_health = {}
        
        for partition in self.disk_partitions:
            device = partition.device
            health_info = {'status': 'Unknown', 'details': []}
            
            if get_os_type() == "windows":
                success, output, error = run_command(f"wmic diskdrive get status")
                if success and "OK" in output:
                    health_info['status'] = 'OK'
                else:
                    health_info['status'] = 'Warning'
            else:
                success, output, error = run_command(f"smartctl -H {device}")
                if success:
                    if "PASSED" in output:
                        health_info['status'] = 'OK'
                    elif "FAILED" in output:
                        health_info['status'] = 'FAILED'
                    else:
                        health_info['status'] = 'Warning'
                else:
                    health_info['status'] = 'Unknown'
            
            self.disk_health[device] = health_info

    def get_large_files(self, path, limit=10):
        large_files = []
        try:
            for root, dirs, files in os.walk(path):
                if len(large_files) >= limit * 2:
                    break
                for file in files:
                    if len(large_files) >= limit * 2:
                        break
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            file_size = os.path.getsize(file_path)
                            if file_size > 100 * 1024 * 1024:
                                large_files.append((file_path, file_size))
                    except (OSError, PermissionError, FileNotFoundError):
                        continue
        except (OSError, PermissionError):
            pass
        
        large_files.sort(key=lambda x: x[1], reverse=True)
        return large_files[:limit]

    def get_old_files(self, path, days=30, limit=10):
        import datetime
        old_files = []
        cutoff_time = time.time() - (days * 24 * 60 * 60)
        
        try:
            for root, dirs, files in os.walk(path):
                if len(old_files) >= limit * 2:
                    break
                for file in files:
                    if len(old_files) >= limit * 2:
                        break
                    try:
                        file_path = os.path.join(root, file)
                        if os.path.isfile(file_path):
                            file_time = os.path.getmtime(file_path)
                            if file_time < cutoff_time:
                                old_files.append((file_path, file_time))
                    except (OSError, PermissionError, FileNotFoundError):
                        continue
        except (OSError, PermissionError):
            pass
        
        old_files.sort(key=lambda x: x[1])
        return old_files[:limit]

    def defragment_disk(self, drive_letter):
        if get_os_type() == "windows":
            print_info(f"Desfragmentando disco {drive_letter}...")
            success, output, error = run_command(f"defrag {drive_letter}: /A")
            if success:
                print_success(f"Desfragmentação iniciada para {drive_letter}")
            else:
                print_error(f"Erro na desfragmentação de {drive_letter}")
            return success
        else:
            print_warning("Desfragmentação automática não disponível no Linux")
            return False

    def run_diagnostic(self):
        print_header("ANALISE DE DISCO")
        print_info("Esta ferramenta verifica:")
        print_info("• Espaço disponível em disco")
        print_info("• Arquivos grandes e antigos")
        print_info("• Saúde das partições")
        print_info("• Sugestões de limpeza")
        print()
        
        if not self.get_disk_partitions():
            return False

        self.analyze_disk_usage()
        self.check_disk_health()

        print_info("Informações das Partições:")
        partition_data = []
        for partition in self.disk_partitions:
            device = partition.device
            if device in self.disk_usage:
                usage = self.disk_usage[device]
                health = self.disk_health.get(device, {'status': 'Unknown'})
                
                partition_data.append([
                    device,
                    partition.mountpoint,
                    format_bytes(usage['total']),
                    format_bytes(usage['used']),
                    format_bytes(usage['free']),
                    f"{usage['percent']:.1f}%",
                    health['status']
                ])

        headers = ["Dispositivo", "Ponto de Montagem", "Total", "Usado", "Livre", "Uso", "Saúde"]
        print(create_table(headers, partition_data))

        print_info("Análise de Espaço:")
        for device, usage in self.disk_usage.items():
            if usage['percent'] > 90:
                print_error(f"Disco {device} com {usage['percent']:.1f}% de uso - CRÍTICO")
            elif usage['percent'] > 80:
                print_warning(f"Disco {device} com {usage['percent']:.1f}% de uso - ATENÇÃO")
            else:
                print_success(f"Disco {device} com {usage['percent']:.1f}% de uso - OK")

        print_info("Arquivos Grandes (>100MB):")
        for partition in self.disk_partitions:
            if partition.mountpoint == "C:\\":
                large_files = self.get_large_files(partition.mountpoint, 5)
                if large_files:
                    print_info(f"Em {partition.mountpoint}:")
                    for file_path, file_size in large_files:
                        print_info(f"  {format_bytes(file_size)} - {os.path.basename(file_path)}")
                break

        return True

    def cleanup_suggestions(self):
        print_header("Sugestões de Limpeza")
        
        for partition in self.disk_partitions:
            if partition.device in self.disk_usage:
                usage = self.disk_usage[partition.device]
                
                if usage['percent'] > 80:
                    print_info(f"Disco {partition.device} ({partition.mountpoint}):")
                    
                    temp_files = self.get_large_files(partition.mountpoint, 3)
                    if temp_files:
                        print_info("  Arquivos grandes encontrados:")
                        for file_path, file_size in temp_files:
                            print_info(f"    {format_bytes(file_size)} - {file_path}")
                    
                    old_files = self.get_old_files(partition.mountpoint, 90, 3)
                    if old_files:
                        print_info("  Arquivos antigos (>90 dias):")
                        for file_path, file_time in old_files:
                            file_date = time.strftime('%Y-%m-%d', time.localtime(file_time))
                            print_info(f"    {file_date} - {file_path}")

        return True 