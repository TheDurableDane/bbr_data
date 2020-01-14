from bs4 import BeautifulSoup
import requests
import pandas as pd


house_price_columns = ['street_and_number', 'postal_code', 'price', 'date', 'residence_type', 'rooms', 'residence_area', 'year_of_construction', 'price_adjustment']
house_price_data = pd.DataFrame(columns=house_price_columns)

n_subpages = 2
for subpage_number in range(n_subpages):
    url = 'https://www.boliga.dk/salg/resultater?page={}&sort=date-d'.format(subpage_number+1)
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    cols = soup.find_all('td', class_='table-col')
    n_addresses = int(len(cols)/10)

    for i in range(n_addresses):
        address_info = cols[10*i].get_text().strip().split(', ')
        print(address_info)
        if len(address_info) == 2:
            street_and_number = address_info[0]
            postal_code = address_info[1].split(' ')[0]
        elif len(address_info) == 3:
            street_and_number = address_info[0] + ', ' + address_info[1]
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

        house_info = [street_and_number, postal_code, price, date, residence_type, rooms, residence_area, year_of_construction, price_adjustment]
        temp_dict = dict(zip(house_price_columns, house_info))
        house_price_data = house_price_data.append(temp_dict, ignore_index=True)
