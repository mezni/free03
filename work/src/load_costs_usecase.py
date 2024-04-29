import pandas as pd
class LoadCostsUseCase:
    def __init__(self, repo):
        self.repo = repo 
    
    def process_data(self, file_path):
        data = []
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                data.append(Data(row[0], row[1]))
        return data