from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from threading import Lock
from Message_classes import *
from time import sleep
class what_bot:
    name="" #bot name
    message_class=None #use message-out when checking your own messages (useful when you do not have a burner phone)
                       #if able to get another phone use message-in (this way client will notifications and will be easier to read and use)

    driver=None #selenium web driver for the bot
    driver_Lock=Lock() #driver lock to prevent multiple concurent uses
    quit=False #state of the bot, if set to true the bot is not running

    def __init__(self,bot_name,message_type):
        """
        create a new instance of what_bot
        message_type can be equal to "message-out" or "message-in"
        """

        self.name=bot_name #set bot name
        if (message_type != "message-out" and message_type != "message-in"):#check if message type is correct
            raise message_type_error(message_type) #if not, raise message_type_error exception
        else:
            self.message_class=message_type #set message type

        self.driver = webdriver.Chrome('C:\Python36\chromedriver.exe') #launch chrome driver
        self.driver.get('https://web.whatsapp.com') #connect to the website

    def get_contacts_list(self):
        """
        returns list of all contact names
        """
        contacts = self.driver.find_elements_by_class_name("_1wjpf")
        s= [contact.text for contact in contacts] #extracts chats and last messsages
        print ("get contacts: "+str(s)) #print only chat names
        return s[::2] #returns only chat names

    def get_last_message(self):
        """
        returns last message in conversation
        """
        self.driver_Lock.acquire() #acquire driver lock
        message=self.driver.find_elements_by_class_name(message_class)[-1].text #
        driver_Lock.release()
        return message


    def send_message(self,message):
        """
        recieves a string or list of strings
        if string:
            send all in one line
        if list:
            each index is a new line

        adds a new lin at the end with the bots name
        """
        connected=False
        self.driver_Lock.acquire()
        while(not connected):
            try:
                whatsapp_msg = self.driver.find_element_by_class_name('_2S1VP') #find text box element
                connected=True
            except Exception as exc:
                print(exc)
                sleep(1)


        if(isinstance(message,str)): #check if the message is of type string
            whatsapp_msg.send_keys(message) #input message
            whatsapp_msg.send_keys(Keys.SHIFT+Keys.ENTER) #create new line

        elif(isinstance(message,list)): #check if the message is of type list
            for line in message: #run through all the lines
                whatsapp_msg.send_keys(line) #input line
                whatsapp_msg.send_keys(Keys.SHIFT+Keys.ENTER) #create new line

        whatsapp_msg.send_keys(Keys.SHIFT+Keys.ENTER) #create new line
        whatsapp_msg.send_keys("-{}".format(bot_name)) #add bot name tag

        whatsapp_msg.send_keys(Keys.ENTER) #send message
        self.driver_Lock.release() #release driver lock




class message_type_error(Exception):
    given_type=""

    def __init__(self,given_type):
        """
        create exception instance and save the bad value that was given
        """
        self.given_type=given_type

    def __str__(self):
        error_str="Message type wasn't set to \"message-out\" or \"message-in\". You gave {}".format(self.given_type)
        return error_str
