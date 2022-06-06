from cgitb import text
from click import echo
import requests
import os
import time
import logging
from bs4 import BeautifulSoup
import stash
# novo
import smtplib
from email.message import EmailMessage

gmail_password = stash.googlePw

def send_email_gmail(subject, message, destination):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('hbtuju@gmail.com', gmail_password)

    msg = EmailMessage()

    message = f'{message}\n'
    msg.set_content(message)
    msg['Subject'] = subject
    msg['From'] = 'hbtuju@gmail.com'
    msg['To'] = destination
    server.send_message(msg)
    echo('msg sent')



URL_TO_MONITOR = "https://www.wbm.de/wohnungen-berlin/angebote/"
DELAY_TIME = 300


def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    soup.prettify()

    for s in soup.select('script'):
        s.extract()

    for s in soup.select('meta'):
        s.extract()

    return str(soup).replace('\r', '')

def webpage_has_changed():

    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
    'Pragma': 'no-cache', 'Cache-Control': 'no-cache'}
    response = requests.get(URL_TO_MONITOR, headers=headers)
    #how to comment out in pzthon
    if not os.path.exists("previous-content.txt"):
        open("previous-content.txt", 'w+').close()

    filehandle = open("previous-content.txt", 'r')
    previous_response_html = filehandle.read() 
    filehandle.close()

    if previous_response_html == response.text:
        return False
    else:
        filehandle = open("previous-content.txt", 'w')
        filehandle.write(response.text)
        filehandle.close()
        return True

def main():
    log = logging.getLogger(__name__)
    logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), format='%(asctime)s %(message)s')
    while True:
        try:
            if webpage_has_changed():
                log.info("WEBPAGE WAS CHANGED.")
                send_email_gmail('WBM', 'WBM Stranica = novi oglasi', 'maja.lovrekovic89@gmail.com')
            else:
                log.info("Webpage was not changed.")
        except:
            log.info("Error checking website.")

        time.sleep(DELAY_TIME)


if __name__ == "__main__":
    main()