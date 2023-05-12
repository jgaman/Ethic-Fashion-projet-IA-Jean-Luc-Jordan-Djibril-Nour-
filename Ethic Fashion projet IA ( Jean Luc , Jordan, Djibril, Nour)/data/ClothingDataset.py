import random
import pandas as pd

    
class ClothingDataset:
    
    """ Classe permettant de générer un jeu de données de vêtements durables.
        - num_items: nombre d'items à générer Int
        - materials: liste des matériaux possibles
        - manufacturing_plants: liste des usines de fabrication possibles
        - carbon_footprint_range: plage de valeurs possibles pour l'empreinte carbone
        - descriptions: liste des descriptions possibles
        - items: liste des items générés
        - to_csv: méthode permettant d'enregistrer le jeu de données dans un fichier CSV
    """

    def __init__(self, num_items):
        self.num_items = num_items
        self.materials = ['coton biologique', 'lin', 'lyocell', 'laine mérinos',
                          'cuir végétalien', 'soie sauvage', 'chanvre biologique']
        self.manufacturing_plants = ['Patagonia', 'Eileen Fisher', 'Outerknown', 'Everlane',
                                     'Alternative Apparel', 'People Tree', 'Prana', 'Thought', 'Kowtow', 'Reformation']
        self.carbon_footprint_range = (0.2, 2.5)  # en kgCO2e
        self.descriptions = [
            "Pull en laine mérinos biologique à col rond pour femmes",
            "Chemise en lin biologique pour hommes",
            "Robe en coton biologique avec imprimé floral pour femmes",
            "Veste légère en lyocell recyclé pour hommes",
            "T-shirt en Tencel et coton biologique pour femmes",
            "Jupe en chanvre biologique pour femmes",
            "Pantalon en coton biologique pour hommes",
            "Blouson en cuir végétalien pour femmes",
            "Sweat à capuche en coton biologique pour hommes",
            "Chemisier en soie sauvage pour femmes",
            "Chaussettes en laine mérinos recyclée pour hommes",
            "Cardigan en laine d'alpaga pour femmes",
            "Veste en cuir recyclé pour hommes",
            "Robe en Tencel recyclé pour femmes",
            "Pantalon de yoga en coton biologique pour femmes",
            "T-shirt en lin biologique pour hommes",
            "Jupe en coton biologique pour femmes",
            "Chemise en chambray de coton biologique pour hommes",
            "Sweat-shirt en polyester recyclé pour femmes",
            "Veste en jean recyclé pour hommes"
        ]
        self.types = ['Pull', 'Chemise', 'Robe', 'Veste', 'T-shirt', 'Jupe',
                      'Pantalon', 'Blouson', 'Sweat', 'Chemisier', 'Chaussettes', 'Cardigan']
        self.genders = ['Femme', 'Homme']
        self.items = self.generate_items()

    def generate_items(self):
        items = []
        for i in range(self.num_items):
            item = {}
            item['description'] = random.choice(self.descriptions)
            item['material'] = random.choice(self.materials)
            item['manufacturing_plant'] = random.choice(
                self.manufacturing_plants)
            item['manufacturing_time'] = random.randint(1, 15)   # en minutes
            item['carbon_footprint'] = round(
                random.uniform(*self.carbon_footprint_range), 2)
            item['type'] = random.choice(self.types)
            item['gender'] = random.choice(self.genders)
            items.append(item)
        return items

    def to_csv(self, filename):
        df = pd.DataFrame(self.items)
        df.to_csv(filename, index=False)




