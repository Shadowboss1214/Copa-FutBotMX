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

---

# Copa FutBotMX — Visión por Computadora

> Proyecto desarrollado para el **Capítulo Visión por Computadora** de la Copa FutBotMX, organizado por la Secretaría de Ciencia, Humanidades, Tecnología e Innovación (Secihti) en colaboración con Meta y Centro.

---

## Descripción

Este proyecto implementa un pipeline de visión por computadora para segmentar, rastrear y analizar videos de partidos de fútbol robótico de la Copa FutBotMX. Utiliza **SAM 3 (Segment Anything Model 3)** de Meta como tecnología base, combinado con **YucaBot**, un modelo de detección personalizado entrenado específicamente para reconocer robots y balones en el contexto de la competencia.

El análisis completo —detección, segmentación, tracking, clasificación de equipos, conteo de goles, mapa táctico y exportación de datos— se ejecuta de manera integrada en el notebook **`03_pipeline_final.ipynb`**, descrito en detalle en la sección [Pipeline Final](#pipeline-final--03_pipeline_finalipynb).

---

## Tecnologías utilizadas

| Tecnología | Rol en el pipeline |
|---|---|
| **SAM 3** (Meta AI) | Segmentación precisa con máscaras por objeto |
| **YucaBot** (YOLOv8m fine-tuned) | Detección especializada de robots y balón |
| **ByteTrack** (Supervision) | Tracking de objetos entre frames |
| **Roboflow Supervision** | Anotación, visualización y procesamiento de video |
| **OpenCV** | Lectura, manipulación de frames y proyección geométrica |
| **OpenPyXL** | Exportación de datos de tracking a Excel |

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

## Pipeline Final — `03_pipeline_final.ipynb`

Este notebook es el **entregable principal** del proyecto: integra de inicio a fin todo el flujo de análisis sobre un video de fútbol robótico capturado con cámara cenital fija, y produce como salida un video anotado, visualizaciones tácticas y una base de datos de tracking en Excel.

### ¿Qué hace este notebook?

1. **Detección** — YucaBot localiza robots y balón en cada frame del video.
2. **Segmentación** — SAM 3 refina cada detección con una máscara de píxeles precisa, coloreada según el equipo al que pertenece el robot detectado.
3. **Tracking** — ByteTrack asigna y mantiene un ID único por objeto a lo largo del video, tolerando oclusiones breves.
4. **Proyección geométrica (Homografía)** — Cada objeto detectado en el video se proyecta a un **campo canónico** (vista cenital estandarizada) usando una matriz de homografía `H`, calculada a partir de las 4 esquinas de la cancha.
5. **Clasificación de equipos** — Cada robot es asignado a un equipo (Amarillo = Equipo 1, Azul = Equipo 2) según su posición en el primer frame del video. Si el tracker pierde y reasigna un nuevo ID a un robot ya conocido, el sistema busca el robot conocido más cercano dentro de una ventana de tiempo y le hereda su equipo, evitando reclasificaciones erróneas.
6. **Detección de goles** — Se definen zonas de portería (`PolygonZone`) fuera del rectángulo de la cancha, en la posición real de cada portería. Cuando el balón entra a alguna de estas zonas se incrementa el marcador del equipo correspondiente, con un periodo de cooldown de 150 frames para evitar conteos duplicados por errores momentáneos de tracking.
7. **Mapa táctico** — Se genera una vista cenital esquemática con los robots, el balón, las porterías coloreadas por equipo y el marcador en tiempo real, con un margen visual adicional alrededor de la cancha para representar las porterías y tolerar pequeños errores de proyección sin perder de vista a los objetos.
8. **Visualizaciones agregadas** — Heatmap de actividad por equipo/robot y mapa de trayectorias (trails) acumulados sobre el campo canónico.
9. **Exportación a Excel** — Se genera un archivo `tracking_data.xlsx` con el registro frame por frame de cada objeto detectado.

### Estructura del archivo Excel generado

| Columna | Descripción |
|---|---|
| `frame` | Número de frame del video |
| `id` | ID de tracking asignado por ByteTrack |
| `clase` | `robot` o `ball` |
| `equipo` | 1 (Amarillo), 2 (Azul), o 0 si es el balón |
| `x_campo` | Coordenada X proyectada al campo canónico (vía matriz H) |
| `y_campo` | Coordenada Y proyectada al campo canónico (vía matriz H) |
| `area` | Área en píxeles de la máscara SAM (si fue detectada; `null` si no) |
| `goles_equipo1` | Marcador acumulado del Equipo 1 al momento del frame |
| `goles_equipo2` | Marcador acumulado del Equipo 2 al momento del frame |

Este archivo es la base para cualquier análisis posterior de datos (posesión, velocidad, distancia recorrida, mapas de calor personalizados, etc.).

### Archivos necesarios para ejecutar el notebook

Este notebook **no funcionará sin dos archivos externos**, que por su peso no están incluidos en este repositorio de GitHub:

| Archivo | Ubicación requerida | Descripción |
|---|---|---|
| `yucabot.pt` | `notebooks/yucabot.pt` | Modelo YOLOv8m entrenado (ver sección YucaBot) |
| `cenital_Analisis.mp4` | `VideosEjemplo/cenital_Analisis.mp4` | Video de análisis, vista cenital fija |

**Ambos archivos están disponibles para descarga en esta carpeta de Google Drive:**
**[Carpeta Drive — Modelo y video](https://drive.google.com/drive/folders/1LjkBYg4E_yi1BCAFKke99IXdQnqPa_Os?usp=sharing)**

Pasos para configurarlos correctamente:
1. Descarga `yucabot.pt` desde el Drive y colócalo directamente dentro de la carpeta `notebooks/` (al mismo nivel que los archivos `.ipynb`).
2. Descarga `cenital_Analisis.mp4` desde el Drive y colócalo dentro de la carpeta `VideosEjemplo/` en la raíz del repositorio.
3. Verifica que las rutas en la celda de configuración del notebook (`VIDEO_PATH`, ruta de `yucabot.pt`) coincidan con esta estructura.

### Limitación importante: solo cámara fija cenital

El pipeline fue diseñado y calibrado para trabajar **exclusivamente con video capturado desde una cámara fija en vista cenital** (toma desde arriba, sin movimiento). Esta decisión se tomó por limitaciones de tiempo del equipo: se exploró inicialmente una alternativa de detección automática de las esquinas de la cancha mediante un modelo de keypoints (`pokolpok.pth`, EfficientNet-B0 entrenado con 2,000 imágenes sintéticas generadas en Blender), pero el modelo no generalizó correctamente a video real debido al domain gap entre los datos sintéticos y las grabaciones reales, por lo que se descartó.

**Si deseas usar un video distinto al proporcionado**, debes:
1. Asegurarte de que la cámara sea fija y la vista sea cenital (desde arriba).
2. Identificar manualmente las coordenadas en píxeles de las **4 esquinas de la cancha** (líneas blancas del área de juego) en el primer frame de tu video.
3. Actualizar la variable `SOURCE_POINTS` en la celda de configuración del notebook con esas 4 coordenadas, en el orden: superior-izquierda, superior-derecha, inferior-derecha, inferior-izquierda.
4. Verificar visualmente con la celda de comprobación de puntos (incluida en el notebook) que las esquinas coincidan correctamente antes de ejecutar el pipeline completo.

---

## Resultados del análisis — `cenital_Analisis.mp4`

*(Espacio para documentar el análisis del video procesado)*

**Video procesado:** `cenital_Analisis.mp4`

**Resumen del partido:**
- Marcador final: Equipo 1 (Amarillo) **_** — **_** Equipo 2 (Azul)
- Duración analizada: *(agregar)*
- Robots detectados: *(agregar)*

**Capturas / GIFs del video anotado:**

*(Agregar aquí capturas del video con segmentación SAM, cajas de equipo y marcador)*

**Mapa de calor de actividad (heatmap):**

*(Agregar imagen `heatmap_final.png`)*<img width="583" height="955" alt="heatmap_final png" src="https://github.com/user-attachments/assets/e7ac0632-6351-4418-b376-11102f7166b9" />


**Mapa de trayectorias (trails):**

*(Agregar imagen `trails_final.png`)*

**Insights del análisis:**

*(Agregar observaciones: equipo con mayor posesión/actividad, zonas de mayor concentración de juego, etc., basadas en `tracking_data.xlsx`)*

---

## Pipeline general

```
Video de entrada (cámara cenital fija)
      ↓
YucaBot detecta robots y balón (bounding boxes)
      ↓
SAM 3 refina las detecciones con máscaras precisas, coloreadas por equipo
      ↓
ByteTrack asigna y mantiene ID único por objeto
      ↓
Proyección geométrica al campo canónico (matriz de homografía H)
      ↓
Clasificación de equipos + detección de goles (PolygonZone)
      ↓
Visualización: video anotado + mapa táctico + heatmap + trails
      ↓
Exportación: video final (.mp4) + datos de tracking (.xlsx)
```

---

## Estructura del repositorio

```
Copa-FutBotMX/
│
├── notebooks/
│   ├── 00_Entrenamiento_yucabot.ipynb   # Entrenamiento del modelo YucaBot
│   ├── 01_exploracion.ipynb             # Análisis exploratorio de los videos
│   ├── 02_segmentacion.ipynb            # Pruebas de segmentación con SAM 3
│   ├── 03_pipeline_final.ipynb          # Pipeline completo integrado (entregable principal)
│   ├── yucabot.pt                       # Modelo personalizado (descargar de Drive, no incluido en git)
│   └── assets/                          # Videos y visualizaciones generadas
│
├── VideosEjemplo/
│   └── cenital_Analisis.mp4             # Video de análisis (descargar de Drive, no incluido en git)
│
├── src/
│   └── utils.py                         # Funciones reutilizables
│
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
- Python 3.11.15
- CUDA 12.8
- Anaconda o virtualenv

### Pasos

**1. Clonar el repositorio**
```bash
git clone https://github.com/Shadowboss1214/Copa-FutBotMX.git
cd Copa-FutBotMX
```

**2. Crear entorno virtual**
```bash
conda create -n supervision python=3.10
conda activate supervision
```

**3. Instalar dependencias**
```bash
pip install -r requirements.txt
```

**4. Descargar archivos necesarios (no incluidos en git por peso)**

Descarga desde la carpeta de Google Drive y colócalos en las rutas indicadas:
- `yucabot.pt` → colocar en `notebooks/yucabot.pt`
- `cenital_Analisis.mp4` → colocar en `VideosEjemplo/cenital_Analisis.mp4`

**[Carpeta Drive — Modelo y video](https://drive.google.com/drive/folders/1LjkBYg4E_yi1BCAFKke99IXdQnqPa_Os?usp=sharing)**

**5. Ejecutar el pipeline**

Para reproducir el análisis completo, abre y ejecuta en orden:
```
03_pipeline_final.ipynb
```

Los notebooks `00`, `01` y `02` documentan el proceso de entrenamiento y experimentación previa, y son opcionales para reproducir el resultado final.

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
openpyxl
roboflow
```

Instalar con:
```bash
pip install -r requirements.txt
```

---

## Metodología e Implementación Técnica

### Entorno de Desarrollo y Ecosistema
* **Lenguaje Base:** Python 3.11.15.
* **Gestor de Entorno:** Anaconda, garantizando el aislamiento de dependencias, el control de versiones de los paquetes y la reproducibilidad del pipeline de ejecución.
* **Interfaz de Trabajo:** Jupyter Notebooks (`.ipynb`), utilizado como entorno interactivo para la experimentación modular, la visualización inmediata de fotogramas procesados y la depuración por bloques de código.
* **Librería de Gestión de Visión:** `supervision` (Roboflow). Esta librería se empleó para estandarizar el manejo de las detecciones, estructurar el flujo de las máscaras binarias, gestionar el dibujado de anotaciones sobre los videos secuenciales, y definir zonas geométricas (`PolygonZone`) para la detección de eventos como goles.

### Elementos Mapeados y Segmentados
El pipeline técnico se diseñó para detectar, delimitar y realizar el seguimiento de las entidades críticas dentro de la cancha de la Copa FutBotMX:
1. **Robots:** Agentes dinámicos en constante movimiento y oclusión mutua, clasificados además por equipo.
2. **Pelota:** Objeto esférico de pequeña escala, caracterizado por desplazamientos de alta velocidad.
3. **Porterías:** Zonas geométricas virtuales, proyectadas en el campo canónico fuera del área de juego delimitada por la matriz de homografía, utilizadas para la detección automática de goles.

### Arquitectura de Modelos y Entrenamiento

La estrategia de visión por computadora combinó un enfoque de segmentación avanzado junto con un modelo de detección de objetos ajustado a un entorno personalizado, integrados con un sistema de proyección geométrica para el análisis táctico.

#### 1. Segmentación y Configuración de Prompts con SAM 3
* **Modelo Utilizado:** `sam3.pt` (Segment Anything Model 3 de Meta AI).
* **Implementación:** Se aprovechó la arquitectura unificada de SAM 3 para realizar la segmentación por píxel de vocabulario abierto en los videos del torneo proporcionados por la Federación Mexicana de Robótica.
* **Estrategia de Prompts:** En el pipeline final, SAM 3 se alimenta con las cajas delimitadoras (bounding boxes) producidas por YucaBot, lo que permite una segmentación dirigida y de mayor precisión sobre robots y balón, evitando los falsos positivos observados en pruebas iniciales con prompts de texto abierto sobre el campo completo.
* **Coloreado por equipo:** Las máscaras generadas por SAM 3 se colorean dinámicamente según el equipo al que pertenece cada robot (Amarillo/Azul), facilitando la lectura visual del video resultante.

#### 2. Detección de Objetos Personalizada con YOLOv8 — YucaBot
* **Limitación del Modelo Base:** Se incorporó inicialmente el modelo ligero `yolov8n.pt` (YOLOv8 Nano) para optimizar la velocidad de inferencia en los notebooks. Sin embargo, los objetos específicos del reto de fútbol robótico no forman parte de las 80 clases estándar del dataset público COCO (Common Objects in Context).
* **Flujo de Etiquetado en Roboflow:** Para resolver esta limitación de dominio, se llevó a cabo un proceso de anotación propia. Se extrajeron fotogramas clave de las grabaciones de la cancha y se cargaron en la plataforma **Roboflow**. Ahí se ejecutó el etiquetado manual y riguroso de cajas delimitadoras (bounding boxes) para entrenar al modelo en el reconocimiento de las clases personalizadas.
* **Ajuste Fino (Fine-Tuning):** El dataset estructurado y exportado desde Roboflow se utilizó para entrenar los pesos de un modelo YOLOv8m, dando como resultado **YucaBot**, capaz de reconocer las características morfológicas particulares de los robots de la competencia y el balón con un mAP50 de 0.978.

#### 3. Proyección Geométrica y Homografía
* **Cálculo de la matriz H:** A partir de las 4 esquinas visibles de la cancha (líneas blancas del área de juego) en el video de cámara fija, se calcula una matriz de transformación de perspectiva (`cv2.getPerspectiveTransform`) que mapea cualquier punto del video a un sistema de coordenadas estandarizado: el **campo canónico**.
* **Uso del campo canónico:** Todas las posiciones de robots y balón se proyectan a este espacio normalizado, lo que permite generar visualizaciones tácticas (mapa cenital, heatmap, trails) independientes de la perspectiva original de la cámara, y habilita la detección geométrica de eventos como goles mediante zonas poligonales (`PolygonZone`) definidas fuera del área de juego, en la posición real de cada portería.

#### 4. Persistencia de Identidad y Clasificación de Equipos
* **Tracking con ByteTrack:** Cada objeto detectado recibe un ID persistente a lo largo del video. Para tolerar oclusiones momentáneas (robots superpuestos, fallos puntuales de detección), se ajustó el parámetro `lost_track_buffer` del tracker.
* **Clasificación inicial:** En el primer frame del video, cada robot es clasificado a un equipo según su posición relativa a la mitad del campo canónico (mitad superior = Equipo 1 / Amarillo, mitad inferior = Equipo 2 / Azul).
* **Herencia de equipo ante pérdida de tracking:** Si ByteTrack pierde un robot y le asigna un nuevo ID al reaparecer, el sistema busca, dentro de una ventana de tiempo reciente, cuál robot conocido tenía la posición más cercana al punto de reaparición, y le hereda su equipo. Esto evita que un robot cambie de equipo erróneamente al cruzar la mitad de la cancha, comportamiento que sí ocurría con un enfoque de clasificación por posición instantánea.

---

## Equipo

| Nombre | Rol |
|---|---|
| *(Hernandez Sanchez Yovani Gabriel)* | Describir rol |
| *(Martin Alamilla Cesar Adrian)* | Describir rol |
| *(Salazar Bastarrachea Gael Francisco)* | Describir rol |

---

## Licencia

Este proyecto está licenciado bajo la **Licencia MIT**. Ver archivo [LICENSE](LICENSE) para más detalles.

### Créditos y atribuciones
- **SAM 3** — Meta AI. Carion et al. (2025). "SAM 3: Segment Anything with Concepts." arXiv:2511.16719. Licencia SAM License.
- **YOLOv8** — Ultralytics. Licencia AGPL-3.0.
- **Supervision** — Roboflow. Licencia MIT.
- **ByteTrack** — integrado vía Roboflow Supervision.
- **OpenPyXL** — Licencia MIT/LGPL.
- Videos de partidos proporcionados por la **Federación Mexicana de Robótica** a través del repositorio oficial de la Copa FutBotMX.

---

## Contacto

Para dudas sobre la competencia: [futbotmx@secihti.mx](mailto:futbotmx@secihti.mx)
Sitio oficial: [secihti.mx/futbotmx](https://secihti.mx/futbotmx/)
