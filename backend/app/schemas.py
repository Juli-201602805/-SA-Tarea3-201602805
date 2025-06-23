from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime
import enum

class TipoCI(str, enum.Enum):
    HARDWARE = "Hardware"
    SOFTWARE = "Software"
    BASE_DATOS = "Base de Datos"
    SERVICIO = "Servicio"
    OTRO = "Otro"

class Ambiente(str, enum.Enum):
    DEV = "DEV"
    QA = "QA"
    PROD = "PROD"

class EstadoCI(str, enum.Enum):
    ACTIVO = "Activo"
    INACTIVO = "Inactivo"
    RETIRADO = "Retirado"

# Esquema para auditoría
class AuditoriaBase(BaseModel):
    fecha_cambio: Optional[datetime] = None
    descripcion_cambio: str
    usuario: Optional[str] = None

class AuditoriaCreate(AuditoriaBase):
    pass

class Auditoria(AuditoriaBase):
    id: int

    class Config:
        orm_mode = True

# Principal de CI
class CIBasic(BaseModel):
    nombre: str
    tipo: TipoCI
    descripcion: Optional[str]
    numero_serie: Optional[str]
    version: Optional[str]
    fecha_adquisicion: Optional[date]
    estado_actual: EstadoCI = EstadoCI.ACTIVO
    propietario: Optional[str]
    ambiente: Ambiente
    nivel_seguridad: Optional[str]
    cumplimiento: Optional[str]
    estado_configuracion: Optional[str]
    numero_licencia: Optional[str]
    fecha_vencimiento: Optional[date]
    documentacion: Optional[str]
    incidentes: Optional[str]

class CICreate(CIBasic):
    padres_ids: Optional[List[int]] = Field(default_factory=list)

class CIUpdate(CIBasic):
    padres_ids: Optional[List[int]] = Field(default_factory=list)

class CI(CIBasic):
    id: int
    padres: List['CI'] = []
    hijos: List['CI'] = []
    auditorias: List[Auditoria] = []

    class Config:
        orm_mode = True

# Soportar referencias recursivas (CI dentro de CI)
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    CI.update_forward_refs()
