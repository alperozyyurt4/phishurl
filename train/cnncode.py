import pandas as pd
import numpy as np
import time
import tensorflow as tf
from keras.layers import BatchNormalization
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv1D, MaxPooling1D, Flatten, Dense, Dropout
from sklearn.preprocessing import  StandardScaler
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt

# CSV'yi oku
df = pd.read_csv("../notebooks/4m_dataset_last_extracted_feature.csv")

# ID ve URL model için gereksizse, düşürüyoruz
df.drop(columns=["id", "url"], inplace=True)

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["label"]).values  # Özellikler
y = df["label"].values  # Etiket (sınıf)

# VERİYİ NORMALİZE ET ⬇️⬇️⬇️
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Veriyi %80 eğitim, %20 test olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

print(f"Train Set: {X_train.shape}, Test Set: {X_test.shape}")

# CNN için giriş verisini 3 boyutlu hale getirme
X_train_cnn = np.expand_dims(X_train, axis=-1)  # (num_samples, num_features, 1)
X_test_cnn = np.expand_dims(X_test, axis=-1)



def create_cnn_model():
    model = Sequential()

    # 1. Convolutional Block
    model.add(Conv1D(filters=64, kernel_size=3, activation='relu', input_shape=(X_train.shape[1], 1)))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.3))

    # 2. Convolutional Block
    model.add(Conv1D(filters=128, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.3))

    # 3. Convolutional Block
    model.add(Conv1D(filters=256, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.4))

    # 4. Convolutional Block (opsiyonel ama büyük veri için mantıklı)
    model.add(Conv1D(filters=256, kernel_size=3, activation='relu'))
    model.add(BatchNormalization())
    model.add(MaxPooling1D(pool_size=2))
    model.add(Dropout(0.4))

    model.add(Flatten())

    # Dense layers
    model.add(Dense(128, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    model.add(Dense(64, activation='relu'))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))

    # Output layer
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model




# 5 Katlı Cross Validation
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

cv_scores = []
cv_time = []

start_time = time.time()
for train_idx, val_idx in cv.split(X_train, y_train):
    X_cv_train, X_cv_val = X_train_cnn[train_idx], X_train_cnn[val_idx]
    y_cv_train, y_cv_val = y_train[train_idx], y_train[val_idx]

    # Modeli oluştur
    model = create_cnn_model()

    # Modeli eğit
    history = model.fit(X_cv_train, y_cv_train, epochs=50, batch_size=64, validation_data=(X_cv_val, y_cv_val),
                        verbose=1)

    # Validasyon setiyle değerlendirme
    val_loss, val_acc = model.evaluate(X_cv_val, y_cv_val, verbose=0)
    cv_scores.append(val_acc)

cv_time.append(time.time() - start_time)

print(f"Cross-validation Accuracy Scores: {cv_scores}")
print(f"Mean CV Accuracy: {np.mean(cv_scores):.4f}")
print(f"CV Training Time: {cv_time[0]:.2f} seconds")

# Tüm eğitim verisiyle final model eğitimi
model = create_cnn_model()
start_time = time.time()

history = model.fit(X_train_cnn, y_train, epochs=50, batch_size=64, validation_data=(X_test_cnn, y_test), verbose=1)

training_time_final = time.time() - start_time

# Test seti ile değerlendirme
y_pred = (model.predict(X_test_cnn) > 0.5).astype("int32")

# Performans metriklerini hesapla
test_accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

# ROC AUC skoru
auc_score = roc_auc_score(y_test, model.predict(X_test_cnn))

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

# Modeli kaydetme
model_filename = "cnn-model.h5"
model.save(model_filename)
print(f"Model saved as {model_filename}")

# Sonuçları dosyaya kaydetme
with open("cnn-model-results.txt", "w") as f:
    f.write(f"Cross-validation Accuracy Scores: {cv_scores}\n")
    f.write(f"Mean CV Accuracy: {np.mean(cv_scores):.4f}\n")
    f.write(f"CV Training Time: {cv_time[0]:.2f} seconds\n")
    f.write(f"Final Training Time: {training_time_final:.2f} seconds\n")
    f.write(f"Test Set Accuracy: {test_accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")
    f.write(f"AUC Score: {auc_score:.4f}\n")

print("Training results saved to cnn-model-results.txt")

# Eğitim ve doğrulama kayıplarını görselleştirme
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

plt.tight_layout()
plt.show()