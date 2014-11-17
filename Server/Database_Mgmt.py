__author__ = 'naval'

import MySQLdb
import time

class DBMS():

    def __init__(self):
        self.db = MySQLdb.connect("localhost", "root", "", "iot_project");

    def execute_sql(self,sql):
        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor

    def check_New_Tiger(self,tiger_id):
        sql = "select count(*) from tiger_info where tiger_rfid = '" + tiger_id + "'"
        try:
            cursor = self.execute_sql(sql)
            if cursor.rowcount == 1:
                return cursor.fetchone()[0]
        except Exception as error:
            # Rollback in case there is any error
            print "Cannot access tiger info :  {err}".format(err=error)
        return -1

    def add_tiger_info(self,tiger_id):
        # Open database connection
        sql = "INSERT INTO tiger_info VALUES ('" + tiger_id + "', curdate())"
        try:
            # Execute the SQL command
            cursor = self.execute_sql(sql)
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def insert_sensor_info(self,id,lat,long,time_info):
        sql = "INSERT INTO sensor_info(rfid,latitude,longitude,record_time) VALUES ('" \
              + id + "'," + str(lat) + "," + str(long) + ",'" + time_info + "')"
        try:
            self.execute_sql(sql)
            self.db.commit()
        except:
            # Rollback in case there is any error
            self.db.rollback()

    def add_sensor_data(self,data):
        if data:
            id = data['rfid']
            latitude = data['location']['latitude']
            longitude = data['location']['longitude']
            record_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(data['record_time']))
            print "Incoming data- Rfid:",id," Timestamp:",str(record_time)
            last_lat,last_long = self.get_last_location_of_tiger(id)
            if last_lat != latitude and last_long != longitude:
                self.insert_sensor_info(id,latitude,longitude,record_time)

    def get_last_location_of_tiger(self,tiger):
        sql = "select latitude,longitude from sensor_info where rfid = '" + tiger + \
              "'and record_time = (select max(record_time) from sensor_info where rfid = '" + tiger + "')"
        try:
            cursor = self.execute_sql(sql)
            if cursor.rowcount == 0:
                #new record
                return (-1,-1)
            else:
                data = cursor.fetchone()
                return (data[0],data[1])
        except Exception as error:
            # Rollback in case there is any error
            print "Cannot access tiger info :  {err}".format(err=error)
        return (-1,-1)

    def getBoundary(self):
        # Open database connection
        sql = "select * from boundary"
        x = 0
        y = 0
        try:
            # Execute the SQL command
            cursor = self.execute_sql(sql)
            for data in cursor.fetchall():
                x = data[0]
                y = data[1]
        except Exception as error:
            # Rollback in case there is any error
            print "Cannot get Boundary details :  {err}".format(err=error)
        return (x,y)

    def get_tigers(self):
        sql = "select tiger_rfid from tiger_info"
        tiger_list = []
        try:
            # Execute the SQL command
            cursor = self.execute_sql(sql)
            for data in cursor.fetchall():
                tiger_list.append(data[0])
        except Exception as error:
            print "Cannot access tiger_info :  {err}".format(err=error)
        return tiger_list

    def check_boundary(self, tiger,max_lat,max_long):
        sql = "select latitude,longitude from sensor_info where rfid = '" + tiger + \
              "'and record_time = (select max(record_time) from sensor_info where rfid = '" + tiger + "')"
        try:
            # Execute the SQL command
            cursor = self.execute_sql(sql)
            if cursor.rowcount == 0:
                #no data exists.
                return 2
            else:
                data = cursor.fetchone()
                if((data[0] > max_lat) or (data[1] > max_long)):
                    return 1
        except Exception as error:
            print "Cannot get tiger details from the sensor info table:  {err}".format(err=error)
        return 0

    def get_last_record_time(self,tiger):
        sql = "select max(record_time) from sensor_info where rfid = '" + tiger + "'"
        try:
            cursor = self.execute_sql(sql)
            if cursor.rowcount == 0:
                #new record
                return -1
            else:
                data = cursor.fetchone()
                return data[0]
        except Exception as error:
            print "Cannot access tiger info :  {err}".format(err=error)
        return -1