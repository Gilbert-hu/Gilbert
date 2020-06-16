from pythonping import ping
import os
import time
import smtplib
from email.message import EmailMessage
import threading
from queue import Queue

address_list = ['10.0.0.10','192.168.43.1','10.0.0.11']
q = Queue()
#pobieranie z kolejki
ip = ''
def send():
    #print(type(ip), ip)
    EMAIL_ADDRESS = 'hiltkom@gmail.com'#os.environ.get('EMAIL_USER')
    PASS = 'SoundEpic69'#os.environ.get('EMAIL_PASS')

    message = EmailMessage()
    message['Subject'] = 'Awaria łącza'
    message['From'] = EMAIL_ADDRESS
    #message['To'] = 'Hubert.Ligocki@jeronimo-martins.com'
    message['To'] = 'hubert.ligocki@gmail.com'

    message.set_content('Wiadomosc testowa. Proszę ją zignorowac ')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, PASS)
        smtp.send_message(message)


def main():

    print('wykonuje glowne funkcje')
    ip = q.get()
    #print('1')
    response_list = ping(ip, size = 1, count = 2, timeout = 1)
    #print('2')
    #print(response_list.rtt_avg_ms)
    if response_list.rtt_avg_ms > 4:
        print(response_list)
        #print(ip)
        #send()
        #print('adres NIE odpowiada')
    else:
        print('adres odpowiada')
    q.task_done()

    #print('koncze wykonywanie glownej funkcji')

for x in range(3):
    print('check')
    t = threading.Thread(target=main)
    #t.daemon = True
    t.start()
    print(t)

for ip in address_list:
    #print(ip)
    ip = q.put(ip)
