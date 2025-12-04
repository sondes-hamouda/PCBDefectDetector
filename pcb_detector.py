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
    model = YOLO("yolov8n.yaml")  # structure du modèle
    model.train(
        data="data.yaml",         # fichier data.yaml avec classes et chemins
        epochs=50,                # nombre d'époques
        imgsz=640,                # taille des images
        batch=8,                  # batch size
        name="my_custom_pcb_model",
        pretrained=False          # pas de modèle pré-entraîné
    )
    print("Entraînement terminé !")


# -------------------------
# 2️⃣ Classe pour détecter les défauts
# -------------------------
class PCBDefectDetector:
    def __init__(self, model_path="runs/train/my_custom_pcb_model/weights/best.pt"):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Le modèle n'existe pas : {model_path}")
        self.model = YOLO(model_path)
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
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"L'image n'existe pas : {image_path}")

        results = self.model(image_path)[0]
        defects = []

        for box in results.boxes:
            cls = int(box.cls[0])
            conf = float(box.conf[0])
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            defects.append({
                "type": self.class_names[cls],
                "confidence": round(conf, 3),
                "bbox": {"x1": int(x1), "y1": int(y1), "x2": int(x2), "y2": int(y2)}
            })

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
    detector = PCBDefectDetector()
    test_image = "images/test/pcb_test.jpg"
    result = detector.detect(test_image)
    print(result["report"])
    detector.model(test_image).show()

