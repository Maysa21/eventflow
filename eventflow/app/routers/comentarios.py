from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import comentarios_col
from app.database.utils import doc, docs
from app.models.schemas import ComentarioCreate, ComentarioUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_comentario(comentario: ComentarioCreate):
    result = await comentarios_col.insert_one(comentario.dict())
    criado = await comentarios_col.find_one({"_id": result.inserted_id})
    return doc(criado)


@router.get("/evento/{evento_id}")
async def comentarios_do_evento(evento_id: str):
    resultado = await comentarios_col.find({"evento_id": evento_id}).to_list(200)
    return docs(resultado)


@router.get("/{comentario_id}")
async def buscar_comentario(comentario_id: str):
    com = await comentarios_col.find_one({"_id": ObjectId(comentario_id)})
    if not com:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
    return doc(com)


@router.put("/{comentario_id}")
async def atualizar_comentario(comentario_id: str, dados: ComentarioUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    campos["editado"] = True
    await comentarios_col.update_one({"_id": ObjectId(comentario_id)}, {"$set": campos})
    return doc(await comentarios_col.find_one({"_id": ObjectId(comentario_id)}))


@router.delete("/{comentario_id}", status_code=204)
async def deletar_comentario(comentario_id: str):
    result = await comentarios_col.delete_one({"_id": ObjectId(comentario_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comentário não encontrado")
