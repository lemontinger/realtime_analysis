#!/usr/sbin/env python

#cur_min come from chargetime and cur_min = chargetime/1000/60
#table_name come from cur_sec=cur_min*60 and get table_suffix from cur_min
import time
from mysql import mysql_handler
class Cache:
    cur_min=time.strftime("%Y%m%d", time.localtime(time.time()))
    ithreshold=1000
    pb_list = list()
    cache_type = ""
    def __init__(self, cur_min, ithreshold, type):
        self.cur_min = cur_min
        self.ithreshold = ithreshold
        self.cache_type = type

    def push_back(self, pb_data, pkg_min, mhandler):
        if pkg_min != self.cur_min:
            self.flush2db(mhandler)
            self.cur_min = pkg_min

        self.pb_list.append(pb_data)

        if len(self.pb_list) >= self.ithreshold:
            self.flush2db(mhandler) 

    def flush2db(self, mhandler):
        if len(self.pb_list)  == 0:
            return

        if self.cache_type == "click":
            self.save_consume(mhandler)
        elif self.cache_type == "antispam_plan":
            self.save_antispam_plan(mhandler)
        elif self.cache_type == "antispam_user":
            self.save_antispam_user(mhandler)
        elif self.cache_type == "user_cost":
            self.save_user_cost(mhandler)
        elif self.cache_type == "plan_cost":
            self.save_plan_cost(mhandler)
        elif self.cache_type == "user_recharge":
            self.save_user_recharge(mhandler)
        elif self.cache_type == "mbudget_plan":
            self.save_mbudget_plan(mhandler)
        elif self.cache_type == "mbudget_user":
            self.save_mbudget_user(mhandler)
        self.pb_list = []
    def save_consume(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into click_%s(userid, planid, query, src, keyword, clickprice, matchtype, chargetime, \
                  lsid, clicktime, dealtime, gspprice, bucket_id, bidprice) values" % table_suffix
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %u, '%s', '%s', '%s', %f, '%s', %u,'%s', %u, %u, %f, %u, %f)" % (self.pb_list[i].budgetmsg.userid, \
                  self.pb_list[i].budgetmsg.planid, self.pb_list[i].budgetmsg.query.replace("'",""), self.pb_list[i].budgetmsg.src.replace("'", ""), \
                  self.pb_list[i].budgetmsg.keyword.replace("'", ""), self.pb_list[i].budgetmsg.clickprice, self.pb_list[i].budgetmsg.matchtype,\
                  self.pb_list[i].budgetmsg.chargetime, str(self.pb_list[i].budgetmsg.lsid), self.pb_list[i].budgetmsg.clicktime, \
                  self.pb_list[i].budgetmsg.dealtime,float(self.pb_list[i].budgetmsg.gspprice), self.pb_list[i].budgetmsg.bucket_id, \
                  self.pb_list[i].budgetmsg.bidprice)
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)

    def save_antispam_plan(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min))
        insert_sql = "insert into antispam_plan_%s(userid, planid, planbudget, plancost, clickprice, lsid, chargetime, dealtime)\
                  values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %u, %f, %f, %f, '%s', %u, %u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.planid,\
                  self.pb_list[i].budgetmsg.planbudget,self.pb_list[i].budgetmsg.plancost, self.pb_list[i].budgetmsg.clickprice,\
                  self.pb_list[i].budgetmsg.lsid, self.pb_list[i].budgetmsg.chargetime, self.pb_list[i].budgetmsg.dealtime)
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)


    def save_antispam_user(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into antispam_user_%s(userid, userbalance, userbudget, usercost, lsid, chargetime, dealtime) values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %f, %f, %f, '%s', %u, %u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.userbalance,\
                  self.pb_list[i].budgetmsg.userbudget, self.pb_list[i].budgetmsg.usercost, self.pb_list[i].budgetmsg.lsid, \
                  self.pb_list[i].budgetmsg.chargetime, self.pb_list[i].budgetmsg.dealtime)
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)

    def save_user_cost(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into user_cost_%s(userid, userbalance, userbudget, usercost, chargetime) values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %f, %f, %f, %u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.userbalance,\
                  self.pb_list[i].budgetmsg.userbudget,self.pb_list[i].budgetmsg.usercost, self.pb_list[i].budgetmsg.chargetime )
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)

    def save_plan_cost(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into plan_cost_%s(userid, planid, planbudget, plancost, chargetime) values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %u, %f, %f, %u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.planid,\
                  self.pb_list[i].budgetmsg.planbudget,self.pb_list[i].budgetmsg.plancost, self.pb_list[i].budgetmsg.chargetime)
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)
       
    def save_user_recharge(self, mhandler):
        table_suffix = self.cur_min#time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into user_recharge_%s(userid, userbalance, chargetime) values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %f, %u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.userbalance,\
                  self.pb_list[i].budgetmsg.chargetime )
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)

    def save_mbudget_plan(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into mbudget_plan_%s(userid, planid, userbalance, userbudget, usercost, planbudget, chargetime) values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %u, %f, %f, %f, %f,%u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.planid,\
                  self.pb_list[i].budgetmsg.userbalance ,self.pb_list[i].budgetmsg.userbudget, self.pb_list[i].budgetmsg.usercost,\
                  self.pb_list[i].budgetmsg.planbudget, self.pb_list[i].budgetmsg.chargetime)
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)

    def save_mbudget_user(self, mhandler):
        table_suffix = self.cur_min #time.strftime("%Y%m%d", time.localtime(self.cur_min*60))
        insert_sql = "insert into mbudget_user_%s(userid, userbalance, userbudget, chargetime) values" % table_suffix
                  
        list_size = len(self.pb_list) 
        values = ""
        for i in range(list_size):
            values += "(%u, %f, %f, %u)" % (self.pb_list[i].budgetmsg.userid, self.pb_list[i].budgetmsg.userbalance,\
                  self.pb_list[i].budgetmsg.userbudget, self.pb_list[i].budgetmsg.chargetime )
            if i+1 != list_size:
               values += ", "
        insert_sql += values
        return mhandler.mysql_insert(insert_sql)
        
