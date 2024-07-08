from riot import RIOT


if __name__ == "__main__":
    
    riot = RIOT()
    game_name = "sowieso"
    tag_line = "1116"
    game_count = 30
    region = "europe"
    game_ids = list()

    #riot.getLeague("RANKED_TFT")
    game_ids= riot.get_gameID_bysummoner(game_name, tag_line, region, game_count)
    
    riot.get_gameResult(region, game_ids[0])
    