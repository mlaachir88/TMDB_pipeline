import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Connexion à DuckDB (à la racine du projet)
con = duckdb.connect("../tmdb_data.duckdb")
df = con.sql("SELECT * FROM clean_movies").fetchdf()

#  Créer la cible binaire : succès critique (vote >= 7)
df["is_highly_rated"] = df["vote_average"].apply(lambda x: 1 if x >= 7 else 0)

#  Features pour entraîner le modèle
features = ["budget", "runtime", "vote_count", "release_year", "profit"]
df_model = df[features + ["is_highly_rated"]].dropna()

X = df_model[features]
y = df_model["is_highly_rated"]

#  Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

#  Standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

#  Random Forest Classifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train_scaled, y_train)
y_pred = model.predict(X_test_scaled)

#  Évaluation
acc = accuracy_score(y_test, y_pred)
print(f"\n Accuracy : {acc:.2f}\n")
print(" Rapport de classification :\n", classification_report(y_test, y_pred))

#  Matrice de confusion
cm = confusion_matrix(y_test, y_pred)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
            xticklabels=["Pas succès critique", "Succès critique"],
            yticklabels=["Pas succès critique", "Succès critique"])
plt.xlabel("Prédit")
plt.ylabel("Réel")
plt.title("Matrice de confusion - Succès critique")
plt.tight_layout()
plt.savefig("ml/confusion_matrix_vote_success.png")
plt.close()




importances = model.feature_importances_
feat_names = features

plt.figure(figsize=(8, 5))
sns.barplot(x=importances, y=feat_names, palette="mako")
plt.title("Importance des variables (succès critique)")
plt.xlabel("Importance")
plt.ylabel("Variable")
plt.tight_layout()
plt.savefig("ml/feature_importance_vote_success.png")
plt.close()

print(" Matrice de confusion sauvegardée dans 'ml/confusion_matrix_vote_success.png'")
print(" Graphe des importances sauvegardé dans 'ml/feature_importance_vote_success.png'")
