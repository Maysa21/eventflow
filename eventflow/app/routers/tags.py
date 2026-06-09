from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import tags_col
from app.database.utils import doc, docs
from app.models.schemas import TagCreate, TagUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_tag(tag: TagCreate):
    existente = await tags_col.find_one({"slug": tag.slug})
    if existente:
        raise HTTPException(status_code=409, detail="Tag com esse slug já existe")
    result = await tags_col.insert_one(tag.dict())
    return doc(await tags_col.find_one({"_id": result.inserted_id}))


@router.get("/")
async def listar_tags():
    resultado = await tags_col.find().to_list(200)
    return docs(resultado)


@router.put("/{tag_id}")
async def atualizar_tag(tag_id: str, dados: TagUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    await tags_col.update_one({"_id": ObjectId(tag_id)}, {"$set": campos})
    return doc(await tags_col.find_one({"_id": ObjectId(tag_id)}))


@router.delete("/{tag_id}", status_code=204)
async def deletar_tag(tag_id: str):
    result = await tags_col.delete_one({"_id": ObjectId(tag_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Tag não encontrada")
