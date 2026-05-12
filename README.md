# PhishURL Detection | Phishing URL Tespit Sistemi

Makine öğrenmesi ve derin öğrenme modelleri ile URL'lerin **güvenli** veya **phishing/tehlikeli** olup olmadığını tahmin eden bir proje.

This project detects whether a URL is **legitimate** or **phishing/malicious** using handcrafted URL features and multiple machine learning / deep learning models.

---

## TR | Proje Özeti

Bu repository, URL tabanlı phishing tespiti için geliştirilmiş üç ana bölümden oluşur:

- **Feature extraction:** URL üzerinden uzunluk, karakter, token, TLD, IP, entropy, typosquatting ve marka benzerliği gibi özellikler çıkarılır.
- **Model eğitimi:** Random Forest, Decision Tree, Extra Trees, LightGBM, XGBoost, ANN, DNN, CNN ve LSTM gibi farklı modeller denenir.
- **Web arayüzü:** Flask tabanlı basit bir GUI ile URL girilir, model seçilir ve tahmin sonucu görüntülenir.

> Etiketleme mantığı: `0 = güvenli`, `1 = phishing / tehlikeli`

---

## EN | Project Overview

This repository contains a phishing URL detection pipeline with three main parts:

- **Feature extraction:** Extracts URL-based features such as length, character counts, tokens, TLD checks, IP detection, entropy, typosquatting signals, and brand indicators.
- **Model training:** Includes experiments with Random Forest, Decision Tree, Extra Trees, LightGBM, XGBoost, ANN, DNN, CNN, and LSTM models.
- **Web interface:** Provides a Flask GUI where users can enter a URL, select a model, and view the prediction result.

> Label convention: `0 = legitimate`, `1 = phishing / malicious`

---

## Features | Özellikler

- 66 URL-based feature extraction
- Multiple classical ML and deep learning models
- Flask-based prediction interface
- Model result reports and confusion matrix images
- Feature extraction timing and prediction timing in GUI
- TLD list support
- Typosquatting and suspicious keyword checks

---

## Project Structure | Proje Yapısı

```text
phishurl/
├── feature_extract/
│   ├── phishurl_feacture_extract.py
│   ├── tldlist.txt
│   └── 4M_dataset_last_extracted_features.csv
├── gui/
│   ├── app.py
│   ├── feature_extraction.py
│   ├── phishurldetectiongui.py
│   ├── tldlist.txt
│   └── templates/
│       └── index.html
├── models/
│   ├── ann/
│   ├── cnn/
│   ├── dnn/
│   ├── dt/
│   ├── lgbm/
│   ├── rf/
│   └── xgb/
├── train/
│   ├── anncode.py
│   ├── cnncode.py
│   ├── decisiontree.py
│   ├── dnncode.py
│   ├── extratree.py
│   ├── fulltrain-full-featurecode.py
│   ├── lightgbmmodel.py
│   ├── logisticregression.py
│   ├── ltsmcode.py
│   └── randomforest.py
├── datasets.zip
├── requirements.txt
└── README.md
```

---

## Dataset | Veri Seti

Large dataset files are not included directly in this repository because they exceed GitHub's file size limit.

Büyük veri dosyaları GitHub dosya boyutu limitini aştığı için repository içine doğrudan eklenmemiştir.

