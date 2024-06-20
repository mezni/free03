import uuid
from tinydb import TinyDB, Query

db = TinyDB('config.json')
# Org
orgs_table = db.table('orgs')
orgs_table.insert({'id': str(uuid.uuid4()), 'name': 'momentum', 'description': 'momentum'})

# Providers
providers_table = db.table('providers')
providers_table.insert({'id': str(uuid.uuid4()), 'name': 'aws', 'description': 'aws'})
providers_table.insert({'id': str(uuid.uuid4()), 'name': 'azure', 'description': 'azure'})
providers_table.insert({'id': str(uuid.uuid4()), 'name': 'oci', 'description': 'oci'})

# Regions
regions_table = db.table('regions')

Provider = Query()
query_result = providers_table.search(Provider.name == 'aws')
print(query_result)
for provider in query_result:
    print(provider["id"])

#us-west-2
all_providers = providers_table.all()
print("All Providers:")
for provider in all_providers:
    print(provider)
    
db.close()
