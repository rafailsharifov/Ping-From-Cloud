import sys
sys.path.insert(1, "/Python_projects")
import time
from Send_sms import sms
from datetime import datetime, date
import multiprocessing as mp
import os, platform



time_count = 1
command_status = True
phone_number = [99451123456,99450987654321]


try:
    def paralel_process(host, result, time_count, command_status, phone_number):

        while True:
            t = 0
            f = 0

            for i in range(1, 10, 1):
                response = os.system("ping -W 1 " + ("-n 1 " if platform.system().lower() == "windows" else "-c 1 ") + host)
                now = datetime.now()
                # and then check the response...
                if host == "11.1.1.1":
                    hostname = "Delta"
                elif host == "22.2.2.2":
                    hostname = "Azertelekom"

                if response == 0:  # we got echo reply packet from partner
                    t += 1  # If True
                else:
                    f += 1  # If False
                    try:
                        temp_file = open(hostname + ".log", "a")
                        temp_file.write(str(i) + ": " + str(now))
                        temp_file.write("\n")
                        temp_file.write("Ping failed! Response is: " + str(response))
                        temp_file.write("\n")
                        temp_file.close()
                    except: sms(to=phone_number, text="Could not write log!\nSent from script on cloud!")

            if (f / i) * 100 > 60:  # If loss is greater than 40 percent
                time_count += 1

                if time_count == 3:  # Retry 2 times to ensure Delta is DOWN
                    command_status = False


            elif (t / i) * 100 > 40:  # If success is greater than 40 percent
                time_count = 1
                time.sleep(15)

            if time_count % 60 == 0:  # repead by 10 min
                sms(to=phone_number, text="ASB Internet connection over " + hostname + " is still down for 10 min!\nSent from script on cloud!")

            if command_status is False:  # If is True, it means last time up_commands was sent, so it is working over Delta right now
                sms(to=phone_number, text="ASB Internet connection over " + hostname + " is down!\nSent from script on cloud!")
                command_status = True
                
             if datetime.today().day == 1:
                if datetime.now().strftime("%H:%M") == "06:30":
                    sms(to =phone_number, text = "It is 1st of month and I am always on.\nRegards,\nYour script on cloud:)")
                    time.sleep(60)

            if time_count == 6000000:
                time_count = 60



    if __name__ == '__main__':

        result = mp.Queue()
        processes = [mp.Process(target=paralel_process, args=(host, result, time_count, command_status, phone_number)) for host in ["11.1.1.1", "22.2.2.2"]]

        for p in processes:
            p.start()
        for p in processes:
            p.join()

            #result = [result.get() for p in processes]




except Exception as text:
     sms(to = phone_number, text = "Ooouups,\nPing checkup failed!\nSent from script on cloud!")

                                                                                                            
