import json
import pandas as pd

'''
This class create the empty dataframe that will get updated by calling the functions of 'basic_processing' class
'''

# Load the JSON file
with open("data/data_dragon.json", 'r') as file:
    data = json.load(file)

class make_list_df:

    def __init__(self, data_dragon):
        self.champions = pd.DataFrame(pd.DataFrame(data_dragon['sets']).loc['champions', '11'])
        self.items = pd.DataFrame(data_dragon['items'])
        self.augments = pd.DataFrame(data_dragon['items'])

    def is_empty_dict(self,x):
        return isinstance(x, dict) and not x

    #Create empty dataframe that stores the basic champion statistics
    def make_champ_list(self):
        champions_mask = self.champions['apiName'].str.startswith('TFT11')
        self.champions = self.champions[champions_mask]
        metrics = [
            'Count', 'Ave_score', 'Ave_score_save', 'Ave_star', 'Ave_star_save',
            'Ave_star_win', 'Win_count', 'Win_rate', 'Save_count', 'Save_rate',
            'Num_items_count', 'Num_items_avg', 'Num_items_save', 'Num_items_win',
            'Full_item_count', 'Full_item_rate', 'Full_item_save', 'Full_item_win'
        ]
        metrics_df = pd.DataFrame(0, index=self.champions.index, columns=metrics)

        metrics_df['Name'] = self.champions['apiName']
        metrics_df['Cost'] = self.champions['cost']

        columns_order = ['Name', 'Cost'] + metrics
        champs_df = metrics_df[columns_order]
        champs_df = champs_df.sort_values(by='Cost', ascending=True)
        champs_df.to_csv('champs_list.csv',sep=',', index=False, encoding='utf-8')

        return champs_df

    # Create empty dataframe that stores the basic item statistics
    def make_item_list(self):
        allowed_prefixes = ['TFT11_Item', 'TFT_Item']
        item_mask = self.items['apiName'].str.startswith(tuple(allowed_prefixes))
        self.items = self.items[item_mask]
        self.items = self.items.dropna(subset=['desc','name'])
        self.items = self.items[~self.items['effects'].apply(self.is_empty_dict)]

        metrics = [
            'Count', 'Ave_score', 'Ave_score_save', 'Win_count',
            'Win_rate', 'Save_count', 'Save_rate'
        ]
        metrics_df = pd.DataFrame(0, index=self.items.index, columns=metrics)

        metrics_df['Name'] = self.items['name']
        metrics_df = metrics_df.dropna(subset=['Name'])
        metrics_df = metrics_df[~metrics_df['Name'].str.contains('Emblem')]
        metrics_df = metrics_df[~metrics_df['Name'].str.contains('TFT')]
        metrics_df = metrics_df[~metrics_df['Name'].str.contains('tft')]
        metrics_df = metrics_df[~metrics_df['Name'].str.contains('displayname')]

        columns_order = ['Name'] + metrics
        items_df = metrics_df[columns_order]
        items_df.to_csv('items_list.csv', sep=',', index=False, encoding='utf-8')

        return items_df

    # Create empty dataframe that stores the basic augment statistics
    def make_augment_list(self):
        augment_mask = self.augments['apiName'].str.contains('Augment')
        self.augments = self.augments[augment_mask]

        metrics = [
            'Count', 'Ave_score', 'Ave_score_save', 'Win_count',
            'Win_rate', 'Save_count', 'Save_rate'
        ]
        metrics_df = pd.DataFrame(0, index=self.augments.index, columns=metrics)

        metrics_df['Name'] = self.augments['name']
        columns_order = ['Name'] + metrics
        augments_df = metrics_df[columns_order]
        augments_df.to_csv('augments_list.csv', sep=',', index=False, encoding='utf-8')

        return augments_df







