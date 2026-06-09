from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import patrocinadores_col
from app.database.utils import doc, docs
from app.models.schemas import PatrocinadorCreate, PatrocinadorUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_patrocinador(pat: PatrocinadorCreate):
    result = await patrocinadores_col.insert_one(pat.dict())
    return doc(await patrocinadores_col.find_one({"_id": result.inserted_id}))


@router.get("/")
async def listar_patrocinadores(nivel: str = None):
    filtro = {}
    if nivel:
        filtro["nivel"] = nivel
    resultado = await patrocinadores_col.find(filtro).to_list(100)
    return docs(resultado)


@router.get("/{pat_id}")
async def buscar_patrocinador(pat_id: str):
    pat = await patrocinadores_col.find_one({"_id": ObjectId(pat_id)})
    if not pat:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")
    return doc(pat)


@router.put("/{pat_id}")
async def atualizar_patrocinador(pat_id: str, dados: PatrocinadorUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    await patrocinadores_col.update_one({"_id": ObjectId(pat_id)}, {"$set": campos})
    return doc(await patrocinadores_col.find_one({"_id": ObjectId(pat_id)}))


@router.delete("/{pat_id}", status_code=204)
async def deletar_patrocinador(pat_id: str):
    result = await patrocinadores_col.delete_one({"_id": ObjectId(pat_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Patrocinador não encontrado")
