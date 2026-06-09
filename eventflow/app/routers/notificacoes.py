from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import notificacoes_col
from app.database.utils import doc, docs
from app.models.schemas import NotificacaoCreate, NotificacaoUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_notificacao(notif: NotificacaoCreate):
    result = await notificacoes_col.insert_one(notif.dict())
    return doc(await notificacoes_col.find_one({"_id": result.inserted_id}))


@router.get("/usuario/{usuario_id}")
async def notificacoes_do_usuario(usuario_id: str, apenas_nao_lidas: bool = False):
    filtro = {"usuario_id": usuario_id}
    if apenas_nao_lidas:
        filtro["lida"] = False
    resultado = await notificacoes_col.find(filtro).sort("criado_em", -1).to_list(100)
    return docs(resultado)


@router.put("/{notif_id}/marcar-lida")
async def marcar_como_lida(notif_id: str):
    await notificacoes_col.update_one(
        {"_id": ObjectId(notif_id)}, {"$set": {"lida": True}}
    )
    return doc(await notificacoes_col.find_one({"_id": ObjectId(notif_id)}))


@router.delete("/{notif_id}", status_code=204)
async def deletar_notificacao(notif_id: str):
    result = await notificacoes_col.delete_one({"_id": ObjectId(notif_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Notificação não encontrada")
