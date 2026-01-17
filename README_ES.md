# 🦆 Patito Viajes

Una poderosa herramienta de automatización para planificación de viajes que combina automatización de flujos de trabajo n8n con una interfaz Streamlit para ayudarte a descubrir y planificar tu viaje perfecto.

Español | [English](README.md)

## 📋 Descripción General

Patito Viajes es un asistente inteligente de planificación de viajes que aprovecha la IA y múltiples fuentes de datos para proporcionar información completa sobre viajes. El sistema extrae datos en tiempo real de:

- ✈️ **Google Flights** - Opciones de vuelos y precios
- 🏨 **Google Hotels** - Opciones de alojamiento y tarifas
- 🎯 **Actividades y Atracciones** - Cosas que hacer en tu destino usando recomendaciones de IA

Toda la extracción de datos está impulsada por el **nodo oficial de SerpAPI para n8n**, garantizando datos confiables y estructurados de los resultados de búsqueda de Google.

## 🏗️ Arquitectura

El sistema consta de dos componentes principales:

### 1. Backend de Flujo de Trabajo n8n
- **Propósito**: Motor de extracción y procesamiento de datos
- **Tecnología**: n8n (plataforma de automatización de flujos de trabajo)
- **Integración**: Nodo oficial de SerpAPI para n8n
- **Funciones**:
  - Recibe solicitudes de búsqueda de viajes
  - Consulta Google Flights a través de SerpAPI
  - Consulta Google Hotels a través de SerpAPI
  - Consulta actividades y atracciones usando Modo IA
  - Agrega y procesa resultados
  - Devuelve datos estructurados al frontend

### 2. Frontend Streamlit
- **Propósito**: Interfaz de usuario para planificación de viajes
- **Tecnología**: Streamlit (framework web de Python)
- **Funciones**:
  - Recopila preferencias de viaje del usuario (destino, fechas, presupuesto)
  - Envía solicitudes al flujo de trabajo n8n
  - Muestra resultados de búsqueda en una interfaz intuitiva
  - Permite comparación de vuelos y hoteles
  - Muestra actividades recomendadas

### Flujo de Datos

```
Entrada del Usuario (Streamlit)
    ↓
Solicitud de Búsqueda de Viaje
    ↓
Orquestación del Flujo de Trabajo n8n
    ↓
├── SerpAPI: Google Flights
├── SerpAPI: Google Hotels
└── SerpAPI: Actividades (Modo IA)
    ↓
Agregación y Procesamiento de Datos
    ↓
Visualización de Resultados (Streamlit)
```

## 🎨 Notas de Diseño

### Diseño del Flujo de Trabajo n8n

El flujo de trabajo n8n está diseñado con modularidad y confiabilidad en mente:

1. **Nodo de Validación de Entrada**: Valida los parámetros de viaje entrantes (destino, fechas, número de pasajeros)
2. **Procesamiento Paralelo**: Las búsquedas de vuelos, hoteles y actividades se ejecutan en paralelo para mejor rendimiento
3. **Manejo de Errores**: Cada llamada API incluye lógica de reintento y mecanismos de respaldo
4. **Transformación de Datos**: Las respuestas crudas de SerpAPI se transforman en un formato unificado
5. **Agregación de Respuestas**: Los resultados se combinan en una respuesta estructurada única

### Integración con SerpAPI

- Utiliza el nodo oficial de SerpAPI para n8n para mayor confiabilidad
- Configurado con parámetros de búsqueda apropiados para cada servicio:
  - **Vuelos**: Aeropuertos de salida/llegada, fechas, número de pasajeros, clase
  - **Hoteles**: Ubicación, fechas de check-in/out, huéspedes, filtros (precio, calificación)
  - **Actividades**: Consultas basadas en ubicación con Modo IA para recomendaciones contextuales

### Diseño del Frontend Streamlit

