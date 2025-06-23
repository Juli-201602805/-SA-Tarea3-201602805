from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from . import models, schemas, crud
from .database import SessionLocal, engine
import uvicorn

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API CMDB - Gestión de Configuración",
    description="API para administración de CIs (Configuration Items) con auditoría y relaciones.",
    version="1.0.0"
)

# Sesión DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoints 
@app.post("/cis/", response_model=schemas.CI)
def create_ci(ci: schemas.CICreate, db: Session = Depends(get_db)):
    return crud.create_ci(db, ci)

@app.get("/cis/{ci_id}", response_model=schemas.CI)
def read_ci(ci_id: int, db: Session = Depends(get_db)):
    db_ci = crud.get_ci(db, ci_id)
    if not db_ci:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    return db_ci

@app.get("/cis/", response_model=List[schemas.CI])
def list_cis(
    nombre: Optional[str] = None,
    tipo: Optional[schemas.TipoCI] = None,
    ambiente: Optional[schemas.Ambiente] = None,
    estado_actual: Optional[schemas.EstadoCI] = None,
    db: Session = Depends(get_db)
):
    filtro = {}
    if nombre: filtro["nombre"] = nombre
    if tipo: filtro["tipo"] = tipo
    if ambiente: filtro["ambiente"] = ambiente
    if estado_actual: filtro["estado_actual"] = estado_actual
    return crud.get_cis(db, filtro=filtro)

@app.put("/cis/{ci_id}", response_model=schemas.CI)
def update_ci(ci_id: int, ci: schemas.CIUpdate, db: Session = Depends(get_db)):
    updated = crud.update_ci(db, ci_id, ci)
    if not updated:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    return updated

@app.delete("/cis/{ci_id}", response_model=dict)
def delete_ci(ci_id: int, db: Session = Depends(get_db)):
    ok = crud.delete_ci(db, ci_id)
    if not ok:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    return {"ok": True}

@app.get("/cis/search/", response_model=List[schemas.CI])
def search_cis(texto: str, db: Session = Depends(get_db)):
    return crud.search_cis(db, texto)

# Endpoint para agregar manualmente cambios a la auditoría
@app.post("/cis/{ci_id}/auditoria/", response_model=schemas.Auditoria)
def add_auditoria(ci_id: int, audit: schemas.AuditoriaCreate, db: Session = Depends(get_db)):
    return crud.add_auditoria(db, ci_id, audit.descripcion_cambio, usuario=audit.usuario)

# Listar auditoría de un CI
@app.get("/cis/{ci_id}/auditoria/", response_model=List[schemas.Auditoria])
def list_auditoria(ci_id: int, db: Session = Depends(get_db)):
    ci = crud.get_ci(db, ci_id)
    if not ci:
        raise HTTPException(status_code=404, detail="CI no encontrado")
    return ci.auditorias

#  Endpoint raíz
@app.get("/")
def root():
    return {"msg": "API CMDB lista. Visita /docs para ver la documentación."}

#  uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
