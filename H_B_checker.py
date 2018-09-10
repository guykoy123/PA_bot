#python3

#import bs4, requests


from selenium import webdriver
from time import sleep

class Bundle:
    """
    Bundle class, used to store information about each bundle
    """
    name=""
    time_left=""
    link=""

    def __init__(self,name,time_left,link="N/A"):
        self.name=name
        self.time_left=time_left
        self.link=link

    def get_name(self):

        return self.name

    def get_time_left(self):
        return self.time_left

    def get_link(self):
        return self.link

    def set_link(self,link):
        self.link=link

def get_current_bundles():
    """
    retrieves currently available bundles on humble bundle
    creates a Bundle object for each that store info like name, time left and link
    """

    driver = webdriver.Chrome('C:\Python36\chromedriver.exe')
    driver.get('https://www.humblebundle.com') #open the site

    driver.find_elements_by_class_name("js-bundle-dropdown")[0].click() #open the tab that holds all the bundles
    print("clicked")
    sleep(2) #delay to wait until tab opens
    bundles_elm=driver.find_elements_by_class_name("navbar-tile") #retrieve bundle elements
    bundles=list()
    for i in bundles_elm:
        parts=i.text.split("\n") #split the text first part is time left, second is the name
        bundles.append(Bundle(parts[1],parts[0])) #create Bundle object withour link

    a=driver.find_elements_by_partial_link_text("HUMBLE") #find all objects with 'HUMBLE' in the text
    #some bundles appear more then once however they appear the second time onle after all the bundles appeared once
    #which means by using the list of Bundles created earlier it is possible to just ignore because the end of the list is reached while looping before link appear twice
    print("got links")

    for i in range(len(bundles)):
        bundles[i].set_link(a[i].get_attribute("href")) #for each existing Bundle add the corresponding link


    #construct message
    message=list()
    for b in bundles:
        message.append(b.get_name())
        message.append(b.get_time_left())
        message.append(b.get_link())
        message.append(" ")

    return message


"""def get_games():
    """
    #checks for game bundles on humble bundles
    """
    #TODO: return readable message with more info (like link,price,images,time)
    res=requests.get("https://www.humblebundle.com/games/")
    soup=bs4.BeautifulSoup(res.text,'html.parser')
    games=list()
    for x in soup.findAll("div", class_="dd-captions"):
        game_name=x.text.split('\n')[-3][4:]
        if game_name.strip() != "":
            games.append(game_name)

    return games"""


#TODO: add finding free games
