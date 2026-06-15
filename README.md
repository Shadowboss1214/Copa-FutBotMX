# Copa-FutBotMX

## Equipo: **Los más 3D** 

Integrantes:
  - **Martín Alamilla Cesar Adrian** -  [LinkedIn](https://www.linkedin.com/in/cesar-m-alamilla/) | [Github](https://github.com/CesarMartinAlamilla)
  - **Hernandez Sanchez Yovani Gabriel** - [LinkedIn](https://www.linkedin.com/in/yovanigabrielhernandezsanchez/) | [Github](https://github.com/YovaniHernandez)
  - **Salazar Bastarrachea Gael Francisco** - [LinkedIn](https://www.linkedin.com/in/gael-salazar-bastarrachea/) | [GitHub](https://github.com/Shadowboss1214)

<div style="display:flex; justify-content:center; gap:20px;">
    <img src="https://github.com/user-attachments/assets/ce3bd324-4cb5-41e9-9444-ed15a78a8d0c" alt= "Cesar Adrian" width = "250" />
    <img src="https://github.com/user-attachments/assets/8ce0ed1e-405d-45a4-89b3-3e8f1e0522ed" alt="Hernandez Yovani" width="300" />
    <img src="https://github.com/user-attachments/assets/9f3dc245-b0f9-4123-a078-c30e898df8d4" alt="Salazar Gael" width="250" />
</div>

## Agregaciones
Agregar dentro de la carpeta notebooks el modelo de SAM3


# Copa FutBotMX — Visión por Computadora

> Proyecto desarrollado para el **Capítulo Visión por Computadora** de la Copa FutBotMX, organizado por la Secretaría de Ciencia, Humanidades, Tecnología e Innovación (Secihti) en colaboración con Meta y Centro.

---

## Descripción

Este proyecto implementa un pipeline de visión por computadora para segmentar, rastrear y analizar videos de partidos de fútbol robótico de la Copa FutBotMX. Utiliza **SAM 3 (Segment Anything Model 3)** de Meta como tecnología base, combinado con **YucaBot**, un modelo de detección personalizado entrenado específicamente para reconocer robots y balones en el contexto de la competencia.

---

## Tecnologías utilizadas

| Tecnología | Rol en el pipeline |
|---|---|
| **SAM 3** (Meta AI) | Segmentación precisa con máscaras por objeto |
| **YucaBot** (YOLOv8m fine-tuned) | Detección especializada de robots y balón |
| **ByteTrack** (Supervision) | Tracking de objetos entre frames |
| **Roboflow Supervision** | Anotación, visualización y procesamiento de video |
| **OpenCV** | Lectura y manipulación de frames |

---

## YucaBot — Modelo personalizado

YucaBot es un modelo de detección de objetos basado en **YOLOv8m**, entrenado desde cero sobre un dataset propio construido específicamente para la Copa FutBotMX.

### Dataset
- **1,032 imágenes etiquetadas a mano** extraídas de múltiples videos de partidos de fútbol robótico
- Etiquetado manual realizado por el equipo, anotando cada robot y balón frame por frame
- Augmentación aplicada vía Roboflow (flip horizontal, variaciones de brillo, blur, rotación)
- Dataset final tras augmentación: **3,088 imágenes**
- División: 70% entrenamiento / 20% validación / 10% prueba
- **2 clases:** `ball`, `robot`

### Resultados del entrenamiento

| Métrica | General | `ball` | `robot` |
|---|---|---|---|
| **mAP50** | **0.978** | 0.962 | 0.994 |
| **Precisión** | 0.985 | 0.983 | 0.987 |
| **Recall** | 0.965 | 0.941 | 0.989 |
| mAP50-95 | 0.784 | 0.649 | 0.918 |

> YucaBot reconoce robots y balones con **97.8% de precisión general**, entregando su ubicación y área con alta precisión mediante bounding boxes y máscaras de segmentación. El modelo prácticamente no falla en la detección de robots (mAP50 = 0.994).

Entrenamiento realizado en Google Colab con GPU Tesla T4, 50 epochs, ~1 hora 52 minutos.

---

## Pipeline

```
Video de entrada
      ↓
YucaBot detecta robots y balón (bounding boxes)
      ↓
SAM 3 refina las detecciones con máscaras precisas
      ↓
ByteTrack asigna ID único a cada objeto entre frames
      ↓
Visualización anotada (máscaras + etiquetas + trayectorias)
      ↓
Video de salida + análisis
```

---

## Estructura del repositorio

```
futbotmx-vision/
│
├── notebooks/
│   ├── 01_exploracion.ipynb       # Análisis exploratorio de los videos
│   ├── 02_segmentacion.ipynb      # Segmentación con SAM 3 + YucaBot
│   ├── 03_tracking.ipynb          # Tracking de robots y balón
│   ├── 04_visualizacion.ipynb     # Mapas de calor, trails y dashboards
│   └── 05_pipeline_final.ipynb    # Pipeline completo integrado
│
├── src/
│   └── utils.py                   # Funciones reutilizables
│
├── assets/                        # Frames de prueba y videos de salida
├── yucabot.pt                     # Modelo personalizado entrenado
├── requirements.txt
└── README.md
```

---

## Instalación y reproducción

### Requisitos de hardware
- GPU NVIDIA con soporte CUDA 12.8+ (recomendado: RTX 3060 o superior)
- Mínimo 8 GB de VRAM
- 16 GB de RAM

### Requisitos de software
- Python 3.10+
- CUDA 12.8
- Anaconda o virtualenv

### Pasos

**1. Clonar el repositorio**
```bash
git clone https://github.com/TU_USUARIO/futbotmx-vision.git
cd futbotmx-vision
```

**2. Crear entorno virtual**
```bash
conda create -n futbotmx python=3.10
conda activate futbotmx
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Agregar archivos necesarios manualmente**

Los siguientes archivos no están incluidos en el repositorio por su tamaño y deben agregarse manualmente:
- `yucabot.pt` — modelo entrenado (solicitar al equipo)
- Videos de partidos en `VideosEjemplo/` (disponibles en el repositorio oficial de la competencia)

**5. Ejecutar el pipeline**

Abre y ejecuta los notebooks en orden:
```
01_exploracion.ipynb → 02_segmentacion.ipynb → 03_tracking.ipynb → 04_visualizacion.ipynb
```

O directamente el pipeline completo:
```
05_pipeline_final.ipynb
```

---

## Dependencias principales

```
ultralytics>=8.4.0
supervision>=0.25.0
opencv-contrib-python>=4.13.0
torch>=2.11.0
torchvision
numpy
matplotlib
roboflow
```

## Metodología e Implementación Técnica

### Entorno de Desarrollo y Ecosistema
* **Lenguaje Base:** Python 3.11.15.
* **Gestor de Entorno:** Anaconda, garantizando el aislamiento de dependencias, el control de versiones de los paquetes y la reproducibilidad del pipeline de ejecución.
* **Interfaz de Trabajo:** Jupyter Notebooks (`.ipynb`), utilizado como entorno interactivo para la experimentación modular, la visualización inmediata de fotogramas procesados y la depuración por bloques de código.
* **Librería de Gestión de Visión:** `supervision` (Roboflow). Esta librería se empleó para estandarizar el manejo de las detecciones, estructurar el flujo de las máscaras binarias y gestionar el dibujado de anotaciones sobre los videos secuenciales.

### Elementos Mapeados y Segmentados
El pipeline técnico se diseñó para detectar, delimitar y realizar el seguimiento de cuatro entidades críticas dentro de la cancha de la Copa FutBotMX:
1. **Robots:** Agentes dinámicos en constante movimiento y oclusión mutua.
2. **Pelota:** Objeto esférico de pequeña escala, caracterizado por desplazamientos de alta velocidad.


### Arquitectura de Modelos y Entrenamiento

La estrategia de visión por computadora combinó un enfoque de segmentación, avanzadon junto con un modelo de detección de objetos ajustado a un entorno personalizado.

#### 1. Segmentación y Configuración de Prompts con SAM 3
* **Modelo Utilizado:** `sam3.pt` (Segment Anything Model 3 de Meta AI).
* **Implementación:** Se aprovechó la arquitectura unificada de SAM 3 para realizar la segmentación por píxel de vocabulario abierto en los videos del torneo proporcionados por la Federación Mexicana de Robótica.
* **Estrategia de Prompts:** Se alimentó el modelo `sam3.pt` mediante prompts específicos aplicados sobre los fotogramas. Estos estímulos (ya sean puntos geométricos, cajas de delimitación o texto) guiaron al modelo para discriminar y aislar las máscaras binarias exactas correspondientes al **robot, pelota, portería y campo**, superando las variaciones físicas de iluminación y posición de las cámaras con IA. Esto generó resultados, pero no del todo completos, así que se opto seguir explorando.

#### 2. Detección de Objetos Personalizada con YOLOv8
* **Limitación del Modelo Base:** Se incorporó inicialmente el modelo ligero `yolov8n.pt` (YOLOv8 Nano) para optimizar la velocidad de inferencia en los notebooks. Sin embargo, los objetos específicos del reto de fútbol robótico no forman parte de las 80 clases estándar del dataset público COCO (Common Objects in Context).
* **Flujo de Etiquetado en Roboflow:** Para resolver esta limitación de dominio, se llevó a cabo un proceso de anotación propia. Se extrajeron fotogramas clave de las grabaciones de la cancha y se cargaron en la plataforma **Roboflow**. Ahí se ejecutó el etiquetado manual y riguroso de cajas delimitadoras (bounding boxes) para entrenar al modelo en el reconocimiento de las clases personalizadas.
* **Ajuste Fino (Fine-Tuning):** El dataset estructurado y exportado desde Roboflow se utilizó para entrenar los pesos del archivo `yolov8n.pt`, permitiendo al modelo aprender las características morfológicas particulares de los robots de la competencia, el balón y la geometría de las porterías a escala.

Instalar con:
```bash
pip install -r requirements.txt
```

---

## Resultados obtenidos

*(Agregar aquí capturas de pantalla o GIFs de los resultados una vez generados)*

---

## 📱 Reel de Instagram

*(Agregar aquí el enlace al reel publicado)*

---

## Equipo

| Nombre | Rol |
|---|---|
| *(Nombre 1)* | Describir rol |
| *(Nombre 2)* | Describir rol |
| *(Nombre 3)* | Describir rol |

---

## 📄 Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Ver archivo [LICENSE](LICENSE) para más detalles.

### Créditos y atribuciones
- **SAM 3** — Meta AI. Carion et al. (2025). "SAM 3: Segment Anything with Concepts." arXiv:2511.16719. Licencia SAM License.
- **YOLOv8** — Ultralytics. Licencia AGPL-3.0.
- **Supervision** — Roboflow. Licencia MIT.
- **ByteTrack** — integrado vía Roboflow Supervision.
- Videos de partidos proporcionados por la **Federación Mexicana de Robótica** a través del repositorio oficial de la Copa FutBotMX.

---

## Contacto

Para dudas sobre la competencia: [futbotmx@secihti.mx](mailto:futbotmx@secihti.mx)  
Sitio oficial: [secihti.mx/futbotmx](https://secihti.mx/futbotmx/)
