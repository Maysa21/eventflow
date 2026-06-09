# 🎬 Roteiro de Apresentação — EventFlow
**Disciplina: Projeto de Banco de Dados | UNAMA**  
Tempo estimado: 15–20 minutos | 3 integrantes

---

## ──────────────────────────────
## 🟣 PARTE 1 — [INTEGRANTE A]
### "Visão Geral e Modelagem"
## ──────────────────────────────

---

### SLIDE 1 — Capa
**Texto no slide:**
```
EventFlow
Sistema de Gerenciamento de Eventos Comunitários

Python · FastAPI · MongoDB
```

**Fala:**  
"Olá, pessoal. Nosso projeto se chama EventFlow — um sistema pensado pra gerenciar eventos de comunidades: bairros, escolas, igrejas. A gente escolheu construir uma API REST usando Python com FastAPI, e o banco de dados é o MongoDB. Vou começar explicando o problema que a gente resolveu e como modelamos os dados."

---

### SLIDE 2 — O Problema
**Texto no slide:**
```
O problema

Eventos comunitários existem,
mas a organização é caótica.

→ WhatsApp pra inscrição
→ Papel pra lista de presença  
→ Nenhum feedback registrado
```

**Fala:**  
"A maioria dos eventos de bairro ainda é organizada no improviso: a inscrição é um link de formulário do Google, a lista de presença é uma folha de papel, e depois do evento ninguém sabe quantas pessoas foram, o que acharam, nada. O EventFlow resolve exatamente isso."

---

### SLIDE 3 — As 10 Coleções
**Texto no slide:**
```
10 coleções no MongoDB

eventos        inscrições
usuários       locais
categorias     patrocinadores
comentários    notificações
avaliações     tags
```

**Fala:**  
"No MongoDB, organizamos os dados em dez coleções. As quatro principais são eventos, usuários, categorias e comentários — que eram as pedidas no trabalho. Mas pra ter um sistema real, a gente foi além: adicionamos locais, inscrições, avaliações, patrocinadores, notificações e tags. Cada uma tem um papel específico."

---

### SLIDE 4 — Estrutura de um Documento (Evento)
**Texto no slide:**
```json
{
  "titulo": "Feira Cultural do Guamá",
  "status": "ativo",
  "gratuito": true,
  "capacidade_maxima": 300,
  "tags": ["familia", "cultura"],
  "coordenadas": { "lat": -1.47, "lng": -48.50 }
}
```

**Fala:**  
"Aqui tá um exemplo do documento de evento. Repara que o campo 'coordenadas' é um subdocumento — é um objeto dentro do objeto. Isso é uma das vantagens do MongoDB: a gente consegue guardar dados aninhados de forma natural, sem precisar criar uma tabela separada só pra isso. Campos como 'tags' ficam como array diretamente no documento, porque são propriedades do evento, não entidades independentes."

---

### SLIDE 5 — Por que NoSQL?
**Texto no slide:**
```
Por que MongoDB e não SQL?

✓ Estrutura flexível por evento
✓ Arrays e subdocumentos nativos
✓ Escala horizontal
✓ Leitura rápida sem joins forçados
```

**Fala:**  
"A escolha do MongoDB foi técnica. Eventos têm estrutura variável: uns têm coordenadas geográficas, outros não; uns têm patrocinadores, outros são totalmente voluntários. No SQL isso geraria colunas vazias em todo lugar, ou tabelas auxiliares pra tudo. No MongoDB, cada documento tem só o que precisa. Além disso, operações de leitura — que são as mais frequentes num sistema de eventos — são muito mais simples quando os dados relacionados já estão no mesmo documento."

---

## ──────────────────────────────
## 🟢 PARTE 2 — [INTEGRANTE B]
### "CRUD e Consultas"
## ──────────────────────────────

---

### SLIDE 6 — A API em Números
**Texto no slide:**
```
EventFlow API

10 routers · 40+ endpoints
CRUD completo em todas as coleções
FastAPI + documentação automática
```

**Fala:**  
"Agora eu vou mostrar o que a gente implementou em código. A API tem dez routers — um pra cada coleção — e todos eles têm as operações de CRUD: criar, ler, atualizar e deletar. Vou mostrar isso rodando agora."

> *(Demonstração: abrir o browser em `http://localhost:8000/docs`)*  
> *(Mostrar os routers, expandir o de `eventos`, executar um GET /eventos e mostrar os dados do seed)*

---

### SLIDE 7 — As 5 Consultas Especiais
**Texto no slide:**
```
5 tipos de consulta

1. Busca por título (regex)
2. Comparação: capacidade ≥ N
3. AND: ativos + gratuitos
4. Campo aninhado: coordenadas.cidade
5. Data futura: próximos eventos
```

**Fala:**  
"Além do CRUD básico, implementamos cinco tipos diferentes de consulta. A primeira é uma busca por texto usando regex — você digita parte do título e ele encontra. A segunda usa operador de comparação, o $gte, pra filtrar por capacidade mínima. A terceira combina duas condições com AND. A quarta acessa um campo dentro de um subdocumento — o 'coordenadas.cidade'. E a quinta filtra eventos pela data, buscando só os futuros."