| File | Link |
|---|---|
| `datasets.zip` | [Google Drive folder](https://drive.google.com/drive/folders/1psaEZ4OS-pbuVQrEErKLm5prFuLb_pWU?usp=sharing) |
| `feature_extract/4M_dataset_last_extracted_features.csv` | [Google Drive file](https://drive.google.com/file/d/1OEI-7I0oQi4X71ATP0744XyHs9tzwjVD/view?usp=sharing) |

After downloading, place the files in the same paths shown above if you want to run training scripts locally.

İndirdikten sonra eğitim scriptlerini yerelde çalıştırmak için dosyaları tabloda gösterilen aynı yollara yerleştirin.

---

## Model Results | Model Sonuçları

| Model | Test Accuracy | F1 Score | AUC |
|---|---:|---:|---:|
| Random Forest | 0.9640 | 0.9640 | 0.9931 |
| XGBoost | 0.9587 | 0.9587 | 0.9935 |
| CNN | 0.9587 | 0.9587 | 0.9935 |
| Decision Tree | 0.9560 | 0.9560 | 0.9857 |
| ANN | 0.9547 | 0.9546 | 0.9920 |
| LightGBM | 0.9541 | 0.9541 | 0.9921 |
| DNN | 0.9219 | 0.9215 | 0.9175 |

> Results are taken from the model result files under the `models/` directory.

---

## Installation | Kurulum

### 1. Clone the repository

```bash
git clone https://github.com/<username>/<repository-name>.git
cd phishurl
```

### 2. Create environment

`requirements.txt` is a conda-style environment export for macOS ARM64. The recommended setup is:

```bash
conda create --name phishurl --file requirements.txt
conda activate phishurl
```

If you prefer pip, install the main dependencies manually:

```bash
pip install flask flask-cors numpy pandas scikit-learn tensorflow keras joblib matplotlib seaborn tldextract fuzzywuzzy requests beautifulsoup4
```

---

## Usage | Kullanım

### Run the Flask GUI | Flask arayüzünü çalıştırma

```bash
cd gui
python app.py
```

Then open:

```text
http://127.0.0.1:5000
```

Steps:

1. Enter a URL.
2. Select a model.
3. Click the prediction button.
4. View the prediction result and extracted features.

---

## Important Note | Önemli Not

The GUI loads model files from paths defined in `gui/app.py` under `MODEL_PATHS`.

GUI, modelleri `gui/app.py` içindeki `MODEL_PATHS` sözlüğünden yükler.

If you clone this repository and run it directly, make sure the paths point to the included `models/` directory. For example:

```python
MODEL_PATHS = {
    "Decision Tree (pkl)": "../models/dt/dt-full-feature.pkl",
    "LightGbm (pkl)": "../models/lgbm/lgbm-full-feature.pkl",
    "XGBoost (pkl)": "../models/xgb/xgb-full-feature.pkl",
    "ANN (h5)": "../models/ann/ann-model.h5",
    "DNN (h5)": "../models/dnn/dnn-model.h5",
    "CNN (h5)": "../models/cnn/f-cnn-model.h5",
}
```

---

## Training | Model Eğitimi

Training scripts are located in the `train/` directory.

Eğitim scriptleri `train/` klasöründedir.

Example:

```bash
cd train
python randomforest.py
python cnncode.py
```

Before training, verify that the dataset path inside each script points to your extracted dataset.

Eğitimden önce scriptlerin içindeki dataset yolunun kendi veri setinizi gösterdiğinden emin olun.

---

## Feature Extraction | Özellik Çıkarımı

Feature extraction logic is available in:

```text
gui/feature_extraction.py
feature_extract/phishurl_feacture_extract.py
```

Extracted feature groups include:

- URL, domain, hostname, path and query length features
- Special character counts
- Digit and letter ratios
- HTTP/HTTPS token checks
- IP address detection
- Punycode detection
- Known TLD checks
- Suspicious keyword checks such as `login`, `bank`, `secure`, `account`, `confirm`, `token`, `free`
- Entropy calculation
- Typosquatting similarity checks

---

## Technologies | Teknolojiler

- Python
- Flask
- NumPy
- Pandas
- Scikit-learn
- TensorFlow / Keras
- LightGBM
- XGBoost
- Matplotlib / Seaborn
- Bootstrap

---

## Disclaimer | Sorumluluk Reddi

TR: Bu proje akademik/deneysel phishing URL tespiti amacıyla geliştirilmiştir. Tek başına güvenlik kararı vermek için kullanılmamalı; gerçek sistemlerde ek kontroller, güncel tehdit istihbaratı ve uzman değerlendirmesi ile desteklenmelidir.

EN: This project is intended for academic/experimental phishing URL detection. It should not be used as the only security decision mechanism in production systems. Real-world deployments should include additional validation, updated threat intelligence, and expert review.

---

## License | Lisans

No license file is currently included in this repository. Add a license before public distribution if needed.

Bu repository içinde henüz bir lisans dosyası bulunmamaktadır. Herkese açık kullanım veya dağıtım için lisans eklenmesi önerilir.
