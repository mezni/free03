import pandas as pd
from tinydb import TinyDB, Query

db = TinyDB("_store/_store.json")
df = pd.read_csv("_data/data.csv")
data = df.to_dict("records")


for record in data:
    db.insert(record)
