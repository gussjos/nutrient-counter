from tkinter import W
from turtle import st
from unicodedata import name
from find_product_item_links import *
from icecream import ic
import re
import numpy as np

def find_contents(link_to_product:str, query:str):
    savename=query+'.html'
    save_link_to_html(link_to_product,savename)
    soup = BeautifulSoup(open(savename),'html.parser')
    cost = _find_cost_of_product(soup)
    name_of_product = _find_name_of_product(soup)

    if not _are_substrings_in_product_name(query,name_of_product):
        return    
    nutrients = _find_macronutrients_of_product(soup)
    nutrients = _supply_extra_fields_to_nutrients(nutrients,name_of_product,query,cost)
    str_to_print = _construct_product_string(query,name_of_product,nutrients)
    print(str_to_print)
    return nutrients


def _are_substrings_in_product_name(query,name_of_product):
    query_substrings = query.split(" ")
    for substr in query_substrings:
        if not (substr in name_of_product) and not (substr.capitalize() in name_of_product):
            print(f'Discarding \"{name_of_product}\", all substrings of query not in product name.')
            return False
    return True


def _supply_extra_fields_to_nutrients(nutrients,name_of_product,query,cost):
    nutrients['name'] = name_of_product.replace("%"," procent")
    nutrients['search_query'] = query
    nutrients['price'] = cost
    return nutrients


def _construct_product_string(query,name_of_product,nutrients):
    str_to_print_for_food = f'\'{query}\': macro_dict(description=\'{name_of_product}\', '
    for key in nutrients:
        if key == 'name' or 'search' in key or 'price' in key:
            continue
        str_to_print_for_food += f'{key}={nutrients[key]}, '
    str_to_print_for_food += "cost={:.2f}),".format(np.round(nutrients['price']/10,2))
    return str_to_print_for_food


def _find_cost_of_product(soup):
    contents = soup.find_all("div", {"class":"spacing__Spacing-sc-1v5y1gf-0 cABhFm"})
    content = str(contents[0])
    res = re.search('kr',content)
    i2 = res.span()[-1]
    info = content[:i2-3]
    info = info.split('>')[-1]
    info = info.replace(',','.')
    return float(info)

def _find_nutrient_amount(nutrient:str, mystr:str):
    res = re.search(rf'{nutrient}',mystr)
    i2 = res.span()[-1]
    substr = mystr[i2+1:]
    split = substr.split(" ")
    try:
        return float(split[0])
    except: # Sometimes it's Kolhydrater instead of Kolhydrat => first element will be an 'r'...
        return float(split[1])

def _find_name_of_product(soup) -> str:
    contents = soup.find_all("h1", {"class":"heading__Base-sc-12x0apr-0-h1 dNTcyY"})
    return str(contents).split('>')[-2].split('<')[0]


def _find_macronutrients_of_product(soup) -> dict:
    contents = soup.find_all("div", {"class":"static-content-wrapper__StaticContentWrapper-sc-3z5iao-0 kgChTt"})
    nutrient_content = str(contents[-1])
    try:
        kcal = _find_nutrient_amount('Energi',nutrient_content)
    except:
        print(contents)
        print('Could not find kcal. Probably not a food.')
        return {}
    protein = _find_nutrient_amount('Protein',nutrient_content)
    carbs = _find_nutrient_amount('Kolhydrat',nutrient_content)
    fat = _find_nutrient_amount('Fett',nutrient_content)

    return ({
        'kcal': kcal,
        'protein': protein,
        'carbs': carbs,
        'fat': fat
    })

