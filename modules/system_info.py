import os
import platform
import psutil
import subprocess
import socket
import json
from datetime import datetime
from .utils import print_header, print_success, print_error, print_info, print_warning, format_bytes, create_table, run_command, get_os_type

class SystemInfo:
    def __init__(self):
        self.system_info = {}
        self.hardware_info = {}
        self.network_info = {}
        self.software_info = {}
        self.gpu_info = []

    def get_basic_system_info(self):
        try:
            self.system_info = {
                'os_name': platform.system(),
                'os_version': platform.version(),
                'os_release': platform.release(),
                'architecture': platform.architecture()[0],
                'machine': platform.machine(),
                'processor': platform.processor(),
                'hostname': platform.node(),
                'python_version': platform.python_version(),
                'boot_time': datetime.fromtimestamp(psutil.boot_time()).strftime('%Y-%m-%d %H:%M:%S')
            }
            return True
        except Exception as e:
            print_error(f"Erro ao obter informações do sistema: {e}")
            return False

    def get_hardware_info(self):
        try:
            cpu_info = {
                'physical_cores': psutil.cpu_count(logical=False),
                'total_cores': psutil.cpu_count(logical=True),
                'max_frequency': psutil.cpu_freq().max if psutil.cpu_freq() else 'N/A',
                'current_frequency': psutil.cpu_freq().current if psutil.cpu_freq() else 'N/A',
                'cpu_usage': psutil.cpu_percent(interval=1)
            }

            memory = psutil.virtual_memory()
            memory_info = {
                'total': memory.total,
                'available': memory.available,
                'used': memory.used,
                'percent': memory.percent
            }

            disk_info = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_info.append({
                        'device': partition.device,
                        'mountpoint': partition.mountpoint,
                        'filesystem': partition.fstype,
                        'total': usage.total,
                        'used': usage.used,
                        'free': usage.free
                    })
                except (OSError, PermissionError):
                    continue

            self.hardware_info = {
                'cpu': cpu_info,
                'memory': memory_info,
                'disks': disk_info
            }
            return True
        except Exception as e:
            print_error(f"Erro ao obter informações de hardware: {e}")
            return False

    def get_network_info(self):
        try:
            network_interfaces = []
            for interface, addresses in psutil.net_if_addrs().items():
                for addr in addresses:
                    if addr.family == socket.AF_INET:
                        network_interfaces.append({
                            'interface': interface,
                            'ip': addr.address,
                            'netmask': addr.netmask
                        })

            network_stats = []
            for interface, stats in psutil.net_io_counters(pernic=True).items():
                network_stats.append({
                    'interface': interface,
                    'bytes_sent': stats.bytes_sent,
                    'bytes_recv': stats.bytes_recv,
                    'packets_sent': stats.packets_sent,
                    'packets_recv': stats.packets_recv
                })

            self.network_info = {
                'interfaces': network_interfaces,
                'stats': network_stats
            }
            return True
        except Exception as e:
            print_error(f"Erro ao obter informações de rede: {e}")
            return False

    def get_software_info(self):
        try:
            if get_os_type() == "windows":
                return self.get_windows_software_info()
            else:
                return self.get_linux_software_info()
        except Exception as e:
            print_error(f"Erro ao obter informações de software: {e}")
            return False

    def get_gpu_info(self):
        try:
            gpus = []
            if get_os_type() == "windows":
                ps_cmd = (
                    'powershell -NoProfile -ExecutionPolicy Bypass '
                    '"Get-CimInstance Win32_VideoController | Select-Object Name, DriverVersion | ConvertTo-Json -Compress"'
                )
                success, output, error = run_command(ps_cmd)
                if success and output and output.strip():
                    try:
                        data = json.loads(output.strip())
                        if isinstance(data, dict):
                            data = [data]
                        for item in data or []:
                            name = str(item.get('Name', '')).strip()
                            drv = str(item.get('DriverVersion', '')).strip()
                            if name:
                                gpus.append({ 'name': name, 'driver': drv or 'N/A' })
                    except Exception:
                        pass

                if not gpus:
                    success, output, error = run_command("wmic path win32_VideoController get Name,DriverVersion /format:list")
                    if success and output:
                        blocks = [b for b in output.split('\n\n') if b.strip()]
                        for blk in blocks:
                            nm = None; dv = None
                            for ln in blk.splitlines():
                                if ln.startswith("Name="):
                                    nm = ln.split("=",1)[1].strip()
                                elif ln.startswith("DriverVersion="):
                                    dv = ln.split("=",1)[1].strip()
                            if nm:
                                gpus.append({ 'name': nm, 'driver': dv or 'N/A' })
            else:
                success, output, error = run_command("lspci | grep -Ei 'vga|3d|2d'")
                if success and output:
                    for line in output.splitlines():
                        line = line.strip()
                        if line:
                            # Exemplo: 01:00.0 VGA compatible controller: NVIDIA Corporation ...
                            parts = line.split(':', 2)
                            name = parts[-1].strip() if parts else line
                            gpus.append({ 'name': name, 'driver': 'N/A' })

            self.gpu_info = gpus
            return True
        except Exception as e:
            print_error(f"Erro ao obter informações de GPU: {e}")
            self.gpu_info = []
            return False

    def get_windows_software_info(self):
        try:
            success, output, error = run_command("wmic product get name,version /format:csv")
            if success:
                lines = output.strip().split('\n')
                software_list = []
                for line in lines[1:]:
                    if line.strip():
                        parts = line.split(',')
                        if len(parts) >= 2:
                            software_list.append({
                                'name': parts[0].strip(),
                                'version': parts[1].strip()
                            })
                self.software_info = {'installed_software': software_list[:20]}
                return True
            return False
        except Exception as e:
            print_error(f"Erro ao obter software Windows: {e}")
            return False

    def get_linux_software_info(self):
        try:
            success, output, error = run_command("dpkg -l | head -20")
            if success:
                lines = output.strip().split('\n')
                software_list = []
                for line in lines[5:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            software_list.append({
                                'name': parts[1],
                                'version': parts[2],
                                'description': ' '.join(parts[3:])[:50]
                            })
                self.software_info = {'installed_software': software_list}
                return True
            return False
        except Exception as e:
            print_error(f"Erro ao obter software Linux: {e}")
            return False

    def get_antivirus_status(self):
        antivirus_status = {}
        
        if get_os_type() == "windows":
            antivirus_services = [
                "WinDefend",
                "McAfeeFramework",
                "McAfeeEngine",
                "McAfeeDLPAgent",
                "McAfeeDLPAgent",
                "McAfeeVSEForShield",
                "McAfeeVSEForShield64",
                "McAfeeEngine",
                "McAfeeDLPAgent",
                "McAfeeDLPAgent",
                "McAfeeVSEForShield",
                "McAfeeVSEForShield64",
                "McAfeeEngine",
                "McAfeeDLPAgent",
                "McAfeeDLPAgent",
                "McAfeeVSEForShield",
                "McAfeeVSEForShield64"
            ]
            
            for service in antivirus_services:
                success, output, error = run_command(f"sc query {service}")
                if success and "RUNNING" in output:
                    antivirus_status[service] = "Ativo"
                else:
                    antivirus_status[service] = "Inativo"
        else:
            antivirus_commands = [
                "clamscan --version",
                "sophos --version",
                "avast --version"
            ]
            
            for command in antivirus_commands:
                success, output, error = run_command(command)
                if success:
                    antivirus_status[command.split()[0]] = "Instalado"
                else:
                    antivirus_status[command.split()[0]] = "Não instalado"
        
        return antivirus_status

    def get_system_health(self):
        health_status = {}
        
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            
            health_status['cpu'] = {
                'usage': cpu_usage,
                'status': 'OK' if cpu_usage < 80 else 'ALTO' if cpu_usage < 95 else 'CRÍTICO'
            }
            
            health_status['memory'] = {
                'usage': memory.percent,
                'status': 'OK' if memory.percent < 80 else 'ALTO' if memory.percent < 95 else 'CRÍTICO'
            }
            
            disk_health = []
            for partition in psutil.disk_partitions():
                try:
                    usage = psutil.disk_usage(partition.mountpoint)
                    disk_health.append({
                        'device': partition.device,
                        'usage': usage.percent,
                        'status': 'OK' if usage.percent < 80 else 'ALTO' if usage.percent < 95 else 'CRÍTICO'
                    })
                except (OSError, PermissionError):
                    continue
            
            health_status['disks'] = disk_health
            
            return health_status
        except Exception as e:
            print_error(f"Erro ao obter saúde do sistema: {e}")
            return None

    def run_diagnostic(self):
        print_header("Informações do Sistema")
        
        if not self.get_basic_system_info():
            return False
        
        if not self.get_hardware_info():
            return False
        
        if not self.get_network_info():
            return False
        
        if not self.get_software_info():
            return False
        
        self.get_gpu_info()

        print_info("Informações Básicas do Sistema:")
        system_data = [
            ["Sistema Operacional", f"{self.system_info['os_name']} {self.system_info['os_release']}"],
            ["Versão", self.system_info['os_version']],
            ["Arquitetura", self.system_info['architecture']],
            ["Processador", self.system_info['processor']],
            ["Hostname", self.system_info['hostname']],
            ["Python", self.system_info['python_version']],
            ["Boot Time", self.system_info['boot_time']]
        ]
        headers = ["Métrica", "Valor"]
        print(create_table(headers, system_data))

        print_info("Informações de Hardware:")
        cpu_data = [
            ["Núcleos Físicos", self.hardware_info['cpu']['physical_cores']],
            ["Núcleos Lógicos", self.hardware_info['cpu']['total_cores']],
            ["Frequência Máxima", f"{self.hardware_info['cpu']['max_frequency']:.2f} MHz" if self.hardware_info['cpu']['max_frequency'] != 'N/A' else 'N/A'],
            ["Frequência Atual", f"{self.hardware_info['cpu']['current_frequency']:.2f} MHz" if self.hardware_info['cpu']['current_frequency'] != 'N/A' else 'N/A'],
            ["Uso de CPU", f"{self.hardware_info['cpu']['cpu_usage']:.1f}%"]
        ]
        print(create_table(headers, cpu_data))

        memory_data = [
            ["Total", format_bytes(self.hardware_info['memory']['total'])],
            ["Disponível", format_bytes(self.hardware_info['memory']['available'])],
            ["Usado", format_bytes(self.hardware_info['memory']['used'])],
            ["Percentual", f"{self.hardware_info['memory']['percent']:.1f}%"]
        ]
        print(create_table(headers, memory_data))

        if self.gpu_info:
            print_info("Informações de GPU:")
            gpu_data = []
            for gpu in self.gpu_info:
                gpu_data.append([
                    gpu.get('name','N/A')[:60],
                    gpu.get('driver','N/A')
                ])
            headers = ["GPU", "Versão do Driver"]
            print(create_table(headers, gpu_data))

        print_info("Informações de Disco:")
        disk_data = []
        for disk in self.hardware_info['disks']:
            disk_data.append([
                disk['device'],
                disk['mountpoint'],
                disk['filesystem'],
                format_bytes(disk['total']),
                format_bytes(disk['used']),
                format_bytes(disk['free'])
            ])
        headers = ["Dispositivo", "Ponto de Montagem", "Sistema de Arquivos", "Total", "Usado", "Livre"]
        print(create_table(headers, disk_data))

        print_info("Interfaces de Rede:")
        network_data = []
        for interface in self.network_info['interfaces']:
            network_data.append([
                interface['interface'],
                interface['ip'],
                interface['netmask']
            ])
        headers = ["Interface", "IP", "Máscara de Rede"]
        print(create_table(headers, network_data))

        print_info("Status do Antivírus:")
        antivirus_status = self.get_antivirus_status()
        if antivirus_status:
            av_data = [[name, status] for name, status in antivirus_status.items()]
            headers = ["Antivírus", "Status"]
            print(create_table(headers, av_data))
        else:
            print_warning("Não foi possível verificar status do antivírus")

        print_info("Saúde do Sistema:")
        health_status = self.get_system_health()
        if health_status:
            health_data = [
                ["CPU", f"{health_status['cpu']['usage']:.1f}%", health_status['cpu']['status']],
                ["Memória", f"{health_status['memory']['usage']:.1f}%", health_status['memory']['status']]
            ]
            headers = ["Componente", "Uso", "Status"]
            print(create_table(headers, health_data))

            for disk in health_status['disks']:
                print_info(f"Disco {disk['device']}: {disk['usage']:.1f}% - {disk['status']}")

        return True 