# TerminalTech - Ferramenta para Técnicos de Computadores

Uma ferramenta completa em Python para técnicos de computadores que funciona tanto no Windows quanto no Linux.

## Funcionalidades

### 🔧 Ferramentas Principais
- 🔍 **Diagnóstico Completo**: Executa todas as verificações automaticamente
- 🦠 **Verificação de Vírus**: Status dos principais antivírus
- 💾 **Verificação de Disco**: Analisa saúde e espaço em disco
- 🧠 **Teste de Memória RAM**: Verifica integridade da memória
- 🚀 **Busca de Drivers**: Encontra drivers atualizados

### 📊 Ferramentas de Análise
- 🌐 **Diagnóstico de DNS**: Testa conectividade e resolve problemas de DNS
- 💿 **Análise de Disco**: Análise detalhada de espaço e performance
- 📈 **Monitoramento de RAM**: Verifica uso e disponibilidade de memória
- 📋 **Informações do Sistema**: Exibe detalhes do hardware e software
- ⚡ **Teste de Velocidade**: Mede performance de disco e internet

### 🛠️ Ferramentas de Manutenção
- 🧹 **Limpeza de Arquivos Temporários**: Remove arquivos desnecessários

## 💻 Modo Terminal e 🖼️ Modo GUI (experimental)

O TerminalTec funciona por terminal e também possui uma interface gráfica (GUI) experimental:

- **Interface Limpa**: Menu organizado e fácil de navegar (terminal) e GUI simples
- **Execução Rápida**: Comandos diretos e eficientes
- **Logs Detalhados**: Saída completa de todas as operações
- **Compatibilidade Total**: Funciona em qualquer terminal
- **Execução em Lote**: Possibilidade de executar múltiplas ferramentas
- **Argumentos de Linha de Comando**: Controle avançado via parâmetros

## Instalação

### Pré-requisitos
- Python 3.7 ou superior
- pip (gerenciador de pacotes Python)

### Passos de Instalação

1. Clone ou baixe este repositório
2. Abra o terminal/prompt de comando
3. Navegue até a pasta do projeto
4. Execute:

```bash
pip install -r requirements.txt
```

## Uso

### 🚀 Inicialização Rápida (Recomendado)
```bash
python start.py
```
Este comando abre um menu com as opções:
- Modo Terminal - Interface completa via terminal
- Modo GUI (experimental)

### 💻 Modo Terminal
```bash
python main.py
```

### 🖼️ Modo GUI (Experimental)
```bash
python gui.py
```
Ou execute `python start.py` e escolha a opção “Modo GUI (experimental)”.

### Execução com Argumentos (Modo Terminal)
```bash
python main.py --dns
python main.py --disk
python main.py --ram
python main.py --clean-temp
python main.py --speed-test
python main.py --internet-test
python main.py --system-info
python main.py --all
```

## Estrutura do Projeto

```
TerminalTec/
├── start.py               # Inicializador com menu de escolha
├── main.py                # Arquivo principal (modo terminal)
├── gui.py                 # Interface gráfica (experimental)
├── test_modules.py        # Teste de módulos
├── modules/               # Módulos de funcionalidades
│   ├── __init__.py
│   ├── compatibility.py   # Verificação de compatibilidade
│   ├── dns_checker.py      # Verificação de DNS
│   ├── disk_analyzer.py    # Análise de disco
│   ├── ram_monitor.py      # Monitoramento de RAM
│   ├── driver_backup.py    # (removido do menu) Backup de drivers
│   ├── temp_cleaner.py     # Limpeza de arquivos temporários
│   ├── speed_tester.py     # Teste de velocidade
│   ├── system_info.py      # Informações do sistema
│   ├── driver_updater.py   # Atualização de drivers
│   ├── virus_scanner.py    # Verificação de vírus
│   ├── memory_tester.py    # Teste de memória RAM
│   ├── disk_checker.py     # Verificação de disco
│   └── utils.py            # Utilitários gerais
├── requirements.txt        # Dependências
├── README.md              # Documentação
├── EXEMPLOS.md            # Exemplos de uso
└── TROUBLESHOOTING.md     # Guia de solução de problemas
```

## Compatibilidade

### ✅ Sistemas Suportados

**Windows:**
- Windows 10 (versão 1903 ou superior)
- Windows 11 (todas as versões)

**Ubuntu/Debian:**
- Ubuntu 18.04 LTS ou superior
- Ubuntu 20.04 LTS (recomendado)
- Ubuntu 22.04 LTS (recomendado)
- Debian 10 ou superior

**macOS:**
- macOS 10.15 (Catalina) ou superior
- macOS 11 (Big Sur) ou superior
- macOS 12 (Monterey) ou superior
- macOS 13 (Ventura) ou superior

### 🔧 Verificação de Compatibilidade

Para verificar se seu sistema é compatível:

```bash
python test_modules.py
```

Este comando irá:
- Detectar seu sistema operacional
- Verificar a versão
- Testar todos os módulos
- Identificar problemas de compatibilidade

### 📋 Requisitos Específicos por Sistema

**Ubuntu/Debian:**
```bash
# Instalar dependências do sistema
sudo apt update
sudo apt install python3 python3-pip python3-psutil -y

# Instalar dependências Python
pip3 install -r requirements.txt
```

**macOS:**
```bash
# Instalar Homebrew (se não tiver)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Instalar Python
brew install python3

# Instalar dependências Python
pip3 install -r requirements.txt
```

**Windows:**
```bash
# Instalar dependências Python
pip install -r requirements.txt
```

### ⚠️ Limitações Conhecidas

**Ubuntu:**
- Versões anteriores a 16.04 podem ter problemas com alguns comandos
- Algumas ferramentas requerem privilégios de administrador

**macOS:**
- Algumas funcionalidades de hardware podem ser limitadas
- Teste de memória RAM usa ferramentas nativas do macOS
- Backup de drivers funciona diferente (baseado em pacotes)

**Geral:**
- Algumas ferramentas antivírus podem não ser detectadas
- Testes de velocidade dependem da conectividade de internet
 - No Windows, operações como chkdsk (/F, /R) e varreduras do Defender podem exigir execução como Administrador (a GUI avisa quando não há privilégios)

### Dependências opcionais (Linux)
- Para diagnóstico DNS mais completo: `dig` (pacote `dnsutils`), `resolvectl` (systemd-resolved) e/ou `nscd`


## 🔧 Solução de Problemas

Se você encontrar problemas com alguma ferramenta específica:

1. **Execute o teste de módulos:**
   ```bash
   python test_modules.py
   ```

2. **Verifique o guia completo:**
   - Consulte `TROUBLESHOOTING.md` para soluções detalhadas

3. **Execute como administrador:**
   - Windows: Clique direito → "Executar como administrador"
   - Linux/macOS: `sudo python main.py`

## Contribuição

Sinta-se à vontade para contribuir com melhorias e novas funcionalidades!

## Licença

Este projeto está sob a licença MIT.

## Notas de Desenvolvimento

- O código não contém comentários para manter a limpeza e legibilidade
- Todas as funcionalidades são auto-explicativas através de nomes de variáveis e funções descritivos
- O código segue padrões de nomenclatura claros e consistentes 
