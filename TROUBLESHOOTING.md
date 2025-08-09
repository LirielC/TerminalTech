# 🔧 Guia de Solução de Problemas - TerminalTec

## Problemas Comuns no Modo Terminal

### 1. ❌ Módulos Não Funcionam

**Sintomas:**
- Mensagens de erro sobre módulos não disponíveis
- Ferramentas não executam
- Erro de importação

**Soluções:**
```bash
# Testar todos os módulos
python test_modules.py

# Verificar dependências
pip install -r requirements.txt

# Executar como administrador (Windows)
# Executar com sudo (Linux)
```

### 2. ❌ Erros de Permissão

**Sintomas:**
- Mensagens de "Acesso Negado"
- Ferramentas que requerem privilégios não funcionam

**Soluções:**
```bash
# Windows: Executar como administrador
# Linux/macOS: Executar com sudo
sudo python main.py
```

### 3. ❌ Interface Travada

**Sintomas:**
- Terminal não responde
- Programa parece congelado
- Operações demoram muito

**Soluções:**
- Aguarde alguns segundos (algumas operações demoram)
- Use Ctrl+C para cancelar operações
- Reinicie o programa se necessário

## 🔍 Diagnóstico de Problemas

### Teste Rápido
```bash
# 1. Testar módulos
python test_modules.py

# 2. Testar importações básicas
python -c "from modules.utils import print_header; print('Import OK')"

# 3. Testar módulo específico
python -c "from modules.dns_checker import DNSChecker; print('DNS Module OK')"
```

### Verificação de Dependências
```bash
# Verificar se todas as dependências estão instaladas
pip list | grep -E "(psutil|requests|colorama|tabulate|tqdm|Pillow)"
```

## 🛠️ Ferramentas de Diagnóstico

### 1. Status de Módulos
- Execute `python test_modules.py` para verificar disponibilidade
- Mostra quais ferramentas estão disponíveis
- Identifica problemas de carregamento

### 2. Logs Detalhados
- Todas as operações são exibidas no terminal
- Erros são mostrados com detalhes completos
- Use redirecionamento para salvar logs: `python main.py > log.txt 2>&1`

### 3. Teste Individual
- Teste cada ferramenta individualmente
- Identifique qual módulo específico está com problema

## 📋 Checklist de Solução de Problemas

### Antes de Reportar um Problema:

- [ ] Execute `python test_modules.py`
- [ ] Execute como administrador/sudo
- [ ] Verifique se todas as dependências estão instaladas
- [ ] Teste a ferramenta específica que não funciona
- [ ] Salve o log de erro usando redirecionamento

### Informações para Incluir no Relatório:

1. **Sistema Operacional:** Windows/Linux/macOS e versão
2. **Versão do Python:** `python --version`
3. **Resultado do teste de módulos:** `python test_modules.py`
4. **Erro específico:** Copie a mensagem de erro
5. **Log completo:** Salve usando redirecionamento

## 🚀 Dicas de Performance

### Para Melhor Experiência:

1. **Execute como Administrador:**
   - Windows: Clique direito → "Executar como administrador"
   - Linux/macOS: `sudo python main.py`

2. **Feche Outros Programas:**
   - Libere recursos do sistema
   - Evite conflitos de permissão

3. **Use o Diagnóstico Completo com Moderação:**
   - Pode demorar vários minutos
   - Use ferramentas individuais para problemas específicos

4. **Monitore a Saída:**
   - Acompanhe o progresso das operações
   - Identifique onde ocorrem problemas

## 🔄 Atualizações e Manutenção

### Manter o Sistema Atualizado:
```bash
# Atualizar dependências
pip install --upgrade -r requirements.txt

# Verificar atualizações do Python
python --version
```

### Backup de Configurações:
- Salve logs regularmente
- Mantenha histórico de diagnósticos
- Use datas nos nomes dos arquivos

## 📞 Suporte

### Se Nenhuma Solução Funcionar:

1. **Colete Informações:**
   - Sistema operacional e versão
   - Versão do Python
   - Log completo de erro
   - Resultado de `python test_modules.py`

2. **Descreva o Problema:**
   - O que você estava tentando fazer
   - Qual ferramenta específica falhou
   - Mensagens de erro exatas

3. **Teste Alternativas:**
   - Use argumentos específicos: `python main.py --dns`
   - Teste ferramentas individuais
   - Verifique se o problema é específico de um módulo

## 🎯 Problemas Específicos por Ferramenta

### Verificação de Vírus
- **Problema:** Não detecta antivírus
- **Solução:** Execute como administrador

### Backup de Drivers

Observação: a funcionalidade de backup de drivers foi removida do menu principal e da GUI. Use ferramentas nativas (Windows Update, site do fabricante) ou `pnputil`/`dism` manualmente se necessário.
- **Problema:** Erro de permissão
- **Solução:** Execute como administrador

### Limpeza de Temporários
- **Problema:** Não consegue remover arquivos
- **Solução:** Execute como administrador

### Teste de Velocidade
- **Problema:** Teste muito lento
- **Solução:** Aguarde, pode demorar dependendo do hardware

### Diagnóstico DNS
- **Problema:** Não consegue resolver domínios
- **Solução:** Verifique conexão com internet

## ✅ Verificação Final

Após aplicar as soluções:

1. Execute `python test_modules.py` - deve mostrar todos OK
2. Execute `python main.py` - deve abrir o menu sem erros
3. Teste uma ferramenta simples como "Informações do Sistema"
4. Se tudo funcionar, teste o "Diagnóstico Completo" 