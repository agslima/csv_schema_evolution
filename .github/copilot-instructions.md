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
- Rodar testes simples (sem pytest hanging): `python run_tests.py` (testes básicos de sanitização e validadores).
- Rodar todos os testes com pytest: `pytest -v` (pasta `tests/` com `unit/` e `integration/`).
  - **Nota**: testes de integração requerem MongoDB rodando; use `docker-compose up` para ambiente completo.
- Subir ambiente completo (recomendado para desenvolvimento):
  - `docker-compose up --build` (arquivo na raiz `docker-compose.yml`).
- Executar localmente o backend (se preferir sem Docker): usar Uvicorn apontando para o módulo FastAPI:
  - `cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000` (ambiente Python ativado, MongoDB acessível).
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
- Testes básicos sem DB: `python run_tests.py` — valida `sanitize_value`, tamanho máximo e constantes.
- Unit tests: `tests/unit/` — testes isolados de sanitização e processamento CSV (com mocks).
- Integration tests: `tests/integration/test_api_files.py` — cenários upload → process → delete/download (requer MongoDB).
- Logs: adicione `print()` ou `logging` no serviço alterado e rode `docker-compose up` ou `uvicorn` com `--reload` para reproduzir.

## Exemplos de Requests HTTP

Todos os exemplos usam `BASE_URL=http://localhost:8000` (ajuste conforme necessário).

### Upload (POST /api/v1/files/upload)
```bash
# Sem id_field
curl -X POST "http://localhost:8000/api/v1/files/upload" \
  -F "file=@myfile.csv"

# Com id_field (query param)
curl -X POST "http://localhost:8000/api/v1/files/upload?id_field=record_id" \
  -F "file=@myfile.csv"
```

**Resposta (200 OK)**
```json
{
  "id": "654f7a2b9c1e4b3a...",
  "filename": "myfile.csv",
  "status": "processed",
  "records_count": 12,
  "fields": ["name", "email", "created_at"]
}
```

### Listar Arquivos (GET /api/v1/files/)
```bash
curl "http://localhost:8000/api/v1/files/"
```

**Resposta**
```json
[
  {
    "id": "654f7a2b9c1e4b3a...",
    "filename": "myfile.csv",
    "status": "processed",
    "records_count": 12,
    "fields": ["name","email","created_at"]
  }
]
```

### Download (GET /api/v1/files/{file_id}/download)
```bash
curl -OJ "http://localhost:8000/api/v1/files/654f7a2b9c1e4b3a.../download"
```

### Deletar (DELETE /api/v1/files/{file_id})
```bash
curl -X DELETE "http://localhost:8000/api/v1/files/654f7a2b9c1e4b3a..."
```

**Resposta (200 OK)**
```json
{"status":"deleted"}
```

### Health Check (GET /api/v1/health/)
```bash
curl "http://localhost:8000/api/v1/health/"
```

**Resposta**
```json
{"status":"ok"}
```

### JavaScript (Browser) — Upload com FormData
```javascript
const BASE_URL = "http://localhost:8000";

async function uploadFile(file, idField = null) {
  const form = new FormData();
  form.append("file", file);

  const url = new URL(`${BASE_URL}/api/v1/files/upload`);
  if (idField) url.searchParams.append("id_field", idField);

  const res = await fetch(url.toString(), { method: "POST", body: form });
  if (!res.ok) throw new Error(`Upload failed: ${res.statusText}`);
  return res.json();
}

// Uso:
// uploadFile(fileInput.files[0], "record_id").then(console.log);
```

### Node.js — Upload com axios + FormData
```javascript
const axios = require("axios");
const fs = require("fs");
const FormData = require("form-data");

async function uploadFile(path, idField) {
  const form = new FormData();
  form.append("file", fs.createReadStream(path));
  const url = `http://localhost:8000/api/v1/files/upload${idField ? `?id_field=${idField}` : ""}`;
  const res = await axios.post(url, form, { headers: form.getHeaders() });
  return res.data;
}
```

## Observações / Detalhes Técnicos
- O `README.md` menciona "Flask"; o código atual usa **FastAPI**. Ignore a documentação desatualizada e confie na implementação em `backend/app/`.
- O upload é processado **sincronamente** — o endpoint aguarda `process_csv` terminar antes de retornar, bloqueando para arquivos grandes.
- CSV Injection: células com prefixo `=`, `+`, `-`, `@` são sanitizadas com `'` em `sanitize.py`; veja fluxo em `csv_processor.py`.
- GridFS: metadados são salvos na coleção `db.files` com campos `status`, `fields`, `records_count`. 
