import socket
import subprocess
import time
import shutil
import requests
from .utils import print_header, print_success, print_error, print_info, print_warning, run_command, get_os_type

class DNSChecker:
    def __init__(self):
        self.dns_servers = [
            "8.8.8.8",
            "8.8.4.4",
            "1.1.1.1",
            "1.0.0.1",
            "208.67.222.222",
            "208.67.220.220"
        ]
        self.test_domains = [
            "google.com",
            "facebook.com",
            "youtube.com",
            "amazon.com",
            "microsoft.com"
        ]

    def check_dns_resolution(self, domain):
        try:
            ip_address = socket.gethostbyname(domain)
            return True, ip_address
        except socket.gaierror:
            return False, None

    def test_dns_server(self, dns_server):
        success_count = 0
        total_time = 0.0

        for domain in self.test_domains:
            start_time = time.time()
            success, _ip = self._resolve_with_server(dns_server, domain)
            end_time = time.time()
            if success:
                success_count += 1
                total_time += (end_time - start_time)

        success_rate = (success_count / len(self.test_domains)) * 100
        avg_time = (total_time / success_count) if success_count > 0 else 0
        return success_rate, avg_time

    def _resolve_with_server(self, server: str, domain: str):
        if get_os_type() == "windows":
            # Preferir PowerShell Resolve-DnsName
            ps_cmd = (
                'powershell -NoProfile -ExecutionPolicy Bypass '
                f'"Resolve-DnsName -Server {server} -Name {domain} -Type A -NoHostsFile -ErrorAction SilentlyContinue | '
                'Select-Object -First 1 IPAddress | Format-Table -HideTableHeaders"'
            )
            ok, out, err = run_command(ps_cmd)
            if ok and out and out.strip() and not out.lower().startswith("resolve-dnsname"):
                ip = out.strip().split()[0]
                return True, ip
            # Fallback: nslookup
            ok, out, err = run_command(f"nslookup {domain} {server}")
            if ok and "Address:" in out:
                lines = [ln for ln in out.splitlines() if "Address:" in ln]
                if lines:
                    ip = lines[-1].split("Address:")[-1].strip()
                    return True, ip
            return False, None
        else:
            # Linux: dig preferencialmente
            if shutil.which("dig"):
                ok, out, err = run_command(f"dig +time=2 +tries=1 @{server} {domain} A +short")
                if ok and out and out.strip():
                    ip = out.strip().splitlines()[0].strip()
                    return True, ip
            # Fallback: nslookup
            ok, out, err = run_command(f"nslookup {domain} {server}")
            if ok and "Address:" in out:
                lines = [ln for ln in out.splitlines() if "Address:" in ln]
                if lines:
                    ip = lines[-1].split("Address:")[-1].strip()
                    return True, ip
            return False, None

    def measure_dns_latency(self, server: str, tries: int = 3, domain: str = "google.com"):
        success = 0
        total = 0.0
        for _ in range(tries):
            t0 = time.perf_counter()
            ok, _ = self._resolve_with_server(server, domain)
            t1 = time.perf_counter()
            if ok:
                success += 1
                total += (t1 - t0)
        avg_ms = (total / success) * 1000 if success else 0.0
        return success, avg_ms

    def flush_dns_cache(self):
        if get_os_type() == "windows":
            success, output, error = run_command("ipconfig /flushdns")
        else:
            # Tentar vários métodos
            success, output, error = run_command("resolvectl flush-caches")
            if not success:
                success, output, error = run_command("sudo systemctl restart systemd-resolved")
            if not success:
                success, output, error = run_command("sudo service nscd restart")
        
        return success

    def get_current_dns_servers(self):
        if get_os_type() == "windows":
            success, output, error = run_command("ipconfig /all")
        else:
            success, output, error = run_command("cat /etc/resolv.conf")
        
        return success, output

    def run_diagnostic(self):
        print_header("DIAGNOSTICO DE DNS")
        print_info("Esta ferramenta verifica:")
        print_info("• Conectividade de rede")
        print_info("• Configuração de DNS")
        print_info("• Velocidade de resolução")
        print_info("• Servidores DNS alternativos")
        print()
        
        self._network_overview()
        self._test_connectivity()
        
        print_info("Verificando conectividade básica...")
        success, ip = self.check_dns_resolution("google.com")
        if success:
            print_success(f"Conectividade básica OK - Google.com resolve para {ip}")
        else:
            print_error("Falha na conectividade básica")
            return False

        print_info("Testando servidores DNS públicos...")
        dns_results = []
        for dns_server in self.dns_servers:
            success_rate, avg_time = self.test_dns_server(dns_server)
            dns_results.append([dns_server, f"{success_rate:.1f}%", f"{avg_time*1000:.1f}ms"])
            print_info(f"DNS {dns_server}: {success_rate:.1f}% sucesso, {avg_time*1000:.1f}ms média")

        print_info("\nLatência por servidor DNS (3 tentativas em google.com):")
        for dns_server in self.dns_servers:
            ok_count, avg_ms = self.measure_dns_latency(dns_server, tries=3)
            status = "OK" if ok_count == 3 else f"{ok_count}/3"
            print_info(f"DNS {dns_server}: {status}, ~{avg_ms:.1f}ms")

        print_info("Verificando servidores DNS atuais...")
        success, output = self.get_current_dns_servers()
        if success:
            print_success("Informações de DNS obtidas com sucesso")
        else:
            print_warning("Não foi possível obter informações de DNS atuais")

        print_info("Testando resolução de domínios específicos...")
        for domain in self.test_domains:
            success, ip = self.check_dns_resolution(domain)
            if success:
                print_success(f"{domain} -> {ip}")
            else:
                print_error(f"Falha ao resolver {domain}")

        self._http_connectivity_tests()
        self._suggest_dns_change()

        return True

    def fix_dns_issues(self):
        print_header("Correção de Problemas de DNS")
        
        print_info("Limpando cache de DNS...")
        if self.flush_dns_cache():
            print_success("Cache de DNS limpo com sucesso")
        else:
            print_warning("Não foi possível limpar o cache de DNS")

        print_info("Testando conectividade após limpeza...")
        success, ip = self.check_dns_resolution("google.com")
        if success:
            print_success("DNS funcionando corretamente após limpeza")
        else:
            print_error("Problemas de DNS persistem após limpeza")
            print_info("Considere alterar para servidores DNS públicos como 8.8.8.8 ou 1.1.1.1")

        return success 

    # ---------------- utilitários de diagnóstico ----------------
    def _network_overview(self):
        try:
            print_info("Visão geral de rede:")
            if get_os_type() == "windows":
                ok, out, err = run_command('powershell -NoProfile "Get-NetAdapter | Select Name, Status, LinkSpeed | Format-Table -AutoSize"')
                if ok and out.strip():
                    print(out)
                else:
                    ok, out, err = run_command("ipconfig /all")
                    if ok:
                        print(out)
            else:
                ok, out, err = run_command("ip -brief addr")
                if ok:
                    print(out)
                ok, out, err = run_command("ip route show")
                if ok:
                    print(out)
        except Exception as e:
            print_warning(f"Falha ao obter visão geral de rede: {e}")

    def _test_connectivity(self):
        try:
            print_info("Testando conectividade básica:")
            if get_os_type() == "windows":
                run_command("ping -n 1 8.8.8.8")
                run_command("ping -n 1 google.com")
                run_command('powershell -NoProfile "Test-NetConnection -ComputerName 8.8.8.8 -Port 53"')
            else:
                run_command("ping -c 1 8.8.8.8")
                run_command("ping -c 1 google.com")
                # UDP 53 nem sempre testável sem ferramentas adicionais; rely em dig/nslookup
        except Exception as e:
            print_warning(f"Falha no teste de conectividade: {e}")

    def _http_connectivity_tests(self):
        try:
            print_info("\nTeste de HTTP/HTTPS (camada de aplicação):")
            tests = [
                ("HTTPS", "https://www.google.com/generate_204"),
                ("HTTP", "http://example.com"),
            ]
            for label, url in tests:
                t0 = time.perf_counter()
                try:
                    resp = requests.get(url, timeout=5)
                    dt = (time.perf_counter() - t0) * 1000
                    print_success(f"{label} OK ({resp.status_code}) em {dt:.0f}ms: {url}")
                except Exception as e:
                    dt = (time.perf_counter() - t0) * 1000
                    print_error(f"{label} ERRO em {dt:.0f}ms: {url} ({e})")
        except Exception as e:
            print_warning(f"Falha no teste HTTP/HTTPS: {e}")

    def _suggest_dns_change(self):
        try:
            print_info("\nComo alterar DNS (opcional):")
            if get_os_type() == "windows":
                ok, out, err = run_command('powershell -NoProfile -Command "Get-NetAdapter | Where-Object {$_.Status -eq \'Up\'} | Select -First 1 -ExpandProperty Name"')
                alias = out.strip().splitlines()[0] if ok and out.strip() else "Ethernet"
                print_info(f"Adapter detectado: {alias}")
                print_info("Comandos (PowerShell, admin):")
                print_info(f"  Set-DnsClientServerAddress -InterfaceAlias '{alias}' -ServerAddresses 1.1.1.1,8.8.8.8")
                print_info(f"  Get-DnsClientServerAddress -InterfaceAlias '{alias}'")
            else:
                print_info("systemd-resolved:")
                print_info("  resolvectl dns <interface> 1.1.1.1 8.8.8.8 && resolvectl flush-caches")
                print_info("NetworkManager (nmcli):")
                print_info('  nmcli con mod "<con-name>" ipv4.dns "1.1.1.1 8.8.8.8" && nmcli con up "<con-name>"')
        except Exception as e:
            print_warning(f"Falha ao sugerir mudança de DNS: {e}")