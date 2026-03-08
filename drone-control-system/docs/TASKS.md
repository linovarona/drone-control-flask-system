'á', 'é', 'í', 'ó', 'ú', 'ñ', 'Á', 'É', 'Í', 'Ó', 'Ú', 'Ñ', 'ü', 'Ü'

# 馃搵 TASKS.md - Plan de Implementación Drone Control System

> **Proyecto:** Sistema de Control Aéreo para Drones (U-space/USSP)  
> **Ubicación:** Neuquén, Argentina - Vaca Muerta  
> **Documento fuente:** NQN_CONTEXTO_1.pdf  
> **Fecha de creación:** 2026-03-04  
> **Versión:** 1.0.0

---

## 馃幆 Estructura del Documento

- [FASE 0: Infraestructura del Proyecto](#fase-0-infraestructura-del-proyecto)
- [FASE 1: Modelos de Datos y Persistencia](#fase-1-modelos-de-datos-y-persistencia)
- [FASE 2: Edge Gateway - Core](#fase-2-edge-gateway---core)
- [FASE 3: Cloud Platform - Core](#fase-3-cloud-platform---core)
- [FASE 4: Simulador de Drones](#fase-4-simulador-de-drones)
- [FASE 5: Integración Inter-Capas](#fase-5-integración-inter-capas)
- [FASE 6: Seguridad y Compliance](#fase-6-seguridad-y-compliance)
- [FASE 7: Monitoreo y Observabilidad](#fase-7-monitoreo-y-observabilidad)
- [FASE 8: Pruebas de Integración y E2E](#fase-8-pruebas-de-integración-y-e2e)
- [FASE 9: Empaquetamiento y Despliegue](#fase-9-empaquetamiento-y-despliegue)
- [FASE 10: Documentación Final](#fase-10-documentación-final)

---

## 馃搶 Convenciones

### Estados de Tarea
- `[ ]` - Pendiente
- `[~]` - En progreso
- `[x]` - Completada
- `[!]` - Bloqueada (requiere atención)

### Prioridades
- **P0:** Crítico - Bloquea siguientes fases
- **P1:** Alto - Importante para funcionalidad core
- **P2:** Medio - Mejora o optimización
- **P3:** Bajo - Nice to have

---
Estructura General del Proyecto

drone-control-system/
├── 📁 .github/workflows/        # CI/CD
├── 📁 docs/                     # Documentación técnica y de usuario
├── 📁 scripts/                  # Scripts de automatización
├── 📁 infrastructure/           # Docker, K8s, Terraform
├── 📁 shared/                   # Contratos API, tipos, protos
├── 📁 edge-gateway/             # Capa de Borde (Python/FastAPI)
├── 📁 cloud-platform/           # Capa de Nube (Node.js/TypeScript)
├── 📁 drone-simulator/          # Simulador de drones
├── 📁 web-dashboard/            # Frontend React (futuro)
└── 📁 tests/                    # Tests de integración E2E

## FASE 0: Infraestructura del Proyecto

**Duración estimada:** 2-3 días  
**Tag objetivo:** `v0.0.1-infra`  
**Requisito crítico:** Estandarización de entorno (<5 min setup)

### Tareas de Configuración

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 0.1 | Inicializar repositorio Git con estructura de carpetas			| P0 | [ ] | | `.gitignore` para Python/Node/Docker |
| 0.2 | Crear `README.md` inicial con descripción del proyecto			| P0 | [ ] | | Incluir arquitectura de alto nivel |
| 0.3 | Configurar entorno virtual Python en `edge-gateway/`  			| P0 | [ ] | | Python 3.11+, venv |
| 0.4 | Inicializar proyecto Node.js en `cloud-platform/` 				| P0 | [ ] | | Node 18+, npm init |
| 0.5 | Crear carpeta `shared/` con contratos API OpenAPI 3.0 			| P0 | [ ] | | Fuente de verdad para ambos lenguajes |
| 0.6 | Configurar Black + Ruff para Python (linting/formatting)		| P1 | [ ] | | `pyproject.toml` |
| 0.7 | Configurar ESLint + Prettier para TypeScript 					| P1 | [ ] | | `.eslintrc.json`, `.prettierrc` |
| 0.8 | Setup pre-commit hooks (validación antes de commit) 			| P1 | [ ] | | `.pre-commit-config.yaml` |
| 0.9 | Crear `scripts/setup.ps1` - Setup automatizado Windows 			| P0 | [ ] | | Verificar prerequisitos |
| 0.10 | Crear `scripts/test.ps1` - Ejecución de tests 					| P1 | [ ] | | Soporte para unit/integration/all |
| 0.11 | Crear `scripts/build.ps1` - Build de componentes 				| P1 | [ ] | | Docker compose build |
| 0.12 | Configurar GitHub Actions básico (lint + test en PR) 			| P1 | [ ] | | `.github/workflows/ci.yml` |
| 0.13 | Crear `docker-compose.yml` base para desarrollo 				| P1 | [ ] | | PostgreSQL, Redis |
| 0.14 | Configurar VS Code workspace (settings, launch, extensions) 	| P2 | [ ] | | `.vscode/` |

### Checklist de Cierre Fase 0

- [ ] **Compilación:** `python -m py_compile` (Python) y `tsc --noEmit` (TypeScript) sin errores
- [ ] **Tests unitarios:** Suite mínima de smoke tests (validar importaciones)
- [ ] **Documentación:** `docs/00-setup.md` con guía de instalación paso a paso
- [ ] **Punto de restauración:** Tag `v0.0.1-infra` creado y pusheado

---

## FASE 1: Modelos de Datos y Persistencia

**Duración estimada:** 3-4 días  
**Tag objetivo:** `v0.1.0-data`  
**Requisito crítico:** Consistencia entre Python y TypeScript (fuente única de verdad)

### Tareas de Modelos

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 1.1 | Definir entidad `Drone` (atributos, estados, validaciones) 	| P0 | [ ] | | ID, tipo, capacidades, propietario |
| 1.2 | Definir entidad `FlightPlan` (plan de vuelo) 				| P0 | [ ] | | Waypoints, horarios, altitudes |
| 1.3 | Definir entidad `Telemetry` (datos de telemetría) 			| P0 | [ ] | | Lat, lon, alt, velocidad, heading |
| 1.4 | Definir entidad `Geofence` (geocercas) 						| P0 | [ ] | | Polígonos, restricciones, horarios |
| 1.5 | Definir entidad `Alert` (alertas de conflicto) 				| P0 | [ ] | | Tipo, severidad, acción recomendada |
| 1.6 | Definir entidad `Operator` (operador de drones) 			| P1 | [ ] | | Licencia ANAC, contacto |
| 1.7 | Implementar modelos SQLAlchemy 2.0 + Pydantic v2 (Python) 	| P0 | [ ] | | `edge-gateway/src/models/` |
| 1.8 | Implementar modelos Zod + TypeScript interfaces 			| P0 | [ ] | | `cloud-platform/src/models/` |
| 1.9 | Crear esquemas JSON compartidos en `shared/schemas/` 		| P0 | [ ] | | Validación cruzada |
| 1.10 | Configurar PostgreSQL con Docker Compose 					| P0 | [ ] | | Volumen persistente |
| 1.11 | Configurar Redis para caché de estado en tiempo real 		| P1 | [ ] | | Estado de drones activos |
| 1.12 | Implementar migraciones Alembic (Python) 					| P0 | [ ] | | `edge-gateway/migrations/` |
| 1.13 | Implementar migraciones TypeORM (Node.js) 					| P0 | [ ] | | `cloud-platform/src/migrations/` |
| 1.14 | Crear repositorios/DAOs con patrón Repository 				| P1 | [ ] | | Abstracción de base de datos |
| 1.15 | Crear seeders de datos de prueba 							| P1 | [ ] | | Geocercas Vaca Muerta, drones ejemplo |
| 1.16 | Implementar validaciones de dominio (reglas ANAC) 			| P1 | [ ] | | Altitudes máximas, zonas restringidas |

### Checklist de Cierre Fase 1

- [ ] **Compilación:** Modelos compilan en ambos lenguajes sin warnings
- [ ] **Tests unitarios:** CRUD completo testeado con SQLite (tests)
- [ ] **Documentación:** `docs/01-data-model.md` con diagrama ER y ejemplos
- [ ] **Punto de restauración:** Tag `v0.1.0-data` creado y pusheado

---

## FASE 2: Edge Gateway - Core

**Duración estimada:** 5-7 días  
**Tag objetivo:** `v0.2.0-edge-core`  
**Requisito crítico:** Latencia <50ms en 95% de operaciones de telemetría

### Tareas de API y Telemetría

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 2.1 | Setup FastAPI con async/await y Uvicorn 					| P0 | [ ] | | Configuración de workers |
| 2.2 | Implementar middleware de timing (medición de latencia) 	| P0 | [ ] | | Header X-Response-Time |
| 2.3 | Crear endpoint POST `/telemetry` con validación Pydantic 	| P0 | [ ] | | Receptor de telemetría |
| 2.4 | Implementar almacenamiento en Redis (estado de drones) 		| P0 | [ ] | | TTL 30 segundos |
| 2.5 | Crear endpoint GET `/drones` (listar drones activos) 		| P0 | [ ] | | Con filtros por zona |
| 2.6 | Implementar endpoint GET `/health` (health check) 			| P1 | [ ] | | Liveness probe |
| 2.7 | Implementar endpoint GET `/ready` (readiness check) 		| P1 | [ ] | | Verifica DB, Redis |
| 2.8 | Implementar endpoint GET `/metrics` (Prometheus metrics) 	| P1 | [ ] | | Latencia, throughput |

### Tareas de Deconflicción Táctica

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 2.9 | Implementar `ConflictDetector` - cálculo distancia 3D 			| P0 | [ ] | | Fórmula Haversine + altitud |
| 2.10 | Definir umbrales de seguridad (50m crítico, 100m advertencia) 	| P0 | [ ] | | Configurable vía env vars |
| 2.11 | Implementar predicción de trayectoria (vector velocidad) 		| P0 | [ ] | | Proyección 60 segundos |
| 2.12 | Crear sistema de alertas en tiempo real 						| P0 | [ ] | | TA (Traffic Alert), Violación |
| 2.13 | Implementar WebSocket `/ws/telemetry` para operadores 			| P0 | [ ] | | FastAPI native o Socket.io |
| 2.14 | Crear broadcaster de alertas a Cloud Platform 					| P0 | [ ] | | HTTP/2 o MQTT |
| 2.15 | Implementar buffer de mensajes ante desconexión 				| P1 | [ ] | | Cola local, retry |

### Tareas de MAVLink

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 2.16 | Crear interfaz abstracta `DroneAdapter` 						| P1 | [ ] | | Patrón adapter |
| 2.17 | Implementar `MAVLinkAdapter` con pymavlink 					| P1 | [ ] | | UDP/TCP connection |
| 2.18 | Implementar parser de mensajes MAVLink (GLOBAL_POSITION_INT) 	| P1 | [ ] | | Conversión a modelo interno |
| 2.19 | Crear modo simulación para desarrollo sin drones reales 		| P0 | [ ] | | `SimulatedAdapter` |

### Tareas de Logging y Configuración

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 2.20 | Implementar logging estructurado JSON 			| P1 | [ ] | | `structlog` o similar |
| 2.21 | Agregar correlation ID (traceo de requests) 	| P1 | [ ] | | Middleware |
| 2.22 | Crear configuración por variables de entorno 	| P1 | [ ] | | `pydantic-settings` |
| 2.23 | Documentar API con OpenAPI/Swagger automático 	| P1 | [ ] | | FastAPI native |

### Checklist de Cierre Fase 2

- [ ] **Compilación:** `docker build` exitoso, imagen <200MB
- [ ] **Tests unitarios:**
  - [ ] Tests de latencia (<50ms en 95% de requests)
  - [ ] Tests de deconflicción (escenarios de colisión)
  - [ ] Tests de carga (100 drones simultáneos, 10Hz)
  - [ ] Tests de WebSocket (conexión, mensajes, desconexión)
- [ ] **Documentación:** `docs/02-edge-gateway.md` con arquitectura y API reference
- [ ] **Punto de restauración:** Tag `v0.2.0-edge-core` creado y pusheado

---

## FASE 3: Cloud Platform - Core

**Duración estimada:** 5-7 días  
**Tag objetivo:** `v0.3.0-cloud-core`  
**Requisito crítico:** Graceful degradation si Edge Gateway offline

### Tareas de API REST

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 3.1 | Setup Express + TypeScript con estructura limpia 			| P0 | [ ] | | Controllers, services, middleware |
| 3.2 | Implementar middleware de errores centralizado 				| P0 | [ ] | | Error handler Express |
| 3.3 | Crear API CRUD `/api/v1/flights` (planificación de vuelos) 	| P0 | [ ] | | POST, GET, PUT, DELETE |
| 3.4 | Implementar validación de plan de vuelo (geocercas) 		| P0 | [ ] | | Chequeo de restricciones |
| 3.5 | Crear API `/api/v1/drones` (gestión de flota) 				| P0 | [ ] | | Registro, búsqueda |
| 3.6 | Crear API `/api/v1/geofences` (geocercas) 					| P0 | [ ] | | CRUD de zonas restringidas |
| 3.7 | Crear API `/api/v1/alerts` (historial de alertas) 			| P1 | [ ] | | Query por fecha, severidad |
| 3.8 | Implementar paginación en todas las APIs 					| P1 | [ ] | | Offset/limit |
| 3.9 | Implementar filtros y búsqueda avanzada 					| P1 | [ ] | | Por zona, fecha, estado |

### Tareas de Deconflicción Estratégica

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 3.10 | Implementar `DeconflictionService` - algoritmo A* 			| P0 | [ ] | | Planificación de rutas |
| 3.11 | Crear verificación de superposición temporal 				| P0 | [ ] | | Vuelos simultáneos |
| 3.12 | Implementar verificación de superposición espacial 		| P0 | [ ] | | Buffer de seguridad 3D |
| 3.13 | Crear generador de rutas alternativas 						| P1 | [ ] | | Cuando hay conflicto |
| 3.14 | Implementar optimización de rutas (minimizar distancia) 	| P2 | [ ] | | Considerando viento, etc. |

### Tareas de Integración y Comunicación

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 3.15 | Crear cliente HTTP/2 para Edge Gateway 		| P0 | [ ] | | `axios` con keep-alive |
| 3.16 | Implementar receptor de alertas del Edge 		| P0 | [ ] | | Endpoint POST `/webhooks/edge-alerts` |
| 3.17 | Crear sincronización bidireccional de estado 	| P0 | [ ] | | WebSocket o MQTT |
| 3.18 | Implementar modo contingencia (Edge offline) 	| P0 | [ ] | | Operar con último estado conocido |
| 3.19 | Crear buffer de comandos para Edge 			| P1 | [ ] | | Comandos pendientes de envío |

### Tareas de Autenticación y Autorización

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 3.20 | Implementar autenticación JWT 				| P0 | [ ] | | Login, refresh token |
| 3.21 | Crear roles: `operator`, `admin`, `system` | P0 | [ ] | | RBAC |
| 3.22 | Implementar middleware de autorización 	| P0 | [ ] | | `@Roles()` decorator |
| 3.23 | Crear API de gestión de usuarios 			| P1 | [ ] | | CRUD de operadores |
| 3.24 | Implementar rate limiting por API key 		| P1 | [ ] | | `express-rate-limit` |

### Tareas de EANA y Normativa

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 3.25 | Crear `EANAService` (adapter pattern) 				| P1 | [ ] | | Interfaz para integración futura |
| 3.26 | Implementar validación RAAC Parte 102 				| P1 | [ ] | | Categoría Específica |
| 3.27 | Crear generador de reportes para ANAC 				| P2 | [ ] | | Formato regulatorio |
| 3.28 | Implementar registro de operaciones (auditoría) 	| P1 | [ ] | | Quién, qué, cuándo |

### Checklist de Cierre Fase 3

- [ ] **Compilación:** `tsc` sin errores, `docker build` exitoso
- [ ] **Tests unitarios:**
  - [ ] Tests de deconflicción estratégica (planificación)
  - [ ] Tests de integración Edge-Cloud (con mock)
  - [ ] Tests de autenticación y autorización
  - [ ] Tests de graceful degradation (simular corte de Edge)
- [ ] **Documentación:** `docs/03-cloud-platform.md` con diagramas de secuencia
- [ ] **Punto de restauración:** Tag `v0.3.0-cloud-core` creado y pusheado

---

## FASE 4: Simulador de Drones

**Duración estimada:** 3-4 días  
**Tag objetivo:** `v0.4.0-simulator`  
**Requisito crítico:** Realismo de comportamientos de Vaca Muerta

### Tareas de Física y Modelado

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 4.1 | Crear clase `DroneSimulator` con estado interno 	| P0 | [ ] | | Posición, velocidad, batería |
| 4.2 | Implementar modelo de física de vuelo 				| P0 | [ ] | | Velocidad, aceleración, heading |
| 4.3 | Agregar simulación de viento (aleatorio) 			| P2 | [ ] | | Afecta trayectoria |
| 4.4 | Implementar consumo de batería 						| P1 | [ ] | | Basado en velocidad/maniobras |
| 4.5 | Crear límites realistas (velocidad máxima, altitud) | P1 | [ ] | | Según tipo de drone |

### Tareas de Trayectorias y Escenarios

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 4.6 | Implementar patrón de inspección de ductos 		| P0 | [ ] | | Líneas paralelas |
| 4.7 | Implementar patrón de búsqueda (grid) 			| P0 | [ ] | | SAR - Search and Rescue |
| 4.8 | Implementar patrón de patrulla perímetro 		| P1 | [ ] | | Seguridad perimetral |
| 4.9 | Crear generador de waypoints realistas 			| P1 | [ ] | | Dentro de polígono Vaca Muerta |
| 4.10 | Implementar escenario: colisión inminente 		| P0 | [ ] | | Dos drones convergen |
| 4.11 | Implementar escenario: violación de geocerca 	| P0 | [ ] | | Entrada a zona restringida |
| 4.12 | Implementar escenario: pérdida de señal 		| P1 | [ ] | | Deja de enviar telemetría |
| 4.13 | Implementar escenario: batería baja 			| P1 | [ ] | | RTL - Return to Launch |
| 4.14 | Crear configuración YAML de escenarios 		| P1 | [ ] | | Definir flotas, rutas, eventos |

### Tareas de Comunicación y Visualización

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 4.15 | Implementar cliente HTTP para Edge Gateway 	| P0 | [ ] | | `aiohttp` async |
| 4.16 | Enviar telemetría a 10Hz (100ms) 				| P0 | [ ] | | Loop asyncio |
| 4.17 | Crear visualización CLI en tiempo real 		| P1 | [ ] | | Tabla con estado de drones |
| 4.18 | Implementar logging de simulación 				| P1 | [ ] | | CSV/JSON con métricas |
| 4.19 | Crear reporte post-simulación 					| P1 | [ ] | | Estadísticas, eventos |
| 4.20 | Implementar modo batch (sin interacción) 		| P2 | [ ] | | Para CI/CD |

### Checklist de Cierre Fase 4

- [ ] **Compilación:** Ejecutable standalone o Docker image <150MB
- [ ] **Tests unitarios:**
  - [ ] Tests de física de vuelo (posición calculada correctamente)
  - [ ] Tests de generación de escenarios
  - [ ] Tests de formato de telemetría (validación contra schema)
  - [ ] Tests de carga (simular 50 drones)
- [ ] **Documentación:** `docs/04-simulator.md` con guía de escenarios de prueba
- [ ] **Punto de restauración:** Tag `v0.4.0-simulator` creado y pusheado

---

## FASE 5: Integración Inter-Capas

**Duración estimada:** 4-5 días  
**Tag objetivo:** `v0.5.0-integration`  
**Requisito crítico:** Autonomía de 30 minutos si se pierde conexión Edge-Cloud

### Tareas de Protocolo y Mensajería

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 5.1 | Definir esquema Protobuf para comunicación 			| P0 | [ ] | | `shared/proto/messages.proto` |
| 5.2 | Implementar serializador/deserializador Python 		| P0 | [ ] | | `edge-gateway` |
| 5.3 | Implementar serializador/deserializador TypeScript 	| P0 | [ ] | | `cloud-platform` |
| 5.4 | Configurar RabbitMQ en Docker Compose 				| P1 | [ ] | | Cola de mensajes |
| 5.5 | Implementar productor de mensajes (Edge) 			| P0 | [ ] | | `aio-pika` |
| 5.6 | Implementar consumidor de mensajes (Cloud) 			| P0 | [ ] | | `amqplib` |
| 5.7 | Crear exchange para alertas prioritarias 			| P1 | [ ] | | Direct exchange |
| 5.8 | Implementar cola de reintentos (dead letter) 		| P1 | [ ] | | Retry con backoff |

### Tareas de Resiliencia y Estado

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 5.9 | Implementar heartbeat Edge 鈫?Cloud 				| P0 | [ ] | | Cada 5 segundos |
| 5.10 | Crear detector de desconexión 						| P0 | [ ] | | Timeout 15 segundos |
| 5.11 | Implementar buffer local en Edge (30 min) 			| P0 | [ ] | | SQLite o archivo |
| 5.12 | Crear mecanismo de sincronización post-reconexión 	| P0 | [ ] | | Enviar buffer pendiente |
| 5.13 | Implementar circuit breaker para llamadas Cloud 	| P1 | [ ] | | `pybreaker` |
| 5.14 | Crear replicación de estado crítico 				| P1 | [ ] | | Drones en vuelo |

### Tareas de Logging Distribuido

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 5.15 | Implementar trace ID en Edge 				| P0 | [ ] | | UUID por request |
| 5.16 | Propagar trace ID a Cloud 					| P0 | [ ] | | Headers HTTP |
| 5.17 | Agregar trace ID a logs de ambos servicios | P1 | [ ] | | Correlación |
| 5.18 | Crear endpoint de tracing distribuido 		| P2 | [ ] | | Visualización de flujo |

### Tareas de Configuración y Despliegue

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 5.19 | Crear Docker Compose completo del stack 				| P0 | [ ] | | Todos los servicios |
| 5.20 | Implementar health checks coordinados 					| P1 | [ ] | | Docker healthcheck |
| 5.21 | Crear script `docker-compose up` un comando 			| P1 | [ ] | | `scripts/start-all.ps1` |
| 5.22 | Documentar variables de entorno requeridas 			| P1 | [ ] | | `.env.example` |
| 5.23 | Crear configuración por ambiente (dev/staging/prod) 	| P1 | [ ] | | `config/` |

### Checklist de Cierre Fase 5

- [ ] **Compilación:** `docker-compose build` exitoso para todos los servicios
- [ ] **Tests unitarios:**
  - [ ] Tests de desconexión/reconexión (simular corte de red)
  - [ ] Tests de ordenamiento de mensajes (secuencia correcta)
  - [ ] Tests de carga de la cola (backpressure)
  - [ ] Tests de buffer local (llenar, reconectar, sincronizar)
- [ ] **Documentación:** `docs/05-integration.md` con diagramas de arquitectura
- [ ] **Punto de restauración:** Tag `v0.5.0-integration` creado y pusheado

---

## FASE 6: Seguridad y Compliance

**Duración estimada:** 4-5 días  
**Tag objetivo:** `v0.6.0-security`  
**Requisito crítico:** Cumplir Resolución 550/2025 ANAC

### Tareas de Cifrado y Transmisión

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 6.1 | Configurar TLS 1.3 para todas las APIs 			| P0 | [ ] | | Certificados autofirmados para dev |
| 6.2 | Implementar HTTPS obligatorio en Edge 			| P0 | [ ] | | Redirect HTTP 鈫?HTTPS |
| 6.3 | Configurar HTTPS en Cloud Platform 				| P0 | [ ] | | `https` module o reverse proxy |
| 6.4 | Implementar cifrado de datos sensibles en DB 	| P0 | [ ] | | AES-256 |
| 6.5 | Crear gestión de secretos (Vault o env) 		| P1 | [ ] | | Claves, tokens |
| 6.6 | Implementar rotación de claves 					| P2 | [ ] | | Automática |

### Tareas de Autenticación y Autorización Avanzada

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 6.7 | Implementar autenticación de dispositivos (drones) 	| P0 | [ ] | | Certificados X.509 o tokens |
| 6.8 | Crear API keys para integraciones externas 			| P1 | [ ] | | Uali, Ministerio |
| 6.9 | Implementar OAuth2/OIDC (futuro) 					| P2 | [ ] | | Integración con ID provincial |
| 6.10 | Crear políticas de contraseñas seguras 			| P1 | [ ] | | Longitud, complejidad |
| 6.11 | Implementar 2FA para administradores 				| P2 | [ ] | | TOTP |

### Tareas de Auditoría y Compliance

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 6.12 | Implementar log inmutable de operaciones 			| P0 | [ ] | | Append-only, firmado |
| 6.13 | Crear registro de quién aprobó cada vuelo 			| P0 | [ ] | | Traza completa |
| 6.14 | Implementar retención de datos (2 años ANAC) 		| P0 | [ ] | | Política automática |
| 6.15 | Crear generador de reportes regulatorios 			| P1 | [ ] | | Formato ANAC |
| 6.16 | Implementar anonimización para datos de prueba 	| P1 | [ ] | | GDPR/Protección datos |
| 6.17 | Crear matriz de riesgos de seguridad 				| P2 | [ ] | | Documento |
| 6.18 | Documentar planes de contingencia 					| P2 | [ ] | | Incident response |

### Tareas de Protección y Hardening

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 6.19 | Implementar rate limiting avanzado 				| P1 | [ ] | | Por IP, por usuario, por endpoint |
| 6.20 | Configurar protección DDoS básica 					| P1 | [ ] | | `express-slow-down` |
| 6.21 | Implementar headers de seguridad (HSTS, CSP, etc.) | P1 | [ ] | | `helmet` |
| 6.22 | Crear validación de input (sanitización) 			| P0 | [ ] | | Prevenir injection |
| 6.23 | Implementar CORS restrictivo 						| P1 | [ ] | | Solo orígenes permitidos |
| 6.24 | Configurar seguridad de contenedores 				| P1 | [ ] | | Non-root user, read-only FS |

### Checklist de Cierre Fase 6

- [ ] **Compilación:** Security scan con `bandit` (Python) y `npm audit` sin críticos
- [ ] **Tests unitarios:**
  - [ ] Tests de penetración básicos (headers, SQL injection, XSS)
  - [ ] Tests de autenticación de dispositivos (certificados)
  - [ ] Tests de auditoría (logs inmutables, no borrado)
  - [ ] Tests de rate limiting (throttling correcto)
- [ ] **Documentación:** `docs/06-security.md` con políticas y procedimientos
- [ ] **Punto de restauración:** Tag `v0.6.0-security` creado y pusheado

---

## FASE 7: Monitoreo y Observabilidad

**Duración estimada:** 3-4 días  
**Tag objetivo:** `v0.7.0-monitoring`  
**Requisito crítico:** Detección de problemas <30 segundos

### Tareas de Métricas y Prometheus

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 7.1 | Integrar `prometheus-client` en Edge Gateway 			| P0 | [ ] | | Python |
| 7.2 | Integrar `prom-client` en Cloud Platform 				| P0 | [ ] | | Node.js |
| 7.3 | Definir métricas clave (latencia, throughput, errores) 	| P0 | [ ] | | Latencia p50, p95, p99 |
| 7.4 | Agregar métricas de negocio (drones activos, alertas) 	| P1 | [ ] | | Custom metrics |
| 7.5 | Configurar Prometheus en Docker Compose 				| P1 | [ ] | | Scraping cada 15s |
| 7.6 | Crear alertas Prometheus (rules) 						| P1 | [ ] | | Latencia >100ms, error rate >1% |

### Tareas de Dashboards y Visualización

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 7.7 | Configurar Grafana en Docker Compose 			| P1 | [ ] | | Puerto 3000 |
| 7.8 | Crear dashboard "Operaciones en Tiempo Real" 	| P0 | [ ] | | Mapa de drones, alertas activas |
| 7.9 | Crear dashboard "Performance del Sistema" 		| P1 | [ ] | | Latencia, throughput |
| 7.10 | Crear dashboard "Negocio - Vaca Muerta" 		| P1 | [ ] | | Vuelos por hora, incidentes |
| 7.11 | Configurar datasources (Prometheus, Loki) 		| P1 | [ ] | | Auto-configurado |

### Tareas de Alerting y Notificaciones

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 7.12 | Configurar Alertmanager 				| P1 | [ ] | | Routing de alertas |
| 7.13 | Integrar notificaciones Slack 			| P1 | [ ] | | Webhook |
| 7.14 | Integrar notificaciones Email 			| P2 | [ ] | | SMTP |
| 7.15 | Crear runbooks para alertas comunes 	| P2 | [ ] | | Procedimientos |
| 7.16 | Configurar PagerDuty (opcional) 		| P3 | [ ] | | On-call |

### Tareas de Logging y Tracing

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 7.17 | Configurar Loki para agregación de logs 		| P1 | [ ] | | Docker plugin |
| 7.18 | Implementar envío de logs estructurados a Loki | P1 | [ ] | | Driver de logging |
| 7.19 | Configurar Jaeger para distributed tracing 	| P2 | [ ] | | OpenTelemetry |
| 7.20 | Instrumentar código con spans 					| P2 | [ ] | | Traza de requests |
| 7.21 | Crear dashboard de tracing en Grafana 			| P2 | [ ] | | Jaeger datasource |

### Tareas de SLOs y Operación

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 7.22 | Definir SLOs del sistema 				| P1 | [ ] | | 99.9% uptime, <50ms p95 |
| 7.23 | Crear SLIs medibles 					| P1 | [ ] | | Queries Prometheus |
| 7.24 | Implementar health checks profundos 	| P1 | [ ] | | Verifica dependencias |
| 7.25 | Crear guía de operación 24/7 			| P2 | [ ] | | Playbook |

### Checklist de Cierre Fase 7

- [ ] **Compilación:** Imágenes Docker con exporters de métricas incluidos
- [ ] **Tests unitarios:**
  - [ ] Tests de endpoints de métricas (Prometheus format)
  - [ ] Tests de alertas (simular condición crítica, verificar notificación)
  - [ ] Tests de health checks (cada dependencia)
- [ ] **Documentación:** `docs/07-monitoring.md` con guía de operación 24/7
- [ ] **Punto de restauración:** Tag `v0.7.0-monitoring` creado y pusheado

---

## FASE 8: Pruebas de Integración y E2E

**Duración estimada:** 4-5 días  
**Tag objetivo:** `v0.8.0-testing`  
**Requisito crítico:** Validación de escenarios realistas de Vaca Muerta

### Tareas de Entorno de Integración

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 8.1 | Crear Docker Compose de integración 			| P0 | [ ] | | `docker-compose.test.yml` |
| 8.2 | Configurar base de datos de prueba 				| P0 | [ ] | | Datos de Vaca Muerta |
| 8.3 | Crear fixtures de drones y vuelos 				| P1 | [ ] | | Factory pattern |
| 8.4 | Implementar cleanup automático post-test 		| P1 | [ ] | | Isolation |
| 8.5 | Configurar CI para tests de integración 		| P1 | [ ] | | GitHub Actions |

### Tareas de Tests de API

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 8.6 | Crear colección Postman/Newman 					| P1 | [ ] | | Todos los endpoints |
| 8.7 | Automatizar tests de API en CI					| P1 | [ ] | | `newman run` |
| 8.8 | Implementar tests de contrato (Pact) 			| P2 | [ ] | | Consumer-driven |
| 8.9 | Validar schema de respuestas 					| P1 | [ ] | | OpenAPI |

### Tareas de Tests E2E

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 8.10 | Setup Playwright para tests E2E 					| P1 | [ ] | | Navegador headless |
| 8.11 | Crear test E2E: planificar vuelo completo 			| P0 | [ ] | | Login 鈫?planificar 鈫?aprobar |
| 8.12 | Crear test E2E: monitorear drones en tiempo real 	| P0 | [ ] | | Dashboard con mapa |
| 8.13 | Crear test E2E: recibir y atender alerta 			| P0 | [ ] | | Flujo crítico |
| 8.14 | Crear test E2E: escenario de contingencia 			| P1 | [ ] | | Edge offline |

### Tareas de Tests de Carga y Caos

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 8.15 | Configurar k6 para tests de carga 					| P1 | [ ] | | Scripts de performance |
| 8.16 | Crear test de carga: 500 drones, 10Hz 				| P0 | [ ] | | 30 minutos |
| 8.17 | Crear test de carga: 50 operadores concurrentes 	| P1 | [ ] | | API de planificación |
| 8.18 | Implementar chaos engineering básico 				| P2 | [ ] | | Matar contenedores aleatoriamente |
| 8.19 | Validar latencia end-to-end <200ms 				| P0 | [ ] | | Edge 鈫?Cloud 鈫?Dashboard |

### Tareas de Validación de Negocio

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 8.20 | Replicar escenario: inspección de ductos (Uali) 		| P0 | [ ] | | Múltiples drones, rutas paralelas |
| 8.21 | Replicar escenario: búsqueda y rescate (Ministerio) 	| P0 | [ ] | | Grid search, múltiples fuerzas |
| 8.22 | Validar prevención de colisión en 50km虏 				| P0 | [ ] | | Densidad realista |
| 8.23 | Documentar resultados de validación 					| P1 | [ ] | | Reporte ejecutivo |

### Tareas de Cobertura y Calidad

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 8.24 | Configurar cobertura de código (Python) 		| P1 | [ ] | | `pytest-cov` |
| 8.25 | Configurar cobertura de código (TypeScript) 	| P1 | [ ] | | `jest --coverage` |
| 8.26 | Alcanzar >80% cobertura en ambos lenguajes 	| P1 | [ ] | | Excluir tests/
| 8.27 | Configurar quality gate en CI 					| P1 | [ ] | | No mergear si <80% |
| 8.28 | Crear reporte de cobertura visual 				| P2 | [ ] | | Badge en README |

### Checklist de Cierre Fase 8

- [ ] **Compilación:** Pipeline CI ejecuta todo el suite en <10 minutos
- [ ] **Tests unitarios:**
  - [ ] Suite completo de integración (mínimo 50 casos)
  - [ ] Tests E2E pasan en Chrome y Firefox
  - [ ] Tests de carga: 500 drones sostenidos por 30 min
  - [ ] Tests de caos: sistema recupera en <60 segundos
- [ ] **Documentación:** `docs/08-testing.md` con estrategia y reportes de cobertura
- [ ] **Punto de restauración:** Tag `v0.8.0-testing` creado y pusheado

---

## FASE 9: Empaquetamiento y Despliegue

**Duración estimada:** 3-4 días  
**Tag objetivo:** `v1.0.0-rc1`  
**Requisito crítico:** Instalación en 30 minutos por técnico de cliente

### Tareas de Optimización

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 9.1 | Optimizar imágenes Docker (multi-stage builds) 	| P1 | [ ] | | Imágenes <100MB |
| 9.2 | Minimizar dependencias de producción 			| P1 | [ ] | | Solo lo necesario |
| 9.3 | Implementar .dockerignore eficiente 			| P1 | [ ] | | Excluir dev files |
| 9.4 | Comprimir assets estáticos 						| P2 | [ ] | | Gzip/brotli |

### Tareas de Kubernetes y Orquestación

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 9.5 | Crear Helm charts básicos 					| P2 | [ ] | | `infrastructure/helm/` |
| 9.6 | Definir deployments, services, ingress 		| P2 | [ ] | | K8s manifests |
| 9.7 | Configurar HPA (auto-scaling) 				| P2 | [ ] | | Basado en CPU/latencia |
| 9.8 | Crear configmaps y secrets 					| P1 | [ ] | | Separar config de código |

### Tareas de Instalación On-Premise

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 9.9 | Crear `install.ps1` para Windows Server 		| P0 | [ ] | | Clientes con Windows |
| 9.10 | Crear `install.sh` para Linux 					| P0 | [ ] | | Servidores cloud |
| 9.11 | Implementar verificación de prerequisitos 		| P0 | [ ] | | Docker, puertos, RAM |
| 9.12 | Crear wizard de configuración inicial 			| P1 | [ ] | | Preguntas interactivas |
| 9.13 | Generar certificados SSL automáticamente 		| P1 | [ ] | | Let's Encrypt o self-signed |
| 9.14 | Crear script de desinstalación limpia 			| P1 | [ ] | | Backup antes de borrar |

### Tareas de Configuración y Ambientes

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 9.15 | Crear configs: `dev`, `staging`, `prod` 		| P1 | [ ] | | `config/` |
| 9.16 | Implementar configuración por cliente 			| P1 | [ ] | | Uali, Ministerio, genérico |
| 9.17 | Crear variables de entorno documentadas 		| P1 | [ ] | | `.env.example` completo |
| 9.18 | Implementar feature flags 						| P2 | [ ] | | Activar/desactivar funciones |

### Tareas de Backup y Licenciamiento

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 9.19 | Implementar backup automático de BD 			| P1 | [ ] | | Diario, retención 30 días |
| 9.20 | Crear script de restore de backup 				| P1 | [ ] | | Verificado |
| 9.21 | Implementar sistema de licencias 				| P2 | [ ] | | Por número de drones |
| 9.22 | Crear validación de licencia en startup 		| P2 | [ ] | | No arrancar sin licencia válida |
| 9.23 | Implementar heartbeat de licencia 				| P2 | [ ] | | Verificación online |

### Tareas de Release

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 9.24 | Automatizar changelog desde commits 			| P1 | [ ] | | `conventional-changelog` |
| 9.25 | Crear GitHub Release con artifacts 			| P1 | [ ] | | Binarios, Docker images |
| 9.26 | Publicar imágenes a Docker Hub (privado) 		| P1 | [ ] | | Registry |
| 9.27 | Crear release notes detallados 				| P1 | [ ] | | Features, bugfixes, breaking |
| 9.28 | Versionar documentación con código 			| P1 | [ ] | | Mismo tag |

### Checklist de Cierre Fase 9

- [ ] **Compilación:** Release automático en GitHub con artifacts
- [ ] **Tests unitarios:**
  - [ ] Tests de instalación (script en VM limpia)
  - [ ] Tests de upgrade (v0.x 鈫?v1.0)
  - [ ] Tests de rollback (volver a versión anterior)
  - [ ] Tests de backup/restore
- [ ] **Documentación:** `docs/09-deployment.md` con guías de instalación y rollback
- [ ] **Punto de restauración:** Tag `v1.0.0-rc1` creado y pusheado (Release Candidate)

---

## FASE 10: Documentación Final

**Duración estimada:** 2-3 días  
**Tag objetivo:** `v1.0.0`  
**Requisito crítico:** Desarrollador externo contribuye en <1 hora de lectura

### Tareas de Documentación de Usuario

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 10.1 | Crear guía de usuario para operadores 			| P0 | [ ] | | PDF y online |
| 10.2 | Documentar flujo de planificación de vuelo 	| P0 | [ ] | | Paso a paso con screenshots |
| 10.3 | Documentar flujo de monitoreo en tiempo real 	| P0 | [ ] | | Dashboard, alertas |
| 10.4 | Crear guía de troubleshooting para operadores 	| P1 | [ ] | | FAQ, problemas comunes |
| 10.5 | Documentar procedimientos de emergencia 		| P0 | [ ] | | Conflicto, pérdida de señal |

### Tareas de Documentación de Administrador

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 10.6 | Crear guía de instalación y configuración 		| P0 | [ ] | | Para técnicos de cliente |
| 10.7 | Documentar mantenimiento del sistema 			| P1 | [ ] | | Updates, backups, monitoreo |
| 10.8 | Crear guía de troubleshooting técnico 			| P1 | [ ] | | Logs, métricas, debug |
| 10.9 | Documentar integración con sistemas externos 	| P1 | [ ] | | EANA, ANAC, otros |
| 10.10 | Crear runbooks de incidentes 					| P1 | [ ] | | Pasos detallados |

### Tareas de Documentación Técnica y API

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 10.11 | Publicar OpenAPI/Swagger completo 			| P0 | [ ] | | Swagger UI accesible |
| 10.12 | Crear ejemplos de código (Python, JS, cURL) 	| P1 | [ ] | | Snippets funcionales |
| 10.13 | Documentar webhooks y eventos 				| P1 | [ ] | | Formatos, retry logic |
| 10.14 | Crear guía de contribución (CONTRIBUTING.md) 	| P1 | [ ] | | Cómo reportar bugs, PRs |
| 10.15 | Documentar arquitectura de decisiones (ADRs) 	| P1 | [ ] | | Por qué FastAPI, por qué PostgreSQL |

### Tareas de Presentación y Marketing

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 10.16 | Crear video demostrativo (5 min) 					| P1 | [ ] | | Screencast de flujo completo |
| 10.17 | Diseñar presentación para stakeholders 			| P1 | [ ] | | Pitch para Uali/Ministerio |
| 10.18 | Crear one-pager técnico 							| P1 | [ ] | | Arquitectura, beneficios |
| 10.19 | Preparar demo live para ANAC 						| P2 | [ ] | | Cumplimiento normativo |
| 10.20 | Crear case study de Vaca Muerta 					| P2 | [ ] | | ROI, prevención de colisiones |

### Tareas de Sitio de Documentación

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 10.21 | Setup MkDocs o similar 						| P1 | [ ] | | Static site generator |
| 10.22 | Organizar documentación navegable 			| P1 | [ ] | | Estructura clara |
| 10.23 | Desplegar en GitHub Pages 					| P1 | [ ] | | docs.dronesystem.ar |
| 10.24 | Configurar búsqueda en documentación 			| P2 | [ ] | | Algolia o local |
| 10.25 | Implementar versioning de docs 				| P2 | [ ] | | v1.0, v1.1, etc. |

### Tareas de README y Repositorio

| ID | Tarea | Prioridad | Estado | Asignado | Notas |
|----|-------|-----------|--------|----------|-------|
| 10.26 | Escribir README.md principal completo 			| P0 | [ ] | | Quick start, arquitectura, badges |
| 10.27 | Agregar badges de CI, cobertura, versión 			| P1 | [ ] | | Shields.io |
| 10.28 | Crear LICENSE.md 									| P1 | [ ] | | Propietario o open source |
| 10.29 | Crear CODE_OF_CONDUCT.md 							| P2 | [ ] | | Comunidad |
| 10.30 | Crear SECURITY.md 								| P1 | [ ] | | Cómo reportar vulnerabilidades |

### Checklist de Cierre Fase 10

- [ ] **Compilación:** Docs site generado y desplegado en GitHub Pages
- [ ] **Tests unitarios:**
  - [ ] Validación de ejemplos en documentación (doctests)
  - [ ] Links rotos verificados (`markdown-link-check`)
  - [ ] Ortografía y gramática (LanguageTool)
- [ ] **Documentación:** `docs/README.md` como índice master completo
- [ ] **Punto de restauración:** Tag `v1.0.0` creado y pusheado (Primera versión estable)

---

## 馃搳 Resumen de Fases

| Fase | Nombre | Duración | Tag | Estado Global |
|------|--------|----------|-----|---------------|
| 0 | Infraestructura 			| 2-3 días | v0.0.1-infra 		| [ ] |
| 1 | Modelos de Datos 			| 3-4 días | v0.1.0-data 		| [ ] |
| 2 | Edge Gateway Core 		| 5-7 días | v0.2.0-edge-core 	| [ ] |
| 3 | Cloud Platform Core 		| 5-7 días | v0.3.0-cloud-core 	| [ ] |
| 4 | Simulador 				| 3-4 días | v0.4.0-simulator 	| [ ] |
| 5 | Integración 				| 4-5 días | v0.5.0-integration | [ ] |
| 6 | Seguridad 				| 4-5 días | v0.6.0-security 	| [ ] |
| 7 | Monitoreo 				| 3-4 días | v0.7.0-monitoring 	| [ ] |
| 8 | Testing E2E 				| 4-5 días | v0.8.0-testing 	| [ ] |
| 9 | Despliegue 				| 3-4 días | v1.0.0-rc1 		| [ ] |
| 10 | Documentación 			| 2-3 días | **v1.0.0** 		| [ ] |
| **TOTAL** 		   			| **38-51 días**	  			| 	  |

---

## 馃攧 Proceso de Cierre de Fase

Para cada fase, crear un Pull Request con este template:

```markdown
## Fase X: [Nombre]

### Checklist de Cierre

#### Compilación
- [ ] Python: `py_compile` sin errores
- [ ] TypeScript: `tsc --noEmit` sin errores
- [ ] Docker: `docker build` exitoso en todos los servicios

#### Tests Unitarios
- [ ] Cobertura >70% en código nuevo
- [ ] Todos los tests pasan (`pytest`, `jest`)
- [ ] Tests de regresión pasan

#### Documentación
- [ ] `docs/0X-fase.md` creado y completo
- [ ] API endpoints documentados (Swagger)
- [ ] Decisiones técnicas registradas (ADRs)
- [ ] README actualizado si aplica

#### Punto de Restauración
- [ ] Tag creado: `git tag -a vX.Y.Z -m "Fase X: Descripción"`
- [ ] Tag pusheado: `git push origin vX.Y.Z`
- [ ] Release notes en GitHub
```

---

## 馃摑 Notas de Uso

### Agregar Nueva Tarea
1. Buscar la fase correspondiente
2. Asignar ID secuencial (ej: 2.21, 2.22)
3. Definir prioridad (P0-P3)
4. Estado inicial: `[ ]`
5. Agregar notas si es necesario

### Mover Tarea entre Fases
- No recomendado una vez iniciada la fase
- Si es crítico, documentar en notas el cambio

### Completar Fase
1. Verificar checklist de cierre completo
2. Ejecutar script de validación
3. Crear tag de Git
4. Actualizar este archivo (marcar fase como completada)
5. Mergear a `main`

---

**Última actualización:** 2026-03-04  
**Responsable de mantenimiento:** [Por definir]  
**Próxima revisión:** Al completar Fase 0
