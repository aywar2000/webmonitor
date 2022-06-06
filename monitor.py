import requests
import os
import time
import logging
from bs4 import BeautifulSoup
import stash
import yagmail

URL_TO_MONITOR = "https://www.ebay-kleinanzeigen.de/"
DELAY_TIME = 15

SENDING_EMAIL_USERNAME = "hbtuju"
SENDING_EMAIL_PASSWORD = stash.stashPw 
RECIPIENT_EMAIL_ADDRESS = "maja.lovrekovic89@gmail.com"

def send_email_alert(alert_str):
    yagmail.SMTP(SENDING_EMAIL_USERNAME, SENDING_EMAIL_PASSWORD).send(
        RECIPIENT_EMAIL_ADDRESS, alert_str, alert_str)


def process_html(string):
    soup = BeautifulSoup(string, features="lxml")

    soup.prettify()

    for s in soup.select('script'):
        s.extract()

    for s in soup.select('meta'):
        s.extract()

    return str(soup).replace('\r', '')

def webpage_has_changed():
    """returns true if changed"""
    print(stash.stashPw)
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
    log.info("Running Website Monitor")
    while True:
        try:
            if webpage_has_changed():
                log.info("WEBPAGE WAS CHANGED.")

            else:
                log.info("Webpage was not changed.")
        except:
            log.info("Error checking website.")
        time.sleep(DELAY_TIME)


if __name__ == "__main__":
    main()