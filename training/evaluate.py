import json
import os
from sklearn.metrics import classification_report, accuracy_score, f1_score, roc_auc_score, confusion_matrix

def evaluate_model(model, X_test_vec, y_test, save_path="data/processed/eval_report.json"):
    y_pred = model.predict(X_test_vec)

    acc = accuracy_score(y_test, y_pred)
    f1  = f1_score(y_test, y_pred, average="weighted")

    auc = None
    if hasattr(model, "predict_proba"):
        y_prob = model.predict_proba(X_test_vec)[:, 1]
        auc = roc_auc_score(y_test, y_prob)

    cm = confusion_matrix(y_test, y_pred).tolist()

    print(classification_report(y_test, y_pred))
    print("Accuracy", acc)
    print("F1", f1)
    if auc:
        print("AUC", auc)

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    result = {
        "accuracy": acc,
        "f1_weighted": f1,
        "roc_auc": auc,
        "confusion_matrix": cm
    }

    with open(save_path, "w") as f:
        json.dump(result, f, indent=2)

    return result