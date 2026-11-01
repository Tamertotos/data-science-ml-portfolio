from airflow.sdk import dag,task
from sklearn.model_selection import train_test_split
import pandas as pd
import requests

#Dataset URL
DATASET_URL = "https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv"
DATA_DIR = "/opt/airflow/data"
RAW_PATH = "/opt/airflow/data/raw.csv"



#This dag's purpose is, with download_dataset python task, to read csv data from a URL with requests
#module, and then put them into a directory in docker's linux environment under opt/airflow/data/raw.csv
#
@dag (
    dag_id="dag1_download_split"
)
def dag1_download_split():

    @task.python
    def download_dataset():
        response = requests.get(DATASET_URL)
        response.raise_for_status()
        with open(RAW_PATH, "w") as file:
            file.write(response.text)
        print(f"Dataset downloaded to {RAW_PATH}")

    @task.python
    def split_data():
        df = pd.read_csv(RAW_PATH)

        train, fine_tune = train_test_split(df, test_size = 0.3, random_state = 42)
        train.to_csv(f"{DATA_DIR}/train.csv", index=False)
        fine_tune.to_csv(f"{DATA_DIR}/fine_tune.csv", index=False)


    first = download_dataset()
    second = split_data()

    first >> second

dag1_download_split()
