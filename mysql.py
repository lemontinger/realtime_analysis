#!/usr/sbin/env python

import MySQLdb
from ConfigParser import SafeConfigParser
from pprint import pprint



class mysql_handler:
    db_host = "127.0.0.1"
    db_port = 3306
    db_user = "root"
    db_passwd = ""
    db_name = ""
    m_conn = None
    m_cur = None
    def __init__(self, host, user, passwd, port, name):
        print("init")
        self.db_host = host
        self.db_user = user
        self.db_passwd = passwd
        self.db_port = port
        self.db_name = name
	                
    def mysql_conn(self):
        try:
            self.m_conn = MySQLdb.connect(host=self.db_host, user=self.db_user, passwd=self.db_passwd, port=self.db_port, charset="utf8")
            self.m_conn.select_db(self.db_name)
            self.m_cur = self.m_conn.cursor() 
        except MySQLdb.Error, e:
            print("Mysql Error %d:%s" % (e.args[0], e.args[1]))
            return False
        return True

    def mysql_select(self, sql):
        try:
            result = self.m_cur.execute(sql)
            results = self.m_cur.fetchall()
        except MySQLdb.Error, e:
            print("Mysql Error %d:%s" % (e.args[0], e.args[1]))
            return None
        return results
    def mysql_insert(self, sql):
        try:
            result = self.m_cur.execute(sql)
            self.m_conn.commit()
        except MySQLdb.Error, e:
            print("Mysql Error %d:%s sql:%s" % (e.args[0], e.args[1], sql))
            return False
        return True 
    def mysql_create(self, sql):
        try:
            result = self.m_cur.execute(sql)
            self.m_conn.commit()
        except MySQLdb.Error, e:
            print("Mysql Error %d:%s" % (e.args[0], e.args[1]))
            return False
        return True 
    def mysql_close(self):
        self.m_conn.close()

if __name__ == "__main__":
    sql_handler = mysql_handler("127.0.0.1", "root", "", 3306, "reach_rate")
   
    ret = sql_handler.mysql_conn()
    if ret == False:
        pprint(sql_handler)
    ret = sql_handler.mysql_select("select * from reach_line_info limit 10")
    pprint(ret) 
