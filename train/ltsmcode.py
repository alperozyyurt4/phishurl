import pandas as pd
import numpy as np
import time
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
from tensorflow.keras.optimizers import Adam
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

import matplotlib.pyplot as plt

# CSV'yi oku
df = pd.read_csv("../notebooks/100k-dataset.csv")

# Gereksiz sütunları kaldır
df.drop(columns=["id", "url"], inplace=True)

# Özellikler ve etiket
X = df.drop(columns=["label"]).values
y = df["label"].values

# Eğitim/test bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

# LSTM için veriyi 3 boyutlu hale getir (örnek sayısı, zaman adımı, özellik sayısı)
X_train_lstm = np.expand_dims(X_train, axis=-1)  # zaman adımı olarak 1 kabul ediyoruz
X_test_lstm = np.expand_dims(X_test, axis=-1)
# LSTM modeli
def create_lstm_model():
    model = Sequential()
    model.add(LSTM(64, input_shape=(X_train_lstm.shape[1], X_train_lstm.shape[2]), return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(128, return_sequences=True))
    model.add(Dropout(0.3))

    model.add(LSTM(256, return_sequences=False))
    model.add(Dropout(0.3))

    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1, activation='sigmoid'))

    model.compile(optimizer=Adam(), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Modeli oluştur
lstm_model = create_lstm_model()

# Eğitimi başlat
start_time = time.time()
history_lstm = lstm_model.fit(X_train_lstm, y_train, epochs=75, batch_size=64, validation_data=(X_test_lstm, y_test), verbose=1)
training_time_lstm = time.time() - start_time

# Tahmin yap
y_pred_lstm = (lstm_model.predict(X_test_lstm) > 0.5).astype("int32")

# Metrikler
test_accuracy_lstm = accuracy_score(y_test, y_pred_lstm)
precision_lstm = precision_score(y_test, y_pred_lstm, average="weighted")
recall_lstm = recall_score(y_test, y_pred_lstm, average="weighted")
f1_lstm = f1_score(y_test, y_pred_lstm, average="weighted")
auc_lstm = roc_auc_score(y_test, lstm_model.predict(X_test_lstm))

# Sonuçlar
print(f"LSTM Test Set Accuracy: {test_accuracy_lstm:.4f}")
print(f"LSTM Precision: {precision_lstm:.4f}")
print(f"LSTM Recall: {recall_lstm:.4f}")
print(f"LSTM F1 Score: {f1_lstm:.4f}")
print(f"LSTM AUC Score: {auc_lstm:.4f}")
print(f"LSTM Final Training Time: {training_time_lstm:.2f} seconds")

# Confusion matrix
cm_lstm = confusion_matrix(y_test, y_pred_lstm)
plt.figure(figsize=(8, 6))
plt.imshow(cm_lstm, interpolation='nearest', cmap=plt.cm.Blues)
plt.title('LSTM Confusion Matrix')
plt.colorbar()
tick_marks = np.arange(2)
plt.xticks(tick_marks, ['Güvenli', 'Phishing'], rotation=45)
plt.yticks(tick_marks, ['Güvenli', 'Phishing'])
plt.xlabel('Tahmin Edilen')
plt.ylabel('Gerçek Değer')

for i in range(2):
    for j in range(2):
        plt.text(j, i, str(cm_lstm[i, j]), horizontalalignment="center",
                 color="white" if cm_lstm[i, j] > cm_lstm.max() / 2 else "black")

plt.show()

# Eğitim & doğrulama kayıp/grafikleri
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.plot(history_lstm.history['accuracy'], label='Eğitim Doğruluğu')
plt.plot(history_lstm.history['val_accuracy'], label='Validasyon Doğruluğu')
plt.title('LSTM Eğitim ve Validasyon Doğruluğu')
plt.xlabel('Epochs')
plt.ylabel('Doğruluk')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history_lstm.history['loss'], label='Eğitim Kayıp')
plt.plot(history_lstm.history['val_loss'], label='Validasyon Kayıp')
plt.title('LSTM Eğitim ve Validasyon Kayıp')
plt.xlabel('Epochs')
plt.ylabel('Kayıp')
plt.legend()

plt.tight_layout()
plt.show()

# Modeli kaydet
lstm_model_filename = "nocvcode/nocv-lstm-model.h5"
lstm_model.save(lstm_model_filename)
print(f"LSTM Model saved as {lstm_model_filename}")

# Sonuçları dosyaya yaz
with open("nocvcode/nocv-lstm-model-results.txt", "w") as f:
    f.write(f"LSTM Test Set Accuracy: {test_accuracy_lstm:.4f}\n")
    f.write(f"LSTM Precision: {precision_lstm:.4f}\n")
    f.write(f"LSTM Recall: {recall_lstm:.4f}\n")
    f.write(f"LSTM F1 Score: {f1_lstm:.4f}\n")
    f.write(f"LSTM AUC Score: {auc_lstm:.4f}\n")
    f.write(f"LSTM Final Training Time: {training_time_lstm:.2f} seconds\n")

print("LSTM training results saved to nocv-lstm-model-results.txt")