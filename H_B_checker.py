#python3

import bs4, requests

def get_games():
    """
    checks for game bundles on humble bundles
    """
    res=requests.get("https://www.humblebundle.com/games/")
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    games=list()
    for x in soup.findAll("div", class_="dd-captions"):
        game_name=x.text.split('\n')[-3][4:]
        if game_name.strip() != "":
            games.append(game_name)
    return games


#TODO: add finding free games
#TODO: return readable message with more info (like link,price,images,time)


def get_bundle():
    games=get_games()
    message="Games availble in the bundle right now are: "

    for game in games:
        message+=game+", "

    message =message[:-2] #remove ", " from the end
    message+="   here is the link: " + "https://www.humblebundle.com/games/"
    return message
