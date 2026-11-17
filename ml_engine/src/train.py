"""
Model Training Module using XGBoost Classifier.
"""
import xgboost as xgb
import os
import joblib
from .preprocess import preprocess_dataset

def train_xgboost(
    data_path: str,
    output_dir: str = "ml_engine/models",
    n_estimators: int = 150,
    max_depth: int = 6,
    learning_rate: float = 0.1
):
    """
    Trains an XGBoost multiclass/binary classifier on preprocessed network data.
    """
    os.makedirs(output_dir, exist_ok=True)

    X_train, X_test, y_train, y_test, label_encoder = preprocess_dataset(
        csv_path=data_path, output_dir=output_dir
    )

    num_classes = len(label_encoder.classes_)
    objective = "binary:logistic" if num_classes == 2 else "multi:softprob"

    model = xgb.XGBClassifier(
        n_estimators=n_estimators,
        max_depth=max_depth,
        learning_rate=learning_rate,
        objective=objective,
        eval_metric="mlogloss" if num_classes > 2 else "logloss",
        use_label_encoder=False,
        random_state=42,
        n_jobs=-1
    )

    print(f"Training XGBoost model with {len(X_train)} samples across {num_classes} classes...")
    model.fit(X_train, y_train, eval_set=[(X_test, y_test)], verbose=True)

    # Save model
    model_path = os.path.join(output_dir, "xgboost_model.json")
    model.save_model(model_path)
    joblib.dump(model, os.path.join(output_dir, "xgboost_model.joblib"))
    print(f"Model saved to {model_path}")

    return model, X_test, y_test, label_encoder

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        train_xgboost(sys.argv[1])
    else:
        print("Usage: python -m ml_engine.src.train <path_to_dataset.csv>")
