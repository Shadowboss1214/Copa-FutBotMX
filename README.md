# Copa-FutBotMX - Reto de visión por computadora.

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

## ESTRUCTURA DEL PROYECTO.

futbotmx-vision/
│
├── README.md                  ← descripción, instrucciones, enlace al reel
├── LICENSE                    ← MIT (requerido por la convocatoria)
│
├── notebooks/
│   ├── 01_exploracion.ipynb   ← explorar los videos, entender el dataset
│   ├── 02_segmentacion.ipynb  ← aplicar SAM 3 a frames del video
│   ├── 03_tracking.ipynb      ← rastrear robots y balón
│   ├── 04_visualizacion.ipynb ← mapas de calor, trails, dashboards
│   └── 05_pipeline_final.ipynb← todo junto, limpio y reproducible
│   └──assets/                 ← donde se guardan pruebas de la exploracion
|      └──Frames_roboflow/     ← para obtener frames concretos
├── src/
│   └── utils.py               ← funciones que reutilizan en varios notebooks
│
├── outputs/
│   ├── frames/                ← imágenes de ejemplo de resultados
│   └── videos/                ← clips cortos de demo
│
└── requirements.txt           ← dependencias del proyecto

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
3. **Porterías:** Estructuras fijas en los extremos del campo que sirven como puntos de referencia espaciales.
4. **Campo de Juego:** Superficie total que define los límites geométricos válidos del partido.


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
