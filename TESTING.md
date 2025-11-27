# Como Executar Testes

Este documento descreve como executar os testes do projeto csv_schema_evolution.

## Pré-requisitos

### 1. Dependências do Python

Instale todas as dependências necessárias:

```bash
cd backend
pip install -r requirements.txt

# Dependências de teste adicionais
pip install pytest pytest-asyncio httpx
```

### 2. MongoDB (Opcional para testes unitários)

Para testes de integração, o MongoDB deve estar disponível:

```bash
# Usando Docker Compose
docker-compose up -d
```

## Executar Testes

### Opção 1: Todos os testes com pytest

```bash
cd /workspaces/csv_schema_evolution
pytest tests/ -v --asyncio-mode=auto
```

### Opção 2: Apenas testes unitários (sem MongoDB necessário)

```bash
pytest tests/unit/ -v
```

Estes testes usam mocks e não requerem MongoDB rodando.

### Opção 3: Apenas testes de integração (requer MongoDB)

```bash
pytest tests/integration/ -v
```

### Opção 4: Executar teste específico

```bash
# Teste de sanitização
pytest tests/unit/test_sanitize.py::test_sanitize_value -v

# Teste de processamento CSV
pytest tests/unit/test_csv_processor.py::test_process_csv -v

# Teste de upload
pytest tests/integration/test_api_files.py::test_upload_file -v
```

## Teste Rápido (sem pytest)

Se preferir testar sem pytest/MongoDB:

```bash
python run_tests.py
```

Este script executa testes básicos de sanitização diretamente.

## Saída Esperada

Um teste bem-sucedido terá saída similar a:

```
tests/unit/test_sanitize.py::test_sanitize_value PASSED
tests/unit/test_csv_processor.py::test_process_csv PASSED
tests/unit/test_csv_processor.py::test_process_csv_with_injection PASSED
tests/integration/test_api_files.py::test_upload_file PASSED
...

====== X passed in Y.XXs ======
```

## Cobertura de Testes

Para gerar relatório de cobertura:

```bash
pytest tests/ --cov=app --cov-report=html
```

Isso criará um relatório em `htmlcov/index.html`

## Solução de Problemas

### Erro: `ModuleNotFoundError: No module named 'app'`

**Solução**: O conftest.py adiciona `backend` ao sys.path automaticamente. Se não funcionar:

```bash
cd /workspaces/csv_schema_evolution
export PYTHONPATH="${PYTHONPATH}:$(pwd)/backend"
pytest tests/ -v
```

### Erro: `RuntimeError: Event loop is closed`

**Solução**: Use `pytest-asyncio` com asyncio-mode:

```bash
pytest tests/ -v --asyncio-mode=auto
```

### Erro: `Connection refused` (MongoDB)

**Solução**: Para testes que precisam de MongoDB:

```bash
docker-compose up -d
```

Ou use apenas testes unitários que não requerem MongoDB:

```bash
pytest tests/unit/ -v
```

## Estrutura dos Testes

```
tests/
├── conftest.py              # Configuração pytest com mocks
├── unit/
│   ├── test_sanitize.py    # Testes de injeção CSV
│   └── test_csv_processor.py # Testes de processamento CSV
└── integration/
    └── test_api_files.py   # Testes de API REST
```

## Validação de Código

Os testes validam:

1. **Sanitização**: Previne CSV Injection com prefixos `=`, `+`, `-`, `@`
2. **Processamento**: Lê CSVs do GridFS e processa registros corretamente
3. **API**: Endpoints funcionam com upload, listagem, download e deleção
4. **Banco de dados**: Integração com MongoDB via Motor (async)

---

Para mais informações, consulte `.github/copilot-instructions.md`
