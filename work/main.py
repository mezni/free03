import uuid
import asyncio
import csv

async def main():
    db_url = "sqlite+aiosqlite:///_usage.db"
    
    with open("aws_data.csv", "r") as f:
        reader = csv.DictReader(f)
        data = list(reader)
    
    clients = list(set([x['Client'] for x in data]))
    print (clients)

#    dates = list(set([x['Date'] for x in data]))
#    print (dates)
asyncio.run(main())


