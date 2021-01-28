"""
I have a shitty ISP.  With varying frequency my modem will reboot as a result of lost connection.  This script
monitors the Arris SB6141 logs for the T4 timeout and will alert when it is about to reboot.
"""
__author__ = 'Mike Kress'


from requests_html import HTMLSession
from datetime import datetime
from time import sleep

session = HTMLSession()


def go():
    # Get the logs page
    try:
        r = session.get('http://192.168.100.1/cmLogsData.htm')
    except ConnectionError:
        return 'There is a connection error'
    except OSError:
        return 'network is disconnected'
    # Select the log messages
    messages = r.html.find('body > center > table > tbody > tr')
    # get a list of the values of the latest message
    fields = messages[1].find('td')
    # do the things
    try:
        log = {
            'date': fields[0].text,
            'id': fields[2].text,
            'message': fields[3].text,
            'severity': fields[1].text
        }
        # This is the message ID that preceeds a modem reboot.  T4 Timeout
        if log.get('id') == 'R04.0':
            status = 1
        else:
            status =0 
        return f'Status {status}  Now: {datetime.now()} Message Time: {log.get("date")} {log.get("id")}'
    except IndexError:
        return f'There are no log messages! {datetime.now()}'

if __name__ == "__main__":
    while True:
        print(go())
        sleep(2)



