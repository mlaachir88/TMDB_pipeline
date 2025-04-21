from setuptools import find_packages, setup

setup(
    name="tmdb_pipeline",
    packages=find_packages(exclude=["tmdb_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "duckdb",
        "pandas",
        "requests",
        "matplotlib",
        "seaborn",
        "scikit-learn"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)