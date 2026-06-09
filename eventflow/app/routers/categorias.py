from fastapi import APIRouter, HTTPException
from bson import ObjectId
from app.database.connection import categorias_col
from app.database.utils import doc, docs
from app.models.schemas import CategoriaCreate, CategoriaUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_categoria(categoria: CategoriaCreate):
    result = await categorias_col.insert_one(categoria.dict())
    criado = await categorias_col.find_one({"_id": result.inserted_id})
    return doc(criado)


@router.get("/")
async def listar_categorias():
    resultado = await categorias_col.find().to_list(100)
    return docs(resultado)


@router.get("/{categoria_id}")
async def buscar_categoria(categoria_id: str):
    cat = await categorias_col.find_one({"_id": ObjectId(categoria_id)})
    if not cat:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
    return doc(cat)


@router.put("/{categoria_id}")
async def atualizar_categoria(categoria_id: str, dados: CategoriaUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    await categorias_col.update_one({"_id": ObjectId(categoria_id)}, {"$set": campos})
    return doc(await categorias_col.find_one({"_id": ObjectId(categoria_id)}))


@router.delete("/{categoria_id}", status_code=204)
async def deletar_categoria(categoria_id: str):
    result = await categorias_col.delete_one({"_id": ObjectId(categoria_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Categoria não encontrada")
