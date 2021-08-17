#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 17 16:22:35 2021

@author: Petra Wenzl
@author: Kannan Thambiah <pygospa@gmail.com>
"""

import argparse
import json
import os
import pandas as pd
from natsort import natsorted


def get_cards(json_data, parsed_arguments):
    if (parsed_arguments.filter):
        json_data = filter_out_special_cards(json_data)
    
    json_data = sort_ascending_by_number(json_data)
    json_data = process_doublefaced(json_data)
    card_dict = reduce_json_to_dict(json_data)

    return card_dict


def read_json(input_file):
    with open(input_file) as file:
        json_file = json.load(file)
    return json_file


def filter_out_special_cards(json_file):
    cards = [card for card in json_file['data']['cards'] if \
            'e' not in card['number'] and '†' not in card['number']]
    json_file['data']['cards'] = cards
    return json_file


def sort_ascending_by_number(json_file):
    sorting_attribute = lambda card: card['number']
    sorted_cards = natsorted(json_file['data']['cards'], key=sorting_attribute)
    sorted_tokens = natsorted(json_file['data']['tokens'], key=sorting_attribute)
    json_file['data']['cards'] = sorted_cards
    json_file['data']['tokens'] = sorted_tokens
    return json_file


def process_doublefaced(json_file):
    unique_cards = []
    prev_card = None

    for card in json_file['data']['cards']:
        if is_double_sided(prev_card, card):
            prev_card['type'] = f"{prev_card['type']} // {card['type']}"
        else:
            unique_cards.append(card)
        prev_card = card

    json_file['data']['cards'] = unique_cards
    return json_file


def is_double_sided(prev_card, card):
    return prev_card is not None \
        and card['name'] == prev_card['name'] \
        and '//' in card['name']


def reduce_json_to_dict(json_file):
    codes = []
    names = []
    numbers = []
    types = []
    colors = []
    rarities = []

    for card in json_file['data']['cards']:
        codes.append(card['setCode'])
        numbers.append(card['number'])
        names.append(card['name'])
        types.append(card['type'])
        colors.append(card['colorIdentity'])
        rarities.append(card['rarity'])

    for token in json_file['data']['tokens']:
        codes.append(token['setCode'])
        numbers.append(token['number'])
        names.append(token['name'])
        types.append(token['type'])
        colors.append(token['colorIdentity'])
        rarities.append('')

    cards_dict = {
        'Set' : codes,
        '#' : numbers,
        'Name': names,
        'Rarity': rarities,
        'Type': types,
        'Color':colors }

    return cards_dict


def save_to_file(cards_dict, set_name):
    df = pd.DataFrame(cards_dict)
    df.index += 1
    
    df.to_csv(index=False, path_or_buf=set_name + '.csv')
    print('Your cardname file has been created! :) ')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filter', action='store_true',
                        help='Filter out cards with non-numeric characters in \
                            their number.')
    parsed_arguments = parser.parse_args()
    
    input_file = input('Enter path to input file (json): ')
    set_name = os.path.splitext(input_file)[0]

    json_data = read_json(input_file)
    cards_dict = get_cards(json_data, parsed_arguments)
    save_to_file(cards_dict, set_name)

