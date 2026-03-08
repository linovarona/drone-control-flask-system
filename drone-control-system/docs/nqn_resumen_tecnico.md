# DOCUMENTO TÉCNICO RESUMEN: SISTEMA DE CONTROL AÉREO PARA DRONES - NEUQUÉN

## VISIÓN GENERAL DEL PROYECTO

**Objetivo:** Desarrollar un servicio de control aéreo para drones (Proveedor de Servicios U-space) en la provincia de Neuquén, Argentina, con capacidad de monitoreo en tiempo real, alertas de conflicto y respuesta activa mediante drones de patrullaje.

**Alcance Geográfico:** Región de Vaca Muerta (epicentro en Añelo), zona de alta actividad con drones industriales (YPF, Shell, PAE), gubernamentales (Ministerio de Seguridad de Neuquén) y servicios comerciales locales.

**Componente Innovador:** Incorporación de un "dron de patrullaje" con capacidad de intercepción y neutralización de amenazas (drones que violen geocercas o normas de vuelo).

---

## ARQUITECTURA TÉCNICA POR CAPAS

### CAPA 1: SIMULACIÓN Y DESARROLLO DE ALGORITMOS

**Propósito:** 
Modelar el comportamiento de múltiples drones en el espacio aéreo de Neuquén 
Desarrollar los algoritmos centrales del sistema sin riesgo operativo.

| Componente 
-| Implementación 
--| Función Específica |
|:---|:---|:---|
| **UavNetSim-v1** 
-| Plataforma de simulación de redes de UAV 
--| Modelar escenario de Vaca Muerta con topología real (coordenadas, terreno, obstáculos). 
---Simular hasta 20 drones simultáneos de diferentes operadores (YPF, gobierno, servicios). |

| **gym-pybullet-drones** 
-| Entorno de simulación física con PyBullet 
--| Entrenar y validar algoritmos de control para el dron de patrullaje. 
---Simular dinámicas de vuelo realistas con modelos de cuadrotores. |

| **uav-collision-avoidance** 
-| Módulo de detección geométrica 
--| Implementar algoritmo de "deconflicción" 
---que detecte trayectorias de colisión y genere alertas tempranas. 
---Basado en enfoque geométrico con predicción a 5 segundos. |

| **FLighthouse** 
-| Framework de guiado multi-agente 
--| Desarrollar lógica de coordinación entre el sistema central y los drones de patrullaje. 
---Planificación de rutas de intercepción. |

**Métricas de Validación en Simulación:**
- Tasa de detección de conflictos: > 99%
- Falsas alarmas: < 1%
- Tiempo de respuesta del dron de patrullaje: < 30 segundos desde la alerta
- Capacidad de procesamiento: 20+ drones en tiempo real

---

### CAPA 2: COMUNICACIÓN Y CONTROL DE DRONES REALES

**Propósito:** 
Establecer el puente entre el sistema de control y los drones físicos que operarán en Neuquén, 
utilizando protocolos estándar de la industria.

|:---|:---|:---|

| **Zenmav** 
-| Biblioteca Python de alto nivel para Ardupilot 	
--| API unificada para: 
---conexión a drones (SITL/reales), 
---navegación por waypoints GPS, 
---control de velocidad, 
---patrones de escaneo, 
---retorno automático (RTL). |

| **LeafSDK** 
-| SDK con capa MAVLink 
--| Control de bajo nivel: 
---planificación de misiones con condicionales, 
---control de gimbal, 
---aterrizaje por visión con marcadores ArUco. |

| **DroneKit-Python + pymavlink** 
-| Stack fundamental de comunicación 
--| Base para toda comunicación con autopilotos (ArduPilot/PX4). 
---Telemetría en tiempo real, 
---envío de comandos, 
---monitoreo de estado. |

| **MAVLink Protocol**
-| Estándar de comunicación 
--| Lenguaje común entre estación ground y drones.
--- Soporta heartbeat, GPS, actitud, waypoints, comandos de misión. |

**Arquitectura de Comunicación:**
[Sistema Central] ←→ [MAVLink Router] ←→ [Drones Comerciales]
↕
[Estaciones Ground GCS]
↕
[Dron de Patrullaje]

