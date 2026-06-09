from motor.motor_asyncio import AsyncIOMotorClient
import os

MONGO_URL = os.getenv("MONGO_URL", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DB_NAME", "eventflow")

client = AsyncIOMotorClient(MONGO_URL)
db     = client[DB_NAME]

# Coleções
eventos_col       = db["eventos"]
usuarios_col      = db["usuarios"]
categorias_col    = db["categorias"]
comentarios_col   = db["comentarios"]
inscricoes_col    = db["inscricoes"]
locais_col        = db["locais"]
patrocinadores_col= db["patrocinadores"]
notificacoes_col  = db["notificacoes"]
avaliacoes_col    = db["avaliacoes"]
tags_col          = db["tags"]
