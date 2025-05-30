# SolicitudService - FastAPI Demo

Este microservicio REST expone los endpoints `/solicitudes` (POST) y `/solicitudes/{id}` (GET) para gestionar solicitudes estudiantiles.
- Valida JWT en el header Authorization.
- Simula la integración con un sistema externo SOAP.
- Responde el estado de la solicitud (procesado, en revisión, rechazado).

## Cómo ejecutar

1. Instala dependencias:

    pip install -r requirements.txt

2. Corre el servicio:

    uvicorn main:app --reload

3. Usa herramientas como **Postman** o **curl** para probar los endpoints.

### Ejemplo de post

```bash
curl -X POST "http://127.0.0.1:8000/solicitudes?tipo=certificado&descripcion=prueba" -H "Authorization: Bearer 123"
```

### Ejemplo de get by id
```bash
curl -X GET "http://127.0.0.1:8000/solicitudes/{Id}}" -H "Authorization: Bearer 123"
```