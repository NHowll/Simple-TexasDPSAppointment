import requests
import time
import os

#Stupid simple script that querys the texas DPS website for the next available appointment checking for canceled appointments (1 query every 5 mins so you dont get auto blocked by network sec)

#660 = Pflugerville
init = 0
fstdday = 0
fststdmnt = 0

headers = {'Host': 'publicapi.txdpsscheduler.com', 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
    'Accept':'application/json, text/plain, */*','Accept-Language':'en-US,en;q=0.5','Accept-Encoding':'gzip, deflate',
    'Referer':'https://public.txdpsscheduler.com/','Content-Type':'application/json;charset=utf-8','Origin': 'https://public.txdpsscheduler.com','DNT':'1','Connection':'keep-alive'}

data = '{"LocationId":"660","TypeId":"710","SameDay":"true","StartDate":"null","PreferredDay":"0"}'
#Change based on location^# 
while True:
    req = requests.post('https://publicapi.txdpsscheduler.com/api/AvailableLocationDates', headers=headers, data=data)
    print(req.status_code)
    mess = req.text
    dlc = mess.index("FirstAvailableDate")
    ndlc = mess.index("NextAvailableGroupDate")
    frstdatestr = mess[dlc+21:dlc+40]
    nxtdatestr = mess[ndlc+25:ndlc+44]
    print("First available Date: ",frstdatestr)
    print("Next available Date ", nxtdatestr)
    frstthres = frstdatestr[5:10]
    nxtthres = nxtdatestr[5:10]
    frstmonth = int(frstthres[0:2])
    frstday = int(frstthres[3:5])
    if init == 0:
        fststdmnt = frstmonth
        fstdday = frstday
        init = 1
    if frstmonth < fststdmnt:
        fststdmnt = frstmonth
        print("AVAILABILITY OPENED")
        os.system("start firefox https://public.txdpsscheduler.com/")
    if frstday < fstdday and frstmonth <= fststdmnt:
        print("AVAILABILITY OPENED")
        os.system("start firefox https://public.txdpsscheduler.com/")
    time.sleep(300)