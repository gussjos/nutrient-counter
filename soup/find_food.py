#!/home/gussjo/miniconda3/bin/python
import sys
from subprocess import call

from yaml import parse

from find_product_item_links import fetch_product_nbrs
from parse_product_page import find_contents
from database import *

STORE_URL = 'https://handlaprivatkund.ica.se/stores/1004219/'
DB_NAME = 'food.db'

def main():
    query = sys.argv[-1]
    product_nbrs = fetch_product_nbrs(query, STORE_URL)
    
    for product_nbr in product_nbrs:
        product_URL = STORE_URL + 'products/' + product_nbr + '/details/'
        _ = find_contents(product_URL, query)
    call("./soup/clean_htmls.sh")
    

if __name__ == "__main__":
    main()
