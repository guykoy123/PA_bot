from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import exit
import H_B_checker
from PA_commands import *
#code for retrieving contacts list:
#   contacts = driver.find_elements_by_class_name("_1wjpf")
#   s= [contact.text for contact in contacts] #extracts chats and last messsages
#   print (s[::2]) #print only chat names



driver = webdriver.Chrome('C:\Python36\chromedriver.exe')
driver.get('https://web.whatsapp.com')
bot_name="shit.py"

class Message_In: #class for recieved messages
    text=""
    time_stamp=""
    def __init__(self,message,time):
        self.text=message
        self.time_stamp=message

    def get_message(self):
        return self.text

    def get_time(self):
        return self.time_stamp

def send_message(message):
    """
    recieves a string or list of strings
    if strings:
        send all in one line
    if list:
        each index is a new line
    """
    whatsapp_msg = driver.find_element_by_class_name('_2S1VP') #find text box elemnt

    if(isinstance(message,str)):
        whatsapp_msg.send_keys(message) #input message
        whatsapp_msg.send_keys(Keys.SHIFT+Keys.ENTER) #create new line

    elif(isinstance(message,list)):
        for line in message: #run through all the lines
            whatsapp_msg.send_keys(line) #input line
            whatsapp_msg.send_keys(Keys.SHIFT+Keys.ENTER) #create new line

    whatsapp_msg.send_keys(Keys.SHIFT+Keys.ENTER) #create new line
    whatsapp_msg.send_keys("-{}".format(bot_name)) #add bot name tag
    whatsapp_msg.send_keys(Keys.ENTER) #send message

def Bot():
    #dictionary of availble commands and their code
    commands={"hello":"hi","date": get_date(),"scream":scream(),"get bundle":H_B_checker.get_bundle()}

    answer="n"
    while (answer.lower() != "y"):
        answer=input("Can i start?")

    send_message("ready for you service")

    message_class="message-out" #use message_out when checking your own messages (useful when you do not have a burner phone) if able to get another phone use message_in (this way client will notifications and will be easier to read and use)

    while(True):
        message_parts=driver.find_elements_by_class_name(message_class)[-1].text.split("\n")
        if(message_parts[-2]!="-shit.py"):
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object

            if(last_message.get_message().lower()=="help"):
                command_list=list(commands.keys())
                command_list.append("quit")
                send_message(command_list)

            elif(last_message.get_message().lower()=="quit"):
                send_message("shutting down....")
                exit()

            else:
                try:
                    message=commands[last_message.get_message().lower()]
                    send_message(message)

                except KeyError:
                    send_message(["command does not exists","type help to see all commands"])





if __name__ == "__main__":
    print("Bot is active, scan your QR code from your phone's WhatsApp")
    Bot()
