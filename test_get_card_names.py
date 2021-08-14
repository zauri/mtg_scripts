#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 12 11:48:13 2021

@author: Kannan Thambiah <pygospa@gmail.com>
"""

import copy
import get_card_names as gcn
import unittest


class TestGetCardNames(unittest.TestCase):

    def test_get_cards(self):
        # given...
        blex = copy.deepcopy(self.blex_front)
        blex['type'] = f"{self.blex_front['type']} // {self.blex_back['type']}"

        given_cards = [self.necromancy, blex, self.vorinclex,
            self.vampire_token, self.sliver_token]

        expected_sets = []
        expected_names = []
        expected_numbers = []
        expected_types = []
        expected_colors = []
        expected_rarities = []

        for card in given_cards:
            expected_sets.append(card['setCode'])
            expected_numbers.append(card['number'])
            expected_names.append(card['name'])
            expected_types.append(card['type'])
            expected_colors.append(card['colorIdentity'])
            if not 'Token' in card['type']:
                expected_rarities.append(card['rarity'])
            else:
                expected_rarities.append('')

        # when...
        cards_dict = gcn.get_cards(self.json)

        # then...
        self.assertEqual(type(cards_dict), dict)
        self.assertEqual(cards_dict['Set'], expected_sets)
        self.assertEqual(cards_dict['#'], expected_numbers)
        self.assertEqual(cards_dict['Name'], expected_names)
        self.assertEqual(cards_dict['Rarity'], expected_rarities)
        self.assertEqual(cards_dict['Type'], expected_types)
        self.assertEqual(cards_dict['Color'], expected_colors)


    def test_is_double_sided(self):
        self.assertFalse(gcn.is_double_sided(self.vorinclex, self.blex_front))
        self.assertFalse(gcn.is_double_sided(self.blex_back, self.necromancy))
        self.assertFalse(gcn.is_double_sided(self.necromancy, self.vorinclex))
        self.assertFalse(gcn.is_double_sided(None, self.vorinclex))
        self.assertFalse(gcn.is_double_sided(None, self.blex_front))

        self.assertTrue(gcn.is_double_sided(self.blex_front, self.blex_back))

    
    def test_process_doublefaced(self):
        # given...
        expected_len = len(self.json['data']['cards']) - 1
        dfcs = self.get_cards_by_number(self.json, self.blex_front['number'])
        self.assertEqual(len(dfcs), 2)

        # when...
        json = gcn.process_doublefaced(self.json)

        # then...
        self.assertEqual(len(json['data']['cards']), expected_len)

        dfcs = self.get_cards_by_number(json, self.blex_front['number'])
        self.assertEqual(len(dfcs), 1)

        self.assertIn(self.blex_front['type'], dfcs[0]['type'])
        self.assertIn(self.blex_back['type'], dfcs[0]['type'])


    def test_sort_by_card_number(self):
        json = gcn.sort_ascending_by_number(self.json)
        prev_card = None
        
        for card in json['data']['cards']:
            if prev_card is not None:
                self.assertTrue(int(prev_card['number']) <= int(card['number']))
            prev_card = card


    def test_reduce_json_to_dict(self):
        # given...
        given_cards = self.json['data']['cards']
        given_tokens = self.json['data']['tokens']

        expected_sets = [card['setCode'] for card in given_cards] + \
            [token['setCode'] for token in given_tokens]
        expected_numbers = [card['number'] for card in given_cards] + \
            [token['number'] for token in given_tokens]
        expected_names = [card['name'] for card in given_cards] + \
            [token['name'] for token in given_tokens]
        expected_types = [card['type'] for card in given_cards] + \
            [token['type'] for token in given_tokens]
        expected_colors = [card['colorIdentity'] for card in given_cards] + \
            [token['colorIdentity'] for token in given_tokens]
        expected_rarities = [card['rarity'] for card in given_cards] + ['', '']

        # when...
        cards = gcn.reduce_json_to_dict(self.json)

        # then...
        self.assertEqual(type(cards), dict)
        self.assertEqual(list(cards.keys()),
            ['Set', '#', 'Name', 'Rarity', 'Type', 'Color'])
        self.assertEqual(cards['Set'], expected_sets)
        self.assertEqual(cards['#'], expected_numbers)
        self.assertEqual(cards['Name'], expected_names)
        self.assertEqual(cards['Rarity'], expected_rarities)
        self.assertEqual(cards['Type'], expected_types)
        self.assertEqual(cards['Color'], expected_colors)


    def get_cards_by_number(self, json, number):
        return [dfc for dfc in json['data']['cards'] \
            if dfc['number'] == number]


    def setUp(self):
        self.vorinclex = {
            'availability': ['arena', 'mtgo', 'paper'],
            'borderColor': 'black',
            'colorIdentity': ['G'],
            'colors': ['G'],
            'convertedManaCost': 6,
            'foreignData': [
            {'language': 'German', 'name': 'Vorinclex, Monströser Plünderer'},
            {'language': 'Japanese', 'name': '巨怪な略奪者、ヴォリンクレックス'}
            ],
            'frameEffects': ['legendary'],
            'frameVersion': '2015',
            'hasFoil': True,
            'hasNoFoil': True,
            'identifiers': {
                'cardKingdomFoilId': '240876',
                'cardKingdomId': '240364'
            },
            'layout': 'normal',
            'legalities': {'brawl': 'legal', 'commander': 'legal'},
            'manaCost': '{4}{G}{G}', #optional
            'name': 'Vorinclex, Monstrous Raider',
            'number': '199', 
            'originalType': 'Legendary Creature - Phyrexian Praetor', #optional
            'purcheUrls': {
                'cardKingdom': 'https://mtgjson.com/links/2747e6565b89d8d7',
                'cardKingdomFoil': 'https://mtgjson.com/links/aa26dedf96eb3b17',
                'cardmarket': 'https://mtgjson.com/links/95b02c738832a8d7',
                'tcgplayer': 'https://mtgjson.com/links/eb11d35e7c6f987c'
            },
            'rarity': 'mythic',
            'rulings':[],
            'setCode': 'KHM',
            'subtypes': ['Phyrexian', 'Praetor'],
            'supertypes': ['Legendary'],
            'type': 'Legendary Creature - Phyrexian Praetor',
            'types': ['Creature'], #optional
            'uuid': '70c713a0-f8a4-5980-9f69-4580764c3955',
            'variations': ['9d9018f2-42b3-5930-9663-f8a9a026d0ff'],
            'watermark': 'phyrexian' #optional
        }

        self.blex_front = {
            'artist': 'Ekaterina Burmak', #optional
            'availability': ['arena', 'mtgo', 'paper'],
            'borderColor': 'black',
            'colorIdentity': ['B', 'G'],
            'colors': ['G'],
            'convertedManaCost': 3,
            'foreignData': [],
            'faceName': 'Blex, Vexing Pest',
            'frameEffects': ['legendary'],
            'frameVersion': '2015',
            'hasFoil': True,
            'hasNoFoil': True,
            'identifiers': {
                'cardKingdomFoilId': '244824',
                'cardKingdomId': '244519'
            },
            'layout': 'modal_dfc',
            'legalities': {
                'brawl': 'legal',
                'commander': 'legal'
            },
            'manaCost': '{2}{G}', #optional
            'name': 'Blex, Vexing Pest // Search for Blex',
            'number': '148', 
            'originalType': 'Sorcery', #optional
            'otherFaceIds': ['55cd326c-01c3-5523-b2fe-22a614594d5c'],
            'purcheUrls': {
                'cardKingdom': 'https://mtgjson.com/links/166ba31249f0ef4',
                'cardKingdomFoil': 'https://mtgjson.com/links/bf3342d9490a7b11',
                'cardmarket': 'https://mtgjson.com/links/987e61793c3e42bb',
                'tcgplayer': 'https://mtgjson.com/links/7b2c31f2567edb6a'
            },
            'rarity': 'mythic',
            'rulings':[
            {'date': '2021-04-16',
                'text': 'If a creature is more than one of the creature types Blex cares about, it may haunt your dreams, but it will get the +1/+1 bonus only once.'},
            {'date': '2021-04-16',
                'text': 'While resolving Search for Blex, you may put any number of the cards into your hand, even if you don’t have enough life to cover it. We’ll assume you have a plan that’s better than “and then I’ll lose the game.”'}],
            'setCode': 'STX',
            'subtypes': ['Pest'],
            'supertypes': ['Legendary'],
            'type': 'Legendary Creature - Pest',
            'types': ['Creature'], #optional
            'uuid': '5a52cce7-3897-5901-a0ab-d1ed087c41ee',
            'variations': ['caa57405-19ac-5d47-923a-af2a132cc509'],
            'watermark': 'witherbloom' #optional
        }

        self.blex_back = {
            'artist': 'Ekaterina Burmak', #optional
            'availability': ['arena', 'mtgo', 'paper'],
            'borderColor': 'black',
            'colorIdentity': ['B', 'G'],
            'colors': ['B'],
            'convertedManaCost': 3,
            'foreignData': [],
            'faceName': 'Search for Blex',
            'frameEffects': ['legendary'],
            'frameVersion': '2015',
            'hasFoil': True,
            'hasNoFoil': True,
            'identifiers': {
                'cardKingdomFoilId': '244824',
                'cardKingdomId': '244519'
            },
            'layout': 'modal_dfc',
            'legalities': {
                'brawl': 'legal',
                'commander': 'legal'
            },
            'manaCost': '{2}{B}{B}', #optional
            'name': 'Blex, Vexing Pest // Search for Blex',
            'number': '148', 
            'originalType': 'Sorcery', #optional
            'otherFaceIds': ['55cd326c-01c3-5523-b2fe-22a614594d5c'],
            'purcheUrls': {
                'cardKingdom': 'https://mtgjson.com/links/166ba31249f0ef4',
                'cardKingdomFoil': 'https://mtgjson.com/links/bf3342d9490a7b11',
                'cardmarket': 'https://mtgjson.com/links/987e61793c3e42bb',
                'tcgplayer': 'https://mtgjson.com/links/7b2c31f2567edb6a'
            },
            'rarity': 'mythic',
            'rulings':[
            {'date': '2021-04-16',
                'text': 'If a creature is more than one of the creature types Blex cares about, it may haunt your dreams, but it will get the +1/+1 bonus only once.'},
            {'date': '2021-04-16',
            'text': 'While resolving Search for Blex, you may put any number of the cards into your hand, even if you don’t have enough life to cover it. We’ll assume you have a plan that’s better than “and then I’ll lose the game.”'}],
            'setCode': 'STX',
            'subtypes': [],
            'supertypes': [],
            'type': 'Sorcery',
            'types': ['Sorcery'], #optional
            'uuid': '55cd326c-01c3-5523-b2fe-22a614594d5c',
            'variations': ['caa57405-19ac-5d47-923a-af2a132cc509'],
            'watermark': 'witherbloom' #optional
        }

        self.necromancy = {
            'artist': 'Pete Venters', #optional
            'availability': ['mtgo', 'paper'],
            'borderColor': 'black',
            'colorIdentity': ['B'],
            'colors': ['B'],
            'convertedManaCost': 3,
            'foreignData': [
                {'language': 'Japanese',
                'name': 'ネクロマンシー'}
            ],
            'frameVersion': '1997',
            'hasFoil': False,
            'hasNoFoil': True,
            'identifiers': {
                'cardKingdomId': '32089'
            },
            'layout': 'normal',
            'legalities': {
                'commander': 'legal',
                'duel': 'legal',
                'legacy': 'legal',
                'premodern': 'legal',
                'vintage': 'legal'
            },
            'manaCost': '{2}{B}', #optional
            'name': 'Necromancy',
            'number': '64', 
            'originalType': 'Enchantment', #optional
            'purcheUrls': {
                'cardKingdom': 'https://mtgjson.com/links/7ec3eae103589862',
                'cardmarket': 'https://mtgjson.com/links/f304e28797337e43',
                'tcgplayer': 'https://mtgjson.com/links/aeb2ecef0dcbe580'
            },
            'rarity': 'uncommon',
            'rulings': [],
            'setCode': 'VIS',
            'subtypes': [],
            'supertypes': [],
            'type': 'Enchantment',
            'types': ['Enchantment'], #optional
            'uuid': 'c7896b11-1cb7-5702-bb03-765517477212'
        }

        self.sliver_token = {
            'availability': ['paper'],
            'borderColor': 'black',
            'colorIdentity': [],
            'colors': [],
            'frameEffects': '',
            'frameVersion': '2015',
            'hasFoil': True,
            'hasNonFoil': True,
            'identifiers': {
                'mtgjsonV4Id': 'b2aba968-8780-5aea-afbb-340115af547a',
                'scryfallId': '2c7e0d67-b627-4cf7-8f56-e1f0bd75cd5c'
            },
            'layout': 'token',
            'name': 'Metallic Sliver',
            'number': '15',
            'reverseRelated': ['Sliversmith'],
            'setCode': 'TTSR',
            'subtypes': ['Sliver'],
            'supertypes': [],
            'type': 'Token Artifact Creature - Sliver',
            'types': ['Token', 'Artifact', 'Creature'],
            'uuid': "134a8ff3-eddb-5e65-9e27-ac521c0357e4"
        }

        self.vampire_token = {
            'availability': ['arena', 'paper'],
            'borderColor': 'black',
            'colorIdentity': ['W'],
            'colors': ['W'],
            'frameEffects':'' ,
            'frameVersion': '2015',
            'hasFoil': True,
            'hasNonFoil': True,
            'identifiers': {
                'mtgjsonV4Id': '9acb46b7-b25f-51f2-8d78-3a33984687a5',
                'scryfallId': '9acb46b7-b25f-51f2-8d78-3a33984687a5',
                'tcgplayerProductId': '145812'
            },
            'layout': 'token',
            'name': 'Vampire',
            'number': '1',
            'reverseRelated': [
                'Call to the Feast',
                "Legion's Landing // Adanto, the First Fort",
                'Mavren Fein, Dusk Apostle',
                'Paladin of the Bloodstained',
                "Queen's Commission"
            ],
            'setCode': 'TXLN',
            'subtypes': ['Vampire'],
            'supertypes': [],
            'type': "Token Creature - Vampire",
            'types': ['Token', 'Creature'],
            'uuid': '625decf2-a1bc-53b6-b601-342906413033'
        }

        self.json = {
            'meta': {
                'date': '2021-08-12',
                'version': '3.14.15'
            },
            'data': {
                'baseSetSize': 4,
                'cards': [self.vorinclex,
                    self.blex_front, self.blex_back, self.necromancy],
                'code': 'TEST',
                'isFoilOnly': False,
                'isOnlineOnly': False,
                'keyruneCode': 'TEST',
                'name': 'Test Set consisting of different Sets Cards',
                'releaseDate': '2021-02-05',
                'tokens': [self.vampire_token, self.sliver_token],
                'totalSetSize': 10,
                'translations': {},
                'type': 'expansion'
            }
        }


if __name__ == '__main__':
    unittest.main()
