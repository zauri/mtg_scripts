#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 16:22:35 2021

@author: zauri
"""

import json
import pandas as pd

def get_card_names(input_file):  
    data = read_json(input_file)
    #data = filter_out_etched_foils(data)
    #data = filter_out_arena_cards(data)
    data = filter_out_special_cards(data)
    data = sort_ascending_by_number(data)
    card_names = filter_out_duplicates(data)
    
    return card_names


def read_json(input_file):
    with open(input_file) as file:
        data = json.load(file)
        
    return data


def filter_out_special_cards(data):
    return [x for x in data['data']['cards'] if 'e' not in x['number'] and \
            '†' not in x['number']]


def filter_out_etched_foils(data):
    return [x for x in data['data']['cards'] if 'e' not in x['number']]

def filter_out_arena_cards(data):
    return [x for x in data['data']['cards'] if '†' not in x['number']]


def sort_ascending_by_number(data):
    names = []
    ascending_numbers = sorted(data, key=lambda x: int(x['number']))
    
    for x in ascending_numbers:
        names.append(x['name'])
    
    return names


def filter_out_duplicates(names):
    names_cleared = []
    
    for x in range(0, len(names)):
        if names[x] == names[x-1] and '//' in names[x]:
            pass
        else:
            names_cleared.append(names[x])
    
    return names_cleared


def save_to_file(card_names, set_name):
    card_names_dict = {'Name': card_names}
    
    df = pd.DataFrame(card_names_dict)
    df.index += 1
    
    df.to_csv(set_name + '.csv')
    print('Your cardname file has been created! :) ')


if __name__ == "__main__":
    input_file = input('Enter path to input file (json): ')
    set_name = input('Enter set name (e.g. stx): ')
    
    card_names = get_card_names(input_file)
    save_to_file(card_names, set_name)
    