- **Interfaz Limpia**: Diseño minimalista enfocado en la experiencia del usuario
- **Revelación Progresiva**: Opciones avanzadas ocultas hasta que se necesiten
- **Actualizaciones en Tiempo Real**: Indicadores de carga durante llamadas API
- **Diseño Responsivo**: Funciona en dispositivos de escritorio y tableta
- **Visualización de Resultados**: Tarjetas, tablas y gráficos para fácil comparación

## 📦 Requisitos Previos

Antes de desplegar Patito Viajes, asegúrate de tener:

- **Python 3.8+** (para el frontend Streamlit)
- **Instancia de n8n** (auto-hospedada o en la nube)
- **Cuenta de SerpAPI** con clave API ([Obtén una aquí](https://serpapi.com/))
- **Docker** (opcional, para despliegue en contenedores)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/tecncr/patito-viajes.git
cd patito-viajes
```

### 2. Configurar el Flujo de Trabajo n8n

#### Opción A: n8n Cloud
1. Inicia sesión en tu cuenta de n8n cloud
2. Importa el archivo JSON del flujo de trabajo: `workflow/patito-viajes-workflow.json`
3. Configura las credenciales de SerpAPI en n8n
4. Activa el flujo de trabajo
5. Anota la URL del webhook para la aplicación Streamlit

#### Opción B: n8n Auto-hospedado
1. Instala n8n:
   ```bash
   npm install -g n8n
   ```

2. Inicia n8n:
   ```bash
   n8n start
   ```

3. Accede a n8n en `http://localhost:5678`
4. Importa el flujo de trabajo: `workflow/patito-viajes-workflow.json`
5. Configura las credenciales de SerpAPI
6. Activa el flujo de trabajo

### 3. Configurar el Frontend Streamlit

1. Crea un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

2. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```

3. Configura las variables de entorno:
   ```bash
   cp .env.example .env
   ```
   
   Edita `.env` y agrega:
   ```
   N8N_WEBHOOK_URL=https://tu-instancia-de-n8n.com/webhook/patito-viajes
   SERPAPI_KEY=tu_clave_serpapi
   ```

## ⚙️ Configuración

### Configuración de SerpAPI

1. Regístrate en [SerpAPI](https://serpapi.com/)
2. Obtén tu clave API desde el panel de control
3. Agrega la clave API a las credenciales de n8n:
   - Ve a **Credentials** → **New**
   - Selecciona **SerpAPI**
   - Ingresa tu clave API
   - Guarda como "SerpAPI Patito Viajes"

### Configuración del Flujo de Trabajo n8n

Abre el flujo de trabajo en n8n y configura:

1. **Nodos SerpAPI**: Vincula con tus credenciales de SerpAPI
2. **Nodo Webhook**: Establece autenticación si es necesario
3. **Nodo de Respuesta**: Asegura el formato adecuado de datos
4. **Manejo de Errores**: Configura las preferencias de notificación

### Configuración de Streamlit

El archivo `.env` controla la configuración de la aplicación Streamlit:

```env
# Configuración de n8n
N8N_WEBHOOK_URL=https://tu-instancia-de-n8n.com/webhook/patito-viajes

# Configuración de SerpAPI (si se llama directamente)
SERPAPI_KEY=tu_clave_serpapi

# Configuración de la Aplicación
APP_TITLE=Patito Viajes
DEFAULT_CURRENCY=USD
RESULTS_PER_PAGE=10
```

## 🌐 Despliegue

### Despliegue Local

1. Inicia n8n (si es auto-hospedado):
   ```bash
   n8n start
   ```

2. Inicia Streamlit:
   ```bash
   streamlit run app.py
   ```

3. Accede a la aplicación en `http://localhost:8501`

### Despliegue con Docker

1. Construye la imagen Docker:
   ```bash
   docker build -t patito-viajes .
   ```

2. Ejecuta el contenedor:
   ```bash
   docker run -p 8501:8501 --env-file .env patito-viajes
   ```

### Despliegue en la Nube

#### Streamlit Cloud

1. Haz un fork de este repositorio a tu cuenta de GitHub
2. Ve a [share.streamlit.io](https://share.streamlit.io)
3. Despliega tu fork
4. Agrega las variables de entorno en la configuración de Streamlit Cloud

#### Heroku

1. Instala Heroku CLI
2. Crea una nueva aplicación Heroku:
   ```bash
   heroku create patito-viajes
   ```

3. Establece las variables de entorno:
   ```bash
   heroku config:set N8N_WEBHOOK_URL=tu_url_webhook
   ```

4. Despliega:
   ```bash
   git push heroku main
   ```

#### Railway

1. Conecta tu repositorio de GitHub a Railway
2. Agrega las variables de entorno en el panel de Railway
3. Despliega automáticamente al hacer push

## 📖 Uso

1. **Abre la Aplicación Streamlit**: Navega a tu URL desplegada o `localhost:8501`

2. **Ingresa los Detalles del Viaje**:
   - Ciudad de destino o código de aeropuerto
   - Ciudad de salida o código de aeropuerto
   - Fechas de viaje (salida y regreso)
   - Número de pasajeros
   - Preferencias de presupuesto (opcional)

3. **Buscar**: Haz clic en "Encontrar Mi Viaje" para iniciar la búsqueda

4. **Ver Resultados**:
   - **Pestaña Vuelos**: Compara opciones de vuelos, precios y duraciones
   - **Pestaña Hoteles**: Explora opciones de alojamiento con calificaciones y precios
   - **Pestaña Actividades**: Descubre cosas que hacer en tu destino

5. **Exportar Resultados**: Descarga los resultados como PDF o comparte el enlace

## 📁 Estructura del Proyecto

```
patito-viajes/
├── workflow/
│   └── patito-viajes-workflow.json    # Definición del flujo de trabajo n8n
├── app.py                              # Aplicación principal Streamlit
├── requirements.txt                    # Dependencias Python
├── .env.example                        # Plantilla de variables de entorno
├── Dockerfile                          # Configuración Docker
├── README.md                           # Documentación en inglés
├── README_ES.md                        # Documentación en español
└── assets/
    ├── logo.png                        # Logo de la aplicación
    └── screenshots/                    # Capturas de pantalla
```

## 🔧 Desarrollo

### Ejecutar Pruebas

```bash
pytest tests/
```

### Formato de Código

```bash
black app.py
flake8 app.py
```

### Agregar Funcionalidades

La arquitectura está diseñada para ser extensible:

1. **Nuevas Fuentes de Datos**: Agrega nuevos nodos SerpAPI en el flujo de trabajo n8n
2. **Filtros Personalizados**: Extiende la barra lateral de Streamlit con filtros adicionales
3. **Formatos de Exportación**: Agrega nuevas opciones de exportación en la visualización de resultados
4. **Temas de UI**: Personaliza el tema de Streamlit en `.streamlit/config.toml`

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Por favor:

1. Haz un fork del repositorio
2. Crea una rama de funcionalidad (`git checkout -b feature/funcionalidad-increible`)
3. Confirma tus cambios (`git commit -m 'Agregar funcionalidad increíble'`)
4. Haz push a la rama (`git push origin feature/funcionalidad-increible`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT - consulta el archivo LICENSE para más detalles.

## 🙏 Reconocimientos

- **n8n** - Plataforma de automatización de flujos de trabajo
- **SerpAPI** - Proveedor de API de búsqueda de Google
- **Streamlit** - Framework web de Python
- **Google** - Fuentes de datos de vuelos, hoteles y actividades

## 📧 Soporte

Para soporte, por favor abre un issue en GitHub o contacta [code@tecncr.com](mailto:code@tecncr.com).

## 🔗 Enlaces

- [Documentación de n8n](https://docs.n8n.io/)
- [Documentación de SerpAPI](https://serpapi.com/docs)
- [Documentación de Streamlit](https://docs.streamlit.io/)

---

Hecho con ❤️ por [tecncr](https://github.com/tecncr)
