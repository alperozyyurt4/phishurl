import time
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import tensorflow as tf
from feature_extraction import extract_url_features

# Streamlit başlığı
st.title("Model Tahmin Arayüzü")

# Model klasörleri
MODEL_PATHS = {
    "Random Forest (pkl)": "../lastcode/full/rf/rf-full-feature.pkl",
    "Decision Tree (pkl)": "../lastcode/full/dt/dt-full-feature.pkl",
    "LightGbm (pkl)": "../lastcode/full/lgbm/lgbm-full-feature.pkl",
    "XGBoost (pkl)": "../lastcode/full/xgb/xgb-full-feature.pkl",
    "ANN (h5)": "../lastcode/full/ann/ann-model.h5",
    "DNN (h5)": "../lastcode/full/dnn/dnn-model.h5",
    "CNN (h5)": "../lastcode/full/cnn/f-cnn-model.h5",
    "LTSM (h5)": "../lastcode/nocvcode/nocv-lstm-model.h5",
}

# Model seçme dropdown
selected_model_name = st.selectbox("Kullanılacak Modeli Seç:", list(MODEL_PATHS.keys()))

# URL giriş alanı
url_input = st.text_input("URL Girin:", "")

# Tahmin butonu
if st.button("Tahmin Yap"):
    if not url_input:
        st.warning("Lütfen bir URL girin!")
    else:
        # Feature extraction işlemi
        start_time = time.time()
        features, feature_times = extract_url_features(url_input)
        end_time = time.time() - start_time

        st.write(f"Feature extraction süresi: {end_time:.5f} saniye")

        if features is None:
            st.warning("URL işlenirken bir hata oluştu, lütfen geçerli bir URL girin!")
        else:
            feature_df = pd.DataFrame({
                "Feature Adı": list(features.keys()),
                "Feature Değeri": list(features.values()),
                "Çalışma Süresi (sn)": [feature_times[key] for key in features.keys()]
            })

            st.subheader("Çıkarılan Feature'lar ve Çalışma Süreleri")
            st.dataframe(feature_df)

            # Model yükleme
            model_path = MODEL_PATHS[selected_model_name]

            load_start_time = time.time()

            if model_path.endswith(".pkl"):
                with open(model_path, "rb") as f:
                    model = joblib.load(f)
            elif model_path.endswith(".h5"):
                model = tf.keras.models.load_model(model_path)

            load_end_time = time.time()
            load_elapsed_time = load_end_time - load_start_time
            st.write(f"Model yükleme süresi: {load_elapsed_time:.5f} saniye")

            # Tahmin işlemi
            predict_start_time = time.time()

            if model_path.endswith(".pkl"):
                prediction = model.predict([list(features.values())])
            elif model_path.endswith(".h5"):
                if "cnn" in model_path.lower():
                    scaler = joblib.load("../lastcode/full/cnn/scaler22.pkl")
                    input_data = np.array([list(features.values())])
                    input_data_scaled = scaler.transform(input_data)
                    input_data_scaled = np.expand_dims(input_data_scaled, axis=-1)
                    prediction = model.predict(input_data_scaled)[0]
                else:
                    input_data = np.array([list(features.values())])
                    prediction = model.predict(input_data)[0]
                prediction = np.round(prediction)

            predict_end_time = time.time()
            predict_elapsed_time = predict_end_time - predict_start_time
            st.write(f"Tahmin süresi: {predict_elapsed_time:.5f} saniye")

            # Tahmin sonucunu göster
            st.subheader("Tahmin Sonucu")
            if prediction == 1:
                st.error("TEHLİKELİ! (1)")
            else:
                st.success("GÜVENLİ (0)")