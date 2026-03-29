import joblib
import json
import os
from datetime import datetime

def save_artifacts(
    model,
    vectorizer,
    model_dir="app/models",
    model_name="svc_model.pkl",
    vectorizer_name="tfidf_vectorizer.pkl",
    meta_name="model_meta.json",
):

    os.makedirs(model_dir, exist_ok=True)

    model_path = os.path.join(model_dir, model_name)
    joblib.dump(model, model_path, compress=3)
    print(f"Model saved      → {model_path}")

    vec_path = os.path.join(model_dir, vectorizer_name)
    joblib.dump(vectorizer, vec_path, compress=3)
    print(f"Vectorizer saved → {vec_path}")

    meta = {
        "saved_at":    datetime.now().isoformat(),
        "model_file":  model_name,
        "vec_file":    vectorizer_name,
        "classifier":  type(model).__name__,
        "tfidf_params": {
            "max_features": vectorizer.max_features,
            "ngram_range":  list(vectorizer.ngram_range),
            "sublinear_tf": vectorizer.sublinear_tf,
        },
    }

    meta_path = os.path.join(model_dir, meta_name)
    with open(meta_path, "w") as f:
        json.dump(meta, f, indent=2)

    print(f"Metadata saved   → {meta_path}")
    return model_path, vec_path
