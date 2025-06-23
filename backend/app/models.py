from sqlalchemy import (
    Column, Integer, String, Date, Enum, ForeignKey, Text, Table, DateTime, func
)
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enumerados para opciones fijas
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

# Tabla de relaciones muchos-a-muchos (Padre/Hijo)
relaciones_ci = Table(
    'relaciones_ci', Base.metadata,
    Column('padre_id', Integer, ForeignKey('cis.id'), primary_key=True),
    Column('hijo_id', Integer, ForeignKey('cis.id'), primary_key=True)
)

class CI(Base):
    __tablename__ = "cis"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoCI), nullable=False)
    descripcion = Column(Text, nullable=True)
    numero_serie = Column(String(100), nullable=True)
    version = Column(String(50), nullable=True)
    fecha_adquisicion = Column(Date, nullable=True)
    estado_actual = Column(Enum(EstadoCI), nullable=False, default=EstadoCI.ACTIVO)
    propietario = Column(String(100), nullable=True)
    ambiente = Column(Enum(Ambiente), nullable=False)
    nivel_seguridad = Column(String(20), nullable=True)
    cumplimiento = Column(String(30), nullable=True)
    estado_configuracion = Column(String(30), nullable=True)
    numero_licencia = Column(String(100), nullable=True)
    fecha_vencimiento = Column(Date, nullable=True)
    # Documentación e incidentes pueden ser URLs o texto plano
    documentacion = Column(Text, nullable=True)
    incidentes = Column(Text, nullable=True)

    # Relaciones padre/hijo
    padres = relationship(
        "CI",
        secondary=relaciones_ci,
        primaryjoin=id==relaciones_ci.c.hijo_id,
        secondaryjoin=id==relaciones_ci.c.padre_id,
        backref="hijos"
    )

    # Auditoría (relación uno a muchos)
    auditorias = relationship("Auditoria", back_populates="ci", cascade="all, delete-orphan")


class Auditoria(Base):
    __tablename__ = "auditoria"

    id = Column(Integer, primary_key=True, index=True)
    ci_id = Column(Integer, ForeignKey("cis.id"))
    fecha_cambio = Column(DateTime, server_default=func.now())
    descripcion_cambio = Column(Text, nullable=False)
    usuario = Column(String(100), nullable=True)

    ci = relationship("CI", back_populates="auditorias")
