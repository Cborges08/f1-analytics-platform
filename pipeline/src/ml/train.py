import os
import joblib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    classification_report,
    mean_absolute_error,
    accuracy_score
)
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier, XGBRegressor

from features import load_features, engineer_features, get_feature_columns

# Output directory for models
MODELS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "models")
os.makedirs(MODELS_DIR, exist_ok=True)


def train_classifier(df: pd.DataFrame, feature_cols: list):
    """Train XGBoost classifier: predicts WIN/PODIUM/POINTS/OUT_OF_POINTS."""
    print("\n🎯 Training CLASSIFIER (result category)...")

    # Encode target
    le = LabelEncoder()
    y = le.fit_transform(df["result_category"])
    X = df[feature_cols].fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = XGBClassifier(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        random_state=42,
        eval_metric="mlogloss",
        verbosity=0
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"   ✅ Accuracy: {acc:.2%}")
    print("\n   Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))

    # Save model and encoder
    joblib.dump(model, os.path.join(MODELS_DIR, "classifier.pkl"))
    joblib.dump(le, os.path.join(MODELS_DIR, "label_encoder.pkl"))
    print("   💾 Classifier saved to models/classifier.pkl")

    return model, le, feature_cols


def train_regressor(df: pd.DataFrame, feature_cols: list):
    """Train XGBoost regressor: predicts exact finish position."""
    print("\n📍 Training REGRESSOR (finish position)...")

    y = df["finish_position"]
    X = df[feature_cols].fillna(0)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = XGBRegressor(
        n_estimators=200,
        max_depth=4,
        learning_rate=0.1,
        subsample=0.8,
        random_state=42,
        verbosity=0
    )
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"   ✅ Mean Absolute Error: {mae:.2f} positions")
    print(f"   (On average, predictions are off by {mae:.1f} positions)")

    # Save model
    joblib.dump(model, os.path.join(MODELS_DIR, "regressor.pkl"))
    print("   💾 Regressor saved to models/regressor.pkl")

    return model, feature_cols


def plot_feature_importance(model, feature_cols: list, model_name: str):
    """Plot and save feature importance chart."""
    importance = pd.DataFrame({
        "feature": feature_cols,
        "importance": model.feature_importances_
    }).sort_values("importance", ascending=True)

    plt.figure(figsize=(10, 6))
    plt.barh(importance["feature"], importance["importance"], color="#e10600")
    plt.xlabel("Importance")
    plt.title(f"Feature Importance — {model_name}")
    plt.tight_layout()

    path = os.path.join(MODELS_DIR, f"feature_importance_{model_name.lower()}.png")
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"   📊 Feature importance chart saved to models/")


def main():
    print("🏎️  F1 ML Training Pipeline")
    print("=" * 40)

    # Load and prepare data
    print("\n📦 Loading features from database...")
    df_raw = load_features()
    df = engineer_features(df_raw)
    feature_cols = get_feature_columns()

    print(f"   ✅ {len(df)} samples loaded")
    print(f"   Features: {len(feature_cols)}")
    print(f"   Target distribution:")
    print(df["result_category"].value_counts().to_string(index=True))

    # Train both models
    clf, le, _ = train_classifier(df, feature_cols)
    plot_feature_importance(clf, feature_cols, "Classifier")

    reg, _ = train_regressor(df, feature_cols)
    plot_feature_importance(reg, feature_cols, "Regressor")

    print("\n✅ Training complete. Models saved to pipeline/models/")


if __name__ == "__main__":
    main()