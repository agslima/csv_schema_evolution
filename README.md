# CSV-Transposer

![Status](https://github.com/agslima/csv_schema_evolution/actions/workflows/ci.yml/badge.svg)

Sistemas de classificação de dados

````markdown
# 📊 CSV Uploader – Full Stack App (Flask + MongoDB)

Aplicação web para **upload, processamento e download de arquivos CSV**, com:
- UI moderna e responsiva.
- Barra de progresso e mensagens visuais.
- Paginação e busca na lista de arquivos.
- Backend seguro em **Flask**.
- Armazenamento de arquivos no **MongoDB (GridFS)**.
- Testes automatizados com **pytest**.
- Workflow de CI/CD com **GitHub Actions**.
- Docker Compose para ambiente completo.

---

## 🧩 Arquitetura

```text
csv-uploader/
├── app/
│   ├── main.py              # Aplicação Flask principal
│   ├── routes.py            # Rotas API (upload, listagem, download)
│   ├── services.py          # Lógica de processamento CSV
│   ├── db.py                # Conexão MongoDB e GridFS
│   ├── utils.py             # Funções auxiliares (segurança, logs)
│   ├── static/              # CSS / JS / Ícones
│   ├── templates/           # HTML (frontend)
│   └── tests/
│       ├── test_api.py      # Testes de API (pytest)
│       └── test_logic.py    # Testes de lógica CSV
│
├── .github/
│   └── workflows/
│       └── ci.yml           # GitHub Actions (testes + build Docker)
│
├── Dockerfile               # Build da imagem Flask
├── docker-compose.yml       # Flask + MongoDB + Mongo Express
├── requirements.txt         # Dependências Python
└── README.md                # Documentação
````

---

## ⚙️ Funcionalidades

* **Upload seguro de CSVs** (máx. 50 MB).
* **Processamento backend Python**:

  * Detecta delimitador automaticamente (`,` ou `;`).
  * Corrige campos, gera schema dinâmico.
  * Previne CSV Injection.
* **Armazenamento MongoDB** via GridFS.
* **Listagem de arquivos** com:

  * Busca por nome.
  * Paginação.
* **Download** de arquivos processados.
* **Logs automáticos** de campos e ocorrências.

---

## 🧠 Stack Tecnológica

| Camada        | Tecnologia              |
| ------------- | ----------------------- |
| **Backend**   | Flask (Python 3.10+)    |
| **Banco**     | MongoDB (GridFS)        |
| **Frontend**  | HTML + JS + Bootstrap   |
| **Testes**    | pytest                  |
| **CI/CD**     | GitHub Actions          |
| **Container** | Docker / Docker Compose |

---

## 🪄 Instalação Local

### 1️⃣ Clonar o repositório

```bash
git clone https://github.com/seuusuario/csv-uploader.git
cd csv-uploader
```

### 2️⃣ Configurar ambiente

Crie e ative o ambiente virtual:

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 4️⃣ Executar com Docker Compose

```bash
docker-compose up --build
```

O app estará disponível em **[http://localhost:5000](http://localhost:5000)**

---

## 💻 Uso

1. Acesse a interface web.
2. Faça upload de um ou mais arquivos CSV.
3. Aguarde o processamento (com barra de progresso).
4. Baixe o arquivo processado ou visualize na lista.
5. Use a busca para encontrar arquivos anteriores.

---

## 🧪 Testes Automatizados

Execute todos os testes:

```bash
pytest -v
```

Tipos de testes:

* **test_logic.py** → valida parsing e processamento CSV.
* **test_api.py** → valida upload, listagem e download (API REST).

---

## 🔒 Segurança

* Upload limitado a **50 MB**.
* Aceita **apenas arquivos CSV** (`.csv`).
* Proteção contra **CSV Injection** (`=`, `+`, `-`, `@` no início de célula).
* Filtragem de entradas de usuário.
* Logging e mensagens de erro seguros.

---

## ⚙️ CI/CD com GitHub Actions

Arquivo: `.github/workflows/ci.yml`

Executa automaticamente:

* Instala dependências.
* Roda testes (`pytest`).
* Faz build da imagem Docker.

---

## 🐳 Docker Compose

Arquivo: `docker-compose.yml`

Serviços incluídos:

* `web`: app Flask.
* `mongo`: banco de dados.
* `mongo-express`: painel web em [http://localhost:8081](http://localhost:8081).

Subir ambiente:

```bash
docker-compose up --build
```

---

## 🧾 API Endpoints (REST)

| Método   | Endpoint         | Descrição                             |
| -------- | ---------------- | ------------------------------------- |
| `POST`   | `/upload`        | Faz upload de um ou mais arquivos CSV |
| `GET`    | `/files`         | Lista arquivos com paginação e busca  |
| `GET`    | `/download/<id>` | Faz download do arquivo processado    |
| `DELETE` | `/files/<id>`    | Remove arquivo do MongoDB             |

---

## 📈 Possíveis Melhorias Futuras

* Autenticação (JWT / OAuth2).
* Dashboard de estatísticas.
* Controle de versão de arquivos.
* Processamento assíncrono com Celery + Redis.
* Interface React/Vue para UX avançada.

---

## 👨‍💻 Autor

**Agnaldo Silva Lima**
🔗 [LinkedIn](https://www.linkedin.com/in/agnaldo-silva-lima)
💡 Projeto desenvolvido com foco em usabilidade, segurança e boas práticas de engenharia de software.

---
