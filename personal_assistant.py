from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import exit
import H_B_checker
from PA_commands import *
import threading
from Message_classes import *
import datetime
import what_bot



def main():

    bot=what_bot.what_bot("shit.py","messagout")
    print("created instance of bot")

    #dictionary of availble commands and their code
    commands={"date": get_date,"scream":scream,"get bundles":H_B_checker.get_current_bundles}

    answer="n"
    while (answer.lower() != "y"):
        answer=input("Can i start? (Y/n)")
    print(bot.get_contacts_list())
    bot.send_message("ready at your service")

    """
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

        """



if __name__ == "__main__":
    print("Bot is active, scan your QR code from your phone's WhatsApp")
    main()
