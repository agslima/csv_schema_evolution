<!-- Copilot instructions for AI coding agents in this repository -->

# Agent Instructions — csv_schema_evolution

Resumo curto: este repositório expõe uma API de upload/processing de CSVs (backend em FastAPI, armazenamento em MongoDB GridFS, frontend JS simples). As instruções abaixo destacam a arquitetura, padrões e comandos concretos que ajudam um agente a ser produtivo imediatamente.

## Arquitetura (big picture)
- **Frontend**: arquivos estáticos em `frontend/` (`upload.js`, `files_list.js`) chamam a API REST para upload/listagem/download.
- **Backend**: FastAPI no diretório `backend/app/`.
  - Entrypoint: `backend/app/main.py` (routers montados em `/api/v1/files` e `/api/v1/health`).
  - Rotas: `backend/app/api/v1/files.py` (upload, list, download, delete) e `backend/app/api/v1/health.py`.
- **Serviços**: separação clara em `backend/app/services/`:
  - `csv_processor.py`: lê CSV a partir do GridFS, aplica sanitização e gera registros.
  - `storage.py`: grava/recupera arquivos no GridFS e gerencia metadados em `db.files`.
  - `sanitize.py`: proteção contra CSV Injection (`sanitize_value`).
- **DB**: MongoDB + GridFS abstraídos em `backend/app/db/mongo.py`.

## Padrões e convenções específicos
- Arquivo máximo: 50 MB (constante `MAX_FILE_SIZE` em `backend/app/utils/validators.py`). Validação básica é feita em `validate_csv_file` e checagem de tamanho no `storage.save_file`.
- CSV Injection: qualquer campo que comece com `=`, `+`, `-` ou `@` é prefixado com `'` por `sanitize_value` em `backend/app/services/sanitize.py`.
- Flow de processamento:
  1. Upload via rota API (`/api/v1/files`) → `storage.save_file` salva bytes no GridFS e registra metadados com `status: "pending"`.
  2. `csv_processor.process_csv(file_id, id_field=None)` lê do GridFS, aplica `sanitize_value`, constrói registros dinamicamente e atualiza metadados (`status: "processed"`, `fields`, `records_count`).
- Naming / structure: mantenha a lógica síncrona/assíncrona dos serviços (as funções `save_file`, `process_csv` são `async`).
- Erros: o backend usa `fastapi.HTTPException` para validações (veja `validators.py`) e lança `ValueError` em casos internos que o agente deve propagar ou traduzir para 5xx/4xx conforme contexto.

## Comandos úteis / workflows
- Rodar todos os testes: `pytest -v` (pasta `tests/` com `unit/` e `integration/`).
- Subir ambiente completo (recomendado para desenvolvimento):
  - `docker-compose up --build` (arquivo na raiz `docker-compose.yml`).
- Executar localmente o backend (se preferir sem Docker): usar Uvicorn apontando para o módulo FastAPI:
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (execute com `cwd=backend/` e ambiente Python ativado).
- CI: referência `.github/workflows/ci.yml` (instala dependências e roda `pytest` + build docker). Alinhe mudanças de dependência com `backend/requirements.txt`.

## Integrações e pontos de atenção
- GridFS: `backend/app/services/storage.py` usa `fs_bucket.open_upload_stream` / `open_download_stream_by_name` e mantém metadados em `db.files`.
- Frontend ↔ Backend: `frontend/js/upload.js` e `frontend/js/files_list.js` chamam endpoints sob `/api/v1/files`; adaptar nomes de rota e payloads conforme esses arquivos.
- Validação de upload: ver `validate_csv_file` (extensão `.csv` e content-type esperados). O tamanho é verificado após leitura dos bytes em `storage.save_file`.

## Exemplos concretos que o agente pode editar/usar
- Para neutralizar CSV injection, use `from app.services.sanitize import sanitize_value` e aplique antes de persistir ou responder.
- Para salvar um `UploadFile` async e respeitar tamanho máximo:

```py
from app.services.storage import save_file
file_id = await save_file(uploaded_file)
```

- Para processar um CSV já gravado (id: `file_id`):

```py
from app.services.csv_processor import process_csv
records = await process_csv(file_id, id_field=None)
```

## Onde adicionar novos recursos / como integrar
- Novas validações → `backend/app/utils/validators.py`.
- Lógica de processamento → `backend/app/services/csv_processor.py`.
- Acesso a GridFS / mudanças de schema → `backend/app/db/mongo.py` e `backend/app/services/storage.py`.

## Testes e debugging rápidos
- Unit tests: `tests/unit/` — comece por `test_csv_processor.py` ao alterar parsing/sanitize.
- Integration tests: `tests/integration/test_api_files.py` para cenários upload → process → download.
- Logs: aplicar prints/`logging` no serviço alterado e rodar `docker-compose up` ou `uvicorn` para reproduzir.

## Observações / inconsistências notadas
- O `README.md` descreve uma versão Flask do app; o código atual usa **FastAPI**. Prefira confiar nos arquivos dentro de `backend/app/` para determinar runtime e rotas.

---
Se quiser, atualizo exemplos de request/responses usando os handlers em `backend/app/api/v1/files.py` ou adiciono snippets de testes `pytest` para validar mudanças. Quais partes você quer que eu detalhe mais? 
