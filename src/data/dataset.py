import pandas as pd
from typing import Text


def get_dataset(dataset_path: Text) -> pd.DataFrame:

    return pd.read_csv(dataset_path)