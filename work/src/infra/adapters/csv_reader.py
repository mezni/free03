import pandas as pd
from typing import List, Dict
from src.interractor.interfaces.data_reader import DataReader


class CSVDataReader(DataReader):
    def read_data(self, file_path: str) -> List[Dict]:
        data = []
        df = pd.read_csv(file_path)
        data = df.to_dict("records")
        return data
