"""
Detection Service: Orchestrates feature extraction, XGBoost inference,
and notifies connected WebSockets / persists alerts.
"""
import sys
import os

# Add ml_engine to sys.path if not present
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
from ml_engine.src.predictor import IntrusionPredictor
from app.services.feature_extractor import FlowFeatureExtractor

class DetectionEngine:
    def __init__(self):
        self.predictor = IntrusionPredictor()
        self.extractor = FlowFeatureExtractor()

    def process_packet(self, packet):
        """
        Extracts features from packet flow, runs XGBoost classification,
        and returns detection alert dictionary if malicious activity is spotted.
        """
        metadata, features = self.extractor.process_packet(packet)
        if metadata and features:
            prediction = self.predictor.predict(features)
            result = {
                **metadata,
                **prediction
            }
            return result
        return None

detection_engine = DetectionEngine()
