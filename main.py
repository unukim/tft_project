from riot import RIOT


if __name__ == "__main__":
    
    riot = RIOT()
    
    riot.getLeague("RANKED_TFT")
    riot.extract_game_by_summoner("sowieso")
    
    