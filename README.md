# imdb-ranking-wrestlers

Este proyecto es una API desarrollada con FastAPI y utiliza Docker para su despliegue. Está diseñada para gestionar autenticación y funcionalidades relacionadas.

### Requisitos previos
Asegúrate de tener instalados los siguientes componentes:

- Docker y Docker Compose
- Python 3.12+
- Git

### Instalación
- Clonar el repositorio:

```bash
git clone <URL_DEL_REPOSITORIO>
cd imdb_wwe
```
### Configuración inicial
- Archivo de configuración .env

Crea un archivo .env en services/auth con las variables de entorno necesarias para la conexión a la base de datos, JWT y otras configuraciones. Ejemplo:

```env
DATABASE_URL=postgresql://username:password@auth-db:5432/database_name
SECRET_KEY=your_secret_key
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Instalar dependencias locales (opcional)

Si deseas trabajar fuera de Docker, puedes instalar las dependencias manualmente:

```bash
cd services/auth
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Ejecutar migraciones con Alembic
Para crear las tablas en la base de datos:

Navega al directorio del servicio de autenticación:

```bash
cd services/auth
```

### Ejecuta las migraciones:

```bash
alembic upgrade head
````

### Ejecución
- Usando Docker
Construir y levantar los servicios

Desde la raíz del proyecto, ejecuta:

```bash
sudo docker-compose up --build
```

#### Esto levantará:

- Un contenedor para la base de datos PostgreSQL (auth-db).
- Un contenedor para el servicio de autenticación (auth-service).

### Verificar el estado de los contenedores

```bash
sudo docker-compose ps
```

### Acceso a la API

La API estará disponible en: http://localhost:8000

- Sin Docker
Activa tu entorno virtual:

```bash
source venv/bin/activate
```

Inicia la aplicación:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000
```
