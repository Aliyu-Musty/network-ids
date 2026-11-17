"""
Inference Module: Loads pre-trained XGBoost model and scaler for real-time predictions.
"""
import os
import joblib
import numpy as np

class IntrusionPredictor:
    def __init__(self, model_dir: str = "ml_engine/models"):
        self.model_dir = model_dir
        self.model = None
        self.scaler = None
        self.label_encoder = None
        self.load_artifacts()

    def load_artifacts(self):
        """Loads trained model, scaler, and label encoder if they exist."""
        model_path = os.path.join(self.model_dir, "xgboost_model.joblib")
        scaler_path = os.path.join(self.model_dir, "scaler.joblib")
        encoder_path = os.path.join(self.model_dir, "label_encoder.joblib")

        if os.path.exists(model_path) and os.path.exists(scaler_path) and os.path.exists(encoder_path):
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.label_encoder = joblib.load(encoder_path)
            print("Successfully loaded ML model and preprocessors.")
        else:
            print("Warning: Model artifacts not found. Please train model or run in dummy mode.")

    def predict(self, feature_vector: list) -> dict:
        """
        Predicts traffic class for a given extracted flow feature vector.
        Returns:
            dict containing:
                is_attack (bool)
                attack_type (str)
                confidence (float)
                severity (str)
        """
        if self.model is None or self.scaler is None:
            # Fallback mock for early testing before model training
            return {
                "is_attack": False,
                "attack_type": "BENIGN",
                "confidence": 0.99,
                "severity": "NORMAL"
            }

        arr = np.array(feature_vector).reshape(1, -1)
        arr_scaled = self.scaler.transform(arr)

        pred_idx = self.model.predict(arr_scaled)[0]
        probs = self.model.predict_proba(arr_scaled)[0]
        confidence = float(np.max(probs))
        label = self.label_encoder.inverse_transform([pred_idx])[0]

        is_attack = str(label).upper() != "BENIGN"
        severity = self._map_severity(label, confidence) if is_attack else "NORMAL"

        return {
            "is_attack": is_attack,
            "attack_type": label,
            "confidence": round(confidence, 4),
            "severity": severity
        }

    @staticmethod
    def _map_severity(attack_type: str, confidence: float) -> str:
        atk = attack_type.upper()
        if "DOS" in atk or "DDOS" in atk or "BOTNET" in atk:
            return "CRITICAL"
        elif "PORT" in atk or "SCAN" in atk or "BRUTE" in atk:
            return "HIGH"
        elif "WEB" in atk or "INJECTION" in atk:
            return "MEDIUM"
        return "LOW"
