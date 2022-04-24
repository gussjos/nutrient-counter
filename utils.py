import copy
import numpy as np
import json
from icecream import ic

def macro_dict(description='', kcal=0,protein=0,carbs=0,fat=0,cost=0,unit='100 g'):
    return ({
        'description': description,
        'kcal': kcal,
        'protein': protein,
        'carbs': carbs,
        'fat': fat,
        'cost': cost,
        'unit': unit
    }) 

# Yeah this is a super alpha version that I am using before I figure out some database stuff :D 
food_dict = {
    '': macro_dict('Empty',0,0,0,0,0,'nothing'),
    'havregryn': macro_dict('Havregryn Axa', 370, 12, 60, 7, 26/15, '100 g'), 
    'jordgubbssylt_lågkalori': macro_dict('Jordgubbssylt Lågkalori Ånås', 40, 0, 8.5, 0, 30/3.6, '100 g'),
    'ägg': macro_dict('Ägg',75, 7, 0, 5, 2, '1x'),
    'lättmjölk': macro_dict('Arla lättmjölk', 40, 3.5, 5, 0.5, 2, '100 g'),
    'mellanmjölk': macro_dict('Arla mellanmjölk', 45, 3.6, 4.8, 1.5, 2, '100 g'),
    'röd_mjölk': macro_dict('Arla Röd mjölk', 60, 3.3, 5, 3, 2, '100 g'),
    'whey_100': macro_dict('Whey 100 MM Sports', 136, 26, 1.4, 2.3, 6, '30 g'),
    'pure_bar_less_sugar': macro_dict('Pure BAR Less sugar', 261, 18, 24, 10.2, 17, '1x (60 g)'),
    'arla_kvarg_mild': macro_dict('Arla Mild Kvarg Vanilj', 60, 9.7, 4, 0.1, 3, '100 g'),
    'riskaka': macro_dict('Riskaka ICA Basic', 380, 8.3, 79, 3.2, 7, '100 g'),
    'jordnötssmör': macro_dict('Jordnötssmör Crunchy med havssalt ICA', 600, 26, 12, 48, 29.50/3.5, '100 g'),
    'banan': macro_dict('banan', 100, 1, 22, 0.5, 3, '100 g'),
    'öl_5.2': macro_dict(description='Öl, 5.2%', kcal=140, protein=0.5*3.33, carbs=3.6*3.33, fat=0, cost='12', unit='33 cl'),
    'pad_thai': macro_dict(description='Pad Thai', kcal=280, protein=20, carbs=67, fat=10, cost=25, unit='100 g'),
    'blandfärs': macro_dict(description='Blandfärs 70/30 ICA', kcal=260, protein=19, carbs=0, fat=21, unit='100g', cost=10),
    'smör': macro_dict(description='Smör Normalsaltat 82% 500g Svenskt smör', kcal=739.0, protein=0.6, carbs=0.7, fat=82, cost=10,unit='100 g'),
    'ris': macro_dict(description='Ris långkornigt kokt', kcal=113, protein=2.5, carbs=24.6, fat=0.2, cost=1, unit='100 g'),
    'valnötter': macro_dict(description='Valnötter', kcal=669, protein=14.3, carbs=13, fat=62, cost=3),
    'nötmix': macro_dict(description='Nötmix Klassisk OLW', kcal=580, protein=24, carbs=14, fat=49, cost=13.5, unit='100 g'),
    'salta_pinnar': macro_dict(description='Salta pinnar 250g ICA', kcal=392.0, protein=12.0, carbs=71.0, fat=5.9, cost=5.98),
}

def load_json(file):
    with open(file,'rw') as f:
        json_file = json.load(f)
    f.close()
    return json_file

def parse_food_dict(alias:str) -> str:
    for item in food_dict:
        if alias in item:
            return item
    return ''
        
def evaluate_food(food_alias:str, amount:float):
    food_dict_copy = {}
    food_name = parse_food_dict(food_alias)
    food_dict_copy = copy.deepcopy(food_dict)
    food_item = food_dict_copy[food_name]
    for item_str in food_item:
        if type(food_item[item_str]) == str:
            continue
        food_item[item_str] *= amount
    kcal = amount*food_item['kcal']
    protein = amount*food_item['protein']
    carbs = amount*food_item['carbs'] 
    fat = amount*food_item['fat'] 
    cost = amount*food_item['cost']
    return food_item
ef = evaluate_food

def initiate_food_dict():
    return ({
        'kcal':0,
        'protein':0,
        'carbs':0,
        'fat':0,
        'cost':0
    })
ifd = initiate_food_dict          

def calculate_meal(meal:tuple,verbose=True): 
    meal_dict = ifd()
    if len(meal) > 1:
        for food_tuple in meal:
            food_str = parse_food_dict(food_tuple[0])
            amount = food_tuple[1]
            macros = evaluate_food(food_str,amount)
            if verbose and amount > 0:
                print(f'Adding {amount}*{food_dict[food_str]["unit"]} of {food_dict[food_str]["description"]}')
                print('\t {} kcal, {:.2f} g protein, {:.2f} g carbs, {:.2f} g fat, {:.2f} SEK'.format(food_dict[food_str]["kcal"]*amount,
                                                                                                  food_dict[food_str]["protein"]*amount,
                                                                                                  food_dict[food_str]["carbs"]*amount,
                                                                                                  food_dict[food_str]["fat"]*amount,
                                                                                                  food_dict[food_str]["cost"]*amount))
            meal_dict = add_macros_to_dict(meal_dict,macros)
    else: 
        food_tuple = meal
        ic(food_tuple)
        food_str = parse_food_dict(food_tuple[0])
        amount = food_tuple[1]
        macros = evaluate_food(food_str,amount)
        if verbose and amount > 0:
            print(f'Adding {amount}*{food_dict[food_str]["unit"]} of {food_dict[food_str]["description"]}. Kcal: {macros["kcal"]}')
            meal_dict = add_macros_to_dict(meal_dict,macros)
    return meal_dict

def add_macros_to_dict(collection:dict,macros:dict):
    for macro in macros:
        if type(macros[macro]) == str:
            continue
        collection[macro] += macros[macro]
    return collection

global kcal_total
kcal_total = 0
def evaluate_daily_macros(meals:dict) -> dict:
    kcal_total = 0
    daily_dict = ifd()
    for meal in meals:
        meal_dict = calculate_meal(meals[meal])
        daily_dict = add_macros_to_dict(daily_dict,meal_dict)
    print(f'\nDaily summary:')
    print('\t{:.0f} {}'.format(np.round(daily_dict['kcal'],-1),'kcal'))
    for macro in daily_dict:
        if macro != 'kcal' and macro != 'cost' and macro != 'unit':
            print('\t{:.2f} g of {}'.format(daily_dict[macro],macro))
    print('Estimated cost: {:.0f} SEK'.format(daily_dict["cost"]))
    return daily_dict