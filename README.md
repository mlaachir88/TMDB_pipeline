#  TMDB Data Pipeline with Dagster

> A complete end-to-end data pipeline using [TMDB API](https://developer.themoviedb.org/) and [Dagster](https://dagster.io/) for extraction, transformation, orchestration, storage, visualization, and analysis — fully containerized with Docker.

---

##  Project Objective

This project was built as part of the **4DATA** course (Data Engineering – Master 1). The goal is to implement a complete **data pipeline**, from **data ingestion to analysis and machine learning**, with orchestration and deployment practices:

- Extract data from the **TMDB API**
- Transform and clean it
- Store it in a lightweight database (**DuckDB**)
- Visualize insights using **Matplotlib** and **Seaborn**
- Apply **machine learning** for prediction (bonus)
- Orchestrate everything with **Dagster**
- Add tests, monitoring, and containerization with **Docker**

---

##  Project Structure

```bash
tmdb_pipeline/
├── tmdb_pipeline/
│   ├── assets/
│   │   ├── tmdb_api.py              # Data extraction from TMDB API
│   │   ├── transform.py             # Data cleaning & enrichment
│   │   └── store_to_duckdb.py       # Saving to DuckDB
│   ├── ml/
│   │   ├── profit_prediction.py     # ML: Predict profit
│   │   └── vote_success_prediction.py # ML: Predict success by votes
│   ├── schedules.py                 # Dagster schedules
│   ├── sensors.py                   # Dagster sensors
│   ├── definitions.py               # Main Dagster definitions
│   └── debug_duckdb.py              # Debug tool for database
├── tmdb_pipeline_tests/
│   └── test_assets.py               # Unit tests
├── visualisations/
│   ├── *.png                        # All generated plots
│   └── visualisation_tmdb.py        # Code for generating visuals
├── .env                             # API Key (not committed)
├── Dockerfile                       # Full container setup
├── setup.py                         # Install project locally
├── dagster.yaml                     # (Optional) disable telemetry
├── tmdb_data.duckdb                 # Local DuckDB database
├── .dockerignore                    # Ignore sensitive/dev files
└── README.md                        # This file
```

---

##  Quickstart Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/tmdb_pipeline.git
cd tmdb_pipeline
```

### 2. Add Your TMDB API Key
Create a `.env` file at the root:
```dotenv
TMDB_API_KEY=your_tmdb_api_key_here
```

### 3. Build Docker Image
```bash
docker build -t dagster-tmdb .
```

### 4. Run the Pipeline in Docker
```bash
docker run --env-file .env -p 3000:3000 -p 3001:3001 dagster-tmdb
```

### 5. Open Dagster UI
 [http://localhost:3000](http://localhost:3000)

---

##  Assets Overview

###  Extraction
- `fetch_genres`
- `fetch_now_playing_movies`
- `fetch_popular_movies`
- `fetch_top_rated_movies`

###  Enrichment
- `fetch_movie_details`
- `fetch_movie_reviews`

###  Transformation
- `clean_movies_data`

###  ML (Bonus)
- `profit_prediction`
- `vote_success_prediction`

###  Storage
- `save_movies_to_duckdb`

---

## ⏱ Orchestration

| Feature          | Description                                      |
|------------------|--------------------------------------------------|
|  Schedules     | e.g. `daily_clean_schedule` every 24h            |
|  Sensors       | Trigger runs on new popular movies detection     |
|  Dagster Daemon| Handles background orchestration & monitoring    |

---

##  Unit Testing

All core assets are tested with `pytest`. Example:
```bash
pytest tmdb_pipeline_tests/
```

Sample test cases:
- Validate movie genre fetching
- Validate popularity data structure
- Validate API failure fallback

---

##  Visualizations

Insights generated using `matplotlib` & `seaborn`:

-  Histogram of vote averages
-  Top 10 most frequent genres
-  Average profit per year
-  Runtime vs Vote Average scatterplot
-  Boxplot of profit by genre
-  Average vote per genre
-  Budget vs Revenue correlation (with regression line)

All plots are saved in `/visualisations/`.

---

##  Machine Learning

**Objective**: Predict movie success using ML classification.

- Logistic Regression
- Random Forest
- Based on vote average, genres, runtime, popularity

All models are tested on real TMDB samples.

---

## 🐳 Dockerized Setup

The full environment is packaged in Docker:

- Based on `python:3.10-slim`
- Includes `.env` loading
- Easy to run anywhere: just `docker run ...`

Sample Dockerfile:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install dagster dagster-cloud duckdb pandas requests matplotlib seaborn scikit-learn dagster-webserver pytest

EXPOSE 3000
EXPOSE 3001

CMD ["dagster", "dev", "-h", "0.0.0.0"]
```

---

##  Final Feature Summary

| Feature                        | Status |
|-------------------------------|--------|
| API Extraction (TMDB)         | ✅     |
| Data Cleaning & Enrichment    | ✅     |
| Storage with DuckDB           | ✅     |
| Data Visualization            | ✅     |
| Machine Learning (Bonus)      | ✅     |
| Dagster Orchestration         | ✅     |
| Schedule & Sensor Integration | ✅     |
| Unit Testing                  | ✅     |
| Docker Container              | ✅     |

---

##  Screenshots

All screenshots of Dagster runs, lineage graphs, visualizations, etc., are available in the external folder:

 `Screens_Outputs/`

This allows easy review without needing to re-run the full pipeline.

---

##  Author

**Mohamed Laachir**  
📚 Master 1 Data Engineering  
📅 2025 — Mini-Projet 4DATA  
💼 Contact: LinkedIn 

---

##  Notes

- TMDB API was chosen for its rich real-time movie dataset.
- Dagster offers best practices for production pipelines.
- DuckDB provides local analytics-ready storage.
- This pipeline follows modular, testable, and portable design.

---

##  Resources

- [TMDB API Docs](https://developer.themoviedb.org/)
- [Dagster Documentation](https://docs.dagster.io/)
- [DuckDB Docs](https://duckdb.org/)
- [Seaborn Docs](https://seaborn.pydata.org/)
- [Scikit-learn](https://scikit-learn.org/stable/)

---

##  Submission Notes

- `.env` is not included in the repo for security.
- All code was developed, tested, and validated inside Docker.
- Screenshots and visual outputs included in `Screens_Outputs`.

---

*Projet terminé et validé avec succès.*  
*Merci pour la lecture !*