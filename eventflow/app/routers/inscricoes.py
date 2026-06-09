from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import inscricoes_col, eventos_col
from app.database.utils import doc, docs
from app.models.schemas import InscricaoCreate, InscricaoUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def inscrever(inscricao: InscricaoCreate):
    # Verifica duplicidade
    existente = await inscricoes_col.find_one({
        "evento_id": inscricao.evento_id,
        "usuario_id": inscricao.usuario_id
    })
    if existente:
        raise HTTPException(status_code=409, detail="Usuário já inscrito neste evento")

    result = await inscricoes_col.insert_one(inscricao.dict())
    criado = await inscricoes_col.find_one({"_id": result.inserted_id})
    return doc(criado)


@router.get("/evento/{evento_id}")
async def inscritos_do_evento(evento_id: str):
    resultado = await inscricoes_col.find({"evento_id": evento_id}).to_list(500)
    return docs(resultado)


@router.get("/usuario/{usuario_id}")
async def eventos_do_usuario(usuario_id: str):
    resultado = await inscricoes_col.find({"usuario_id": usuario_id}).to_list(200)
    return docs(resultado)


@router.put("/{inscricao_id}")
async def atualizar_inscricao(inscricao_id: str, dados: InscricaoUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    await inscricoes_col.update_one({"_id": ObjectId(inscricao_id)}, {"$set": campos})
    return doc(await inscricoes_col.find_one({"_id": ObjectId(inscricao_id)}))


@router.delete("/{inscricao_id}", status_code=204)
async def cancelar_inscricao(inscricao_id: str):
    result = await inscricoes_col.delete_one({"_id": ObjectId(inscricao_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Inscrição não encontrada")
