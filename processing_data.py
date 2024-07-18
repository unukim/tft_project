import numpy as np
import pandas as pd
from copy import deepcopy
from collections import Counter
from datetime import datetime
import json


class basic_preprocessing:

    def __init__(self, game_result, unit_result, cluster_on=False):

        self.game_result = game_result
        self.unit_result = unit_result
        self.augment_list = pd.read_csv('augments_list.csv')
        self.champion_list = pd.read_csv('champs_list.csv')
        self.item_result = pd.read_csv('items_list.csv')

        if not cluster_on:
            self.after_join = pd.merge(self.unit_result, self.game_result[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3']],
                                       on=['Game_id', 'Player_id', 'Datetime'])
            self.after_join = self.after_join[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3', 'character_id',
                 'rarity', 'tier', 'item1', 'item2', 'item3']]
        else:
            self.after_join = pd.merge(self.unit_result, self.game_result[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3', 'Deck']],
                                       on=['Game_id', 'Player_id', 'Datetime'])
            self.after_join = self.after_join[
                ['Datetime', 'Game_id', 'Player_id', 'Placement', 'Deck', 'augment1', 'augment2', 'augment3',
                 'character_id', 'rarity', 'tier', 'item1', 'item2', 'item3']]

    def change_gloves_item(self):

        check = np.logical_or(self.after_join.item1 == "Thief's Gloves", self.after_join.item1 == "Accomplice's Gloves")

        self.after_join.loc[check, 'item2'] = 'None'

        self.after_join.loc[check, 'item3'] = 'None'
        return self.after_join

    def check_item_unit_itemver(self):

        check = self.after_join.apply(lambda x: 3 - list(x).count('None'), axis=1)

        self.after_join['num_item'] = check
        after_join = pd.DataFrame(self.after_join)
        after_join.to_csv("afterjoin.csv", sep=',', index=False, encoding='utf-8')

        return self.after_join

    def make_augment_stack(self):

        check = self.after_join[
            ['Datetime', 'Game_id', 'Player_id', 'Placement', 'augment1', 'augment2', 'augment3']].drop_duplicates()

        result = self.augment_list.copy()

        for i in range(1, 9):
            place = check.loc[check.Placement == i,]
            augments = place.augment1.tolist() + place.augment2.tolist() + place.augment3.tolist()
            augments = Counter(augments)
            augment_result = [0] * 7

            for augment in augments.keys():
                number = augments[augment]

                if i == 1:
                    augment_score = [number, number * i, number * i, number, number, number, number]
                elif i <= 4:
                    augment_score = [number, number * i, number * i, 0, 0, number, number]
                else:
                    augment_score = [number, number * i, 0, 0, 0, 0, 0]

                result.loc[result.Name == augment,
                ['Count', 'Ave_score', 'Ave_score_save', 'Win_count', 'Win_rate', 'Save_count',
                 'Save_rate']] += augment_score

        result.Ave_score = round(result.Ave_score / result.Count, 1)

        result.Ave_score_save = round(result.Ave_score_save / result.Save_count, 1)

        result.Win_rate = round(result.Win_rate / result.Count * 100, 1)

        result.Save_rate = round(result.Save_rate / result.Count * 100, 1)

        result.to_csv('augment.csv', sep=',', index=False, encoding='utf-8')

        return result
