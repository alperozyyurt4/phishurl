from sklearn.linear_model import LogisticRegression
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score

# CSV dosyanı buraya yükle (dosya adını güncelle)
df = pd.read_csv("../notebooks/4m_dataset_last_extracted_feature.csv")

# Gereksiz sütunları kaldıralım (ID ve URL model için gereksiz)
df.drop(columns=['id', 'url'], inplace=True)

# Bağımsız değişkenler (X) ve bağımlı değişken (y)
X = df.drop(columns=['label'])  # Özellikler (features)
y = df['label']                 # Hedef değişken (0 = güvenli, 1 = phishing)

# Veriyi %80 eğitim, %20 test olarak ayıralım
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"Train Set: {X_train.shape}, Test Set: {X_test.shape}")


lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)
y_pred = lr_model.predict(X_test)

print("Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))