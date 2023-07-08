#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jul 08 12:33:44 2023

@author: Kannan Thambiah <pygospa@gmail.com>
"""

import argparse
import numpy as np
import pandas as pd


def add_cards_to_db(db, count, booster, database_file):
    for _, card in count_csv.iterrows():
        index = db.index[(db['#'] == card['Card Number']) &
                         (db['Set'] == card['Set Code'])]

        if len(index) > 0:
            index = index[0]
            stock = db.at[index, card['Printing']]
            if np.isnan(stock):
                db.at[index, card['Printing']] = int(card['Quantity'])
            else:
                db.at[index, card['Printing']] = int(stock + card['Quantity'])

            if booster is not None:
                boosters = db.at[index, 'Booster']

                if pd.isnull(boosters):
                    db.at[index, 'Booster'] = booster
                else:
                    db.at[index, 'Booster'] = \
                        f"{db.at[index, 'Booster']}, {booster}"

    print(db.loc[340:345, :])
    db.to_csv(index=False, path_or_buf=database_file)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', type=str, required=True,
                        help='Database file in CSV format')
    parser.add_argument('-c', '--countfile', type=str, required=True,
                        help='File with count (in TCG-Player Format')
    parser.add_argument('-b', '--booster', type=str, required=False,
                        help='Booster Number/Comment for field')

    parsed_arguments = parser.parse_args()
    database_file = parsed_arguments.database
    count_file = parsed_arguments.countfile
    booster = parsed_arguments.booster
    database_csv = pd.read_csv(database_file, header=0)
    count_csv = pd.read_csv(count_file, header=0)

    add_cards_to_db(database_csv, count_csv, booster, database_file)
