#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 17 10:53:56 2021

@author: Petra Wenzl
"""

from mtg_json import read_json

import os
import pandas as pd


filepath = input('Enter filepath for json files to process: ')
directory = os.fsencode(filepath)

special_cards = dict()

for file in os.listdir(directory):
    file_name = os.fsdecode(file)
    if file_name.endswith('.json'):
        json_file = read_json(filepath + file_name)
        set_name = json_file['data']['code']
        special_cards[set_name] = []
        
        for card in json_file['data']['cards']:
            if card['number'].isdigit() == False:
                special_cards[set_name].append(card['number'])
                

sorted_dict = dict(sorted(special_cards.items()))
                
df = pd.DataFrame(sorted_dict.items(), columns=['set_code', 'card_numbers'])
df.to_csv('special_cards.csv', header=True, index=False)

print('List of special cards has been saved.')
            