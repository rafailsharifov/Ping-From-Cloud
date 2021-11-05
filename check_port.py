import socket
import sys
sys.path.insert(1, "/Python_projects")
from Send_sms import sms
import time
from datetime import datetime

phone_number = [9945123456789,99450987654321]
url = "https://google.com"

a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
location = (url, 443)

time_count = 1
command_status = True
try:
    while True:
        t = 0
        f = 0
        for i in range(1, 10, 1):
            try:
                result_of_check = a_socket.connect_ex(location)
                a_socket.close()
            except: result_of_check = 404  #site is not reachable

            if result_of_check == 0:
                t+=1
            else:
                f+=1
            time.sleep(1)

        if (f / i) * 100 > 60:  # If loss is greater than 40 percent
            time_count += 1

            if time_count == 3:  # Retry 2 times to ensure Delta is DOWN
                command_status = False


        elif (t / i) * 100 > 40:  # If success is greater than 40 percent
            time_count = 1
            time.sleep(15)

        if time_count % 60 == 0:  # repead by 10 min
            sms(to=phone_number,
                text="Google:443 still is not reachable for 10 min!\nSent from script on cloud!")

        if command_status is False:  # If is True, it means last time up_commands was sent, so it is working over Delta right now
            sms(to=phone_number, text="Google:443 is not reachable\nSent from script on cloud!")
            command_status = True

        if datetime.today().day == 1:
            if datetime.now().strftime("%H:%M") == "06:31":
                sms(to=phone_number, text="It is 1st of month and I am always on.\nRegards,\nYour port checker script on cloud")
                time.sleep(60)

        if time_count == 6000000:
            time_count = 60


except Exception as text:
     sms(to = phone_number, text = "Ooouups,\Port checkup failed!\nSent from script on cloud!")