> *(Demonstração ao vivo: executar cada consulta no Swagger ou no terminal com httpie/curl)*  
> Sugestão de comando:
> ```bash
> curl "http://localhost:8000/eventos/busca/ativos-gratuitos"
> curl "http://localhost:8000/eventos/busca/titulo?q=feira"
> curl "http://localhost:8000/eventos/busca/capacidade?minimo=200"
> ```

---

### SLIDE 8 — Demonstração do CRUD Completo
**Texto no slide:**
```
CRUD ao vivo

POST   /eventos       → cria
GET    /eventos       → lista
PUT    /eventos/{id}  → atualiza
DELETE /eventos/{id}  → remove
```

**Fala:**  
"Vou criar um evento novo agora pra vocês verem a operação completa. Primeiro o POST, que insere no banco. Depois o GET pra confirmar que apareceu. Depois um PUT pra mudar o status pra 'cancelado'. E por último o DELETE."

> *(Demonstrar no Swagger: POST com dados de um evento fictício → GET → PUT → DELETE. Mostrar o MongoDB Compass ou o terminal com `mongosh` confirmando as mudanças em tempo real.)*

---

## ──────────────────────────────
## 🔵 PARTE 3 — [INTEGRANTE C]
### "Agregações e Decisões Técnicas"
## ──────────────────────────────

---

### SLIDE 9 — Pipelines de Agregação
**Texto no slide:**
```
3 Pipelines de Agregação

① Participantes por evento
② Média de avaliações por evento
③ Eventos mais comentados
```

**Fala:**  
"A parte que eu fiquei responsável foram as agregações — que é onde o MongoDB realmente brilha. Vou explicar cada uma das três."

---

### SLIDE 10 — Pipeline 1: Participantes por Evento
**Texto no slide:**
```
$match → $group → $lookup → $unwind → $sort

inscrições  ──→  agrupadas por evento
                 ──→ enriquecidas com nome do evento
                      ──→ ordenadas pelo total
```

**Fala:**  
"O primeiro pipeline começa na coleção de inscrições. O $match filtra só as confirmadas. O $group conta quantas inscrições existem por evento_id. Aí vem o $lookup, que é o 'join' do MongoDB: ele vai buscar os dados do evento correspondente. O $unwind abre o array que o lookup retorna — porque ele sempre devolve um array. E por fim ordenamos pelo total de participantes. Vou rodar agora."

> *(Demonstração: `GET /eventos/agregacao/participantes-por-evento`)*

---

### SLIDE 11 — Pipeline 2 e 3
**Texto no slide:**
```
② Média de notas por evento
   $group + $avg → ordenado por nota

③ Eventos mais comentados
   comentarios → $group → $lookup → top 10
```

**Fala:**  
"O segundo usa $avg dentro do $group pra calcular a média de notas de cada evento — útil pra saber quais eventos tiveram melhor recepção. O terceiro parte dos comentários, conta quantos cada evento recebeu, e enriquece com o título do evento via $lookup. O resultado é um ranking dos dez mais comentados. Esses três pipelines juntos dão ao organizador uma visão analítica real do sistema."

> *(Demonstração: executar os dois endpoints e mostrar o resultado formatado)*

---

### SLIDE 12 — Decisões Técnicas
**Texto no slide:**
```
Escolhas que fizemos (e por quê)

→ Motor (async) em vez de PyMongo síncrono
→ IDs como string nos relacionamentos
→ Tags embutidas no evento
→ Notificações como coleção separada
```

**Fala:**  
"Pra fechar, quero falar sobre as decisões técnicas que tomamos. Usamos Motor em vez de PyMongo porque o FastAPI é assíncrono por natureza — seria um desperdício bloquear o event loop em cada query. Armazenamos IDs relacionais como string pra simplificar a serialização na API. Tags ficam embutidas no evento porque são propriedades dele, não entidades que vão existir independentemente. E notificações ficaram numa coleção separada justamente o contrário: elas crescem muito com o tempo e inflariam o documento do usuário se fossem subdocumentos."

---

### SLIDE 13 — Conclusão
**Texto no slide:**
```
EventFlow

10 coleções  ·  5 consultas  ·  3 agregações
CRUD completo  ·  API documentada

GitHub: github.com/seu-usuario/eventflow
```

**Fala (todos podem encerrar juntos ou o Integrante C conclui):**  
"O EventFlow atende todos os requisitos do projeto: modelagem com dez coleções, CRUD em todas elas, cinco tipos de consulta incluindo campos aninhados e operadores de comparação, e três pipelines de agregação com $group, $lookup e $unwind. Fica aberto pra perguntas."

---

## 📋 Divisão de Apresentação (resumo)

| Integrante | Slides | Tema |
|-----------|--------|------|
| A | 1 a 5  | Visão geral, modelagem, justificativa NoSQL |
| B | 6 a 8  | CRUD completo, 5 consultas, demonstração ao vivo |
| C | 9 a 13 | Pipelines de agregação, decisões técnicas, encerramento |

---

## 🎥 Dicas para a gravação

- Deixem o terminal e o Swagger abertos antes de começar
- Populem o banco com `python scripts/seed.py` antes de gravar
- Mostrem o MongoDB Compass (ou `mongosh`) ao lado da API pra evidenciar as mudanças no banco em tempo real
- Cada integrante fala enquanto o outro compartilha a tela — assim fica claro quem fez o quê
