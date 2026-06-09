from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import avaliacoes_col
from app.database.utils import doc, docs
from app.models.schemas import AvaliacaoCreate, AvaliacaoUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_avaliacao(avaliacao: AvaliacaoCreate):
    if not (1 <= avaliacao.nota <= 5):
        raise HTTPException(status_code=422, detail="Nota deve ser entre 1 e 5")
    result = await avaliacoes_col.insert_one(avaliacao.dict())
    return doc(await avaliacoes_col.find_one({"_id": result.inserted_id}))


@router.get("/evento/{evento_id}")
async def avaliacoes_do_evento(evento_id: str):
    resultado = await avaliacoes_col.find({"evento_id": evento_id}).to_list(200)
    return docs(resultado)


@router.put("/{aval_id}")
async def atualizar_avaliacao(aval_id: str, dados: AvaliacaoUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    await avaliacoes_col.update_one({"_id": ObjectId(aval_id)}, {"$set": campos})
    return doc(await avaliacoes_col.find_one({"_id": ObjectId(aval_id)}))


@router.delete("/{aval_id}", status_code=204)
async def deletar_avaliacao(aval_id: str):
    result = await avaliacoes_col.delete_one({"_id": ObjectId(aval_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Avaliação não encontrada")
