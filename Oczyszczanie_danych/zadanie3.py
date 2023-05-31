import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist


# 1
bankruptcy = pd.read_csv("Cwiczenia2/bankruptcy.csv")

# 2
np.random.seed(1234)

# 3
kolumny = bankruptcy.select_dtypes(include=[np.number]).sample(n=2,axis=1)

# 4 
# Braki danych w 20% procentach losowych przypadkow 
kolumny_BrakDanych = kolumny.apply(lambda x: x.sample(frac=0.8).reindex_like(x))

# 5 

# Wybieranie kolumn bez braków danych i numeryczne 
kolumny_bez_brakow = bankruptcy.select_dtypes(include=[np.number]).columns[bankruptcy.select_dtypes(include=[np.number]).notna().all()]

# Skalowanie min-max kolumn bez braków danych do zakresu 1-5
bankruptcy[kolumny_bez_brakow] = (bankruptcy[kolumny_bez_brakow] - bankruptcy[kolumny_bez_brakow].mean()) /bankruptcy[kolumny_bez_brakow].std()

# 6 

bankruptcy_numeryczne = bankruptcy[kolumny_bez_brakow]

# Liczenie odleglosci eukledisowych
# Obliczanie odległości euklidesowych między wierszami
bankruptcy_numeryczne.reset_index(drop=True, inplace=True)
distances = cdist(bankruptcy_numeryczne.dropna(), bankruptcy_numeryczne.dropna())

# Wybieranie trzech najbliższych wierszy dla wierszy zawierających braki danych
najblizsze_indeksy = np.argsort(distances, axis=1)[:, :3]

for i,row in bankruptcy.iterrows():
    if row.isnull().any():
        podobne_wiersze = bankruptcy_numeryczne.dropna().iloc[najblizsze_indeksy[i]]
        print("Dla wiersza", i, "najbardziej podobne wiersze to:",end="\n")