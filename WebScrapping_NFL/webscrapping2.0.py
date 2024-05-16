import re
import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.nfl.com/standings/league/2023/reg"
page = requests.get(url)
soup = BeautifulSoup(page.text, "lxml")


"""usar um dicionário pra achar o valor que eu quero, é melhor do que tentar achar
as propriedades do dicionário"""
table = soup.find("table", {"summary": "Standings - Detailed View"})

headers = []


for each_element in table.find_all("th"):
    title = each_element.text.strip()
    headers.append(title)

dataset = pd.DataFrame(columns=headers)

for each_row in table.find_all("tr")[1:]:
    row_data = []
    
    first_td = each_row.find_all("td")[0].find("div", class_="d3-o-club-fullname").text.strip()
    first_td = re.sub(r"\s+"," ", first_td)
    row_data.append(first_td)
    
    for each_td in each_row.find_all("td")[1:]:
        row_data.append(each_td.text.strip())
    
    dataset.loc[len(dataset)] = row_data
    
print(dataset.head())
dataset.to_csv("nfl_rip.csv")