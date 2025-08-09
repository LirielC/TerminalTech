import os
import subprocess
import re
import json
from .utils import print_header, print_success, print_error, print_info, print_warning, run_command, get_os_type, create_table

class DriverUpdater:
    def __init__(self):
        self.drivers_info = []
        self.outdated_drivers = []
        self.system_info = {}

    def get_system_info(self):
        try:
            if get_os_type() == "windows":
                # 1) PowerShell (mais confiável em Win10/11)
                ps_cmd = (
                    'powershell -NoProfile -ExecutionPolicy Bypass '
                    '"$cs = Get-CimInstance -ClassName Win32_ComputerSystem; '
                    '[PSCustomObject]@{Manufacturer=$cs.Manufacturer; Model=$cs.Model} | ConvertTo-Json -Compress"'
                )
                success, output, error = run_command(ps_cmd)
                if success and output and output.strip():
                    try:
                        obj = json.loads(output.strip())
                        if isinstance(obj, dict):
                            manufacturer = str(obj.get('Manufacturer', '')).strip()
                            model = str(obj.get('Model', '')).strip()
                            if manufacturer or model:
                                self.system_info = {'manufacturer': manufacturer, 'model': model}
                                return True
                    except Exception:
                        pass

                # 2) WMIC em formato lista (fácil de parsear)
                success, output, error = run_command("wmic computersystem get manufacturer,model /format:list")
                if success and output:
                    manu_match = re.search(r"Manufacturer\s*=\s*(.*)", output)
                    model_match = re.search(r"Model\s*=\s*(.*)", output)
                    manufacturer = manu_match.group(1).strip() if manu_match else ''
                    model = model_match.group(1).strip() if model_match else ''
                    if manufacturer or model:
                        self.system_info = {'manufacturer': manufacturer, 'model': model}
                        return True

                # 3) WMIC tabela simples (deprecated, mas ainda presente)
                success, output, error = run_command("wmic computersystem get manufacturer,model")
                if success and output:
                    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
                    # Esperado: ["Manufacturer  Model", "Dell Inc.   Latitude 7420"]
                    if len(lines) >= 2:
                        header = lines[0].lower()
                        data = lines[1]
                        if 'manufacturer' in header and 'model' in header:
                            parts = data.split()
                            if len(parts) >= 2:
                                manufacturer = parts[0].strip()
                                model = ' '.join(parts[1:]).strip()
                                self.system_info = {'manufacturer': manufacturer, 'model': model}
                                return True

                # 4) Registro do Windows como último recurso
                success, out1, _ = run_command('reg query "HKLM\\HARDWARE\\DESCRIPTION\\System\\BIOS" /v SystemManufacturer')
                success2, out2, _ = run_command('reg query "HKLM\\HARDWARE\\DESCRIPTION\\System\\BIOS" /v SystemProductName')
                manufacturer, model = '', ''
                if success and out1:
                    m = re.search(r"SystemManufacturer\s+REG_SZ\s+(.*)", out1)
                    if m:
                        manufacturer = m.group(1).strip()
                if success2 and out2:
                    m = re.search(r"SystemProductName\s+REG_SZ\s+(.*)", out2)
                    if m:
                        model = m.group(1).strip()
                if manufacturer or model:
                    self.system_info = {'manufacturer': manufacturer, 'model': model}
                    return True
            else:
                success, output, error = run_command("cat /sys/class/dmi/id/product_name")
                if success:
                    self.system_info['model'] = output.strip()
                    success, output, error = run_command("cat /sys/class/dmi/id/sys_vendor")
                    if success:
                        self.system_info['manufacturer'] = output.strip()
                        return True
            return False
        except Exception as e:
            print_error(f"Erro ao obter informações do sistema: {e}")
            return False

    def get_windows_drivers(self):
        try:
            success, output, error = run_command("pnputil /enum-drivers")
            if success:
                drivers = []
                current_driver = {}
                
                for line in output.split('\n'):
                    if 'Published name' in line:
                        if current_driver:
                            drivers.append(current_driver)
                        current_driver = {'published_name': line.split(':')[1].strip()}
                    elif 'Original file name' in line:
                        current_driver['original_file'] = line.split(':')[1].strip()
                    elif 'Provider Name' in line:
                        current_driver['provider'] = line.split(':')[1].strip()
                    elif 'Driver Date' in line:
                        current_driver['date'] = line.split(':')[1].strip()
                    elif 'Driver Version' in line:
                        current_driver['version'] = line.split(':')[1].strip()
                
                if current_driver:
                    drivers.append(current_driver)
                
                self.drivers_info = drivers
                return True
            return False
        except Exception as e:
            print_error(f"Erro ao obter drivers Windows: {e}")
            return False

    def get_linux_drivers(self):
        try:
            drivers = []
            
            success, output, error = run_command("lsmod")
            if success:
                for line in output.split('\n')[1:]:
                    if line.strip():
                        parts = line.split()
                        if len(parts) >= 3:
                            drivers.append({
                                'name': parts[0],
                                'size': parts[1],
                                'used_by': parts[2] if parts[2] != '-' else 'N/A'
                            })
            
            self.drivers_info = drivers
            return True
        except Exception as e:
            print_error(f"Erro ao obter drivers Linux: {e}")
            return False

    # ---------------- GPU detection and vendor links -----------------
    def _detect_gpu_windows(self):
        gpus = []
        ps_cmd = (
            'powershell -NoProfile -ExecutionPolicy Bypass '
            '"Get-CimInstance Win32_VideoController | Select-Object Name | ConvertTo-Json -Compress"'
        )
        success, output, error = run_command(ps_cmd)
        if success and output and output.strip():
            try:
                data = json.loads(output.strip())
                if isinstance(data, dict):
                    data = [data]
                for item in data or []:
                    name = str(item.get('Name', '')).strip()
                    if name:
                        gpus.append(name)
            except Exception:
                pass

        if not gpus:
            success, output, error = run_command("wmic path win32_VideoController get Name /format:list")
            if success and output:
                for line in output.splitlines():
                    if line.startswith("Name="):
                        nm = line.split("=",1)[1].strip()
                        if nm:
                            gpus.append(nm)
        return gpus

    def _detect_gpu_linux(self):
        gpus = []
        success, output, error = run_command("lspci | grep -Ei 'vga|3d|2d'")
        if success and output:
            for line in output.splitlines():
                line = line.strip()
                if line:
                    parts = line.split(':', 2)
                    name = parts[-1].strip() if parts else line
                    gpus.append(name)
        return gpus

    def _get_gpu_vendor_links(self):
        vendor_links = []
        gpu_brand = None

        if get_os_type() == "windows":
            gpu_names = self._detect_gpu_windows()
        else:
            gpu_names = self._detect_gpu_linux()

        def pick_vendor(name: str):
            low = name.lower()
            if any(k in low for k in ["nvidia", "geforce", "quadro", "rtx", "gtx"]):
                return "NVIDIA", "https://www.nvidia.com/pt-br/geforce/drivers/"
            if any(k in low for k in ["amd", "radeon", "rx ", "vega"]):
                return "AMD", "https://www.amd.com/pt/support"
            if any(k in low for k in ["intel", "uhd", "iris", "arc "]):
                return "Intel", "https://www.intel.com.br/content/www/br/pt/download-center/home.html"
            return None, None

        for name in gpu_names:
            brand, link = pick_vendor(name)
            if brand and link:
                vendor_links.append((brand, name, link))

        if vendor_links:
            gpu_brand = vendor_links[0][0]

        return gpu_brand, vendor_links

    def check_driver_updates_windows(self):
        try:
            print_info("Verificando drivers desatualizados...")
            
            if not self.get_system_info():
                print_warning("Não foi possível obter informações do sistema")
                print_info("Continuando com informações básicas...")
            
            if self.system_info:
                print_info(f"Sistema: {self.system_info.get('manufacturer', 'N/A')} {self.system_info.get('model', 'N/A')}")
            
            success, output, error = run_command("dism /online /get-drivers /format:table")
            if success:
                print_info("Drivers presentes no Driver Store (DISM):")
                print(output)
            
            # GPU vendor links
            brand, links = self._get_gpu_vendor_links()
            if links:
                print_info("Atualização de drivers de GPU:")
                for vendor, gpu_name, url in links:
                    print_info(f"   - {gpu_name} ({vendor}): {url}")
            
            print_info("Para atualizar drivers:")
            print_info("1. Use Windows Update: Configurações > Atualização e Segurança")
            print_info("2. Visite o site do fabricante:")
            if self.system_info and self.system_info.get('manufacturer'):
                manufacturer = self.system_info['manufacturer'].lower()
                if 'dell' in manufacturer:
                    print_info("   - Dell: https://www.dell.com/support/home")
                elif 'hp' in manufacturer or 'hewlett' in manufacturer:
                    print_info("   - HP: https://support.hp.com/br-pt/drivers")
                elif 'lenovo' in manufacturer:
                    print_info("   - Lenovo: https://support.lenovo.com/br/pt/downloads")
                elif 'asus' in manufacturer or 'asustek' in manufacturer:
                    print_info("   - ASUS: https://www.asus.com/support/")
                elif 'acer' in manufacturer:
                    print_info("   - Acer: https://www.acer.com/ac/pt/BR/content/support")
                elif 'gigabyte' in manufacturer:
                    print_info("   - Gigabyte: https://www.gigabyte.com/br/Support")
                elif 'msi' in manufacturer or 'micro-star' in manufacturer:
                    print_info("   - MSI: https://www.msi.com/support")
                elif 'asrock' in manufacturer:
                    print_info("   - ASRock: https://www.asrock.com/support/index.asp")
                elif 'microsoft' in manufacturer or 'surface' in manufacturer:
                    print_info("   - Microsoft Surface: https://support.microsoft.com/surface/download-drivers-and-firmware")
                else:
                    print_info(f"   - {self.system_info['manufacturer']}: Site oficial do fabricante")
            else:
                print_info("   - Verifique o site oficial do fabricante do seu computador")
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar atualizações: {e}")
            return False

    def check_driver_updates_linux(self):
        try:
            print_info("Verificando drivers no Linux...")
            
            if not self.get_system_info():
                print_warning("Não foi possível obter informações do sistema")
                return False
            
            print_info(f"Sistema: {self.system_info.get('manufacturer', 'N/A')} {self.system_info.get('model', 'N/A')}")
            
            success, output, error = run_command("ubuntu-drivers devices")
            if success:
                print_info("Drivers recomendados:")
                print(output)
            
            success, output, error = run_command("apt list --upgradable | grep -i driver")
            if success and output.strip():
                print_info("Drivers com atualizações disponíveis:")
                print(output)
            else:
                print_success("Todos os drivers estão atualizados")

            # GPU vendor links
            brand, links = self._get_gpu_vendor_links()
            if links:
                print_info("Atualização de drivers de GPU:")
                for vendor, gpu_name, url in links:
                    print_info(f"   - {gpu_name} ({vendor}): {url}")
            
            return True
        except Exception as e:
            print_error(f"Erro ao verificar drivers Linux: {e}")
            return False

    def install_driver_windows(self, driver_name):
        try:
            print_info(f"Instalando driver: {driver_name}")
            
            success, output, error = run_command(f"pnputil /add-driver {driver_name} /install")
            if success:
                print_success(f"Driver {driver_name} instalado com sucesso")
                return True
            else:
                print_error(f"Erro ao instalar driver: {error}")
                return False
        except Exception as e:
            print_error(f"Erro ao instalar driver: {e}")
            return False

    def run_diagnostic(self):
        print_header("BUSCA DE DRIVERS RECENTES")
        print_info("Esta ferramenta verifica:")
        print_info("• Drivers desatualizados no sistema")
        print_info("• Atualizações disponíveis no Windows Update")
        print_info("• Links para sites dos fabricantes")
        print_info("• Recomendações de atualização")
        print()
        
        if get_os_type() == "windows":
            return self.check_driver_updates_windows()
        else:
            return self.check_driver_updates_linux()

    def list_drivers(self):
        print_header("Lista de Drivers")
        
        if get_os_type() == "windows":
            if self.get_windows_drivers():
                if self.drivers_info:
                    print_info("Drivers instalados:")
                    driver_data = []
                    for driver in self.drivers_info[:20]:
                        driver_data.append([
                            driver.get('provider', 'N/A'),
                            driver.get('version', 'N/A'),
                            driver.get('date', 'N/A'),
                            driver.get('original_file', 'N/A')
                        ])
                    
                    headers = ["Fabricante", "Versão", "Data", "Arquivo"]
                    print(create_table(headers, driver_data))
                    return True
                else:
                    print_warning("Nenhum driver encontrado")
                    return False
            else:
                return False
        else:
            if self.get_linux_drivers():
                if self.drivers_info:
                    print_info("Módulos de kernel carregados:")
                    driver_data = []
                    for driver in self.drivers_info[:20]:
                        driver_data.append([
                            driver.get('name', 'N/A'),
                            driver.get('size', 'N/A'),
                            driver.get('used_by', 'N/A')
                        ])
                    
                    headers = ["Módulo", "Tamanho", "Usado por"]
                    print(create_table(headers, driver_data))
                    return True
                else:
                    print_warning("Nenhum módulo encontrado")
                    return False
            else:
                return False 