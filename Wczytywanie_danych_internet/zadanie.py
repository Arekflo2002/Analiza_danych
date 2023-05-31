import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
import requests
import scipy.stats as stats

"""1. Przygotowywanie danych z 2 zrodel"""


"""
Przygotowanie tabeli dla produktu krajowego brutto na 1 mieszkanca dla danego wojewodztwa 
"""

url = "http://eregion.wzp.pl/wskaznik/produkt-krajowy-brutto-na-1-mieszkanca"

# Scraper 
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')


# Tutaj znajduje tabele na stronie 

table = soup.find_all('table')[0]

# Wczytuje tabele do zmiennej po wierszach Omijajac tytuly tabeli oraz Polska bo nie bedzie uczestniczyla w badaniu 
rows = table.tbody.find_all('tr')[1:]
list_data = []

# Iteruje po wierszach i wyszczegolniam poszczegolne komorki tabeli tak aby polaczyc je w jedna liste 
# Przy okazji filtruje dane, mianowicie bede prowadzil badanie od roku 2016 do 2019(przez braki w danych) wiec tez od razu fitruje dane
for row in rows:
    # Znajdowanie komorek
    cells = list(row.find_all('td'))
    # Filtracja
    cells = cells[:1] + cells[5:len(cells)-1]
    # Tworzenie listy
    list_data.append([cells[0].contents[0],cells[1].contents[0],cells[2].contents[0],cells[3].contents[0],cells[4].contents[0]])

# Tutaj sa gotowe dane do pracy 
woj_pkb = pd.DataFrame(data=list_data,columns =['Wojewodztwo','PKB-2016','PKB-2017','PKB-2018','PKB-2019'])

# Zamiana na same male litery bo pozniej byly problemy z merge
woj_pkb['Wojewodztwo'] = woj_pkb['Wojewodztwo'].str.lower()



"""
Przygotowanie tabeli dla pozostalych informacjach o wojewodztwach 
"""

url = "https://przeglad-turystyczny.pl/warto/341-lista-wojewodztw-w-polsce"

# Scraper 
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')


# Tutaj znajduje tabele na stronie 
table_2 = soup.find_all('table')[0]

# Wczytuje tabele do zmiennej po wierszach Omijajac tytuly tabeli oraz Polska bo nie bedzie uczestniczyla w badaniu 
rows_2 = table_2.find_all('tr')[1:-1]
list_data_2 = []

# Iteruje po wierszach i wyszczegolniam poszczegolne komorki tabeli tak aby polaczyc je w jedna liste 
# Przy okazji filtruje dane, mianowicie chce tyklko nazwe wojewodztwa jego siedzibe, powierzchnie oraz stope bezrobocia 
for row in rows_2:
    # Znajdowanie komorek
    cells = row.find_all('td')

    # Wybieram ktore dane chce 
    cells = cells[2:6] 

    """
        Tutaj pojawil sie problem, bo niektore dane na tej stronie byly w postaci <td><a>Moje dane</a></td>
        przez co nie moglem ich wyciagnac bezposrednio wiec od razu wyciagam napis z tagu 'a', a jesli nie 
        ma tego tagu to wyciagam dane z 'td'. 
    """

    cells_or = []
    for i,cell in enumerate(cells): 
        # Sprawdzam czy jest tag 
        if cell.find('a') is not None:
            # Jesli jest to wyciagam tekst i podmieniam wartosci
            cell_temp = cell.get_text()
            cells_or.append(cell_temp)
            continue 

        # Wyciagam dane z 'td'
        cells_or.append(cell.contents[0])

    # Podmieniam tablice i zamieniam wszystkie napisy tak zeby mialy male litery bo pozniej jest problem 
    cells = [element.lower() for element in cells_or]            

    # Tworzenie listy
    list_data_2.append([cells[0],cells[1],cells[2],cells[3]])


# Tutaj sa gotowe dane do pracy 
woj_info = pd.DataFrame(data=list_data_2,columns =['Wojewodztwo','siedziba','powierzchnia','liczba ludnosci'])


"""
    Przeksztalcenie danych
"""

wynik = pd.merge(woj_info,woj_pkb,on=['Wojewodztwo'])

# Wyswietlanie danych
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.colheader_justify', 'center')
pd.set_option('display.precision', 3)
print(wynik.head())


"""
    Regresja dla kazdego z wojewodztw dla przyszlego PKB wiec skorzystam z woj_pkb
"""

woj_pkb.columns = ['Wojewodztwo','2016','2017','2018','2019']

for i_woj,row in woj_pkb[1:].iterrows():

    row = row.str.replace(' ','')
    X = woj_pkb.columns[1:].astype(int)  # Lata jako zmienna niezależna
    Y = row[1:].values.astype(float)

    # Regresja
    slope, intercept, r_value, p_value, std_err = stats.linregress(X, Y)

    # print(f"Województwo: {row[0]}")
    # print("Nachylenie:", slope)
    # print("Punkt przecięcia:", intercept)

    # Wykres 
    plt.scatter(X, Y)
    plt.plot(X, intercept + slope * X)

# Wykres
plt.xlabel('Rok')
plt.ylabel('PKB na 1 mieszkańca')
plt.title("Wojewodztwa PKB - regresja")
plt.show()
"""
    Wnioski:
    Regresja jest bardzo dobrze dopasowana
"""
