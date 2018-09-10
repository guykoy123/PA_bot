from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import exit
import H_B_checker
from PA_commands import *
import threading
from Message_classes import *
import datetime

#code for retrieving contacts list:
#   contacts = driver.find_elements_by_class_name("_1wjpf")
#   s= [contact.text for contact in contacts] #extracts chats and last messsages
#   print (s[::2]) #print only chat names

#dictionary of availble commands and their code
commands={"date": get_date,"scream":scream,"set reminder":set_reminder,"get bundles":H_B_checker.get_current_bundles}
bot_name="shit.py"
message_class="message-out" #use message_out when checking your own messages (useful when you do not have a burner phone) if able to get another phone use message_in (this way client will notifications and will be easier to read and use)
scheduled_messages=list()

#driver needs to be public so it is declared here
driver = webdriver.Chrome('C:\Python36\chromedriver.exe')
driver.get('https://web.whatsapp.com')#connect to the website

def scheduled_sender():
    while(True):
        if (scheduled_messages):
            for message in scheduled_messages:
                if (message.get_time()>= time.localtime()):
                    send_message(message.get_message())
                    scheduled_messages.remove(message)

def set_reminder():
    send_message("Set reminder time")
    while(True):
        message_parts=driver.find_elements_by_class_name(message_class)[-1].text.split("\n")
        if(message_parts[-2]!="-shit.py"):
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object
            rem_time=time.strptime(last_message.get_message(),'%H:%M')
            break

    send_message("set reminder message")
    while(True):
        message_parts=driver.find_elements_by_class_name(message_class)[-1].text.split("\n")
        if(message_parts[-2]!="-shit.py"):
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object
            rem_text=last_message.get_message()
            print(rem_text)
            break

    global scheduled_messages
    scheduled_messages.append(Message_Out(rem_text,rem_time))
    return("reminder set for "+str(rem_time))


def send_message(message):
    """
    recieves a string or list of strings
    if strings:
        send all in one line
    if list:
        each index is a new line
    """
    whatsapp_msg = driver.find_element_by_class_name('_2S1VP') #find text box element

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
    answer="n"
    while (answer.lower() != "y"):
        answer=input("Can i start? (Y/n)")

    t=threading.Thread(target=scheduled_sender)
    t.start() #start thread that is responsible for sending scheduled messages

    send_message("ready at your service")

    while(True):
        message_parts=driver.find_elements_by_class_name(message_class)[-1].text.split("\n") #extract last message and split by new lines
        if(message_parts[-2]!="-shit.py"): #check that the message was not sent by the bot (by checking that there is no '-shit.py' tag at the end)
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object

            if(last_message.get_message().lower()=="help"): #check if the command is help
                command_list=list(commands.keys()) #send command list
                command_list.append("quit")
                send_message(command_list)

            elif(last_message.get_message().lower()=="quit"): #check if command is quit
                send_message("shutting down....") #send notification about shutting down
                #TODO: add closing of the browser
                exit() #shut down bot

            else: #if command is not 'help' or 'quit'
                try:
                    message=commands[last_message.get_message().lower()]() #try to execute the command by inputing the message text as a key in the commands dictiory
                    send_message(message)

                except KeyError: #if the command doesn't exist notify the user
                    send_message(["command does not exists","type help to see all commands"])

                except Exception as exc:
                    print(exc)





if __name__ == "__main__":
    print("Bot is active, scan your QR code from your phone's WhatsApp")
    Bot()
