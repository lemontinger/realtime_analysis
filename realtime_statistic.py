#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import sys
import MySQLdb
from log import logger
from mysql import mysql_handler
from ConfigParser import SafeConfigParser
from pprint import pprint

g_conf = dict()
back_time = 600
db_cli = None
show_cli = None
g_ratio = 1.1
def load_conf(file_path, conf_data):
    ret = True
    parser = SafeConfigParser()
    parser.read(file_path)

    # db
    conf_data['db_host'] = parser.get('db', 'db_host')
    conf_data['db_port'] = parser.getint('db', 'db_port')
    conf_data['db_user'] = parser.get('db', 'db_user')
    conf_data['db_passwd'] = parser.get('db', 'db_passwd')
    conf_data['db_name'] = parser.get('db', 'db_name')
    conf_data['show_db'] = parser.get('db', 'show_db')

    return ret
def click_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `account_click_%s`(\
           userid                      bigint(20) unsigned NOT NULL comment '账户id',\
           planid                      int(10) unsigned comment '计划id', \
           click_price_sum              float(15, 3) comment '点击消费和',\
           statistic_time               int(10) unsigned comment '统计时间', \
           time_index                  int(10) unsigned default 0 comment '时间index [0,143]',\
	   PRIMARY KEY(`userid`, `planid`, `statistic_time`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select userid, planid, sum(clickprice) from click_%s where clicktime >= %u and"\
          " clicktime < %u group by userid,planid order by userid desc" % (table_suffix, min_sec_start, min_sec_end)
    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)
    insert_sql = "insert into account_click_%s(userid, planid, click_price_sum, statistic_time, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %u, %f, %u, %u)" % (results[i][0], results[i][1], results[i][2], min_sec_start, time_index)
        if i+1 != results_size:
            insert_sql += ","

    try:
    	show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)
def antispam_plan_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    #TODO:table stuct 
    sql = "create table if not exists `antispam_plan_%s`(\
          `userid`                                bigint(20) NOT NULL comment '账户id',\
          `planid`                                int(10) unsigned NOT NULL comment '计划id',\
          `planbudget`                            float(10,1) comment '计划预算',\
          `plancost`                              float(10,1) comment '计划消费',\
          `spam_click_sum`                        float(10,1) comment '反作弊点击和',\
          `spam_click_count`                      int(10) unsigned comment '反作弊点击次数', \
          `chargetime`                            bigint(20) unsigned comment '结算时间',\
          `time_index`                 int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
	   PRIMARY KEY(`userid`, `planid`, `chargetime`)\
          )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.userid, A.planid, A.planbudget, A.plancost, B.spam_click_sum, B.count, A.chargetime "\
          " from  antispam_plan_%s A, (select userid, planid, sum(clickprice) spam_click_sum, count(*) count, "\
          " max(chargetime) chargetime from antispam_plan_%s where chargetime >= %u and chargetime < %u group by userid,planid) "\
          " B where A.userid = B.userid and A.planid = B.planid and A.chargetime = B.chargetime" \
           % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)
    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              

    insert_sql = "insert into antispam_plan_%s(userid, planid, planbudget, plancost, spam_click_sum, spam_click_count, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %u, %f, %f, %f, %u, %u, %u)" % (results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5], results[i][6], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)

def antispam_user_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `antispam_user_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `userbalance`        float(20,3) comment '账户id',\
           `userbudget`	        float(20,3) comment '账户预算',\
           `usercost`           float(20,3) comment '账户消费',\
           `antispam_count`     int(10) unsigned comment '反作弊次数',\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.userid, A.userbalance, A.userbudget, A.usercost, B.count, A.chargetime "\
           " from antispam_user_%s A,(select userid, max(chargetime) chargetime ,count(*) count "\
           " from antispam_user_%s where chargetime >= %u and chargetime < %u group by userid)"\
           " B where A.userid = B.userid and A.chargetime = B.chargetime order by A.userid;" \
           % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)
    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    #insert_sql = ""
    insert_sql = "insert into antispam_user_%s(userid, userbalance, userbudget, usercost, antispam_count, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %.1f, %.1f, %.1f, %u, %u, %u)" % (results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], results[i][5], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)
def user_cost_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `user_cost_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `userbalance`        float(10,1) comment '账户id',\
           `userbudget`	        float(10,1) comment '账户预算',\
           `usercost`           float(10,1) comment '账户消费',\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.* from user_cost_%s A,(select userid, max(chargetime) chargetime from user_cost_%s "\
          "where chargetime >= %u and chargetime < %u group by userid) B where A.userid = B.userid and"\
          " A.chargetime = B.chargetime order by A.userid;" % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)

    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    insert_sql = "insert into user_cost_%s(userid, userbalance, userbudget, usercost, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %.1f, %.1f, %.1f,%u, %u)" % (results[i][1], results[i][2], results[i][3], results[i][4], results[i][5], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)

