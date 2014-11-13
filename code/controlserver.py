__author__ = 'NAVAL'

import MySQLdb, smtplib
from email.mime.text import MIMEText
import winsound

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
    db = MySQLdb.connect("localhost", "root", "1234", "iot_project");
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
        for i in range(0, 3):
            winsound.Beep(10000, 100)
        for i in range(0, 3):
            winsound.Beep(20000, 400)
        for i in range(0, 3):
            winsound.Beep(25000, 100)
        Freq = 800 # Set Frequency To 2500 Hertz
        Dur = 3000 # Set Duration To 1000 ms == 1 second
        winsound.Beep(Freq,Dur)
    except Exception as error:
        print "Error: unable to generate alarm :  {err}".format(err=error)

if __name__=="__main__":
    #insert_sensor_info('ABCD1234',5,5,'2004-01-01 12:00:00');
    #send_mail()
    generate_alarm()