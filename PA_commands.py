import time


def get_date():
    return time.strftime("%a, %d %b %Y", time.gmtime())

def scream():
    message=""
    for i in range(500):
        message+="aaaaa"
    return message
