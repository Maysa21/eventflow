"""
Script de seed – popula o banco com dados realistas para demonstração.
Execute: python scripts/seed.py
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import random

MONGO_URL = "mongodb://localhost:27017"
DB_NAME   = "eventflow"

client = AsyncIOMotorClient(MONGO_URL)
db     = client[DB_NAME]


async def limpar():
    colecoes = [
        "eventos","usuarios","categorias","comentarios",
        "inscricoes","locais","patrocinadores","notificacoes",
        "avaliacoes","tags"
    ]
    for col in colecoes:
        await db[col].drop()
    print("🗑  Banco limpo.")


async def seed():
    await limpar()

    # ── TAGS ──
    tags_data = [
        {"nome": "Família",     "slug": "familia"},
        {"nome": "Gratuito",    "slug": "gratuito"},
        {"nome": "Ao ar livre", "slug": "ar-livre"},
        {"nome": "Cultura",     "slug": "cultura"},
        {"nome": "Esporte",     "slug": "esporte"},
    ]
    tags_res = await db["tags"].insert_many(tags_data)
    tag_ids  = [str(i) for i in tags_res.inserted_ids]
    print(f"✅ Tags: {len(tag_ids)}")

    # ── CATEGORIAS ──
    cats_data = [
        {"nome": "Cultural",    "descricao": "Saraus, feiras, exposições",    "cor_hex": "#8B5CF6"},
        {"nome": "Esportivo",   "descricao": "Torneios, caminhadas, corridas","cor_hex": "#10B981"},
        {"nome": "Educacional", "descricao": "Palestras, workshops, cursos",  "cor_hex": "#3B82F6"},
        {"nome": "Religioso",   "descricao": "Missas, cultos, retiros",       "cor_hex": "#F59E0B"},
        {"nome": "Gastronômico","descricao": "Feiras de comida, festivais",   "cor_hex": "#EF4444"},
    ]
    cats_res = await db["categorias"].insert_many(cats_data)
    cat_ids  = [str(i) for i in cats_res.inserted_ids]
    print(f"✅ Categorias: {len(cat_ids)}")

    # ── LOCAIS ──
    locais_data = [
        {"nome": "Praça da República",   "endereco": "Praça da República, s/n",      "bairro": "Campina",       "cidade": "Belém", "estado": "PA", "capacidade": 500, "coordenadas": {"lat": -1.4558, "lng": -48.5025}},
        {"nome": "Espaço Cultural Casa das Artes","endereco": "Av. Gentil Bittencourt, 650","bairro": "Nazaré","cidade": "Belém", "estado": "PA", "capacidade": 200, "coordenadas": {"lat": -1.4503, "lng": -48.4876}},
        {"nome": "Escola Municipal Almirante Tamandaré","endereco": "Tv. Mauriti, 1580","bairro": "Jurunas","cidade": "Belém", "estado": "PA", "capacidade": 120, "coordenadas": {"lat": -1.4701, "lng": -48.5034}},
        {"nome": "Quadra do Bairro do Guamá","endereco": "Passagem São João, s/n",    "bairro": "Guamá",         "cidade": "Belém", "estado": "PA", "capacidade": 300},
        {"nome": "Igreja Nossa Senhora de Nazaré","endereco": "Praça Justo Chermont, s/n","bairro": "Nazaré",  "cidade": "Belém", "estado": "PA", "capacidade": 800},
    ]
    locais_res = await db["locais"].insert_many(locais_data)
    local_ids  = [str(i) for i in locais_res.inserted_ids]
    print(f"✅ Locais: {len(local_ids)}")

    # ── PATROCINADORES ──
    pats_data = [
        {"nome": "Açaí do Pará",   "contato_email": "contato@acaidopara.com",  "nivel": "ouro",   "site": "https://acaidopara.com"},
        {"nome": "TechBelém",      "contato_email": "oi@techbelem.com.br",     "nivel": "prata",  "site": "https://techbelem.com.br"},
        {"nome": "Gráfica Norte",  "contato_email": "grafica@norte.com",       "nivel": "bronze"},
    ]
    await db["patrocinadores"].insert_many(pats_data)
    print(f"✅ Patrocinadores: {len(pats_data)}")

    # ── USUÁRIOS ──
    usuarios_data = [
        {"nome": "Ana Tavares",   "email": "ana@email.com",    "cidade": "Belém", "bairro": "Nazaré",  "ativo": True, "senha_hash": "hash1", "criado_em": datetime.utcnow()},
        {"nome": "Bruno Farias",  "email": "bruno@email.com",  "cidade": "Belém", "bairro": "Guamá",   "ativo": True, "senha_hash": "hash2", "criado_em": datetime.utcnow()},
        {"nome": "Carla Moura",   "email": "carla@email.com",  "cidade": "Belém", "bairro": "Jurunas", "ativo": True, "senha_hash": "hash3", "criado_em": datetime.utcnow()},
        {"nome": "Diego Pinto",   "email": "diego@email.com",  "cidade": "Belém", "bairro": "Campina", "ativo": True, "senha_hash": "hash4", "criado_em": datetime.utcnow()},
        {"nome": "Elisa Nunes",   "email": "elisa@email.com",  "cidade": "Belém", "bairro": "Marco",   "ativo": True, "senha_hash": "hash5", "criado_em": datetime.utcnow()},
        {"nome": "Felipe Costa",  "email": "felipe@email.com", "cidade": "Belém", "bairro": "Pedreira","ativo": True, "senha_hash": "hash6", "criado_em": datetime.utcnow()},
    ]
    users_res = await db["usuarios"].insert_many(usuarios_data)
    user_ids  = [str(i) for i in users_res.inserted_ids]
    print(f"✅ Usuários: {len(user_ids)}")

    # ── EVENTOS ──
    agora = datetime.utcnow()
    eventos_data = [
        {
            "titulo": "Feira Cultural do Guamá",
            "descricao": "Arte, música e comida típica paraense num sábado de sol no coração do bairro.",
            "data_inicio": agora + timedelta(days=10),
            "data_fim":    agora + timedelta(days=10, hours=6),
            "local_id":    local_ids[3],
            "categoria_id":cat_ids[0],
            "organizador_id": user_ids[0],
            "capacidade_maxima": 300,
            "status": "ativo",
            "gratuito": True,
            "valor_ingresso": 0.0,
            "tags": [tag_ids[0], tag_ids[1], tag_ids[3]],
            "criado_em": agora,
        },
        {
            "titulo": "Torneio de Futebol Comunitário",
            "descricao": "Campeonato de rua com times do bairro. Troféu e medalhas para os três primeiros.",
            "data_inicio": agora + timedelta(days=5),
            "data_fim":    agora + timedelta(days=5, hours=8),
            "local_id":    local_ids[3],
            "categoria_id":cat_ids[1],
            "organizador_id": user_ids[1],
            "capacidade_maxima": 150,
            "status": "ativo",
            "gratuito": True,
            "valor_ingresso": 0.0,
            "tags": [tag_ids[4]],
            "criado_em": agora,
        },
        {
            "titulo": "Workshop: Introdução ao MongoDB",
            "descricao": "Aprenda modelagem de dados NoSQL com exemplos práticos do dia a dia.",
            "data_inicio": agora + timedelta(days=15),
            "data_fim":    agora + timedelta(days=15, hours=4),
            "local_id":    local_ids[1],
            "categoria_id":cat_ids[2],
            "organizador_id": user_ids[2],
            "capacidade_maxima": 50,
            "status": "ativo",
            "gratuito": False,
            "valor_ingresso": 30.0,
            "tags": [tag_ids[3]],
            "criado_em": agora,
        },
        {
            "titulo": "Círio de Nazaré – Missa de Abertura",
            "descricao": "Celebração religiosa que reúne milhares de fiéis. Entrada franca.",
            "data_inicio": agora + timedelta(days=30),
            "data_fim":    agora + timedelta(days=30, hours=3),
            "local_id":    local_ids[4],
            "categoria_id":cat_ids[3],
            "organizador_id": user_ids[0],
            "capacidade_maxima": 800,
            "status": "ativo",
            "gratuito": True,
            "valor_ingresso": 0.0,
            "tags": [tag_ids[0]],
            "criado_em": agora,
        },
        {
            "titulo": "Festival Gastronômico da Amazônia",
            "descricao": "Sabores da floresta: tacacá, maniçoba, pato no tucupi e muito mais.",
            "data_inicio": agora + timedelta(days=20),
            "data_fim":    agora + timedelta(days=20, hours=10),
            "local_id":    local_ids[0],
            "categoria_id":cat_ids[4],
            "organizador_id": user_ids[3],
            "capacidade_maxima": 500,
            "status": "ativo",
            "gratuito": False,
            "valor_ingresso": 15.0,
            "tags": [tag_ids[0], tag_ids[2]],
            "criado_em": agora,
        },
    ]
    events_res = await db["eventos"].insert_many(eventos_data)
    event_ids  = [str(i) for i in events_res.inserted_ids]
    print(f"✅ Eventos: {len(event_ids)}")

    # ── INSCRIÇÕES ──
    inscricoes_data = []
    for uid in user_ids[:4]:
        inscricoes_data.append({"evento_id": event_ids[0], "usuario_id": uid, "status": "confirmada", "presenca_confirmada": False, "criado_em": agora})
    for uid in user_ids[1:5]:
        inscricoes_data.append({"evento_id": event_ids[1], "usuario_id": uid, "status": "confirmada", "presenca_confirmada": True, "criado_em": agora})
    for uid in user_ids[:3]:
        inscricoes_data.append({"evento_id": event_ids[2], "usuario_id": uid, "status": "confirmada", "presenca_confirmada": False, "criado_em": agora})
    await db["inscricoes"].insert_many(inscricoes_data)
    print(f"✅ Inscrições: {len(inscricoes_data)}")

    # ── COMENTÁRIOS ──
    comentarios_data = [
        {"evento_id": event_ids[0], "usuario_id": user_ids[0], "texto": "Mal posso esperar! O ano passado foi incrível.", "criado_em": agora, "editado": False},
        {"evento_id": event_ids[0], "usuario_id": user_ids[1], "texto": "Vou levar minha família toda. Vai ter comida típica?", "criado_em": agora, "editado": False},
        {"evento_id": event_ids[1], "usuario_id": user_ids[2], "texto": "Nosso time tá treinando há semanas pra esse torneio!", "criado_em": agora, "editado": False},
        {"evento_id": event_ids[2], "usuario_id": user_ids[3], "texto": "Workshop muito bem explicado. Recomendo pra quem tá começando.", "criado_em": agora, "editado": False},
        {"evento_id": event_ids[4], "usuario_id": user_ids[4], "texto": "Espero que tenha tacacá. Faz tempo que não como um bom!", "criado_em": agora, "editado": False},
        {"evento_id": event_ids[4], "usuario_id": user_ids[5], "texto": "Alguém sabe se vai ter estacionamento por perto?", "criado_em": agora, "editado": False},
    ]
    await db["comentarios"].insert_many(comentarios_data)
    print(f"✅ Comentários: {len(comentarios_data)}")

    # ── AVALIAÇÕES ──
    avaliacoes_data = [
        {"evento_id": event_ids[0], "usuario_id": user_ids[0], "nota": 5, "comentario": "Melhor evento do bairro!", "criado_em": agora},
        {"evento_id": event_ids[0], "usuario_id": user_ids[1], "nota": 4, "comentario": "Muito bom, só precisava de mais banheiros.", "criado_em": agora},
        {"evento_id": event_ids[1], "usuario_id": user_ids[2], "nota": 5, "comentario": "Organização impecável.", "criado_em": agora},
        {"evento_id": event_ids[2], "usuario_id": user_ids[3], "nota": 4, "comentario": "Conteúdo denso mas vale muito.", "criado_em": agora},
        {"evento_id": event_ids[2], "usuario_id": user_ids[4], "nota": 3, "comentario": "Poderia ter mais exercícios práticos.", "criado_em": agora},
    ]
    await db["avaliacoes"].insert_many(avaliacoes_data)
    print(f"✅ Avaliações: {len(avaliacoes_data)}")

    # ── NOTIFICAÇÕES ──
    notifs_data = [
        {"usuario_id": user_ids[0], "titulo": "Inscrição confirmada!", "mensagem": "Você está inscrito na Feira Cultural do Guamá.", "tipo": "confirmacao", "lida": False, "criado_em": agora, "evento_id": event_ids[0]},
        {"usuario_id": user_ids[1], "titulo": "Evento se aproximando", "mensagem": "O Torneio de Futebol começa em 2 dias.", "tipo": "alerta", "lida": False, "criado_em": agora, "evento_id": event_ids[1]},
        {"usuario_id": user_ids[2], "titulo": "Novo evento na sua área", "mensagem": "Tem um workshop de MongoDB perto de você!", "tipo": "info", "lida": True, "criado_em": agora, "evento_id": event_ids[2]},
    ]
    await db["notificacoes"].insert_many(notifs_data)
    print(f"✅ Notificações: {len(notifs_data)}")

    print("\n🎉 Seed concluído com sucesso!")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
