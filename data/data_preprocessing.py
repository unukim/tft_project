import json
import pandas as pd

def item_data():
	file_path = 'data_dragon.json'
	with open(file_path, 'r') as json_file:
		data_dragon = json.load(json_file)
		items = pd.DataFrame(data_dragon['items'])
		allowed_prefixes = ['TFT11_Item', 'TFT_Item', 'TFT_Consumable']
		# Create a boolean mask for rows starting with any of the allowed prefixes
		mask = items['apiName'].str.startswith(tuple(allowed_prefixes))
		# Filter the DataFrame using the mask
		items = items[mask]
		items = items.drop(columns=['from','id', 'unique','icon', 'incompatibleTraits' ])
		items.to_csv('item_list.csv', sep=',', index=False, encoding='utf-8')
	
	return items


def augment_data():
	file_path = 'data_dragon.json'
	with open(file_path,'r') as json_file:
		data_dragon = json.load(json_file)
		augments = pd.DataFrame(data_dragon['items'])
		# Create a boolean mask for rows starting with any of the allowed prefixes
		mask = augments['apiName'].str.contains('Augment')
		# Filter the DataFrame using the mask
		augments = augments[mask]
		augments = augments.drop(columns=['from', 'id', 'unique', 'icon', 'incompatibleTraits'])

		augments.to_csv('augment_list.csv',sep=',', index=False, encoding='utf-8')

	return augments


def champion_data():
	file_path = 'data_dragon.json'
	with open(file_path, 'r') as json_file:
		data_dragon = json.load(json_file)
		
		champions = pd.DataFrame(pd.DataFrame(data_dragon['sets']).loc['champions', '11'])
		champions['ability'] = champions['ability'].apply(
			lambda x: x['desc'] if isinstance(x, dict) and 'desc' in x else x)
		champions = champions.drop(columns=['tileIcon', 'squareIcon', 'characterName'])

		desired_order = ['apiName', 'name', 'cost','traits','stats', 'ability' ]  # replace with actual column names
		champions = champions[desired_order]
		champions.to_csv('champion_list.csv',sep=',', index=False, encoding='utf-8')

	return champions


def traits_data():
	file_path = 'data_dragon.json'
	with open(file_path, 'r') as json_file:
		data_dragon = json.load(json_file)
		traits = pd.DataFrame(pd.DataFrame(data_dragon['sets']).loc['traits', '11'])
		traits = traits.drop(columns=['icon'])
		traits.to_csv('trait_list.csv', sep=',', index=False, encoding='utf-8')

	return traits

item_data()
augment_data()
champion_data()
traits_data()

