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

## Exposición por Kong API Gateway

1. Levanta Kong y su base de datos con Docker Compose (ver ejemplo de `docker-compose.yml`):

docker compose up -d

markdown
Copy
Edit

2. Registra el microservicio FastAPI en Kong:

curl -i -X POST http://localhost:8001/services/ --data "name=solicitud-service" --data "url=http://host.docker.internal:8000"
curl -i -X POST http://localhost:8001/services/solicitud-service/routes --data "paths[]=/solicitudes"

markdown
Copy
Edit

3. Aplica plugins de seguridad y rate limiting:

curl -i -X POST http://localhost:8001/services/solicitud-service/plugins --data "name=rate-limiting" --data "config.minute=5"
curl -i -X POST http://localhost:8001/services/solicitud-service/plugins --data "name=key-auth"
curl -i -X POST http://localhost:8001/consumers --data "username=demo"
curl -i -X POST http://localhost:8001/consumers/demo/key-auth --data "key=MICLAVE123"

markdown
Copy
Edit

4. Asegúrate que la ruta tenga `strip_path=false`:

curl -i -X PATCH http://localhost:8001/routes/<ROUTE_ID> --data "strip_path=false"

markdown
Copy
Edit

5. Prueba el acceso por Kong:

curl -X POST "http://localhost:8000/solicitudes?tipo=certificado" -H "Authorization: Bearer 123" -H "apikey: MICLAVE123"
curl -X GET "http://localhost:8000/solicitudes/{Id}" -H "Authorization: Bearer 123" -H "apikey: MICLAVE123"

yaml
Copy
Edit

---

## Despliegue y resiliencia en Kubernetes con Istio

1. Construye y sube la imagen de tu microservicio a DockerHub, o cárgala localmente en Minikube/KIND.
2. Despliega los manifiestos Kubernetes para el deployment y service del microservicio y, si lo necesitas, un mock SOAP.
3. Instala Istio y habilita la inyección automática de sidecars en el namespace:
    ```
    istioctl install --set profile=demo -y
    kubectl label namespace default istio-injection=enabled
    ```
4. Aplica los recursos Istio para **Circuit Breaking** y **Retry**:
    - Aplica ambos manifiestos:
      ```
      kubectl apply -f destinationrule-soap.yaml
      kubectl apply -f virtualservice-soap.yaml
      ```

5. Para probar resiliencia, escala el mock SOAP a cero y observa cómo se disparan los retries y circuit breaking desde los logs o desde la interfaz de Kiali si la tienes instalada.

---



