__author__ = 'naval gupta'

import MySQLdb
import smtplib
from email.mime.text import MIMEText
import os
import time
import datetime
from COAP_Baseserver import BaseServer
from Database_Mgmt import DBMS

def send_mail(tiger_id, flag):
    sender = 'naval.gupta07@gmail.com'
    receivers = 'naval.gupta07@gmail.com'
    content = ""
    if(flag == 1):
        #crossed the boundary
        content +=  (tiger_id + " has crossed the reserve boundary")
    elif(flag == 2):
        content += (tiger_id + "has no details. Contact Forest Rangers.")
    elif(flag == 3):
        content += (tiger_id + "has not moved. Contact Forest Rangers.")
    print content
    msg = MIMEText(content, "plain")
    msg["Subject"] = "System Alert"
    msg["From"] = sender
    msg["To"] = receivers

    try:
        GMAIL_SMTP = "smtp.gmail.com"
        GMAIL_SMTP_PORT = 587
        smtpObj = smtplib.SMTP(GMAIL_SMTP, GMAIL_SMTP_PORT, timeout=30)
        #Identify yourself to GMAIL ESMTP server.
        smtpObj.ehlo()
        #Put SMTP connection in TLS mode and call ehlo again.
        smtpObj.starttls()
        smtpObj.ehlo()
        #Login to service
        smtpObj.login(user=receivers, password='*****')
        smtpObj.sendmail(sender, receivers, msg.as_string())
        #print "Successfully sent email"
    except smtplib.SMTPException as error:
        print "Error: unable to send email :  {err}".format(err=error)

def generate_alarm():
    try:
        os.system('beep -f %s -l %s' % (2000,2000))
    except Exception as error:
        print "Error: unable to generate alarm :  {err}".format(err=error)

if __name__=="__main__":
    sensor_list = [('localhost',60001),('localhost',60002)]
    dbms = DBMS()
    new_process = os.fork()
    if new_process == 0:
        boundary_x,boundary_y = dbms.getBoundary()
        while True:
            tiger_list = dbms.get_tigers()
            for tiger in tiger_list:
                flag = dbms.check_boundary(tiger,boundary_x,boundary_y)
                if flag > 0:
                    send_mail(tiger,flag)
                timestamp = dbms.get_last_record_time(tiger)
                if timestamp == -1:
                    send_mail(tiger,2)
                else:
                    time_diff = (datetime.datetime.now() - timestamp).total_seconds()
                    if time_diff > 60:
                        send_mail(tiger,3)
            time.sleep(30)
    else:
        while True:
            for sensor in sensor_list:
                print "Contacting sensor",sensor
                router = BaseServer(sensor[0],sensor[1])
                data = router.getClientLocation()
                if data != 0:
                    #response from the client sensor
                    new_flag = dbms.check_New_Tiger(data['rfid'])
                    if new_flag == 0:
                        dbms.add_tiger_info(data['rfid'])
                    dbms.add_sensor_data(data)
            time.sleep(5)
