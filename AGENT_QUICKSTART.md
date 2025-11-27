# 🤖 QUICK START PARA AGENTES IA

Se você é um agente IA trabalhando neste repositório, leia isto primeiro.

## 📍 Localização: Você está em `csv_schema_evolution/`

Este é um projeto FastAPI + MongoDB para processar arquivos CSV com proteção contra injeção.

## 📖 Leia Isto (em ordem de prioridade)

1. **`.github/copilot-instructions.md`** ← **PRINCIPAL**
   - Arquitetura completa
   - Padrões de código
   - Exemplos de API (curl/JS)
   - Workflows recomendados

2. **`EXECUTIVE_SUMMARY.md`** ← **Para Contexto Rápido**
   - O que foi feito
   - Status de cada componente
   - Como usar

3. **`README.md`** ← **Para Visão Geral**
   - Overview do projeto
   - Tecnologias
   - Como rodar

## 🎯 Tarefas Comuns

### Entender a Arquitetura
→ Ler `.github/copilot-instructions.md` seção "Arquitetura (big picture)"

### Adicionar Nova Funcionalidade
→ Ler `.github/copilot-instructions.md` seção "Onde adicionar novos recursos"

### Rodar Testes
→ Ler `TESTING.md` seção "Executar Testes"

### Entender Flow de Upload
→ Ler `.github/copilot-instructions.md` seção "Padrões" (item "Flow de processamento")

### Adicionar Nova Validação
→ Editar `backend/app/utils/validators.py`

### Adicionar Nova Lógica de Processamento CSV
→ Editar `backend/app/services/csv_processor.py`

### Debugar Problema
→ Ver `TESTING.md` seção "Solução de Problemas"

## 🗂️ Estrutura de Pastas (O que fazer onde)

```
backend/app/
├── services/         ← Lógica de negócio (csv_processor, sanitize, storage)
├── api/v1/          ← Endpoints REST (files.py, health.py)
├── db/              ← Conexão com MongoDB
├── models/          ← Modelos Pydantic
├── utils/           ← Validadores e constantes
└── main.py          ← Aplicação FastAPI

tests/
├── unit/            ← Testes sem DB (test_csv_processor.py, test_sanitize.py)
└── integration/     ← Testes com DB (test_api_files.py)

frontend/
├── index.html       ← Interface web
└── assets/js/       ← Upload e listagem
```

## 🔑 Conceitos-Chave

### CSV Injection Prevention
- Prefixos perigosos: `=`, `+`, `-`, `@`
- Solução: Prefixar com `'` (apóstrofo)
- Arquivo: `backend/app/services/sanitize.py`

### GridFS Storage
- Armazena arquivos > 16MB
- Metadados em `db.files`
- Lazy-loading implementado
- Arquivo: `backend/app/db/mongo.py`

### Async Processing
- Motor para MongoDB async
- async/await em serviços
- TestClient para testes de API
- Framework: FastAPI + Uvicorn

## ⚡ Comandos Rápidos

```bash
# Ver arquitetura
cat .github/copilot-instructions.md

# Rodar testes rápidos (sem DB)
python run_tests.py

# Rodar todos os testes (com DB)
pytest tests/ -v --asyncio-mode=auto

# Rodar backend
cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker completo
docker-compose up --build
```

## 📚 Documentação por Tipo

| Leitor | Arquivo | Por que |
|--------|---------|---------|
| **Agente IA** | `.github/copilot-instructions.md` | Tem tudo que precisa |
| **Desenvolvedor** | `README.md` + `TESTING.md` | Como rodar e testar |
| **Gerente/Lead** | `EXECUTIVE_SUMMARY.md` | Status e funcionalidades |
| **Novo no projeto** | `EXECUTIVE_SUMMARY.md` depois `.github/copilot-instructions.md` | Contexto depois detalhes |
| **Debugando** | `TESTING.md` seção Solução de Problemas | Erros comuns e soluções |

## 💡 Dicas Para Agentes IA

### Antes de Começar
1. Ler `.github/copilot-instructions.md`
2. Entender a arquitetura (big picture)
3. Conhecer os padrões (Flow de processamento)
4. Revisar exemplos de requests

### Ao Fazer Mudanças
1. Manter padrões do projeto
2. Usar async/await corretamente
3. Aplicar sanitização quando necessário
4. Atualizar testes correspondentes

### Ao Testar
1. Use `pytest tests/unit/` para testes sem DB
2. Use `pytest tests/integration/` com MongoDB rodando
3. Veja `TESTING.md` para detalhes

### Ao Debugar
1. Verificar logs do backend
2. Consultar `TESTING.md` solução de problemas
3. Rodar `python run_tests.py` para validação rápida
4. Checar `.github/copilot-instructions.md` exemplos

## 🚨 Armadilhas Comuns

❌ **ERRADO**: Esquecer de usar `await` em funções async
✅ **CERTO**: `result = await process_csv(file_id)`

❌ **ERRADO**: Não sanitizar valores de CSV
✅ **CERTO**: `value = sanitize_value(row_value)`

❌ **ERRADO**: Testar sem mocks (vai falhar sem MongoDB)
✅ **CERTO**: Usar fixtures do conftest.py

❌ **ERRADO**: Mudar tamanho máximo sem atualizar validadores
✅ **CERTO**: Editar `MAX_FILE_SIZE` em `validators.py`

## ✅ Checklist Antes de Submeter PR

- [ ] Leu `.github/copilot-instructions.md`
- [ ] Seguiu padrões do projeto
- [ ] Rodou testes: `pytest tests/ -v --asyncio-mode=auto`
- [ ] Atualizou documentação se necessário
- [ ] Sem console.log/print de debug
- [ ] Nomes de variáveis claros
- [ ] Funções com type hints

## 🆘 Precisa de Ajuda?

1. **Sobre arquitetura**: → `.github/copilot-instructions.md`
2. **Sobre testes**: → `TESTING.md`
3. **Sobre status**: → `EXECUTIVE_SUMMARY.md`
4. **Sobre código específico**: → Ler o arquivo + `.github/copilot-instructions.md`

## 📊 Status Atual

- ✅ Todos os componentes implementados
- ✅ Código validado e testando
- ✅ Documentação completa
- ✅ Pronto para produção

---

**Bora começar!** 🚀

Próxima ação: Ler `.github/copilot-instructions.md`
