from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class EventoBase(BaseModel):
    titulo: str
    descricao: str
    data_inicio: datetime
    data_fim: datetime
    local_id: str
    categoria_id: str
    organizador_id: str
    capacidade_maxima: int
    status: str = "ativo"
    tags: List[str] = []
    banner_url: Optional[str] = None
    gratuito: bool = True
    valor_ingresso: Optional[float] = 0.0

class EventoCreate(EventoBase):
    pass

class EventoUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    status: Optional[str] = None
    capacidade_maxima: Optional[int] = None
    valor_ingresso: Optional[float] = None


class UsuarioBase(BaseModel):
    nome: str
    email: str
    telefone: Optional[str] = None
    bairro: Optional[str] = None
    cidade: str = "Belém"
    bio: Optional[str] = None
    foto_url: Optional[str] = None
    ativo: bool = True

class UsuarioCreate(UsuarioBase):
    senha_hash: str

class UsuarioUpdate(BaseModel):
    nome: Optional[str] = None
    telefone: Optional[str] = None
    bairro: Optional[str] = None
    bio: Optional[str] = None
    ativo: Optional[bool] = None


class CategoriaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    cor_hex: str = "#3B82F6"
    icone: Optional[str] = None

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    cor_hex: Optional[str] = None


class ComentarioBase(BaseModel):
    evento_id: str
    usuario_id: str
    texto: str
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    editado: bool = False

class ComentarioCreate(ComentarioBase):
    pass

class ComentarioUpdate(BaseModel):
    texto: Optional[str] = None


class InscricaoBase(BaseModel):
    evento_id: str
    usuario_id: str
    status: str = "confirmada"
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    presenca_confirmada: bool = False

class InscricaoCreate(InscricaoBase):
    pass

class InscricaoUpdate(BaseModel):
    status: Optional[str] = None
    presenca_confirmada: Optional[bool] = None


class LocalBase(BaseModel):
    nome: str
    endereco: str
    bairro: str
    cidade: str = "Belém"
    estado: str = "PA"
    capacidade: int
    descricao: Optional[str] = None
    coordenadas: Optional[dict] = None

class LocalCreate(LocalBase):
    pass

class LocalUpdate(BaseModel):
    nome: Optional[str] = None
    endereco: Optional[str] = None
    capacidade: Optional[int] = None


class PatrocinadorBase(BaseModel):
    nome: str
    logo_url: Optional[str] = None
    site: Optional[str] = None
    contato_email: str
    nivel: str = "bronze"

class PatrocinadorCreate(PatrocinadorBase):
    pass

class PatrocinadorUpdate(BaseModel):
    nome: Optional[str] = None
    nivel: Optional[str] = None
    site: Optional[str] = None


class NotificacaoBase(BaseModel):
    usuario_id: str
    titulo: str
    mensagem: str
    tipo: str = "info"
    lida: bool = False
    criado_em: datetime = Field(default_factory=datetime.utcnow)
    evento_id: Optional[str] = None

class NotificacaoCreate(NotificacaoBase):
    pass

class NotificacaoUpdate(BaseModel):
    lida: Optional[bool] = None


class AvaliacaoBase(BaseModel):
    evento_id: str
    usuario_id: str
    nota: int
    comentario: Optional[str] = None
    criado_em: datetime = Field(default_factory=datetime.utcnow)

class AvaliacaoCreate(AvaliacaoBase):
    pass

class AvaliacaoUpdate(BaseModel):
    nota: Optional[int] = None
    comentario: Optional[str] = None


class TagBase(BaseModel):
    nome: str
    slug: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    nome: Optional[str] = None
    slug: Optional[str] = None