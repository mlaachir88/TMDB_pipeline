FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip
RUN pip install dagster dagster-cloud duckdb pandas requests matplotlib seaborn scikit-learn dagster-webserver pytest

# Permet au container de se relancer proprement à chaque fois
EXPOSE 3000
EXPOSE 3001

CMD ["dagster", "dev", "-h", "0.0.0.0"]
