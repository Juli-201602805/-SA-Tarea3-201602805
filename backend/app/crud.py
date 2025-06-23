from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, and_
from . import models, schemas
from datetime import datetime

# Crear un CI
def create_ci(db: Session, ci: schemas.CICreate):
    db_ci = models.CI(
        nombre=ci.nombre,
        tipo=ci.tipo,
        descripcion=ci.descripcion,
        numero_serie=ci.numero_serie,
        version=ci.version,
        fecha_adquisicion=ci.fecha_adquisicion,
        estado_actual=ci.estado_actual,
        propietario=ci.propietario,
        ambiente=ci.ambiente,
        nivel_seguridad=ci.nivel_seguridad,
        cumplimiento=ci.cumplimiento,
        estado_configuracion=ci.estado_configuracion,
        numero_licencia=ci.numero_licencia,
        fecha_vencimiento=ci.fecha_vencimiento,
        documentacion=ci.documentacion,
        incidentes=ci.incidentes
    )
    # Relaciones padre
    if ci.padres_ids:
        padres = db.query(models.CI).filter(models.CI.id.in_(ci.padres_ids)).all()
        db_ci.padres = padres
    db.add(db_ci)
    db.commit()
    db.refresh(db_ci)
    # Auditoría: creación
    auditoria = models.Auditoria(
        ci_id=db_ci.id,
        descripcion_cambio="Creación de CI",
        fecha_cambio=datetime.now()
    )
    db.add(auditoria)
    db.commit()
    return db_ci

# Obtener un CI por id
def get_ci(db: Session, ci_id: int):
    return db.query(models.CI).options(
        joinedload(models.CI.padres),
        joinedload(models.CI.hijos),
        joinedload(models.CI.auditorias)
    ).filter(models.CI.id == ci_id).first()

# Listar todos los CIs (con filtro opcional)
def get_cis(db: Session, filtro: dict = None):
    query = db.query(models.CI)
    if filtro:
        # Buscar por campos: nombre, tipo, ambiente, estado_actual
        if "nombre" in filtro:
            query = query.filter(models.CI.nombre.ilike(f"%{filtro['nombre']}%"))
        if "tipo" in filtro:
            query = query.filter(models.CI.tipo == filtro['tipo'])
        if "ambiente" in filtro:
            query = query.filter(models.CI.ambiente == filtro['ambiente'])
        if "estado_actual" in filtro:
            query = query.filter(models.CI.estado_actual == filtro['estado_actual'])
    return query.options(
        joinedload(models.CI.padres),
        joinedload(models.CI.hijos),
        joinedload(models.CI.auditorias)
    ).all()

# Actualizar CI
def update_ci(db: Session, ci_id: int, ci_update: schemas.CIUpdate):
    db_ci = db.query(models.CI).filter(models.CI.id == ci_id).first()
    if not db_ci:
        return None
    for field, value in ci_update.dict(exclude_unset=True).items():
        if hasattr(db_ci, field):
            setattr(db_ci, field, value)
    # Actualizar relaciones padre/hijo
    if ci_update.padres_ids is not None:
        db_ci.padres = db.query(models.CI).filter(models.CI.id.in_(ci_update.padres_ids)).all()
    db.commit()
    db.refresh(db_ci)
    # Auditoría: actualización
    auditoria = models.Auditoria(
        ci_id=db_ci.id,
        descripcion_cambio="Actualización de CI",
        fecha_cambio=datetime.now()
    )
    db.add(auditoria)
    db.commit()
    return db_ci

# Eliminar CI
def delete_ci(db: Session, ci_id: int):
    db_ci = db.query(models.CI).filter(models.CI.id == ci_id).first()
    if not db_ci:
        return False
    db.delete(db_ci)
    db.commit()
    return True

# Agregar entrada a la auditoría manualmente
def add_auditoria(db: Session, ci_id: int, descripcion, usuario=None):
    auditoria = models.Auditoria(
        ci_id=ci_id,
        descripcion_cambio=descripcion,
        usuario=usuario,
        fecha_cambio=datetime.now()
    )
    db.add(auditoria)
    db.commit()
    return auditoria

# Búsqueda avanzada por varios atributos
def search_cis(db: Session, texto: str):
    return db.query(models.CI).filter(
        or_(
            models.CI.nombre.ilike(f"%{texto}%"),
            models.CI.descripcion.ilike(f"%{texto}%"),
            models.CI.numero_serie.ilike(f"%{texto}%"),
            models.CI.version.ilike(f"%{texto}%"),
            models.CI.propietario.ilike(f"%{texto}%"),
            models.CI.documentacion.ilike(f"%{texto}%")
        )
    ).all()
