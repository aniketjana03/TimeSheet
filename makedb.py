import pymysql
import os
from helpers import parse_sql
from boto.s3.connection import S3Connection

class MakeDB:
    def __init__(self):
        host = '127.0.0.1'
        user = 'root'
        password ='root'

        stmts = parse_sql('final.sql')
        self.con = pymysql.connect(host=host, user=user, password=password,
                                   cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()
        for stmt in stmts:
            self.cur.execute(stmt)
        self.con.commit()
