import requests
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd


def get_zipcodes():
    url = 'https://www.boliga.dk/salg'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    zipcodes_dropdown = soup.find_all('select', class_='form-control border rounded p-2')[0].contents

    zipcodes = []
    for item in zipcodes_dropdown:
        if item != "\n":
            zipcode_content = item.contents[0].split()[0]
            try:
                zipcode = int(zipcode_content)
            except ValueError as e:
                print("Item '{}' could not be converted to datatype integer.".format(zipcode_content))
            else:
                zipcodes.append(zipcode)

    return(zipcodes)


zipcodes = get_zipcodes()
