import os
import time
import subprocess
import smtplib
from email.message import EmailMessage
import threading
from queue import Queue

file = open('ip.txt') #zmienna normalnie uzywana, ale dla testow adresy ip podane w kodzie
adres = ''

address_list = ['10.0.0.10','10.0.0.11','10.0.0.12','10.0.0.13','10.0.0.14']

print_lock = threading.Lock()

def threader():
    while True:
        ip = q.get()
        q.task_done()

q = Queue()

for x in range(5):
    t = threading.Thread(target=threader)
    t.daemon = True
    t.start()
#wysylanie wiadomosci o awarii
def send():
        alfa=1
        EMAIL_ADDRESS = 'WYSLANEPRZEZ@gmail.com'
        PASS = 'HASLO'

        message = EmailMessage()
        message['Subject'] = 'Awaria łącza'
        message['From'] = EMAIL_ADDRESS
        message['To'] = 'WYSLIJDO@gmail.com'

        message.set_content('TESC WIADOMOSCI '+ adres)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL_ADDRESS, PASS)
            smtp.send_message(message)
#sprawdzanie czy ip odpowiada
def ping_result():
    for ip in address_list:

        global adres
        adres = ip
        result = subprocess.Popen(['ping','-n','1',ip],stdout=file).wait()
        print(result,'   ', ip)
        if result == 1:
            q.put((ip))
            send()

ping_result()

q.join()
