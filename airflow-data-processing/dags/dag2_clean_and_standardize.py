from airflow.sdk import dag,task
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import pandas as pd

DATA_DIR = "/opt/airflow/data"
TRAIN_DATA_PATH = "/opt/airflow/data/train.csv"
CLEANED_PATH = f"{DATA_DIR}/train_cleaned.csv"
FINAL_PATH = f"{DATA_DIR}/train_processed.csv"
SCALED_PATH = f"{DATA_DIR}/train_scaled.csv"

@dag (
    dag_id="clean_and_standardize"
)

def dag2_clean_and_standardize():


    @task.python
    def load():
        """Loads the dataframe object from trained data set initialized by DAG1

        Returns :
            Training data's file path to be used by the 2nd task in this DAG
        """
        df = pd.read_csv(TRAIN_DATA_PATH)

        return TRAIN_DATA_PATH

    @task.python
    def clean_data(path):
        """Loads the dataframe object coming from previous task, finds numeric columns and fill empty columns
        by mean of the whole column, finds categorical columns and fills empty columns with the most
        frequent categorical value.
            Searches for duplicates values and removes them if there is one.

        Args:
            path: Training data csv file's path from docker linux virtual machine.

        Returns:
            Cleaned data is saved in another file under /opt/airflow/data path in docker environment and returned
            """
        df = pd.read_csv(path).drop(columns=["rownames"])

        num_cols = df.select_dtypes(include="number").columns
        cat_cols = df.select_dtypes(exclude="number").columns

        df[num_cols] = SimpleImputer(strategy="mean").fit_transform(df[num_cols])
        df[cat_cols] = SimpleImputer(strategy="most_frequent").fit_transform(df[cat_cols])

        num_duplicates = df.duplicated().sum()

        if num_duplicates > 0:
            print(f"Found {num_duplicates} duplicates. Removing them.")
            df = df.drop_duplicates()
        else:
            print("No duplicates found.")

        df.to_csv(CLEANED_PATH, index=False)
        print(f"Data processed and saved to {CLEANED_PATH}")
        return CLEANED_PATH

    @task.python
    def standardize(path):
        """Loads the dataframe object coming from the previous task, standardization is done in this function.
        The logic is to reduce/cancel the dominant numeric value. For example first row tuition is 0.8891500234603882 , however
        score is 51.84000015258789 which would cause score to dominate other numerical values in this data set when we use ML algorithms. Standardization is a mandatory data preprocessing
        and changes all numerical values to [-3;3]
         Args:
            path: Cleaned data csv file's path from docker linux virtual machine.

        Returns:
            Scaled data is saved in another file under /opt/airflow/data path in docker environment and returned
        """

        df = pd.read_csv(path)

        num_cols = df.select_dtypes(include="number").columns
        df[num_cols] = StandardScaler().fit_transform(df[num_cols])

        df.to_csv(SCALED_PATH, index=False)
        return SCALED_PATH

    @task.python
    def save(path):
        df = pd.read_csv(path)
        df.to_csv(FINAL_PATH, index=False)

    first = load()
    second = clean_data(first)
    third = standardize(second)
    fourth = save(third)

dag2_clean_and_standardize()
