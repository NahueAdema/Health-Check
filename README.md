⚙️ Ejecución local

Instala dependencias:

python -m venv venv

pip install -r requirements.txt

Ejecuta el servicio:

uvicorn main:app --reload

Prueba el endpoint:

curl http://localhost:8000/health

Deberías ver:

{
"status": "ok",
"timestamp": "2025-09-17T15:00:00Z"
}
