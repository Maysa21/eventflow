from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import (
    eventos, usuarios, categorias, comentarios,
    inscricoes, locais, patrocinadores, notificacoes,
    avaliacoes, tags
)

app = FastAPI(
    title="EventFlow API",
    description="Sistema de Gerenciamento de Eventos Comunitários",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(eventos.router,       prefix="/eventos",       tags=["Eventos"])
app.include_router(usuarios.router,      prefix="/usuarios",      tags=["Usuários"])
app.include_router(categorias.router,    prefix="/categorias",    tags=["Categorias"])
app.include_router(comentarios.router,   prefix="/comentarios",   tags=["Comentários"])
app.include_router(inscricoes.router,    prefix="/inscricoes",    tags=["Inscrições"])
app.include_router(locais.router,        prefix="/locais",        tags=["Locais"])
app.include_router(patrocinadores.router,prefix="/patrocinadores",tags=["Patrocinadores"])
app.include_router(notificacoes.router,  prefix="/notificacoes",  tags=["Notificações"])
app.include_router(avaliacoes.router,    prefix="/avaliacoes",    tags=["Avaliações"])
app.include_router(tags.router,          prefix="/tags",          tags=["Tags"])

@app.get("/", tags=["Root"])
def root():
    return {"mensagem": "EventFlow API está no ar 🎉"}
