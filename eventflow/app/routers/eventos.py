from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId
from typing import Optional
from datetime import datetime

from app.database.connection import eventos_col, inscricoes_col, comentarios_col, avaliacoes_col
from app.database.utils import doc, docs
from app.models.schemas import EventoCreate, EventoUpdate

router = APIRouter()


# ──────────────────────────────────────────
# CREATE
# ──────────────────────────────────────────
@router.post("/", status_code=201)
async def criar_evento(evento: EventoCreate):
    novo = evento.dict()
    novo["criado_em"] = datetime.utcnow()
    result = await eventos_col.insert_one(novo)
    criado = await eventos_col.find_one({"_id": result.inserted_id})
    return doc(criado)


# ──────────────────────────────────────────
# READ – listar todos
# ──────────────────────────────────────────
@router.get("/")
async def listar_eventos(
    status: Optional[str]       = None,
    gratuito: Optional[bool]    = None,
    categoria_id: Optional[str] = None,
):
    filtro = {}
    if status:        filtro["status"]       = status
    if gratuito is not None: filtro["gratuito"] = gratuito
    if categoria_id:  filtro["categoria_id"] = categoria_id

    resultado = await eventos_col.find(filtro).to_list(100)
    return docs(resultado)


# ──────────────────────────────────────────
# READ – buscar por ID
# ──────────────────────────────────────────
@router.get("/{evento_id}")
async def buscar_evento(evento_id: str):
    evento = await eventos_col.find_one({"_id": ObjectId(evento_id)})
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado")
    return doc(evento)


# ──────────────────────────────────────────
# UPDATE
# ──────────────────────────────────────────
@router.put("/{evento_id}")
async def atualizar_evento(evento_id: str, dados: EventoUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="Nenhum campo enviado")
    await eventos_col.update_one({"_id": ObjectId(evento_id)}, {"$set": campos})
    atualizado = await eventos_col.find_one({"_id": ObjectId(evento_id)})
    return doc(atualizado)


# ──────────────────────────────────────────
# DELETE
# ──────────────────────────────────────────
@router.delete("/{evento_id}", status_code=204)
async def deletar_evento(evento_id: str):
    result = await eventos_col.delete_one({"_id": ObjectId(evento_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Evento não encontrado")


# ══════════════════════════════════════════
# CONSULTAS ESPECIAIS
# ══════════════════════════════════════════

# Consulta 1 – Simples: busca por título (texto parcial)
@router.get("/busca/titulo")
async def buscar_por_titulo(q: str = Query(..., min_length=2)):
    resultado = await eventos_col.find(
        {"titulo": {"$regex": q, "$options": "i"}}
    ).to_list(50)
    return docs(resultado)


# Consulta 2 – Comparação: eventos com capacidade acima de N
@router.get("/busca/capacidade")
async def eventos_por_capacidade(minimo: int = 50):
    resultado = await eventos_col.find(
        {"capacidade_maxima": {"$gte": minimo}}
    ).to_list(100)
    return docs(resultado)


# Consulta 3 – Múltiplas condições (AND): ativos + gratuitos
@router.get("/busca/ativos-gratuitos")
async def eventos_ativos_gratuitos():
    resultado = await eventos_col.find(
        {"$and": [{"status": "ativo"}, {"gratuito": True}]}
    ).to_list(100)
    return docs(resultado)


# Consulta 4 – Campo aninhado: por coordenadas de bairro
@router.get("/busca/por-campo")
async def eventos_por_campo(campo: str, valor: str):
    """Ex: campo=coordenadas.cidade&valor=Belém"""
    resultado = await eventos_col.find({campo: valor}).to_list(100)
    return docs(resultado)


# Consulta 5 – Data futura: próximos eventos
@router.get("/busca/proximos")
async def proximos_eventos():
    agora = datetime.utcnow()
    resultado = await eventos_col.find(
        {"data_inicio": {"$gt": agora}, "status": "ativo"}
    ).sort("data_inicio", 1).to_list(50)
    return docs(resultado)


# ══════════════════════════════════════════
# AGREGAÇÕES
# ══════════════════════════════════════════

# Agregação 1 – Número de participantes por evento
@router.get("/agregacao/participantes-por-evento")
async def participantes_por_evento():
    pipeline = [
        {"$match": {"status": "confirmada"}},
        {"$group": {
            "_id": "$evento_id",
            "total_participantes": {"$sum": 1}
        }},
        {"$lookup": {
            "from": "eventos",
            "let": {"eid": {"$toObjectId": "$_id"}},
            "pipeline": [{"$match": {"$expr": {"$eq": ["$_id", "$$eid"]}}}],
            "as": "evento"
        }},
        {"$unwind": {"path": "$evento", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "evento_titulo": "$evento.titulo",
            "total_participantes": 1
        }},
        {"$sort": {"total_participantes": -1}}
    ]
    resultado = await inscricoes_col.aggregate(pipeline).to_list(100)
    for r in resultado:
        r["_id"] = str(r["_id"])
    return resultado


# Agregação 2 – Média de avaliações por evento
@router.get("/agregacao/media-avaliacoes")
async def media_avaliacoes_por_evento():
    pipeline = [
        {"$group": {
            "_id": "$evento_id",
            "media_nota": {"$avg": "$nota"},
            "total_avaliacoes": {"$sum": 1}
        }},
        {"$sort": {"media_nota": -1}}
    ]
    resultado = await avaliacoes_col.aggregate(pipeline).to_list(100)
    for r in resultado:
        r["_id"] = str(r["_id"])
    return resultado


# Agregação 3 – Eventos com mais comentários
@router.get("/agregacao/mais-comentados")
async def eventos_mais_comentados():
    pipeline = [
        {"$group": {
            "_id": "$evento_id",
            "total_comentarios": {"$sum": 1}
        }},
        {"$lookup": {
            "from": "eventos",
            "let": {"eid": {"$toObjectId": "$_id"}},
            "pipeline": [{"$match": {"$expr": {"$eq": ["$_id", "$$eid"]}}}],
            "as": "evento"
        }},
        {"$unwind": {"path": "$evento", "preserveNullAndEmptyArrays": True}},
        {"$project": {
            "titulo": "$evento.titulo",
            "total_comentarios": 1
        }},
        {"$sort": {"total_comentarios": -1}},
        {"$limit": 10}
    ]
    resultado = await comentarios_col.aggregate(pipeline).to_list(100)
    for r in resultado:
        r["_id"] = str(r["_id"])
    return resultado
