from setuptools import setup, find_packages

setup(
    name="stat386stonks",
    version="0.1.0",
    description="STAT 386 final project: Alpha Vantage stock data pipeline + analysis tools",
    authors = ["Cameron Hamilton", "Ridge Atwood"],
    url = "https://github.com/chamiltonb8/final_project",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "requests",
        "python-dotenv",
        "scikit-learn",
        "seaborn",
    ],
    python_requires=">=3.10",
)