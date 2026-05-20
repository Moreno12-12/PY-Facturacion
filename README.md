# FreshMart - Sistema de Facturacion Multi-Base de Datos

Sistema de facturacion para un supermercado que utiliza **4 tecnologias de bases de datos** diferentes, implementado con **Arquitectura Hexagonal** (Ports and Adapters).

## Arquitectura Hexagonal

El proyecto sigue el patron de Arquitectura Hexagonal que separa las responsabilidades en capas:

```
┌─────────────────────────────────────────────────────────┐
│                    WEB LAYER (Controllers)               │
│  persona_controller | producto_controller | factura...  │
├─────────────────────────────────────────────────────────┤
│              APPLICATION LAYER (Services + DTO)          │
│  PersonaService | ProductoService | FacturaService...    │
├─────────────────────────────────────────────────────────┤
│                DOMAIN LAYER (Entities + Ports)           │
│  Persona, Producto, Factura | Repository Interfaces      │
├─────────────────────────────────────────────────────────┤
│           INFRASTRUCTURE LAYER (Adapters + Connections)  │
│  CassandraRepo | MongoRepo | MySQLRepo | Neo4jRepo       │
└─────────────────────────────────────────────────────────┘
```

### Capas

| Capa | Ubicacion | Responsabilidad |
|---|---|---|
| **Web** | `web/controllers/` | Controladores HTTP, recibe peticiones y devuelve respuestas |
| **Application** | `src/application/` | Casos de uso, orquesta la logica de negocio |
| **Domain** | `src/domain/` | Entidades y puertos (interfaces). No depende de nada externo |
| **Infrastructure** | `src/infrastructure/` | Implementaciones concretas de repositorios y conexiones a BD |

## Tecnologias de Bases de Datos

| Base de Datos | Modelo | Adapter | Uso |
|---|---|---|---|
| **Apache Cassandra** | Column-Family | `CassandraPersonaRepository` | Personas (Clientes y Empleados) |
| **MongoDB** | Documento | `MongoProductoRepository` | Productos (catalogo flexible) |
| **MySQL** | Relacional | `MySQLFacturaRepository` | Facturas y Detalle_Factura |
| **Neo4j** | Grafo | `Neo4jRecomendacionRepository` | Recomendaciones de productos |

## Estructura del Proyecto

```
fact-proyecto/
├── .env                          # Variables de entorno
├── .gitignore
├── requirements.txt
├── README.md
├── app.py                        # Entry point + Factory (create_app)
│
├── src/                          # Core del negocio
│   ├── domain/                   # CAPA DE DOMINIO (sin dependencias externas)
│   │   ├── entities/             # Entidades: Persona, Producto, Factura...
│   │   └── ports/                # Interfaces: Repository contracts
│   │
│   ├── application/              # CAPA DE APLICACION
│   │   ├── services/             # Casos de uso: PersonaService, etc.
│   │   └── dto/                  # Data Transfer Objects
│   │
│   └── infrastructure/           # CAPA DE INFRAESTRUCTURA
│       ├── adapters/             # Implementaciones de repositorios
│       │   ├── cassandra_persona_repository.py
│       │   ├── mongo_producto_repository.py
│       │   ├── mysql_factura_repository.py
│       │   └── neo4j_recomendacion_repository.py
│       └── connections/          # Conexiones Singleton a BD
│           ├── cassandra_connection.py
│           ├── mongo_connection.py
│           ├── mysql_connection.py
│           └── neo4j_connection.py
│
├── web/                          # CAPA WEB (presentacion)
│   ├── controllers/              # Controladores Flask
│   │   ├── persona_controller.py
│   │   ├── producto_controller.py
│   │   ├── factura_controller.py
│   │   └── recomendacion_controller.py
│   ├── templates/                # Plantillas HTML
│   └── static/                   # CSS, JS, imagenes
│
└── dbs/                          # Scripts de setup y datos
    ├── setup_cassandra.py
    ├── setup_mongo.py
    ├── setup_mysql.py
    ├── setup_neo4j.py
    └── seed_data.py
```

## Requisitos Previos

### Bases de Datos

1. **Apache Cassandra** (puerto 9042)
2. **MongoDB** (puerto 27017)
3. **MySQL** (puerto 3306)
4. **Neo4j** (puerto 7687)

### Python 3.10+

## Instalacion

### 1. Clonar el repositorio

```bash
git clone <url-del-repositorio>
cd fact-proyecto
```

### 2. Crear entorno virtual

```bash
python -m venv env
```

**Windows:**
```powershell
.\env\Scripts\activate
```

**Linux/Mac:**
```bash
source env/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

El archivo `.env` contiene la configuracion de conexiones:

```env
CASSANDRA_HOST=127.0.0.1
CASSANDRA_KEYSPACE=freshmart

MONGO_HOST=127.0.0.1
MONGO_PORT=27017
MONGO_DB=freshmart

MYSQL_HOST=127.0.0.1
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=
MYSQL_DB=freshmart

NEO4J_URI=bolt://127.0.0.1:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=neo4j

FLASK_DEBUG=True
FLASK_SECRET_KEY=supersecreto123
```

### 5. Configurar bases de datos

```bash
python dbs/setup_cassandra.py
python dbs/setup_mongo.py
python dbs/setup_mysql.py
python dbs/setup_neo4j.py    # Opcional
python dbs/seed_data.py
```

### 6. Ejecutar la aplicacion

```bash
python app.py
```

Disponible en: **http://localhost:5000**

## Flujo de una Peticion (Ejemplo: Crear Persona)

```
1. HTTP POST /personas/nueva
       ↓
2. persona_controller.py recibe el request
       ↓
3. Crea CrearPersonaDTO con los datos del form
       ↓
4. PersonaService.crear(dto) aplica la logica
       ↓
5. CassandraPersonaRepository.create(persona) ejecuta CQL
       ↓
6. CassandraConnection envia a la BD
       ↓
7. Respuesta HTTP redirect /personas

## Gestion de Dependencias

El proyecto incluye el archivo `requirements.txt` con las dependencias necesarias. Para mantenerlo actualizado se recomienda:

- **Actualizar todo el archivo:**
  ```bash
  pip freeze > requirements.txt
  ```

- **Agregar o actualizar dependencias sin perder el orden o edicion manual:**
  ```bash
  pip freeze >> requirements.txt
  ```

## Notas

- El parche de compatibilidad Python 3.12+ para Cassandra esta en `src/infrastructure/connections/cassandra_connection.py`
