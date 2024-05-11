import asyncio
import pandas as pd
from db_config import init_db, create_db_engine


def get_distinct( df, cols):
    df_temp = df.groupby(cols).size().reset_index(name="Freq")[cols]
    return df_temp.to_dict("records")

async def execute():
    db_url = "sqlite+aiosqlite:///_store/_dwh.db"
    engine = await create_db_engine(db_url)
    df = pd.read_csv("_data/data.csv")
    orgs =  get_distinct( df, ["Client"])
    print (orgs)

asyncio.run(execute())
