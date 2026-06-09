# 🎉 EventFlow

> Sistema de Gerenciamento de Eventos Comunitários  
> **UNAMA · Análise e Desenvolvimento de Sistemas · Projeto de Banco de Dados**

---

## 📌 Descrição do Sistema

O **EventFlow** é uma API REST construída com **Python + FastAPI** e banco de dados **MongoDB**. Ela centraliza o gerenciamento de eventos realizados em comunidades (bairros, escolas, igrejas), permitindo que moradores se inscrevam, avaliem e comentem os eventos, enquanto organizadores controlam locais, categorias, patrocinadores e notificações.

---

## 📦 Tecnologias

| Ferramenta | Versão | Papel |
|------------|--------|-------|
| Python     | 3.11+  | Linguagem principal |
| FastAPI    | 0.111  | Framework web / geração automática de docs |
| Motor      | 3.4    | Driver assíncrono para MongoDB |
| MongoDB    | 7.x    | Banco de dados NoSQL (documento) |
| Pydantic   | 2.7    | Validação e serialização de dados |
| Uvicorn    | 0.29   | Servidor ASGI |

---

## 🗂️ Coleções do Banco de Dados (10)

### 1. `eventos`
```json
{
  "_id": "ObjectId",
  "titulo": "Feira Cultural do Guamá",
  "descricao": "Arte, música e comida típica paraense.",
  "data_inicio": "ISODate",
  "data_fim": "ISODate",
  "local_id": "string (ref → locais)",
  "categoria_id": "string (ref → categorias)",
  "organizador_id": "string (ref → usuarios)",
  "capacidade_maxima": 300,
  "status": "ativo | cancelado | encerrado",
  "gratuito": true,
  "valor_ingresso": 0.0,
  "tags": ["string"],
  "criado_em": "ISODate"
}
```

### 2. `usuarios`
```json
{
  "_id": "ObjectId",
  "nome": "Ana Tavares",
  "email": "ana@email.com",
  "telefone": "(91) 99999-0000",
  "bairro": "Nazaré",
  "cidade": "Belém",
  "senha_hash": "string",
  "ativo": true,
  "criado_em": "ISODate"
}
```

### 3. `categorias`
```json
{
  "_id": "ObjectId",
  "nome": "Cultural",
  "descricao": "Saraus, feiras, exposições",
  "cor_hex": "#8B5CF6",
  "icone": "string (opcional)"
}
```

### 4. `comentarios`
```json
{
  "_id": "ObjectId",
  "evento_id": "string",
  "usuario_id": "string",
  "texto": "Mal posso esperar!",
  "criado_em": "ISODate",
  "editado": false
}
```

### 5. `inscricoes`
```json
{
  "_id": "ObjectId",
  "evento_id": "string",
  "usuario_id": "string",
  "status": "confirmada | cancelada | lista_espera",
  "presenca_confirmada": false,
  "criado_em": "ISODate"
}
```

### 6. `locais`
```json
{
  "_id": "ObjectId",
  "nome": "Praça da República",
  "endereco": "Praça da República, s/n",
  "bairro": "Campina",
  "cidade": "Belém",
  "estado": "PA",
  "capacidade": 500,
  "coordenadas": { "lat": -1.4558, "lng": -48.5025 }
}
```

### 7. `patrocinadores`
```json
{
  "_id": "ObjectId",
  "nome": "Açaí do Pará",
  "contato_email": "contato@acaidopara.com",
  "nivel": "bronze | prata | ouro | diamante",
  "site": "https://..."
}
```

### 8. `notificacoes`
```json
{
  "_id": "ObjectId",
  "usuario_id": "string",
  "titulo": "Inscrição confirmada!",
  "mensagem": "Você está inscrito na Feira Cultural do Guamá.",
  "tipo": "info | alerta | confirmacao",
  "lida": false,
  "evento_id": "string (opcional)",
  "criado_em": "ISODate"
}
```

### 9. `avaliacoes`
```json
{
  "_id": "ObjectId",
  "evento_id": "string",
  "usuario_id": "string",
  "nota": 5,
  "comentario": "Melhor evento do bairro!",
  "criado_em": "ISODate"
}
```

