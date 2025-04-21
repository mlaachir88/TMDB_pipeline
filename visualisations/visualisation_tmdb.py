import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

#  Créer un dossier "visualisations" s'il n'existe pas
OUTPUT_DIR = "visualisations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

#  Charger les données depuis DuckDB
con = duckdb.connect("tmdb_data.duckdb")
df = con.sql("SELECT * FROM clean_movies").fetchdf()

#  Style
sns.set(style="whitegrid")

# 1. Histogramme des notes
plt.figure(figsize=(10, 6))
plt.hist(df["vote_average"].dropna(), bins=20, color="skyblue", edgecolor="black")
plt.title("Distribution des notes moyennes")
plt.xlabel("Note moyenne")
plt.ylabel("Nombre de films")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/1_histogram_vote_average.png")
plt.close()

# 2. Top 10 genres
all_genres = df["genre_names"].explode().dropna()
genre_counts = all_genres.value_counts().head(10)

plt.figure(figsize=(10, 6))
sns.barplot(x=genre_counts.values, y=genre_counts.index, palette="viridis")
plt.title("Top 10 des genres les plus fréquents")
plt.xlabel("Nombre de films")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/2_top_genres.png")
plt.close()

# 3. Profit moyen par année
profit_by_year = df.groupby("release_year")["profit"].mean().dropna()

plt.figure(figsize=(12, 6))
sns.lineplot(x=profit_by_year.index, y=profit_by_year.values, marker="o")
plt.title("Profit moyen par année")
plt.xlabel("Année de sortie")
plt.ylabel("Profit moyen ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/3_profit_par_annee.png")
plt.close()

# 4. Durée vs Note
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df, x="runtime", y="vote_average", alpha=0.6)
plt.title("Durée du film vs Note moyenne")
plt.xlabel("Durée (minutes)")
plt.ylabel("Note moyenne")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/4_runtime_vs_vote.png")
plt.close()



# 5. Boxplot du profit par genre (corrigé)
exploded = df.explode("genre_names").reset_index(drop=True)

plt.figure(figsize=(14, 8))
sns.boxplot(
    data=exploded,
    x="profit",
    y="genre_names",
    orient="h",
    palette="coolwarm",
    showfliers=False
)
plt.title("Distribution des profits par genre")
plt.xlabel("Profit ($)")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/5_boxplot_profit_genres.png")
plt.close()


# 6. Moyenne des votes par genre
plt.figure(figsize=(12, 6))
mean_votes = exploded.groupby("genre_names")["vote_average"].mean().sort_values(ascending=False).head(10)
sns.barplot(x=mean_votes.values, y=mean_votes.index, palette="crest")
plt.title("Top 10 genres par note moyenne")
plt.xlabel("Note moyenne")
plt.ylabel("Genre")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/6_moyenne_votes_genres.png")
plt.close()

# 7. Corrélation budget vs revenue (avec ligne de tendance)
plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="budget",
    y="revenue",
    scatter_kws={"alpha": 0.5},
    line_kws={"color": "red"},
)
plt.title("Corrélation entre budget et revenue (avec régression)")
plt.xlabel("Budget ($)")
plt.ylabel("Revenue ($)")
plt.tight_layout()
plt.savefig(f"{OUTPUT_DIR}/7_budget_vs_revenue.png")
plt.close()



print(" Visualisations générées dans le dossier 'visualisations/'.")
