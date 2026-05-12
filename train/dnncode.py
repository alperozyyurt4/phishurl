import pandas as pd
import numpy as np
import time
import tensorflow as tf
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from matplotlib import pyplot as plt

# CSV'yi oku
df = pd.read_csv("../notebooks/4m_dataset_last_extracted_feature.csv")

# ID veya URL model için gereksiz olabilir, düşürüyoruz
df.drop(columns=["id", "url"], inplace=True)

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["label"])  # Özellikler
y = df["label"]  # Etiket (sınıf)

dnnscaler = StandardScaler()
X = dnnscaler.fit_transform(X)

# Veriyi %80 eğitim, %20 test olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

print(f"Train Set: {X_train.shape}, Test Set: {X_test.shape}")

# Çapraz doğrulama için Stratified K-Fold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)


# Modeli oluşturma fonksiyonu
def create_dnn_model():
    model = Sequential()
    model.add(Dense(64, input_dim=X_train.shape[1], activation='relu'))  # Tek gizli katman
    model.add(Dense(128, activation='relu'))  # 2. gizli katman
    model.add(Dense(256, activation='relu'))  # 3. gizli katman
    model.add(Dense(128, activation='relu'))  # 4. gizli katman
    model.add(Dense(64, activation='relu'))  # 5. gizli katman
    model.add(Dense(1, activation='sigmoid'))  # Çıktı katmanı (binary sınıflandırma için sigmoid)
    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model


# 5 Katlı Cross Validation ile model eğitimi ve değerlendirme
cv_scores = []
cv_time = []

start_time = time.time()
for train_idx, val_idx in cv.split(X_train, y_train):
    X_cv_train, X_cv_val = X_train.iloc[train_idx], X_train.iloc[val_idx]
    y_cv_train, y_cv_val = y_train.iloc[train_idx], y_train.iloc[val_idx]

    # Modeli oluştur
    model = create_dnn_model()

    # Modeli eğit (epoch sayısını arttırabilirsiniz)
    history = model.fit(X_cv_train, y_cv_train, epochs=10, batch_size=32, validation_data=(X_cv_val, y_cv_val),
                        verbose=0)

    # Validasyon setiyle değerlendirme
    val_loss, val_acc = model.evaluate(X_cv_val, y_cv_val, verbose=0)
    cv_scores.append(val_acc)

cv_time.append(time.time() - start_time)

print(f"Cross-validation Accuracy Scores: {cv_scores}")
print(f"Mean CV Accuracy: {np.mean(cv_scores):.4f}")
print(f"CV Training Time: {cv_time[0]:.2f} seconds")

# Modeli tüm eğitim verisi ile eğitme
model = create_dnn_model()
start_time = time.time()

# Eğitim sırasında doğruluk ve kayıp değerlerini kaydet
history = model.fit(X_train, y_train, epochs=10, batch_size=32, validation_data=(X_test, y_test), verbose=1)

training_time_final = time.time() - start_time

# Test seti ile değerlendirme
y_pred = (model.predict(X_test) > 0.5).astype("int32")

# Performans metriklerini hesapla
test_accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

# ROC AUC skoru
auc_score = roc_auc_score(y_test, model.predict(X_test))

print(f"Test Set Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"AUC Score: {auc_score:.4f}")
print(f"Final Training Time: {training_time_final:.2f} seconds")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
print(cm)

plt.figure(figsize=(8, 6))
plt.imshow(cm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['Güvenli', 'Phishing'], rotation=45)
plt.yticks(tick_marks, ['Güvenli', 'Phishing'])
plt.xlabel('Tahmin Edilen')
plt.ylabel('Gerçek Değer')

for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm[i, j]), horizontalalignment="center",
                 color="white" if cm[i, j] > cm.max() / 2 else "black")

plt.show()

# Modeli kaydetme (H5 formatında)
model_filename = "dnn-model.h5"
model.save(model_filename)  # Modeli H5 formatında kaydediyoruz
print(f"Model saved as {model_filename}")

# Sonuçları bir dosyaya kaydetme
with open("dnn-model-results.txt", "w") as f:
    f.write(f"Cross-validation Accuracy Scores: {cv_scores}\n")
    f.write(f"Mean CV Accuracy: {np.mean(cv_scores):.4f}\n")
    f.write(f"CV Training Time: {cv_time[0]:.2f} seconds\n")
    f.write(f"Final Training Time: {training_time_final:.2f} seconds\n")
    f.write(f"Test Set Accuracy: {test_accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")
    f.write(f"AUC Score: {auc_score:.4f}\n")

print("Training results saved to dnn-model-results.txt")

# Grafiklerle eğitim ve doğruluk kaybını görselleştirme
# Eğitim kaybı ve doğruluğunu çizme
plt.figure(figsize=(12, 6))

## Eğitim doğruluğu ve kaybı grafiklerini çizme
plt.figure(figsize=(12, 6))

# Doğruluk grafiği
plt.subplot(1, 2, 1)
plt.plot(history.history['accuracy'], label='Eğitim Doğruluğu')
plt.plot(history.history['val_accuracy'], label='Validasyon Doğruluğu')
plt.title('Eğitim ve Validasyon Doğruluğu')
plt.xlabel('Epochs')
plt.ylabel('Doğruluk')
plt.legend()

# Kayıp grafiği
plt.subplot(1, 2, 2)
plt.plot(history.history['loss'], label='Eğitim Kayıp')
plt.plot(history.history['val_loss'], label='Validasyon Kayıp')
plt.title('Eğitim ve Validasyon Kayıp')
plt.xlabel('Epochs')
plt.ylabel('Kayıp')
plt.legend()

# Grafikleri gösterme
plt.tight_layout()
plt.show()

import joblib
joblib.dump(dnnscaler, "dnnscaler22.pkl")
print("Scaler başarıyla kaydedildi.")