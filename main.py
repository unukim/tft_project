from src.riotapi import RiotAPI


if __name__ == "__main__":
    
    riot_api = RiotAPI()
    game_name = "Upin and Ipin"
    tag_line = "EUW"
    game_count = 1
    region = "europe"
    game_ids = list()
    
    game_ids = riot_api.get_gameID_bysummoner(game_name, tag_line, region, game_count)
    
    game_result = riot_api.get_game_result(region, game_ids[0])

    