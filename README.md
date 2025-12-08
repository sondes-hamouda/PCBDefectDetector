# 🛠️ PCBDefectDetector

PCBDefectDetector est une application d’inspection automatique de circuits imprimés (PCB) basée sur un modèle YOLO.  
Elle permet de détecter plusieurs types de défauts à partir d’images et de générer un rapport clair via une interface web développée avec FastAPI et Jinja2.  
Le projet inclut un Dockerfile pour un déploiement simple et reproductible.

---

## 🚀 Fonctionnalités principales

- Détection automatique de défauts PCB avec YOLOv8.
- Analyse complète d’images via une interface web.
- Génération d’un rapport détaillé des anomalies détectées.
- API légère et rapide basée sur FastAPI.
- Déploiement conteneurisé avec Docker.


## 📂 Structure du projet
PCBDefectDetector/
├── Dockerfile
├── main.py # Application FastAPI
├── pcb_detector.py # Classe PCBDefectDetector et fonctions YOLO
├── requirements.txt # Dépendances Python
├── README.md
└── templates/
└── index.html # Interface web
