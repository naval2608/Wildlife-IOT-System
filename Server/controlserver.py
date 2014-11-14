__author__ = 'naval gupta'

import MySQLdb
import smtplib
from email.mime.text import MIMEText
import os
import time
from COAP_Baseserver import BaseServer;

def send_mail():
    sender = 'naval.gupta07@gmail.com'
    receivers = 'naval.gupta07@gmail.com'

    #Create the message
    msg = MIMEText("This is a test e-mail message.", "plain")
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
        smtpObj.login(user=receivers, password='vesper2901')
        smtpObj.sendmail(sender, receivers, msg.as_string())
        print "Successfully sent email"
    except smtplib.SMTPException as error:
        print "Error: unable to send email :  {err}".format(err=error)

def insert_sensor_info(id,lat,long,time_info):
    # Open database connection
    db = MySQLdb.connect("localhost", "root", "", "iot_project");
    cursor = db.cursor()
    sql = "INSERT INTO sensor_info(rfid,latitude,longitude,record_time) VALUES ('" \
          + id + "'," + str(lat) + "," + str(long) + ",'" + time_info + "')";
    try:
        # Execute the SQL command
        cursor.execute(sql)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
    # disconnect from server
    db.close()

def generate_alarm():
    try:
        os.system('beep -f %s -l %s' % (2000,2000))
    except Exception as error:
        print "Error: unable to generate alarm :  {err}".format(err=error)

def add_sensor_data(data):
    if data:
        id = data['rfid']
        latitude = data['location']['latitude']
        longitude = data['location']['longitude']
        record_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['record_time']))
        print "Incoming data- Rfid:",id," Timestamp:",str(record_time)
        insert_sensor_info(id,latitude,longitude,record_time);

def monitor_data():
    print "hello"

if __name__=="__main__":
    new_process = os.fork()
    if new_process == 0:
        while True:
            monitor_data()
            time.sleep(10)
    else:
        while True:
            router = BaseServer()
            data = router.getClientLocation()
            add_sensor_data(data)
            time.sleep(5)
