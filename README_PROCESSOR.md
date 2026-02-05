# CommandProcessor - Processador de Comandos

## Descrição

Este módulo implementa a classe `CommandProcessor` que substitui a antiga abordagem baseada em tuplas (`TuplaDeComandos`) por um sistema mais organizado baseado em dicionários.

## Estrutura do Projeto

```
app/
├── __init__.py
├── actions/
│   ├── __init__.py
│   ├── gui_commands.py      # Comandos relacionados à interface gráfica
│   └── business_logic.py    # Comandos de lógica de negócio
└── core/
    ├── __init__.py
    ├── config.py
    └── processor.py          # Classe CommandProcessor
```

## Componentes

### 1. `app/actions/gui_commands.py`

Contém funções relacionadas à interação com a interface gráfica e automação:

- `falar(texto)` - Fala o texto usando text-to-speech
- `digitar(texto)` - Digita o texto usando o controlador de teclado
- `aperta(botao)` - Pressiona tecla(s) especificada(s)
- `abrirgaveta(teste)` - Abre gaveta usando atalho de teclado
- `clicarNaNet(comando)` - Clica em elemento no navegador
- `abrirInternet(teste)` - Abre navegador

### 2. `app/actions/business_logic.py`

Contém funções de lógica de negócio específicas do domínio:

- `FazerRequisicaoSulfite(teste)` - Cria requisição de sulfite
- `FazerRequisicaoPT1(teste)` - Cria requisição geral
- `AbrirPlanilha(teste)` - Abre planilha
- `AtualizarInventario(teste)` - Atualiza inventário
- `ImprimirBalancete(teste)` - Imprime balancete
- `AbrirAlmox(teste)` - Abre sistema de almoxarifado
- `Cod4rMaterial(teste)` - Codifica material
- `QuantMaterial()` - Processa quantidade de material
- `ConsultarEstoque(teste)` - Consulta estoque
- `abrirsite(comando)` - Abre site baseado no comando

### 3. `app/core/processor.py`

Classe principal `CommandProcessor`:

#### Inicialização

```python
from app.core.processor import CommandProcessor

processor = CommandProcessor()
```

Ao ser inicializada, a classe cria um dicionário que mapeia strings de comando para suas funções correspondentes.

#### Método `execute(comando: str)`

Executa um comando identificando a ação correta e executando-a:

```python
processor.execute("falar olá mundo")
processor.execute("planilha financeira")
processor.execute("sulfite")
```

O método:
1. Itera pelos comandos registrados
2. Verifica se a chave do comando está presente na string de comando
3. Remove a chave do comando da string para obter os parâmetros
4. Executa a ação com os parâmetros
5. Retorna o resultado da ação ou `None` se nenhum comando for encontrado

## Comparação: Antiga vs Nova Abordagem

### Abordagem Antiga (assistente.pyw)

```python
TuplaDeComandos = {
    ('sulfite', FazerRequisicaoSulfite),
    ('requisição', FazerRequisicaoPT1),
    ('planilha', AbrirPlanilha),
    ...
}

for comandos, acao in TuplaDeComandos:
    if comandos in comando:
        comando = comando.replace(f'{comandos} ', '')
        acao(comando)
```

**Problemas:**
- Usa um set de tuplas, que não é a estrutura de dados mais apropriada
- Lógica de execução misturada com definição de comandos
- Difícil de manter e estender
- Todas as funções e imports no mesmo arquivo

### Nova Abordagem (CommandProcessor)

```python
from app.core.processor import CommandProcessor

processor = CommandProcessor()
processor.execute(comando)
```

**Vantagens:**
- Separação clara de responsabilidades (GUI vs Lógica de Negócio)
- Estrutura de dicionário mais apropriada
- Código organizado em módulos
- Fácil de testar e manter
- API simples e clara

## Comandos Registrados

Os seguintes comandos estão registrados no CommandProcessor:

| Comando | Função | Tipo |
|---------|--------|------|
| `sulfite` | `FazerRequisicaoSulfite` | Business Logic |
| `requisição` | `FazerRequisicaoPT1` | Business Logic |
| `planilha` | `AbrirPlanilha` | Business Logic |
| `inventário` | `AtualizarInventario` | Business Logic |
| `balancete` | `ImprimirBalancete` | Business Logic |
| `almoxarifado` | `AbrirAlmox` | Business Logic |
| `digitar produto` | `Cod4rMaterial` | Business Logic |
| `digitar quantidade` | `QuantMaterial` | Business Logic |
| `gaveta` | `abrirgaveta` | GUI |
| `escreva` | `digitar` | GUI |
| `aperte` | `aperta` | GUI |
| `falar` | `falar` | GUI |
| `internet` | `abrirInternet` | GUI |
| `estoque` | `ConsultarEstoque` | Business Logic |
| `site` | `abrirsite` | Business Logic |
| `clicar em` | `clicarNaNet` | GUI |

## Exemplo de Uso

Veja o arquivo `exemplo_processor.py` para uma demonstração completa de como usar o CommandProcessor.

```python
from app.core.processor import CommandProcessor

# Criar instância
processor = CommandProcessor()

# Executar comandos
processor.execute("falar olá mundo")
processor.execute("planilha financeira")
processor.execute("sulfite")
```

## Testes

Para testar o CommandProcessor sem instalar todas as dependências, você pode usar mocks:

```python
import sys
from unittest.mock import MagicMock

# Mock das dependências externas
sys.modules['pynput'] = MagicMock()
sys.modules['pynput.keyboard'] = MagicMock()
sys.modules['pyautogui'] = MagicMock()
sys.modules['pyttsx3'] = MagicMock()
sys.modules['pandas'] = MagicMock()
sys.modules['webbrowser'] = MagicMock()

# Agora pode importar e testar
from app.core.processor import CommandProcessor
processor = CommandProcessor()
```

## Próximos Passos

Para integrar o CommandProcessor no `assistente.pyw`:

1. Importar o CommandProcessor:
   ```python
   from app.core.processor import CommandProcessor
   ```

2. Criar uma instância global:
   ```python
   command_processor = CommandProcessor()
   ```

3. Substituir a função `comandos()` para usar o processor:
   ```python
   def comandos(comando):
       command_processor.execute(comando)
   ```

Isso substituirá completamente a antiga `TuplaDeComandos` mantendo a mesma funcionalidade.
