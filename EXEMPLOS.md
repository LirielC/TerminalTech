# Exemplos de Uso - TerminalTec

## 🚀 Iniciando o Programa

### Opção 1: Menu de Escolha (Recomendado)
```bash
python start.py
```
Este comando abre um menu que permite escolher:
- Modo Terminal

### Opção 2: Modo Terminal Direto
```bash
python main.py
```

## 💻 Usando o Modo Terminal

### Comandos Básicos
```bash
# Executar todas as verificações
python main.py --all

# Verificar apenas DNS
python main.py --dns

# Análise de disco
python main.py --disk

# Monitoramento de RAM
python main.py --ram

# Backup de drivers

# Limpeza de arquivos temporários
python main.py --clean-temp

# Teste de velocidade
python main.py --speed-test

# Informações do sistema
python main.py --system-info

# Verificação de vírus
python main.py --virus-scan

# Teste de memória
python main.py --memory-test

# Verificação de disco
python main.py --disk-check
```

### Menu Interativo
```bash
python main.py
```
Este comando abre um menu interativo com as seguintes opções:

1. **Diagnóstico Completo** - Executa todas as verificações
2. **Verificar Vírus e Segurança** - Status dos antivírus
3. **Verificar Disco** - Análise de saúde e espaço
4. **Testar Memória RAM** - Verificação de integridade
5. **Buscar Drivers Recentes** - Atualizações de drivers
6. **Diagnóstico de DNS** - Teste de conectividade
7. **Análise de Disco** - Análise detalhada
8. **Monitoramento de RAM** - Uso de memória
9. **Informações do Sistema** - Detalhes do hardware
10. **Teste de Velocidade** - Performance de disco e internet
11. **Limpeza de Temporários** - Remover arquivos temporários
12. **Limpeza de Arquivos Temporários** - Limpeza do sistema
13. **Sair do Programa**

## 📊 Recursos do Modo Terminal

### Saída Colorida
- **Verde**: Sucessos e informações positivas
- **Vermelho**: Erros e problemas
- **Azul**: Informações gerais
- **Amarelo**: Avisos e alertas

### Logs Detalhados
- Todas as operações são exibidas no terminal
- Informações completas sobre cada verificação
- Possibilidade de salvar logs usando redirecionamento

### Execução em Lote
- Use argumentos para executar múltiplas ferramentas
- Combine verificações específicas
- Automatize processos com scripts

## 🔧 Dicas de Uso

### Para Técnicos Iniciantes
1. Use o **Menu Interativo** para facilitar o uso
2. Comece com o **"Diagnóstico Completo"** para uma visão geral
3. Use as opções individuais para problemas específicos
4. Salve os logs para documentação

### Para Técnicos Avançados
1. Use **Argumentos de Linha de Comando** para automação
2. Combine argumentos para verificações específicas
3. Use scripts para execução em lote
4. Integre com outras ferramentas

### Para Manutenção Preventiva
1. Execute o diagnóstico completo semanalmente
2. Monitore o uso de disco regularmente
3. Verifique drivers mensalmente
4. Mantenha logs para histórico

## 🚨 Solução de Problemas

### Erro de Módulos
```bash
# Instalar dependências
pip install -r requirements.txt

# Verificar instalação
pip list | grep -E "(psutil|speedtest|requests|colorama|tabulate|tqdm)"
```

### Problemas de Permissão
- Execute como administrador no Windows
- Use `sudo` no Linux para operações que requerem privilégios

### Teste de Módulos
```bash
# Verificar se todos os módulos funcionam
python test_modules.py
```

## 📝 Logs e Relatórios

### Salvando Logs
```bash
# Salvar toda a saída em um arquivo
python main.py > log.txt 2>&1

# Salvar apenas erros
python main.py 2> errors.txt

# Salvar com timestamp
python main.py > log_$(date +%Y%m%d_%H%M%S).txt 2>&1
```

### Formato dos Logs
- **Data e Hora**: Timestamp de cada operação
- **Tipo de Verificação**: Nome da ferramenta executada
- **Resultados Detalhados**: Todas as informações coletadas
- **Status**: Sucesso ou erro de cada operação

## 🔄 Atualizações

### Verificar Atualizações
```bash
# Atualizar dependências
pip install --upgrade -r requirements.txt

# Verificar versão do Python
python --version
```

### Backup de Configurações
- Os logs salvos podem ser usados como backup
- Mantenha histórico de diagnósticos para comparação
- Use datas nos nomes dos arquivos para organização 