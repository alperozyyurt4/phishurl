from flask import Flask, render_template, request
import numpy as np
import pandas as pd
import joblib
import tensorflow as tf
import os
import time
from feature_extraction import extract_url_features

# ⬇️ Custom LSTM: 'time_major' parametresi silinir
from keras.layers import LSTM as KerasLSTM
class PatchedLSTM(KerasLSTM):
    @classmethod
    def from_config(cls, config):
        config.pop("time_major", None)  # Hatalı parametreyi kaldır
        return super().from_config(config)

app = Flask(__name__)

MODEL_PATHS = {
    "Random Forest (pkl)": "../lastcode/full/rf/rf-full-feature.pkl",
    "Extra Tree (pkl)": "../lastcode/full/et/et-full-feature.pkl",
    "Decision Tree (pkl)": "../lastcode/full/dt/dt-full-feature.pkl",
    "LightGbm (pkl)": "../lastcode/full/lgbm/lgbm-full-feature.pkl",
    "XGBoost (pkl)": "../lastcode/full/xgb/xgb-full-feature.pkl",
    "ANN (h5)": "../lastcode/full/ann/ann-model.h5",
    "DNN (h5)": "../lastcode/full/dnn/dnn-model.h5",
    "CNN (h5)": "../lastcode/full/cnn/f-cnn-model.h5",
    "LTSM (h5)": "../lastcode/nocvcode/nocv-lstm-model.h5",
}

@app.route("/", methods=["GET", "POST"])
def index():
    prediction_result = None
    features_table = None
    times = {}
    selected_model = None

    if request.method == "POST":
        url = request.form["url"]
        selected_model = request.form["model"]
        model_path = MODEL_PATHS[selected_model]

        # Özellik çıkar
        t0 = time.time()
        features, feature_times = extract_url_features(url)
        times["extract_time"] = time.time() - t0

        if features is not None:
            input_data = np.array([list(features.values())])

            # Model yükle
            t1 = time.time()
            if model_path.endswith(".pkl"):
                model = joblib.load(model_path)
            else:
                # Eğer LSTM içeriyorsa PatchedLSTM kullan
                if "lstm" in model_path.lower():
                    model = tf.keras.models.load_model(model_path, custom_objects={"LSTM": PatchedLSTM})
                else:
                    model = tf.keras.models.load_model(model_path)
            times["load_time"] = time.time() - t1

            # Tahmin yap
            t2 = time.time()
            if model_path.endswith(".pkl"):
                prediction = model.predict(input_data)
            elif "cnn" in model_path.lower():
                scaler = joblib.load("../lastcode/full/cnn/scaler22.pkl")
                input_data_scaled = scaler.transform(input_data)
                input_data_scaled = np.expand_dims(input_data_scaled, axis=-1)
                prediction = model.predict(input_data_scaled)[0]
            else:
                prediction = model.predict(input_data)[0]
            prediction = np.round(prediction)
            times["predict_time"] = time.time() - t2

            prediction_result = int(prediction)
            features_table = pd.DataFrame({
                "Feature": features.keys(),
                "Value": features.values(),
                "Time (s)": [feature_times[k] for k in features.keys()]
            })

    return render_template("index.html",
                           models=list(MODEL_PATHS.keys()),
                           prediction_result=prediction_result,
                           selected_model=selected_model,
                           features_table=features_table,
                           times=times)

if __name__ == "__main__":
    app.run(debug=True)