# csv_schema_evolution

Breve documentação do projeto csv_schema_evolution — ferramenta para validar, transformar e aplicar evolução controlada de esquemas em arquivos CSV.

## Visão geral
Esta ferramenta ajuda a:
- Validar CSVs contra um esquema (tipos, obrigatoriedade, formatos).
- Aplicar migrações de esquema (renomear colunas, converter tipos, adicionar/remover colunas).
- Gerar relatórios de compatibilidade entre versões de esquema.

## Requisitos
- Ubuntu 24.04+ (ambiente de desenvolvimento suportado)
- Docker (opcional)
- Ferramentas CLI: git, curl, python (ou runtime do projeto), pip/npm conforme implementação

## Instalação
Opção local (exemplo Python):
```bash
git clone <repo-url>
cd csv_schema_evolution
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Opção Docker:
```bash
docker build -t csv_schema_evolution .
docker run --rm -v "$(pwd)/data:/data" csv_schema_evolution <comando>
```

## Estrutura do repositório
- README.md — visão geral
- DOCUMENTATION.md — (este arquivo)
- src/ — código fonte
- schemas/ — versões de esquema (ex.: v1.json, v2.json)
- migrations/ — scripts de migração entre versões
- tests/ — casos de teste

## Uso
Validação de CSV contra um esquema:
```bash
csv-schema-cli validate --schema schemas/v1.json --input data/input.csv
```

Aplicar migração de esquema:
```bash
csv-schema-cli migrate --from v1 --to v2 --input data/input.csv --output data/output.csv
```

Gerar relatório de compatibilidade:
```bash
csv-schema-cli report --from schemas/v1.json --to schemas/v2.json --output report.md
```

## Formato de esquema (exemplo)
Formato JSON simples com tipos e regras:
```json
{
    "name": "v1",
    "columns": [
        {"name": "id", "type": "integer", "required": true},
        {"name": "email", "type": "string", "format": "email", "required": false},
        {"name": "created_at", "type": "datetime", "required": true}
    ]
}
```

## Estratégia de evolução
- Versões de esquema nomeadas (v1, v2, ...).
- Migrations são idempotentes: podem ser aplicadas apenas uma vez.
- Compatibilidade:
    - Backward compatible: novos campos opcionais, não alterar tipos existentes.
    - Breaking changes devem ter uma migration explícita e relatório de impacto.

## Testes
Rodar suíte de testes:
```bash
pytest tests/
```
Incluir casos para validação, migração e geração de relatório.

## Contribuição
- Fork -> branch feature -> PR com descrição das mudanças.
- Siga o padrão de commit e inclua testes para novas funcionalidades.
- Documente alterações de esquema em schemas/ e migrations/.

## Licença
Arquivo LICENSE no repositório. Informe-se antes de redistribuir.

## Contato
Abra issues para bugs ou propostas de melhoria.