def plan_cost_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `plan_cost_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `planid`             int(10) comment '计划id',\
           `planbudget`	        float(20,3) comment '计划预算',\
           `plancost`           float(20,3) comment '计划消费',\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `planid`, `chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.* from plan_cost_%s A,(select userid, planid, max(chargetime) chargetime from plan_cost_%s "\
          "where chargetime >= %u and chargetime < %u group by userid, planid) B where A.userid = B.userid and "\
          "A.chargetime = B.chargetime and A.planid = B.planid order by A.userid;" % (table_suffix, table_suffix,\
           min_sec_start*1000, min_sec_end*1000)

    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              

    insert_sql = "insert into plan_cost_%s(userid, planid, planbudget, plancost, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %u, %.1f, %.1f,%u, %u)" % (results[i][1], results[i][2], results[i][3], results[i][4], results[i][5], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)
def recharge_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `user_recharge_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `userbalance`        float(10,1) comment '账户id',\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.* from user_recharge_%s A,(select userid, max(chargetime) chargetime from user_recharge_%s "\
          " where chargetime >= %u and chargetime < %u group by userid) B where A.userid = B.userid "\
          " and A.chargetime = B.chargetime order by A.userid;" % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)

    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              

    insert_sql = "insert into user_recharge_%s(userid, userbalance, chargetime, time_index) values " % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %.1f, %u, %u)" % (results[i][1], results[i][2], results[i][3], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)

def rline_user_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    global g_ratio
    sql = "create table if not exists `rline_user_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `userbalance`        float(10,1) comment '账户id',\
           `userbudget`	        float(10,1) comment '账户预算',\
           `usercost`           float(10,1) comment '账户消费',\
           `rline_count`        int(10) unsigned,\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.*, B.count from user_cost_%s A,(select userid, max(chargetime)"\
          " chargetime ,count(*) count from user_cost_%s where chargetime >= %u and"\
          " chargetime < %u and ((userbudget> 0 and usercost >= userbudget*1.1) or"\
          " userbalance <= 0) group by userid) B where  A.userid = B.userid and "\
          " A.chargetime = B.chargetime ;"\
          % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)

    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    #insert_sql = ""
    insert_sql = "insert into rline_user_%s(userid, userbalance, userbudget, usercost, rline_count, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %.1f, %.1f, %.1f,%u, %u, %u)" % (results[i][1], results[i][2], results[i][3], results[i][4], results[i][6], results[i][5], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)

def rline_plan_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `rline_plan_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `planid`             int(10) unsigned NOT NULL,\
           `planbudget`	        float(10,1) comment '账户预算',\
           `plancost`           float(10,1) comment '账户消费',\
           `rline_count`        int(10) unsigned comment '撞线次数',\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `planid`,`chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.*, B.count from plan_cost_%s A,(select userid, max(chargetime) chargetime"\
          ",count(*) count from plan_cost_%s where chargetime >= %u and chargetime < %u"\
          " and planbudget> 0 and plancost >= planbudget*1.1 group by userid,planid) B where "\
          " A.userid = B.userid and A.chargetime = B.chargetime;"\
          % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)
    pprint(min_sec_start)
    pprint(min_sec_end)
    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    #insert_sql = ""
    insert_sql = "insert into rline_plan_%s(userid, planid, planbudget, plancost, rline_count, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %u, %.1f, %.1f, %.1f,%u, %u)" % (results[i][1], results[i][2], results[i][3], results[i][4], results[i][6], results[i][5], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)
