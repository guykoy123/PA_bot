from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import H_B_checker
#code for retrieving contacts list:
#   contacts = driver.find_elements_by_class_name("_1wjpf")
#   s= [contact.text for contact in contacts] #extracts chats and last messsages
#   print (s[::2]) #print only chat names

driver = webdriver.Chrome('C:\Python36\chromedriver.exe')
driver.get('https://web.whatsapp.com')
bot_name="shit.py"
class Message:
    text=""
    time_stamp=""
    def __init__(self,message):
        self.text=message[0]
        self.time_stamp=message[1]

    def get_message(self):
        return self.text

def send_message(message):
    whatsapp_msg = driver.find_element_by_class_name('_2S1VP')
    whatsapp_msg.send_keys(message+"     -{}".format(bot_name))
    whatsapp_msg.send_keys(Keys.ENTER)


def Bot():


    time.sleep(10) #TODO: replace delay with question if bot can start

    message_class="message-out" #use message_out when checking your own messages (useful when you do not have a burner phone) if able to get another phone use message_in (this way client will notifications and will be easier to read and use)

    while(True):
        last_message=Message(driver.find_elements_by_class_name(message_class)[-1].text.split("\n"))

        if(last_message.get_message().lower()=="hello"):
            send_message("hi")
        elif(last_message.get_message().lower()=="date"):
            current_time=time.strftime("%a, %d %b %Y", time.gmtime())
            send_message(current_time)
        elif(last_message.get_message().lower()=="scream"):
            message=""
            for i in range(500):
                message+="aaaaa"
            send_message(message)
        elif(last_message.get_message().lower()=="get games"):
            send_message(H_B_checker.get_bundle())





if __name__ == "__main__":
    print("Bot is active, scan your QR code from your phone's WhatsApp")
    Bot()