### 10. `tags`
```json
{
  "_id": "ObjectId",
  "nome": "Família",
  "slug": "familia"
}
```

---

## 🔍 Consultas Implementadas (5 tipos)

| # | Tipo | Endpoint | Descrição |
|---|------|----------|-----------|
| 1 | Consulta Simples | `GET /eventos/busca/titulo?q=feira` | Busca por título com regex |
| 2 | Comparação (operadores) | `GET /eventos/busca/capacidade?minimo=100` | Capacidade `≥ N` com `$gte` |
| 3 | Múltiplas condições (AND) | `GET /eventos/busca/ativos-gratuitos` | Status + gratuito com `$and` |
| 4 | Campo aninhado | `GET /eventos/busca/por-campo?campo=coordenadas.cidade&valor=Belém` | Acesso a subdocumento |
| 5 | Comparação de data | `GET /eventos/busca/proximos` | Eventos futuros com `$gt` em data |

---

## ⚙️ Pipelines de Agregação (3)

### Pipeline 1 – Participantes por evento
```
GET /eventos/agregacao/participantes-por-evento
```
Junta `inscricoes` com `eventos` via `$lookup`, agrupa por `evento_id` e conta inscrições confirmadas.

### Pipeline 2 – Média de avaliações por evento
```
GET /eventos/agregacao/media-avaliacoes
```
Usa `$group` com `$avg` para calcular a nota média recebida por cada evento.

### Pipeline 3 – Eventos mais comentados
```
GET /eventos/agregacao/mais-comentados
```
Conta comentários por evento com `$group`, enriquece com dados do evento via `$lookup` e ordena pelo total.

---

## 🏗️ Justificativas de Modelagem

**Por que NoSQL / MongoDB?**  
Eventos têm estrutura variável (uns têm coordenadas, outros não; uns têm patrocinadores, outros são locais). MongoDB permite que cada documento tenha apenas os campos que fazem sentido para ele, sem `NULL` espalhado por colunas vazias.

**Referências por string em vez de ObjectId nativo**  
Os `evento_id`, `usuario_id` etc. são armazenados como `string` para facilitar a integração com a API sem conversões manuais constantes. Nos pipelines de agregação, usamos `$toObjectId` onde o `$lookup` precisa do tipo correto.

**Tags como array de strings dentro do evento**  
Tags são propriedades do evento e raramente mudam de forma isolada. Embutir os IDs diretamente evita joins desnecessários na leitura, que é a operação mais frequente.

**Notificações desacopladas**  
Mantemos notificações como coleção separada (e não subdocumento do usuário) para escalar o volume de mensagens sem inflar o documento principal do usuário.

---

## 🚀 Como executar localmente

### Pré-requisitos
- Python 3.11+
- MongoDB rodando em `localhost:27017` (ou via Docker)

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/eventflow.git
cd eventflow
```

### 2. Crie o ambiente virtual e instale dependências
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente
```bash
cp .env.example .env
# Edite .env se necessário
```

### 4. Popule o banco com dados de exemplo
```bash
python scripts/seed.py
```

### 5. Suba a API
```bash
uvicorn app.main:app --reload
```

### 6. Acesse a documentação interativa
```
http://localhost:8000/docs
```

---

## 📁 Estrutura do Projeto

```
eventflow/
├── app/
│   ├── main.py                  # Ponto de entrada da API
│   ├── database/
│   │   ├── connection.py        # Conexão com MongoDB
│   │   └── utils.py             # Serialização de documentos
│   ├── models/
│   │   └── schemas.py           # Modelos Pydantic (10 coleções)
│   └── routers/
│       ├── eventos.py           # CRUD + 5 consultas + 3 agregações
│       ├── usuarios.py
│       ├── categorias.py
│       ├── comentarios.py
│       ├── inscricoes.py
│       ├── locais.py
│       ├── patrocinadores.py
│       ├── notificacoes.py
│       ├── avaliacoes.py
│       └── tags.py
├── scripts/
│   └── seed.py                  # Popula o banco com dados realistas
├── requirements.txt
├── .env.example
└── README.md
```
