# tmdb_pipeline/ml/profit_classification.py

import duckdb
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

#  Connexion à la base principale (1 seul fichier .duckdb dans tout le projet)
con = duckdb.connect("../tmdb_data.duckdb")  # attention au chemin

#  Charger les films nettoyés
df = con.sql("SELECT * FROM clean_movies").fetchdf()

#  Créer la variable cible binaire : rentable ou non
df["is_profitable"] = df["profit"].apply(lambda x: 1 if x > 0 else 0)

#  Colonnes utiles pour prédiction
features = ["budget", "runtime", "vote_average", "vote_count", "release_year"]
df_model = df[features + ["is_profitable"]].dropna()

#  Séparer X et y
X = df_model[features]
y = df_model["is_profitable"]

#  Split train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  Standardiser
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#  Entraîner modèle (régression logistique)
model = LogisticRegression()
model.fit(X_train_scaled, y_train)

#  Prédictions
y_pred = model.predict(X_test_scaled)

#  Évaluation
accuracy = accuracy_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n=== Résultats du modèle ===")
print(f"Accuracy : {accuracy:.2f}")
print(f"F1-score : {f1:.2f}")
print("\nClassification Report :")
print(classification_report(y_test, y_pred))

#  Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Non rentable", "Rentable"],
            yticklabels=["Non rentable", "Rentable"])
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de confusion - Rentabilité des films")
plt.tight_layout()

#  Sauvegarde (corrigée)
plt.savefig("ml/confusion_matrix_profit.png")
plt.close()


print(" Modèle entraîné et matrice de confusion sauvegardée dans 'tmdb_pipeline/ml/confusion_matrix_profit.png'")
