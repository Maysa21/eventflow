from fastapi import APIRouter, HTTPException
from bson import ObjectId
from datetime import datetime

from app.database.connection import usuarios_col
from app.database.utils import doc, docs
from app.models.schemas import UsuarioCreate, UsuarioUpdate

router = APIRouter()


@router.post("/", status_code=201)
async def criar_usuario(usuario: UsuarioCreate):
    existente = await usuarios_col.find_one({"email": usuario.email})
    if existente:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado")
    novo = usuario.dict()
    novo["criado_em"] = datetime.utcnow()
    result = await usuarios_col.insert_one(novo)
    criado = await usuarios_col.find_one({"_id": result.inserted_id})
    return doc(criado)


@router.get("/")
async def listar_usuarios(ativo: bool = True):
    resultado = await usuarios_col.find({"ativo": ativo}).to_list(100)
    return docs(resultado)


@router.get("/{usuario_id}")
async def buscar_usuario(usuario_id: str):
    usuario = await usuarios_col.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return doc(usuario)


@router.put("/{usuario_id}")
async def atualizar_usuario(usuario_id: str, dados: UsuarioUpdate):
    campos = {k: v for k, v in dados.dict().items() if v is not None}
    if not campos:
        raise HTTPException(status_code=400, detail="Nenhum campo enviado")
    await usuarios_col.update_one({"_id": ObjectId(usuario_id)}, {"$set": campos})
    atualizado = await usuarios_col.find_one({"_id": ObjectId(usuario_id)})
    return doc(atualizado)


@router.delete("/{usuario_id}", status_code=204)
async def deletar_usuario(usuario_id: str):
    result = await usuarios_col.delete_one({"_id": ObjectId(usuario_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")


# Busca por cidade (campo aninhado / filtro)
@router.get("/busca/por-cidade")
async def usuarios_por_cidade(cidade: str = "Belém"):
    resultado = await usuarios_col.find({"cidade": cidade, "ativo": True}).to_list(100)
    return docs(resultado)
