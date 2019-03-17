import requests
from bs4 import BeautifulSoup
import json


def get_zipcodes():
    url = 'https://www.boliga.dk/salg'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    zipcodes_dropdown = soup.find_all('select', class_='form-control border rounded p-2')[0].contents

    zipcodes = []
    for item in zipcodes_dropdown[1:]:
        if item != "\n":
            zipcode = item.contents[0].split()[0]
            zipcodes.append(zipcode)

    return zipcodes


def get_streetnames(zipcode):
    url = "https://www.boliga.dk/services/OIS.asmx/GetStreetNamesDK?zip=" + zipcode
    page = requests.get(url)
    street_info = json.loads(page.json())['streets']
    street_names = [street['name'] for street in street_info]

    return street_names


zipcodes = get_zipcodes()
print(zipcodes)
"""
for zipcode in zipcodes[0:1]:
    streetnames = get_streetnames(zipcode)
    for streetname in streetnames[1:2]:
        print(zipcode, streetname)
        url = 'https://www.boliga.dk/salg/resultater?so=1&sort=omregnings_dato-d&maxsaledate=today&iPostnr={0}&gade={1}&type=&minsaledate=1992'.format(zipcode, streetname)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        sales = soup.find_all('td', class_="align-middle text-center text-md-left d-md-table-cell")
        for sale in sales:
            address = sale.contents[1].contents[1].contents[0]
            price = int(sale.contents[3].contents[1].contents[1].contents[0].replace(' kr.', '').replace('.', ''))
            date = sale.contents[3].contents[3].contents[0].split(', ')[0]
            sale_type = sale.contents[3].contents[3].contents[0].split(', ')[1]
            house_type = sale.contents[3].contents[5].contents[0].split(', ')[0]
            house_area = sale.contents[3].contents[5].contents[0].split(', ')[1].replace(' m', '')

            print(address, price, date, sale_type, house_type, house_area, sep='\n')
"""
