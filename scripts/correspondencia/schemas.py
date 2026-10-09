from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr


class TipoRadicadoEnum(str, Enum):
    ENTRADA = "Entrada"
    SALIDA = "Salida"
    INTERNO = "Interno"


class EstadoRadicadoEnum(str, Enum):
    PENDIENTE = "Pendiente"
    EN_TRAMITE = "En Tramite"
    FINALIZADO = "Finalizado"


# --- ESQUEMAS REMITENTE ---
class RemitenteBase(BaseModel):
    numero_documento: str
    nombre_completo: str
    email: EmailStr
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class RemitenteCreate(RemitenteBase):
    pass


class RemitenteUpdate(BaseModel):
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None


class RemitenteResponse(RemitenteBase):
    id: int


# --- ESQUEMAS RADICADO ---
class RadicadoBase(BaseModel):
    numero_radicado: str
    asunto: str
    tipo_radicado: TipoRadicadoEnum
    estado: EstadoRadicadoEnum = EstadoRadicadoEnum.PENDIENTE
    remitente_id: int


class RadicadoCreate(RadicadoBase):
    pass


class RadicadoUpdate(BaseModel):
    asunto: Optional[str] = None
    tipo_radicado: Optional[TipoRadicadoEnum] = None
    estado: Optional[EstadoRadicadoEnum] = None


class RadicadoResponse(RadicadoBase):
    id: int
    fecha_radicacion: str
    remitente: Optional[RemitenteResponse] = None