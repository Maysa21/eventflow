from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import locais_col
from app.database.utils import doc, docs
from app.models.schemas import LocalCreate, LocalUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_local(local: LocalCreate):
    result = await locais_col.insert_one(local.dict())
    return doc(await locais_col.find_one({"_id": result.inserted_id}))


@router.get("/")
async def listar_locais(bairro: str = None):
    filtro = {}
    if bairro:
        filtro["bairro"] = {"$regex": bairro, "$options": "i"}
    resultado = await locais_col.find(filtro).to_list(100)
    return docs(resultado)


@router.get("/{local_id}")
async def buscar_local(local_id: str):
    local = await locais_col.find_one({"_id": ObjectId(local_id)})
    if not local:
        raise HTTPException(status_code=404, detail="Local não encontrado")
    return doc(local)


@router.put("/{local_id}")
async def atualizar_local(local_id: str, dados: LocalUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    await locais_col.update_one({"_id": ObjectId(local_id)}, {"$set": campos})
    return doc(await locais_col.find_one({"_id": ObjectId(local_id)}))


@router.delete("/{local_id}", status_code=204)
async def deletar_local(local_id: str):
    result = await locais_col.delete_one({"_id": ObjectId(local_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Local não encontrado")
