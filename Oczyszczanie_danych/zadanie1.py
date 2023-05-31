import pandas as pd
import numpy as np

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
# Najpierw wstawiam zmienione kolumny z brakami danych do bankruptcy
bankruptcy[kolumny_BrakDanych.columns] = kolumny_BrakDanych

statystki = bankruptcy.describe()

# 6 
bankruptcy[kolumny_BrakDanych.columns] = bankruptcy[kolumny_BrakDanych.columns].fillna(kolumny_BrakDanych.mean())

# 7 
statystki = bankruptcy.describe()

# 8 
bankruptcy.to_csv("bankcruptcy_uzupelnione.csv",sep=",",encoding="utf-8",index=False)