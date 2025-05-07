import csv
import os

def lire_numeros(fichier=os.path.join("..", "enterprise_short.csv")):
    with open(fichier, newline="") as f:
        reader = csv.DictReader(f)
        return [ligne["EnterpriseNumber"].strip() for ligne in reader]
