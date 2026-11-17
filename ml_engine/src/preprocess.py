"""
Data Preprocessing Pipeline for Network Intrusion Detection Datasets (e.g. CIC-IDS2017 / NSL-KDD).
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os

FEATURE_COLUMNS = [
    "flow_duration",
    "total_fwd_packets",
    "total_bwd_packets",
    "total_len_fwd_packets",
    "total_len_bwd_packets",
    "fwd_packet_length_max",
    "fwd_packet_length_min",
    "fwd_packet_length_mean",
    "flow_bytes_per_s",
    "flow_packets_per_s",
    "packet_length_mean",
    "packet_length_std",
    "fin_flag_count",
    "syn_flag_count",
    "rst_flag_count",
    "psh_flag_count",
    "ack_flag_count",
    "urg_flag_count",
    "down_up_ratio",
    "average_packet_size"
]

def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Removes infinite values, handles missing values, and drops duplicates."""
    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna()
    df = df.drop_duplicates()
    return df

def preprocess_dataset(
    csv_path: str,
    target_column: str = "label",
    test_size: float = 0.2,
    random_state: int = 42,
    output_dir: str = "ml_engine/models"
):
    """
    Loads dataset, cleans, encodes target labels, scales features,
    and returns train/test splits while saving the scaler and encoder.
    """
    os.makedirs(output_dir, exist_ok=True)
    df = pd.read_csv(csv_path)
    df = clean_data(df)

    X = df[FEATURE_COLUMNS]
    y = df[target_column]

    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y_encoded, test_size=test_size, random_state=random_state, stratify=y_encoded
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Save scaler and label encoder
    joblib.dump(scaler, os.path.join(output_dir, "scaler.joblib"))
    joblib.dump(label_encoder, os.path.join(output_dir, "label_encoder.joblib"))

    return X_train_scaled, X_test_scaled, y_train, y_test, label_encoder
