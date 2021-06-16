import pymysql
import os
from datetime import datetime
from boto.s3.connection import S3Connection

timesheetID = 1
default_EndDate = '9999-12-31'

class Database:
    def __init__(self):
        host = os.environ.get('server')
        user = os.environ.get('SQLusername')
        password = os.environ.get('SQLpassword')
        db = os.environ.get('SQLname')

        self.con = pymysql.connect(host=host, user=user, password=password, db=db,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def __staggered_insert(self, emp_id, dayStatus, weekID):
        global timesheetID
        timesheetID+=1
        sql = "INSERT INTO timesheet_TGT (TimesheetID, EmployeeID, Day_1, Day_2, Day_3, Day_4, Day_5, Day_6, Day_7, WeekID, START_DATE, END_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        self.cur.execute(sql, (str(emp_id)+str(timesheetID), emp_id, dayStatus[0], dayStatus[1], dayStatus[2], dayStatus[3], dayStatus[4], dayStatus[5], dayStatus[6], weekID, datetime.now(), default_EndDate))
        self.con.commit()

    def check_credentials(self, username):
        sql = "SELECT * from login WHERE EmployeeID = %s"
        self.cur.execute(sql, username)
        rows = self.cur.fetchall()
        return rows

    def return_emp_id(self, email):
        sql = "SELECT * from login WHERE email_id = %s"
        self.cur.execute(sql, email)
        rows = self.cur.fetchall()
        if len(rows)==1:
            return rows[0]["EmployeeID"]

    def check_credentials_from_email(self, email):
        sql = "SELECT * from login WHERE email_id = %s"
        self.cur.execute(sql, email)
        rows = self.cur.fetchall()
        return rows

    def check_exist(self, email):
        sql = "SELECT * from login WHERE email_id = %s"
        self.cur.execute(sql, email.lower())
        rows = self.cur.fetchall()
        return rows

    def insert_user(self, email, password):
        sql = "INSERT INTO login (email_id, user_password) VALUES (%s, %s)"
        self.cur.execute(sql, (email.lower(), password))
        self.con.commit()

    def insert_employee_details(self, emp_id, fname, lname, dob):
        sql = "INSERT INTO employee (EmployeeID, Employee_FName, Employee_LName, dob) VALUES (%s, %s, %s, %s)"
        self.cur.execute(sql, (emp_id, fname.lower(), lname.lower(), dob))
        self.con.commit()

    # def timesheet_staging(self, emp_id, dayStatus, weekID):
    #     sql = "INSERT INTO timesheet_STG (EmployeeID, Day_1, Day_2, Day_3, Day_4, Day_5, Day_6, Day_7, WeekID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    #     self.cur.execute(sql, (emp_id, dayStatus[0], dayStatus[1], dayStatus[2], dayStatus[3], dayStatus[4], dayStatus[5], dayStatus[6], weekID))
    #     self.con.commit()
    #     return True

    def timesheet_target(self, emp_id, dayStatus, weekID):
        sql = "SELECT * from timesheet_TGT WHERE EmployeeID = %s AND weekID = %s"
        self.cur.execute(sql, (emp_id, weekID))
        rows = self.cur.fetchall()
        if(len(rows)==0):
            global timesheetID
            timesheetID=1
            sql = "INSERT INTO timesheet_TGT (TimesheetID, EmployeeID, Day_1, Day_2, Day_3, Day_4, Day_5, Day_6, Day_7, WeekID, START_DATE, END_DATE) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            self.cur.execute(sql, (str(emp_id)+str(timesheetID), emp_id, dayStatus[0], dayStatus[1], dayStatus[2], dayStatus[3], dayStatus[4], dayStatus[5], dayStatus[6], weekID, datetime.now(), default_EndDate))
            self.con.commit()
        else:
            length=len(rows)
            sql = "UPDATE timesheet_TGT SET ACTIVE_FLAG = %s WHERE EmployeeID = %s AND weekID = %s"
            self.cur.execute(sql, ('N', emp_id, weekID))
            self.con.commit()
            sql = "UPDATE timesheet_TGT SET END_DATE = %s WHERE EmployeeID = %s AND weekID = %s"
            self.cur.execute(sql, (datetime.now(), emp_id, weekID))
            self.con.commit()
            self.__staggered_insert(emp_id, dayStatus, weekID)


    def close_cursor(self):
        self.con.close()
