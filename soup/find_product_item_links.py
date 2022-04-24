from bs4 import BeautifulSoup
import requests
import os

def save_link_to_html(an_url: str, savename: str):
    r = requests.get(an_url)
    with open(savename, 'w') as file:
        file.write(r.text)

def find_product_numbers(path_to_html_file: str):
    soup = BeautifulSoup(open(path_to_html_file), "html.parser")
    product_nbrs = []
    for a in soup.find_all('a', href=True):
        link = a['href']
        if '/details' in link:
            product_nbr = link.split('/')[-2]
            if product_nbr not in product_nbrs:
                product_nbrs.append(product_nbr)
    return product_nbrs

def fetch_product_nbrs(search_query:str, STORE_URL:str):
    my_url = f'{STORE_URL}products/search?q={search_query}'
    savename=f'query_{search_query}.html'
    save_link_to_html(an_url=my_url, savename=savename)
    path_to_html_file=savename
    nbrs = find_product_numbers(path_to_html_file)
    print(f'Found {len(nbrs)} product numbers!')
    print('search query:', search_query)
    clean_up_htmls(search_query)
    return nbrs

def clean_up_htmls(query):
    os.remove(f"query_{query}.html")


















#print(contents)
#nbr_succesful_items = []
#for product_id in ids:
    #url = f"https://handlaprivatkund.ica.se/stores/1004219/products/{product_id}/details"
    #response = urllib.request.urlopen(url)
    #print(response)
    
    #r = requests.get(url)
    #with open(f'file_{product_id}.html', 'w') as file:
        #file.write(r.text)
    

    #try: 
        #soup = BeautifulSoup(open("file_{product_id}.html"), "html.parser")
        #contents = soup.find_all("div", {"class":"static-content-wrapper__StaticContentWrapper-sc-3z5iao-0 kgChTt"})
    
        #print(contents[-1])
        #nbr_succesful_items.append(product_id)
    #except:
        #pass
    
    
#print('nbr_succesful_items =',nbr_succesful_items)