**Requisitos Técnicos:**
- Frecuencias: 2.4 GHz (control) / 5.8 GHz (video)
- Enlace de datos: Telemetría cada 100ms mínimo
- Redundancia: Múltiples estaciones ground en puntos estratégicos de Vaca Muerta
- Seguridad: Encriptación de comandos para evitar interferencias maliciosas

---

### CAPA 3: GEOCERCAS, COORDENADAS Y PROCESAMIENTO ESPACIAL

**Propósito:** 
Implementar la lógica de "espacio aéreo digital" que define dónde, cuándo y a qué altura pueden volar los drones, generando alertas automáticas ante violaciones.

|:---|:---|:---|

| **PyProj** 
-| Transformaciones de coordenadas PROJ 
--| Conversión precisa entre WGS84 (lat/lon) y sistemas locales (UTM zona 19S, coordenadas planas para cálculos de distancia). |

| **Shapely** 
-| Geometría espacial 
--| Implementación de geocercas como polígonos. 
---Algoritmo de ray casting para detección de intrusión (punto en polígono). 
---Cálculo de distancias mínimas a zonas restringidas. |

| **GeoPandas** 
-| Extensiones geoespaciales 
--| Manejo de datasets geográficos de Neuquén 
---(límites de yacimientos, áreas urbanas, infraestructura crítica). 
---Operaciones espaciales optimizadas. |

| **Filtros de Kalman (filterpy)** 
-| Fusión sensorial 
--| Estimación robusta de posición fusionando GPS, IMU, barómetro. 
---Reducción de ruido y outliers en telemetría. |

**Estructura de Datos de Geocercas:**

| Tipo de Zona 		| Ejemplo Neuquén 		| AltitudMx | Prioridad | Acción ante Violación 			|
|:------------------|:----------------------|:----------|:----------|:----------------------------------|
| **Prohibida** 	| Aeropuerto Añelo 		| 0 m 		| Crítica 	| Alerta inmediata + intercepción 	|
| **Restringida** 	| Casco urbano Añelo 	| 120 m 	| Alta 		| Alerta + registro 				|
| **Operacional**	| Yacimiento Llancanelo | 400 m 	| Media 	| Monitoreo 						|
| **Temporal**		| Eventos/Incendios 	| Variable 	| Variable 	| Alerta dinámica 					|

**Algoritmo de Detección (Pseudocódigo):**
```python
def monitorear_posiciones(drones, geocercas):
    for dron in drones:
        punto = Point(dron.lon, dron.lat)
        for zona in geocercas:
            if zona.poligono.contains(punto):
                if dron.altitud > zona.altitud_max:
                    generar_alerta("ALTITUD_EXCEDIDA", dron, zona)
                if zona.tipo == "PROHIBIDA":
                    activar_patrullaje(dron)
            else:
                # Predecir trayectoria para alerta temprana
                if zona.poligono.distance(punto) < UMBRAL_SEGURIDAD:
                    trayectoria = predecir_posicion(dron, t=5)
                    if zona.poligono.contains(trayectoria):
                        generar_alerta("APROXIMACION_RIESGO", dron, zona)
						
```						
### CAPA 4: SERVICIOS U-SPACE Y BACKEND
**Propósito:** 
Construir la plataforma central que integra todas las capacidades anteriores, 
ofrece interfaces de usuario y se conecta con los sistemas regulatorios (ANAC/EANA).

-Flask (Backend API)	
--Python microframework	
---API RESTful para: 
----registro de operadores, 
----planificación de vuelos, 
----consulta de geocercas, 
----streaming de telemetría,
----gestión de alertas.

-Node.js + Leaflet (Frontend)	
--JavaScript + mapas interactivos	
---Dashboard de control: 
----visualización de todos los drones en tiempo real, 
----superposición de geocercas, 
----panel de alertas, 
----video streaming del dron de patrullaje.

-BlueSky Open Air Traffic Simulator	
--Simulador de tráfico aéreo	
---Validación final del sistema integrado con tráfico tripulado simulado (aviones, helicópteros que operan en la región).
-PostgreSQL + PostGIS	
--Base de datos espacial	
---Almacenamiento de: 
----vuelos históricos, 
----incidentes, 
----operadores, 
----geocercas dinámicas, 
----métricas de rendimiento.

