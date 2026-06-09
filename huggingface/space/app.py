import os
import time

import gradio as gr
import joblib
import numpy as np
import pandas as pd

from feature_extraction import extract_url_features


MODEL_PATHS = {
    "XGBoost": "models/xgb/xgb-full-feature.pkl",
    "Decision Tree": "models/dt/dt-full-feature.pkl",
    "LightGBM": "models/lgbm/lgbm-full-feature.pkl",
}

MODEL_CACHE = {}


def load_model(model_name):
    if model_name in MODEL_CACHE:
        return MODEL_CACHE[model_name]

    model_path = MODEL_PATHS[model_name]
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")

    model = joblib.load(model_path)
    MODEL_CACHE[model_name] = model
    return model


def predict_url(url, model_name):
    if not url or not isinstance(url, str):
        return "Enter a URL.", None, None

    started = time.time()
    extracted = extract_url_features(url)
    if not extracted:
        return "Could not extract features from this URL.", None, None

    features, feature_times = extracted
    input_data = np.array([list(features.values())])

    model = load_model(model_name)
    model_path = MODEL_PATHS[model_name]

    raw_prediction = model.predict(input_data)
    label = int(raw_prediction[0])
    confidence = None
    if hasattr(model, "predict_proba"):
        probability = model.predict_proba(input_data)[0]
        confidence = float(np.max(probability))

    result = "Phishing / malicious" if label == 1 else "Legitimate / safe"
    elapsed_ms = round((time.time() - started) * 1000, 2)
    confidence_text = "N/A" if confidence is None else f"{confidence:.3f}"
    summary = f"Prediction: {result} ({label})\nConfidence: {confidence_text}\nTotal time: {elapsed_ms} ms"

    feature_table = pd.DataFrame(
        {
            "feature": list(features.keys()),
            "value": list(features.values()),
            "time_ms": [round(feature_times[name] * 1000, 4) for name in features.keys()],
        }
    )

    return summary, feature_table, "Experimental result only. Do not use as the only security decision."


with gr.Blocks(title="PhishURL Detection") as demo:
    gr.Markdown("# PhishURL Detection")
    gr.Markdown("Classify a URL as legitimate or phishing/malicious using handcrafted URL features.")

    with gr.Row():
        url_input = gr.Textbox(
            label="URL",
            placeholder="https://example.com/login",
            scale=3,
        )
        model_input = gr.Dropdown(
            choices=list(MODEL_PATHS.keys()),
            value="XGBoost",
            label="Model",
            scale=1,
        )

    submit = gr.Button("Analyze URL", variant="primary")
    prediction_output = gr.Textbox(label="Result", lines=4)
    warning_output = gr.Textbox(label="Note", interactive=False)
    features_output = gr.Dataframe(label="Extracted Features", wrap=True)

    submit.click(
        predict_url,
        inputs=[url_input, model_input],
        outputs=[prediction_output, features_output, warning_output],
    )


if __name__ == "__main__":
    demo.launch()
