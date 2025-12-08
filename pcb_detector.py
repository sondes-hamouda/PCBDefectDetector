# pcb_detector.py
from ultralytics import YOLO
from datetime import datetime
import os

# -------------------------
# 1️⃣ Fonction pour entraîner le modèle (optionnel)
# -------------------------
def train_model():
    """
    Entraîne un modèle YOLOv8 sur les PCB.
    """
    # Utilise un modèle pré-entraîné léger (vérifie que YOLOv8 est installé)
    model = YOLO("yolov8s.pt")  # ou yolov8n.pt si tu veux très léger
    model.train(
        data="data.yaml",         # fichier data.yaml avec chemins et classes
        epochs=50,                # nombre d'époques
        imgsz=640,                # taille des images
        batch=8,                  # taille du batch
        name="pcb_detector",      # nom du projet (dossier runs/train/pcb_detector)
        pretrained=True           # utiliser le modèle pré-entraîné
    )
    print("Entraînement terminé !")
    print("Le modèle best.pt se trouve dans : runs/train/pcb_detector/weights/best.pt")


# -------------------------
# 2️⃣ Classe pour détecter les défauts
# -------------------------
class PCBDefectDetector:
    def __init__(self, model_path="runs/train/pcb_detector/weights/best.pt"):
        # Vérifie que le modèle existe
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Le modèle n'existe pas : {model_path}")
        self.model = YOLO(model_path)

        # Liste des classes correspondant à ton dataset
        self.class_names = [
            "missing_component",
            "wrong_orientation",
            "cold_solder",
            "short_circuit",
            "broken_track",
            "burn_mark",
            "misaligned_component",
            "extra_solder"
        ]

    def detect(self, image_path):
        # Vérifie que l'image existe
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"L'image n'existe pas : {image_path}")

        results = self.model(image_path)[0]  # YOLOv8 retourne une liste, on prend le 1er élément
        defects = []

        # Parcours toutes les boîtes détectées
        for box in results.boxes:
            cls = int(box.cls[0])      # indice de classe
            conf = float(box.conf[0])  # confiance
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            defects.append({
                "type": self.class_names[cls],
                "confidence": round(conf, 3),
                "bbox": {"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)}
            })

        # Génère un rapport
        report = self.generate_report(defects)
        return {"image": image_path, "detected_defects": defects, "report": report}

    def generate_report(self, defects):
        if len(defects) == 0:
            return "Aucun défaut détecté sur ce PCB."
        
        report = "📌 Rapport de Détection PCB\n"
        report += f"Date : {datetime.now()}\n"
        report += "--------------------------------\n"
        for d in defects:
            report += f"- Défaut : {d['type']} (confiance : {d['confidence']})\n"
        report += "--------------------------------\n"
        report += f"Total des défauts détectés : {len(defects)}"
        return report


# -------------------------
# 3️⃣ Exemple d'utilisation
# -------------------------
if __name__ == "__main__":
    # Crée un objet détecteur
    detector = PCBDefectDetector()

    # Exemple : image de test (à adapter selon ton dataset)
    test_image = "dataset/test/images/OC_Spur44_jpg.rf.34453e14e70673e08385fbfa1d4f8b2a.jpg"

    # Détection
    result = detector.detect(test_image)
    print(result["report"])

    # Affiche l'image avec les boîtes détectées
    detector.model(test_image).show()

