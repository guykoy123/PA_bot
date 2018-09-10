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

class Message_Out: #class for scheduled messages
    text=""
    send_time=None
    def __init__(self,message,time):
        self.text=message
        self.send_time=time

    def get_time(self):
        return self.send_time

    def get_message(self):
        return self.text
