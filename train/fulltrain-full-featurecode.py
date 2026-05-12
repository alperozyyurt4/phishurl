import pandas as pd
import numpy as np
import time
import joblib
import xgboost as xgb
from matplotlib import pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix

# CSV'yi oku
df = pd.read_csv("../notebooks/4m_dataset_last_extracted_feature.csv")

# ID veya URL model için gereksiz olabilir, düşürüyoruz
df.drop(columns=["id", "url"], inplace=True)

# Bağımsız değişkenler (X) ve hedef değişken (y)
X = df.drop(columns=["label"])  # Özellikler
y = df["label"]  # Etiket (sınıf)

# Veriyi %80 eğitim, %20 test olarak bölme
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

print(f"Train Set: {X_train.shape}, Test Set: {X_test.shape}")

# Çapraz doğrulama için Stratified K-Fold
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

#  MODEL OLUŞTURMA (Makine Öğrenmesi algoritma modellerini tanımla)
model = xgb.XGBClassifier(n_estimators=100, random_state=42, use_label_encoder=False, eval_metric='logloss', n_jobs=-1)

# Eğitimi başlatmadan önce zaman ölçümü
start_time = time.time()

# 5 Katlı Cross Validation ile model eğitimi ve değerlendirme
cv_scores = cross_val_score(model, X_train, y_train, cv=cv, scoring="accuracy")

# Eğitim süresi hesapla
training_time = time.time() - start_time

print(f"Cross-validation Accuracy Scores: {cv_scores}")
print(f"Mean CV Accuracy: {np.mean(cv_scores):.4f}")
print(f"Training Time: {training_time:.2f} seconds")

# Modeli tüm eğitim verisi ile eğitme
start_time = time.time()
model.fit(X_train, y_train)
training_time_final = time.time() - start_time

# Test seti ile değerlendirme
start_time = time.time()
y_pred = model.predict(X_test)
test_time = time.time() - start_time

# Performans metriklerini hesapla
test_accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred, average="weighted")
recall = recall_score(y_test, y_pred, average="weighted")
f1 = f1_score(y_test, y_pred, average="weighted")

# ROC AUC skoru
if len(np.unique(y_test)) == 2:
    auc_score = roc_auc_score(y_test, model.predict_proba(X_test)[:, 1])
else:
    auc_score = "N/A"

print(f"Test Set Accuracy: {test_accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall: {recall:.4f}")
print(f"F1 Score: {f1:.4f}")
print(f"AUC Score: {auc_score}")
print(f"Final Training Time: {training_time_final:.2f} seconds")
print(f"Test Time: {test_time:.2f} seconds")

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
        plt.text(j, i, str(cm[i, j]), horizontalalignment="center", color="white" if cm[i, j] > cm.max() / 2 else "black")

plt.show()

# Modeli kaydetme
model_filename = "xgb-full-feature.pkl"
joblib.dump(model, model_filename)
print(f"Model saved as {model_filename}")

# Sonuçları bir dosyaya kaydetme
with open("xgb-full-feature.txt", "w") as f:
    f.write(f"Cross-validation Accuracy Scores: {cv_scores}\n")
    f.write(f"Mean CV Accuracy: {np.mean(cv_scores):.4f}\n")
    f.write(f"Training Time: {training_time:.2f} seconds\n")
    f.write(f"Final Training Time: {training_time_final:.2f} seconds\n")
    f.write(f"Test Set Accuracy: {test_accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall: {recall:.4f}\n")
    f.write(f"F1 Score: {f1:.4f}\n")
    f.write(f"AUC Score: {auc_score}\n")
    f.write(f"Test Time: {test_time:.2f} seconds\n")

print("Training results saved to xgb-full-feature.txt")
