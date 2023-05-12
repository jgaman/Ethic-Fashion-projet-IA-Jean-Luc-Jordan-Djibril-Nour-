from ClothingDataset import ClothingDataset
import os


# Créer un dataset avec 8000 articles
dataset = ClothingDataset(num_items=15000)

# Exporter le dataset en CSV dans le dossier 'data'
file_path = os.path.join('data', 'ethicdata.csv')
dataset.to_csv(file_path)
