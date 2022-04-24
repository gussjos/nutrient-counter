import sqlite3
from sqlite3 import Error
from venv import create
from icecream import ic


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn 

def create_meal_table(DB_NAME:str):
    conn = create_connection(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE meal
                    (food, amount, unit)''') 

def create_food_table(DB_NAME:str):
    conn = create_connection(DB_NAME)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE food
                    (name, search_query, kcal, protein, carbs, fat, price)''') 

def delete_table(DB_NAME,table):
    conn = create_connection(DB_NAME)
    cur = conn.cursor()
    cur.execute(f''' DROP TABLE {table} ''')

def add_food_to_database(DB_NAME:str,food:dict):
    con = create_connection(DB_NAME)
    cur = con.cursor()
    columns = ', '.join(food.keys())
    placeholders = ':'+', :'.join(food.keys())
    
    search_result = cur.execute(f'SELECT * FROM food \
    WHERE name == %s' % (food["name"])).fetchall()
    ic(search_result)


    query = 'INSERT INTO food (%s) VALUES (%s)' % (columns, placeholders)
    cur.execute(query, food)
    con.commit()

def parse_food_table(DB_NAME:str):
    con = create_connection(DB_NAME)
    cur = con.cursor()
    ic(cur.execute('SELECT * FROM food').fetchall())
    

#con=create_connection('food.db')
#cur=con.cursor()
#delete_table(cur,'food')
#create_food_table(cur)
#
#q = 'SELECT * FROM food'
#cur = create_connection('food.db').cursor()
#for row in cur.execute(q):
#    print(row)