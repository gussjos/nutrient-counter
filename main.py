#! /home/gussjo/miniconda3/bin/python
import numpy as np
import pandas as pd
import argparse
from icecream import ic

my_parser = argparse.ArgumentParser(description="Adds food item to daily caloric database")


my_parser.add_argument('Food',
                        metavar='food',
                        type=str,
                        help='Food item you have eaten.'
)
my_parser.add_argument('Grams',
                        metavar='grams',
                        type=str,
                        help='Grams eaten of specified food.'
) 
                        
args = my_parser.parse_args()
food_item = args.Food
grams = args.Grams

print(f'You ate {grams} grams of {food_item}.')

# Connect to database
           