Endpoints Críticos de la API:
Endpoint				Método		Función
/api/v1/flight/plan		POST		Registrar plan de vuelo, validar contra geocercas
/api/v1/flight/track	GET			Obtener posición de todos los drones activos
/api/v1/alert/subscribe	WebSocket	Streaming de alertas en tiempo real
/api/v1/patrol/dispatch	POST		Ordenar intercepción a dron de patrullaje
/api/v1/geofence/list	GET			Obtener geocercas activas (para apps de pilotos)

Integración con Entidades Regulatorias:
-ANAC: 
--Conexión con sistema PDSA (Proveedor de Servicio Digital de Autorización) para validación de permisos de vuelo.
-EANA: 
--Interfaz con control de tráfico aéreo tradicional para operaciones cerca de aeropuertos.
-Ministerio de Seguridad Neuquén: Feed de datos de su flota de 24 drones para coordinación en emergencias.

FLUJO DE TRABAJO INTEGRADO
┌─────────────────────────────────────────────────────────────────┐
│                    ENTRADA DE DATOS                             │
│  - Telemetría en tiempo real (MAVLink)                          │
│  - Planes de vuelo registrados                                  │
│  - Geocercas estáticas + dinámicas                              │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    CAPA 3: PROCESAMIENTO ESPACIAL               │
│  - Fusión de sensores (Kalman)                                  │
│  - Verificación de geocercas (Shapely)                          │
│  - Predicción de trayectorias                                   │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    DETECCIÓN DE EVENTOS                         │
│  ¿Violación de geocerca? → Alerta tipo 1                        │
│  ¿Riesgo de colisión? → Alerta tipo 2                           │
│  ¿Intruso no autorizado? → Alerta tipo 3                        │
└───────────────────────────────┬─────────────────────────────────┘
                                ↓
┌─────────────────────────────────────────────────────────────────┐
│                    RESPUESTA                                    │
│  - Notificación en dashboard                                    │
│  - Alerta al operador del dron infractor                        │
│  - SI alerta tipo 3 → ACTIVAR DRON DE PATRULLAJE                │
│      • Calcular punto de intercepción óptimo                    │
│      • Navegar a posición del intruso                           │
│      • Desplegar red de captura / interferencia                 │
└─────────────────────────────────────────────────────────────────┘


ESPECIFICACIONES TÉCNICAS DEL DRON DE PATRULLAJE
Parámetro			Especificación									Justificación
Tipo				Multirrotor de 6 hélices						Mayor estabilidad y capacidad de carga
Velocidad máxima	25 m/s (90 km/h)								Superar a drones comerciales típicos (15-20 m/s)
Autonomía			30 minutos										Suficiente para patrullaje + intercepción
Sensores			Cámara 360°, LiDAR, detector RF					Detección visual + electrónica
Método de 
neutralización		Red de captura (primario) / 
					Interferencia RF (secundario)					Captura física evita caídas descontroladas
Base				Estación de acoplamiento automática 			Despliegue rápido 24/7
					(ej: DJI Dock)	
Comunicación		Enlace dual: 2.4 GHz control + 4G/5G respaldo	Redundancia crítica

PLAN DE IMPLEMENTACIÓN POR FASES
Fase						Duración	Actividades			
Entregables
FASE 1: 
-Simulación					3-4 meses	- Configurar UavNetSim-v1 con escenario Neuquén
										- Desarrollar algoritmos de detección
										- Validar en entorno virtual	
 Modelo validado en simulación
 Algoritmos base documentados
 
FASE 2: 
-Prototipo Software			4-6 meses	- Implementar backend Flask
										- Desarrollar frontend Leaflet
										- Integrar geocercas con PyProj/Shapely	
 Plataforma funcional con datos simulados
 
FASE 3: 
-Integración con Hardware	3-4 meses	- Adaptar Zenmav/LeafSDK
										- Pruebas SITL con drones virtuales
										- Configurar estaciones ground	
 Conexión exitosa con drones simulados
 
