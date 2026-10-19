"""
This is a boilerplate pipeline 'data_processing'
generated using Kedro 1.7.0
"""

import pandas as pd


def is_true(x: pd.Series) -> pd.Series:
    return x == "t"


def parse_percentage(x: pd.Series) -> pd.Series:
    return x.str.replace("%", "").astype(float)


def parse_money(x: pd.Series) -> pd.Series:
    return x.str.replace("$", "").str.replace(",", "").astype(float)


def preprocess_companies(df: pd.DataFrame) -> pd.DataFrame:
    df["iata_approved"] = is_true(df["iata_approved"])
    df["company_rating"] = parse_percentage(df["company_rating"])
    return df


def preprocess_shuttles(df: pd.DataFrame) -> pd.DataFrame:
    df["d_check_complete"] = is_true(df["d_check_complete"])
    df["moon_clearance_complete"] = is_true(df["moon_clearance_complete"])
    df["price"] = parse_money(df["price"])
    return df

def create_model_input_table(shuttles: pd.DataFrame, companies: pd.DataFrame, reviews: pd.DataFrame ) -> pd.DataFrame:
    rated_shuttles = shuttles.merge(reviews, left_on="id", right_on="shuttle_id")
    model_input_table = rated_shuttles.merge(companies, left_on="company_id", right_on="id")
    return model_input_table.dropna()