from bs4 import BeautifulSoup
import requests


url = 'https://www.boliga.dk/salg/resultater?page=1&sort=date-d'
r = requests.get(url)
soup = BeautifulSoup(r.content, 'html.parser')
cols = soup.find_all('td', class_='table-col')
n_addresses = int(len(cols)/10)

for i in range(n_addresses):
    address_info = cols[10*i].get_text().strip().split(', ')
    if len(address_info) == 2:
        road_and_number = address_info[0]
        postal_code = address_info[1].split(' ')[0]
    elif len(address_info) == 3:
        road_and_number = address_info[0] + ', ' + address_info[1]
        postal_code = address_info[2].split(' ')[0]
    else:
        print('Address info doesn\'t have the required length.')

    price = int(cols[10*i+1].get_text().strip().split()[1].replace('.', ''))

    date = cols[10*i+2].get_text().strip().split()[1]

    residence_type = cols[10*i+3].get_text().strip().split()[1]

    rooms = int(cols[10*i+5].get_text().strip().split()[1])

    residence_area = int(cols[10*i+6].get_text().strip().split()[1])

    year_of_construction = int(cols[10*i+7].get_text().strip().split()[1])

    price_adjustment_info = cols[10*i+8].get_text().strip().split()
    if len(price_adjustment_info) == 2:
        price_adjustment = int(price_adjustment_info[1].replace('%', ''))
    else:
        price_adjustment = 0
