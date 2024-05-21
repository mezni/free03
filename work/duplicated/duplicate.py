import re

docs_list = []
with open("duplicated/_txt.db", "r") as file:
    lines = file.readlines()
    for line in lines:
        if line.startswith("  Type :"):
            line = line.strip()
            line = line.replace("Type :", "")
            line_split = re.split(r"\s{2,}", line)
            docs_list.append(line_split[1])

for item in set(docs_list):
    if docs_list.count(item) > 1:
        print(item, docs_list.count(item))
