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

Docker Logs:

redis-cli KEYS "health_log:\*"

redis-cli GET "health_log:"

Ver cuanto tiempo le queda:

redis-cli TTL "health_log:"

# redis-cli

# Token 1

SET token:abc123 "activo" EX 3600

# Token 2

SET token:xyz789 "activo" EX 3600

# Token 3 (puedes usar cualquier texto: UUID, JWT, etc.)

SET token:eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9... "activo" EX 3600

### usarlos en tu API

Authorization: Bearer abc123
Authorization: Bearer xyz789
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