def over_threshold_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `over_threshold_%s`(\
           userid                      bigint(20) unsigned NOT NULL comment '账户id',\
           planid                      int(10) unsigned comment '计划id',\
           othreshold_count             int(10) unsigned default 0 comment'超投次数',\
           statistic_time               int(10) unsigned NOT NULL comment '统计时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
	   PRIMARY KEY(`userid`, `planid`, `statistic_time`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select userid, planid, count(*) count from click_%s where clicktime >= %u "\
          " and clicktime < %u and clickprice < gspprice group by userid,planid" \
          % (table_suffix, min_sec_start, min_sec_end)

    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    insert_sql = "insert into over_threshold_%s(userid, planid, othreshold_count, statistic_time, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %u, %u, %u, %u)" % (results[i][0], results[i][1], results[i][2], min_sec_start, time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)
def mbudget_user_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `mbudget_user_%s`(\
        `userid`                                bigint(20) NOT NULL comment '账户id',\
        `userbalance`                           float(10,1) comment '账户余额',\
        `userbudget`                            float(10,1) comment '账户预算',\
        `mbudget_count`                         int(10)unsigned comment '修改预算次数',\
        `chargetime`                            bigint(15) unsigned comment '结算时间',\
        `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
        index chargetime(chargetime),\
         PRIMARY KEY(`userid`, `chargetime`)\
         )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.userid, A.userbalance, A.userbudget, B.count, A.chargetime from "\
          " mbudget_user_%s A,(select userid, max(chargetime) chargetime, "\
          " count(*) count from mbudget_user_%s where chargetime >= %u and chargetime "\
          " < %u group by userid) B where A.userid = B.userid and A.chargetime = "\
          " B.chargetime order by A.userid;" % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)
    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    insert_sql = "insert into mbudget_user_%s(userid, userbalance, userbudget,mbudget_count, chargetime, time_index) values "% table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %f, %f, %u, %u, %u)" % (results[i][0], results[i][1], results[i][2], results[i][3], results[i][4], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)
def mbudget_plan_dump(min_sec_start, min_sec_end, table_suffix, time_index):
    global db_cli
    global show_cli
    sql = "create table if not exists `mbudget_plan_%s`(\
           `userid`             bigint(20) NOT NULL comment '账户id',\
           `planid`             int(10) comment '计划id',\
           `userbalance`        float(10,1) comment '账户余额',\
           `userbudget`         float(10,1) comment '账户预算',\
           `usercost`           float(10,1) comment '账户消费',\
           `planbudget`	        float(10,1) comment '计划预算',\
           `mbudget_count`      int(10) unsigned comment '修改预算次数',\
           `chargetime`         bigint(15) unsigned comment '结算时间',\
           `time_index`                  int(10) unsigned default 0 comment '时间index [0,143]',\
           index chargetime(chargetime),\
           PRIMARY KEY(`userid`, `planid`, `chargetime`)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" % table_suffix
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    sql = "select A.*, B.count from mbudget_plan_%s A,(select userid, planid, "\
          " max(chargetime) chargetime, count(*) count from mbudget_plan_%s where"\
          " chargetime >= %u and chargetime < %u group by userid, planid) B "\
          " where A.userid = B.userid and A.chargetime = B.chargetime and "\
          "A.planid = B.planid order by A.userid;" % (table_suffix, table_suffix, min_sec_start*1000, min_sec_end*1000)

    pprint(sql)
    results = db_cli.mysql_select(sql)
    results_size = len(results)                              
    #insert_sql = ""
    insert_sql = "insert into mbudget_plan_%s(userid, planid, userbalance, userbudget, usercost,"\
                 " planbudget, mbudget_count, chargetime, time_index) values" % table_suffix
    for i in range(results_size):
        insert_sql += "(%u, %u, %.1f, %.1f, %.1f, %.1f, %u, %u, %u)" % (results[i][1], results[i][2], \
                  results[i][3], results[i][4], results[i][5], results[i][6], results[i][8], results[i][7], time_index)
        if i+1 != results_size:
            insert_sql += ","
    try:
        show_cli.mysql_insert(insert_sql)
    except Exception, e:
        pprint("insert sql(%s) failed"% insert_sql)

def main():
    global g_conf
    global back_time
    global db_cli
    global show_cli
    ret = load_conf("./conf/consumer.conf", g_conf)
    if ret != True:
        pprint("load conf failed")
        return ret
    db_cli = mysql_handler(g_conf['db_host'], g_conf['db_user'], g_conf['db_passwd'], 
                           g_conf['db_port'], g_conf['db_name'])
    ret = db_cli.mysql_conn()
    if ret == False:
        pprint("mysql origin db connnect failed")
        return ret
    show_cli = mysql_handler(g_conf['db_host'], g_conf['db_user'], g_conf['db_passwd'],
                           g_conf['db_port'], g_conf['show_db'])
    ret = show_cli.mysql_conn()
    if ret == False:
        pprint("mysql show db connect failed")
        return ret
    
    cur_time = time.time()
    static_sec = time.localtime(cur_time - back_time)
    day_start = time.strftime("%Y-%m-%d", static_sec)
    day_start_sec = int(time.mktime(time.strptime(day_start, '%Y-%m-%d')))
    time_index = int((cur_time-day_start_sec)/600)
    #sys.exit(0)
    min = time.strftime("%Y-%m-%d %H:%M", static_sec)
    min_sec_start = int(time.mktime(time.strptime(min, '%Y-%m-%d %H:%M')))
    min_sec_end = min_sec_start + 600
    pprint(min_sec_start)
    pprint(min_sec_end)
    table_sec = time.localtime(cur_time - back_time -5)
    table_suffix = time.strftime("%Y%m%d", table_sec)
    #click
    click_dump(min_sec_start, min_sec_end, table_suffix, time_index) 
    #antispam
    antispam_plan_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    antispam_user_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    #cost
    user_cost_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    plan_cost_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    #recharge
    recharge_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    #reach line
    rline_user_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    rline_plan_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    #over threshold
    over_threshold_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    #mbudet
    mbudget_user_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    mbudget_plan_dump(min_sec_start, min_sec_end, table_suffix, time_index)
    cost_time = time.time() - cur_time
    pprint("cur time:%s dump cost time:%u"% (min, cost_time))
    
if __name__ == "__main__":
    main()
