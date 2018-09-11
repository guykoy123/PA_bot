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


bot_name="shit.py"
message_class="message-out" #use message_out when checking your own messages (useful when you do not have a burner phone) if able to get another phone use message_in (this way client will notifications and will be easier to read and use)
scheduled_messages=list()
quit=False #state of the bot, if set to true the bot is not running
driver_Lock=threading.Lock()

#driver needs to be public so it is declared here
driver = webdriver.Chrome('C:\Python36\chromedriver.exe')
driver.get('https://web.whatsapp.com')#connect to the website

def get_last_message():
    driver_Lock.acquire()
    message=driver.find_elements_by_class_name(message_class)[-1].text
    driver_Lock.release()
    return message

def scheduled_sender():
    while(not quit):
        if (scheduled_messages):
            for message in scheduled_messages:
                if (message.get_time() - datetime.datetime.now() <= datetime.timedelta(seconds=30)):
                    send_message("reminder: "+message.get_message())
                    scheduled_messages.remove(message)


def set_reminder():
    send_message("In how much would you like me to remind you?")
    while(True):
        message_parts=driver.find_elements_by_class_name(message_class)[-1].text.split("\n")
        if(message_parts[-2]!="-shit.py"):
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object
            try:
                t=datetime.datetime.strptime(last_message.get_message(),'%H:%M')
                rem_time=datetime.datetime.now().replace(hour=t.hour,minute=t.minute,second=0)
                break
            except Exception as exc:
                print(str(exc))
                send_message("error")

    send_message("set reminder message")
    while(True):
        message_parts=get_last_message().split("\n")
        if(message_parts[-2]!="-shit.py"):
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object
            rem_text=last_message.get_message()
            print(rem_text)
            break

    global scheduled_messages
    scheduled_messages.append(Message_Out(rem_text,rem_time))
    print("reminder set for "+str(rem_time.time()).split('.')[0])
    return("reminder set for "+str(rem_time.time()).split('.')[0]) #send only the time (without date) but without microseconds))


def send_message(message):
    """
    recieves a string or list of strings
    if strings:
        send all in one line
    if list:
        each index is a new line
    """
    connected=False
    driver_Lock.acquire()
    while(not connected):
        try:
            whatsapp_msg = driver.find_element_by_class_name('_2S1VP') #find text box element
            connected=True
        except Exception as exc:
            print(exc)
            time.sleep(1)


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
    driver_Lock.release()


def Bot():

    #dictionary of availble commands and their code
    commands={"date": get_date,"get weather":get_weather_forecast,"scream":scream,"set reminder":set_reminder,"get bundles":H_B_checker.get_current_bundles}

    answer="n"
    while (answer.lower() != "y"):
        answer=input("Can i start? (Y/n)")

    t=threading.Thread(target=scheduled_sender)
    t.start() #start thread that is responsible for sending scheduled messages

    send_message("ready at your service")

    while(True):
        message_parts=get_last_message().split("\n") #extract last message and split by new lines
        if(message_parts[-2]!="-shit.py"): #check that the message was not sent by the bot (by checking that there is no '-shit.py' tag at the end)
            last_message=Message_In(message_parts[0],message_parts[-1]) #extract last message and create Message_In object

            if(last_message.get_message().lower()=="help"): #check if the command is help
                command_list=list(commands.keys()) #send command list
                command_list.append("quit")
                send_message(command_list)

            elif(last_message.get_message().lower()=="quit"): #check if command is quit
                send_message("shutting down....") #send notification about shutting down
                driver.quit() #ends WebDriver session gracefullly
                global quit
                quit=True #set wuit to to signal shutting down
                t.join() #wait for the thread to close
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
