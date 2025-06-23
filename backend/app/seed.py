from .database import SessionLocal
from . import models
from datetime import date

def seed():
    db = SessionLocal()
    # Borrar datos previos 
    db.query(models.Auditoria).delete()
    db.query(models.CI).delete()
    db.commit()

    # Crear algunos CIs
    servidor = models.CI(
        nombre="Servidor1",
        tipo=models.TipoCI.HARDWARE,
        descripcion="Servidor de aplicaciones principal",
        numero_serie="SN123456",
        version="v1.0",
        fecha_adquisicion=date(2022, 1, 1),
        estado_actual=models.EstadoCI.ACTIVO,
        propietario="Equipo de Infraestructura",
        ambiente=models.Ambiente.PROD,
        nivel_seguridad="Alto",
        cumplimiento="Cumple",
        estado_configuracion="Aprobado",
        numero_licencia="ABC123",
        fecha_vencimiento=date(2023, 1, 1),
        documentacion="[Enlace a Manual](url)",
        incidentes="[Enlace a Incidente](url)"
    )

    aplicacion = models.CI(
        nombre="Aplicación",
        tipo=models.TipoCI.SOFTWARE,
        descripcion="Aplicación de contabilidad",
        version="v2.5",
        fecha_adquisicion=date(2022, 3, 15),
        estado_actual=models.EstadoCI.ACTIVO,
        propietario="Equipo de Desarrollo",
        ambiente=models.Ambiente.PROD,
        nivel_seguridad="Medio",
        cumplimiento="Cumple",
        estado_configuracion="Aprobado",
        numero_licencia="XYZ456",
        fecha_vencimiento=date(2024, 1, 1),
        documentacion="[Enlace a Documentación Técnica](url)",
        incidentes="[Enlace a Incidente](url)"
    )

    # Relacionar aplicación como hija de servidor
    aplicacion.padres = [servidor]

    db.add(servidor)
    db.add(aplicacion)
    db.commit()

    # Auditoría
    audit1 = models.Auditoria(
        ci_id=servidor.id, descripcion_cambio="Creación de Servidor1"
    )
    audit2 = models.Auditoria(
        ci_id=aplicacion.id, descripcion_cambio="Creación de Aplicación"
    )
    db.add(audit1)
    db.add(audit2)
    db.commit()
    db.close()

if __name__ == "__main__":
    seed()
    print("¡Datos de ejemplo insertados!")
from .database import SessionLocal
from . import models
from datetime import date


