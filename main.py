from fastapi import FastAPI, HTTPException, Header, status
from fastapi.responses import JSONResponse
from typing import Optional
import uuid
import time

app = FastAPI()

solicitudes_db = {}

# Simulación de validación JWT (solo ejemplo, en producción usar librería como PyJWT)
def validate_jwt(token: str) -> bool:
    # Para demo, acepta cualquier token que empiece con "Bearer "
    return token and token.startswith("Bearer 123")

# Mock a servicio SOAP externo (simulado)
def call_soap_service(data):
    # Aquí simularías una llamada real al SOAP
    # Puede retornar éxito, en revisión o rechazo aleatoriamente
    import random
    estados = ["procesado", "en revisión", "rechazado"]
    # Simulando latencia
    time.sleep(0.5)
    return {"estado": random.choice(estados)}

@app.post("/solicitudes")
def crear_solicitud(
    tipo: str,
    descripcion: Optional[str] = None,
    authorization: Optional[str] = Header(None)
):
    print("Authorization recibido:", repr(authorization))
    if not authorization or not validate_jwt(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    # Crear solicitud
    solicitud_id = str(uuid.uuid4())
    # Llamada a sistema de certificación (SOAP)
    estado_certificacion = call_soap_service({"tipo": tipo, "descripcion": descripcion})
    solicitudes_db[solicitud_id] = {
        "id": solicitud_id,
        "tipo": tipo,
        "descripcion": descripcion,
        "estado": estado_certificacion["estado"]
    }
    return solicitudes_db[solicitud_id]

@app.get("/solicitudes/{solicitud_id}")
def obtener_solicitud(solicitud_id: str, authorization: Optional[str] = Header(None)):
    if not authorization or not validate_jwt(authorization):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    solicitud = solicitudes_db.get(solicitud_id)
    if not solicitud:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Solicitud no encontrada")
    return solicitud