#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import time
import MySQLdb
from log import logger
from mysql import mysql_handler
from ConfigParser import SafeConfigParser
from pprint import pprint

g_conf = dict()
back_time = 3600*24
db_cli = None
show_cli = None
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
def active_plan(table_suffix):
    global db_cli
    global show_cli
    sql = "create table if not exists active_plan(\
               statics_date	                    int(10) unsigned NOT NULL,\
               plan_active_count                    bigint(20) unsigned NOT NULL,\
               PRIMARY KEY(statics_date)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    results = db_cli.mysql_select("select count(distinct(planid)) from click_%u" % table_suffix)
    #insert_sql = ""
    for result in results:
        try:
            insert_sql = "insert into active_plan(statics_date, plan_active_count) values\
                          (%u, %u)" % (table_suffix, result[0])
            show_cli.mysql_insert(insert_sql)
        except Exception, e:
            pprint("insert sql(%s) failed"% insert_sql)
def active_user(table_suffix):
    global db_cli
    global show_cli
    sql = "create table if not exists `active_user`(\
               statics_date			    int(10) unsigned NOT NULL,\
               userid_active_count		    bigint(20) unsigned NOT NULL,\
               PRIMARY KEY(statics_date)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    results = db_cli.mysql_select("select count(distinct(userid)) from click_%u" % table_suffix)
    #insert_sql = ""
    for result in results:
        try:
            insert_sql = "insert into active_user(statics_date, userid_active_count) values\
                          (%u, %u)" % (table_suffix, result[0])
            show_cli.mysql_insert(insert_sql)
        except Exception, e:
            pprint("insert sql(%s) failed"% insert_sql)
def click_src_top(table_suffix):
    global db_cli
    global show_cli
    sql = "create table if not exists `click_src_top`(\
               `id` 				int(10) unsigned NOT NULL AUTO_INCREMENT,\
               click_src			varchar(128) NOT NULL,\
               click_count		        bigint(20) NOT NULL,\
               click_day			int(10) unsigned NOT NULL,\
               PRIMARY KEY(id)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;" 
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    results = db_cli.mysql_select("select distinct(src), count(*) count from click_%u group by src order by count desc limit 50" % table_suffix)
    #insert_sql = ""
    for result in results:
        try:
            insert_sql = "insert into click_src_top(click_src, click_count, click_day) values\
                          ('%s', %u, %u)" % (result[0], result[1], table_suffix)
            show_cli.mysql_insert(insert_sql)
        except Exception, e:
            pprint("insert sql(%s) failed"% insert_sql)
def click_bid_top(table_suffix):
    global db_cli
    global show_cli
    sql = "create table if not exists `click_bid_top`(\
               `id` 				int(10) unsigned NOT NULL AUTO_INCREMENT,\
               click_bidword		        varchar(128) NOT NULL,\
               click_count		        bigint(20) NOT NULL,\
               click_day		        int(10) unsigned NOT NULL,\
               PRIMARY KEY(id)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    results = db_cli.mysql_select("select distinct(keyword), count(*) count from click_%u group by keyword order by count desc limit 50" % table_suffix)
    #insert_sql = ""
    for result in results:
        try:
            insert_sql = "insert into click_bid_top(click_bidword, click_count, click_day) values\
                          ('%s', %u, %u)" % (result[0], result[1], table_suffix)
            show_cli.mysql_insert(insert_sql)
        except Exception, e:
            pprint("insert sql(%s) failed"% insert_sql)
def click_query_top(table_suffix):
    global db_cli
    global show_cli
    sql = "create table if not exists `click_query_top`(\
               `id` 				int(10) unsigned NOT NULL AUTO_INCREMENT,\
               click_query	                varchar(128) NOT NULL,\
               click_count		        bigint(20) NOT NULL,\
               click_day		        int(10) unsigned NOT NULL,\
               PRIMARY KEY(id)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    results = db_cli.mysql_select("select distinct(query), count(*) count from click_%u group by query order by count desc limit 50" % table_suffix)
    #insert_sql = ""
    for result in results:
        try:
            insert_sql = "insert into click_query_top(click_query, click_count, click_day) values\
                          ('%s', %u, %u)" % (result[0], result[1], table_suffix)
            show_cli.mysql_insert(insert_sql)
        except Exception, e:
            pprint("insert sql(%s) failed"% insert_sql)
def click_channel_top(table_suffix):
    global db_cli
    global show_cli
    sql = "create table if not exists `click_channel_top`(\
               `id` 				int(10) unsigned NOT NULL AUTO_INCREMENT,\
               `click_channel`	                int(10) NOT NULL,\
               `click_count`		        bigint(20) NOT NULL,\
               click_day		        int(10) unsigned NOT NULL,\
               PRIMARY KEY(id)\
           )ENGINE=InnoDB DEFAULT CHARSET=utf8;"
    ret = show_cli.mysql_create(sql)
    if ret == False:
        pprint("create table(%s) failed"% sql)
        return ret

    results = db_cli.mysql_select("select distinct(lsid), count(*) count from click_%u group by lsid order by count desc limit 20" % table_suffix)
    #insert_sql = ""
    if results == None:
        pprint("result src is none")
        return False
    pprint(results)
    for result in results:
        try:
            insert_sql = "insert into click_channel_top(click_channel, click_count, click_day) values\
                          (%u, %u, %u)" % ( result[0], result[1], table_suffix)
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
    
    static_sec = time.localtime(time.time() - back_time)
    #min = time.strftime("%Y-%m-%d ", static_sec)
    #min_sec_start = int(time.mktime(time.strptime(min, '%Y-%m-%d')))
    #min_sec_end = min_sec_start + 3600*24 
    table_suffix = int(time.strftime("%Y%m%d", static_sec))

    active_plan(table_suffix) 
    active_user(table_suffix)
    click_src_top(table_suffix)
    click_bid_top(table_suffix)
    click_query_top(table_suffix)
    click_channel_top(table_suffix)
    
if __name__ == "__main__":
    main()
