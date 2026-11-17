"""
Model Evaluation Module: Generates metrics, classification reports, and confusion matrix plots.
Useful for Chapter 4 of the thesis.
"""
import os
import joblib
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score

def evaluate_model(model, X_test, y_test, label_encoder, output_dir: str = "docs/evaluation_results"):
    """
    Computes performance metrics and plots confusion matrix.
    """
    os.makedirs(output_dir, exist_ok=True)
    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    report = classification_report(y_test, y_pred, target_names=label_encoder.classes_)
    cm = confusion_matrix(y_test, y_pred)

    print(f"Accuracy: {accuracy * 100:.2f}%\n")
    print("Classification Report:")
    print(report)

    # Save classification report to text file
    with open(os.path.join(output_dir, "classification_report.txt"), "w") as f:
        f.write(f"Accuracy: {accuracy * 100:.2f}%\n\n")
        f.write(report)

    # Plot Confusion Matrix
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        cm,
        annot=True,
        fmt="d",
        cmap="Blues",
        xticklabels=label_encoder.classes_,
        yticklabels=label_encoder.classes_
    )
    plt.title("XGBoost Confusion Matrix")
    plt.ylabel("Actual Label")
    plt.xlabel("Predicted Label")
    plt.tight_layout()

    plot_path = os.path.join(output_dir, "confusion_matrix.png")
    plt.savefig(plot_path)
    plt.close()
    print(f"Confusion matrix plot saved to {plot_path}")