FASE 4: 
-Piloto Controlado			3 meses		- Pruebas con 1 dron real en zona autorizada
										- Validar alertas y respuesta
										- Ajustar algoritmos	
 Informe de validación
 Métricas de rendimiento real
 
FASE 5: 
Despliegue Neuquén			Continuo	- Registro PDSA ante ANAC
										- Alianza con operadores locales
										- Operación gradual en Vaca Muerta	
 Servicio comercial operativo
 

RECOMENDACIÓN ESTRATÉGICA PARA EL DISEÑO:

Comienzar con UavNetSim-v1 : 
-Es el más completo para simular redes de drones y probar algoritmos de control. 
-Incluye 
--modelos de movilidad 3D, 
--planificación de rutas (A*), 
--y visualización de trayectorias. 
-Ideal para simular el espacio aéreo de Vaca Muerta con múltiples operadores.

Para el dron de patrullaje, utiliza Zenmav  o LeafSDK . 
-Ambas bibliotecas te permitirán:
--Conectar con simuladores (SITL) para pruebas sin riesgo
--Programar misiones autónomas (patrullaje por waypoints)
--Controlar el dron en tiempo real cuando detecte una amenaza
--Implementar lógica de respuesta (intercepción, toma de imágenes)
--Para las geocercas y alertas, combina PyProj + Shapely :

```	python
from pyproj import Proj, transform
from shapely.geometry import Point, Polygon

# Definir geocerca (ej: zona prohibida alrededor de aeropuerto)
geocerca = Polygon([(lon1,lat1), (lon2,lat2), ...])

# Obtener posición del dron (de telemetría MAVLink)
posicion_dron = Point(longitud, latitud)

# Verificar violación
if geocerca.contains(posicion_dron):
    generar_alerta("VIOLACIóN_ESPACIO_AéREO", dron_id)
```	

Para la interfaz de visualización, 
--el stack Flask + Leaflet  
---ha sido validado en proyectos U-space reales (ENAC-Airbus). 
---Te permitirá mostrar:
----Posición de todos los drones en tiempo real
----Geocercas activas
----Alertas de colisión/violación
----Video en streaming del dron de patrullaje







REQUERIMIENTOS DE RECURSOS
Recurso				Mínimo (Fase 1-2)					Óptimo (Fase 3-5)
Equipo humano		Fundador + 1 desarrollador senior	+1 systems engineer + asesor regulatorio
Infraestructura		Servidores cloud (AWS/GCP) + estaciones de desarrollo	+ estaciones ground en Neuquén + drones de prueba
Software			Stack Python open source	+ licencias MATLAB (opcional)
Presupuesto mensual estimado	USD 4.000 - 5.000				USD 10.000 - 15.000


RIESGOS TÉCNICOS Y MITIGACIONES
Riesgo								Probabilidad	Impacto		Mitigación
Regulación BVLOS no disponible		Alta			Alto		Diseñar sistema para VLOS inicial; participar 																 activamente con ANAC en pilotos
Interferencia de comunicaciones		Media			Alto		Diseño con redundancia (RF + 4G/5G) y espectro 																  diverso
Falsas alarmas						Media			Medio		Validación extensiva en simulación; umbrales 																calibrados
Fallo del dron de patrullaje		Baja			Alto		Sistema manual de respaldo; múltiples unidades
Ciberseguridad						Media			Alto		Encriptación de comandos; autenticación fuerte			

CONCLUSIÓN
El sistema propuesto integra cuatro capas técnicas que cubren todo el ciclo de vida del servicio: 
desde la simulación inicial en UavNetSim-v1 hasta la operación real con drones en Vaca Muerta, 
pasando por comunicación robusta con MAVLink/Zenmav, procesamiento espacial preciso con PyProj/Shapely, y una plataforma U-space completa con Flask/Leaflet.

La arquitectura por capas permite:
-Desarrollo incremental (empezar con simulación, agregar complejidad gradualmente)
-Validación continua (cada capa se prueba independientemente)
-Escalabilidad (capacidad de crecer a otras provincias)
-Adaptabilidad regulatoria (diseño preparado para cuando ANAC habilite BVLOS)

Próximo paso inmediato: Configurar UavNetSim-v1 con coordenadas de Neuquén e iniciar simulación de escenarios base con 3-5 drones.