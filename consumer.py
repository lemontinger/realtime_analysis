#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
import json
import struct
import random
import argparse
import traceback
import multiprocessing
from multiprocessing import Process, Queue
import shutil
from ConfigParser import SafeConfigParser
import MySQLdb

from log import init_log
import collector_data_pb2
import msg_pb2
from kafka.client import KafkaClient
from kafka.consumer import SimpleConsumer
from google.protobuf.text_format import MessageToString
from mysql import mysql_handler
from cache import Cache
from pprint import pprint


CONF_ROOT_PATH="./conf/"
CONSUMER_CONF_FILE="consumer.conf"
g_conf = dict()
g_cur_day = "19700101"
process_num = 10
MAX_NODE=20000000
g_update_info = dict()
g_master_logger = init_log("master.log")
logger = None



def load_conf(file_path, conf_data):
    ret = True
    parser = SafeConfigParser()
    parser.read(file_path)

    # kafka
    conf_data["broker_list"] = parser.get('kafka', 'broker_list').strip().split(',')
    conf_data["fetch_size_bytes"] = parser.getint('kafka', 'fetch_size_bytes')
    conf_data["buffer_size"] = parser.getint('kafka', 'buffer_size')
    conf_data["max_buffer_size"] = parser.getint('kafka', 'max_buffer_size')
    conf_data["iter_timeout"] = parser.getint('kafka', 'iter_timeout')
    conf_data["topic_name"] = parser.get('kafka', 'topic_name')
    conf_data["group_name"] = parser.get('kafka', 'group_name')
    conf_data["partition_num"] = parser.getint('kafka', 'partition_num')

    conf_data["msg_topic_name"] = parser.get('kafka', 'msg_topic_name')
    conf_data["msg_group_name"] = parser.get('kafka', 'msg_group_name')
    conf_data["msg_partition_num"] = parser.getint('kafka', 'msg_partition_num')
    if (conf_data["partition_num"] < 0):
        logger.info("partition_num err, [%d]" % (conf_data["partition_num"],))
        return False
    conf_data['auto_commit_every_n'] = parser.getint('kafka', 'auto_commit_every_n')
    conf_data['auto_commit_every_t'] = parser.getint('kafka', 'auto_commit_every_t')

    # common
    conf_data["quit_signal_file"] = parser.get('common', 'quit_signal_file')
    conf_data["bin_log_pre"] = parser.get('common', 'bin_log_pre')
    conf_data["data_folder"] = parser.get('common', 'data_folder')
    if os.path.exists(conf_data["data_folder"]) == False:
        os.makedirs(conf_data["data_folder"])
    conf_data["source_ips"] = set(parser.get('common', 'source_ips').strip().split(','))
    conf_data["thread_num"] = parser.getint('common', 'thread_num')
    conf_data["hadoop_dir"] = parser.get('common', 'hadoop_dir')

    # sec
    conf_data["start_stamp"] = 0
    # db
    conf_data['db_host'] = parser.get('db', 'db_host')
    conf_data['db_port'] = parser.getint('db', 'db_port')
    conf_data['db_user'] = parser.get('db', 'db_user')
    conf_data['db_passwd'] = parser.get('db', 'db_passwd')
    conf_data['db_name'] = parser.get('db', 'db_name')

    return ret

def save_mc_msg(message, idx, db_cli, msg_cache):
    global g_conf
    global logger
    ret = True
    
    try:
        pb_data = msg_pb2.AdBudgetMsgReq()
        pb_data.ParseFromString(message.message.value)

        date = "0000_00_00"
        pkg_min = time.strftime("%Y%m%d", time.localtime(time.time()))
        if pb_data.budgetmsg.HasField("chargetime"):
            sec = pb_data.budgetmsg.chargetime/1000
            date = time.strftime("%Y%m%d", time.localtime(sec))
            pkg_min = date
            #pkg_min = time.strftime("%Y%m%d%H%M", time.localtime(sec))
        else:
            logger.warning("msg not tv_sec field.")
            return False

        if sec < g_conf['begin_stamp']:
            return ret
        if int(g_conf['table_suffix']) != int(date):
            ret = create_table(date, db_cli)
            if ret == True:
                g_conf['table_suffix'] = date    
            else:
                logger.error("create table_suffix:%s failed" % date)
        #点击消息
        if pb_data.budgetmsg.budgettype == msg_pb2.CONSUME:
           #start = time.time()*1000
           #save_consume(date, pb_data, db_cli) 
           msg_cache['click'].push_back(pb_data, pkg_min, db_cli) 
           #cost = int(time.time()*1000-start)
           #logger.info("click cost:%u", cost)
        #反作弊计划
        if pb_data.budgetmsg.budgettype == msg_pb2.ANTI_SPAM and pb_data.budgetmsg.HasField('clickprice'):
           #save_antispam_plan(date, pb_data, db_cli)
           msg_cache['antispam_plan'].push_back(pb_data, pkg_min, db_cli) 
        #反作弊user
        if pb_data.budgetmsg.budgettype == msg_pb2.ANTI_SPAM and pb_data.budgetmsg.HasField('userbalance'):
           #save_antispam_user(date, pb_data, db_cli)
           msg_cache['antispam_user'].push_back(pb_data, pkg_min, db_cli) 
        #消费user
        if pb_data.budgetmsg.budgettype == msg_pb2.COST and pb_data.budgetmsg.HasField('userbalance'):
           #save_user_cost(date, pb_data, db_cli)
           msg_cache['user_cost'].push_back(pb_data, pkg_min, db_cli) 
        #消费plan
        if pb_data.budgetmsg.budgettype == msg_pb2.COST and pb_data.budgetmsg.HasField('planid'):
           #save_plan_cost(date, pb_data, db_cli)
           msg_cache['plan_cost'].push_back(pb_data, pkg_min, db_cli) 
        #充值
        if pb_data.budgetmsg.budgettype == msg_pb2.RECHARGE:
           #save_user_recharge(date, pb_data, db_cli)
           msg_cache['user_recharge'].push_back(pb_data, pkg_min, db_cli) 
        #调整预算
        if pb_data.budgetmsg.budgettype == msg_pb2.MODIFY_BUDGET and pb_data.budgetmsg.HasField('planid'):
           #save_mbudget_plan(date, pb_data, db_cli)
           msg_cache['mbudget_plan'].push_back(pb_data, pkg_min, db_cli) 
        elif pb_data.budgetmsg.budgettype == msg_pb2.MODIFY_BUDGET:
           #save_mbudget_user(date, pb_data, db_cli)
           msg_cache['mbudget_user'].push_back(pb_data, pkg_min, db_cli) 
        return True
        
    except Exception,e: 
        logger.warning("work error, exception is [%s], traceback is [%s]" % (e, traceback.format_exc()))
        return False
    return ret
def save_consume(date, pb_data, db_cli):
    #start = time.time()*1000
    insert_sql = "insert into click_%s(userid, planid, query, src, keyword, clickprice, matchtype, chargetime, \
                  lsid, clicktime, dealtime, gspprice, bucket_id, bidprice) values(%u, %u, '%s', '%s', '%s', %f, '%s', %u,\
                  '%s', %u, %u, %f, %u, %f)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.planid, pb_data.budgetmsg.query,\
                  pb_data.budgetmsg.src, pb_data.budgetmsg.keyword, pb_data.budgetmsg.clickprice, pb_data.budgetmsg.matchtype,\
                  pb_data.budgetmsg.chargetime, str(pb_data.budgetmsg.lsid), pb_data.budgetmsg.clicktime, pb_data.budgetmsg.dealtime,\
                  float(pb_data.budgetmsg.gspprice), pb_data.budgetmsg.bucket_id, pb_data.budgetmsg.bidprice)
    db_cli.mysql_insert(insert_sql)    
    #end = int(time.time()*1000-start)
    #logger.info("sql:%s cost:%u" %(insert_sql, end))
    return True

def save_antispam_plan(date, pb_data, db_cli):
    insert_sql = "insert into antispam_plan_%s(userid, planid, planbudget, plancost, clickprice, lsid, chargetime, dealtime)\
                  values(%u, %u, %f, %f, %f, '%s', %u, %u)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.planid,
                  pb_data.budgetmsg.planbudget, pb_data.budgetmsg.plancost, pb_data.budgetmsg.clickprice,\
                  pb_data.budgetmsg.lsid, pb_data.budgetmsg.chargetime, pb_data.budgetmsg.dealtime)
    return db_cli.mysql_insert(insert_sql)    
def save_antispam_user(date, pb_data, db_cli):
    insert_sql = "insert into antispam_user_%s(userid, userbalance, userbudget, usercost, lsid, chargetime, dealtime)\
                  values(%u, %f, %f, %f, '%s', %u, %u)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.userbalance,
                  pb_data.budgetmsg.userbudget, pb_data.budgetmsg.usercost, \
                  pb_data.budgetmsg.lsid, pb_data.budgetmsg.chargetime, pb_data.budgetmsg.dealtime)
    return db_cli.mysql_insert(insert_sql)    
def save_user_cost(date, pb_data, db_cli):
    insert_sql = "insert into user_cost_%s(userid, userbalance, userbudget, usercost, chargetime)\
                  values(%u, %f, %f, %f, %u)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.userbalance,\
                  pb_data.budgetmsg.userbudget, pb_data.budgetmsg.usercost, pb_data.budgetmsg.chargetime )
    return db_cli.mysql_insert(insert_sql)    
def save_plan_cost(date, pb_data, db_cli):
    insert_sql = "insert into plan_cost_%s(userid, planid, planbudget, plancost, chargetime)\
                  values(%u, %u, %f, %f, %u)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.planid,\
                  pb_data.budgetmsg.planbudget, pb_data.budgetmsg.plancost, pb_data.budgetmsg.chargetime )
    return db_cli.mysql_insert(insert_sql)    
def save_user_recharge(date, pb_data, db_cli):
    insert_sql = "insert into user_recharge_%s(userid, userbalance, chargetime)\
                  values(%u, %f, %u)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.userbalance, pb_data.budgetmsg.chargetime )
    return db_cli.mysql_insert(insert_sql)    
def save_mbudget_plan(date, pb_data, db_cli):
    insert_sql = "insert into mbudget_plan_%s(userid, planid, userbalance, userbudget, usercost, planbudget, chargetime)\
                  values(%u, %u, %f, %f, %f, %f,%u)" % ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.planid, pb_data.budgetmsg.userbalance, 
                 pb_data.budgetmsg.userbudget, pb_data.budgetmsg.usercost, pb_data.budgetmsg.planbudget, pb_data.budgetmsg.chargetime )
    return db_cli.mysql_insert(insert_sql)    
def save_mbudget_user(date, pb_data, db_cli):
    insert_sql = "insert into mbudget_user_%s(userid, userbalance, userbudget, chargetime) values(%u, %f, %f, %u)" % \
                 ( date, pb_data.budgetmsg.userid, pb_data.budgetmsg.userbalance, pb_data.budgetmsg.userbudget, pb_data.budgetmsg.chargetime )
    return db_cli.mysql_insert(insert_sql)    
def is_quit():
    global g_conf
    quit_signal_file = g_conf['data_folder'] + "/" + g_conf['quit_signal_file']
    if os.path.exists(quit_signal_file) == True:
        return True
    return False


def clear_signal():
    global g_conf
    quit_signal_file = g_conf['data_folder'] + "/" + g_conf['quit_signal_file']
    if os.path.exists(quit_signal_file) == True:
        os.remove(quit_signal_file)
    return

def msg_work(message_queue, idx):
    global g_conf
    global logger
    
    logger = init_log("worker."+str(idx)+".log")
    
    ret = True
    db_cli = mysql_handler(g_conf['db_host'], g_conf['db_user'],
                            g_conf['db_passwd'], g_conf['db_port'], g_conf['db_name'])
    ret = db_cli.mysql_conn()
    if ret == False:
        logger.error("connect mysql(%s:%u) failed" % (g_conf['db_host'], g_conf['db_port']))
        return ret
    cur_min = time.strftime("%Y%m%d", time.localtime(time.time()))
    msg_cache = dict()
    msg_cache['click'] = Cache(cur_min, 1000, "click")
    msg_cache['antispam_plan'] = Cache(cur_min, 1000, "antispam_plan")
    msg_cache['antispam_user'] = Cache(cur_min, 1000, "antispam_user")
    msg_cache['user_cost'] = Cache(cur_min, 1000, "user_cost")
    msg_cache['plan_cost'] = Cache(cur_min, 1000, "plan_cost")
    msg_cache['user_recharge'] = Cache(cur_min, 1000, "user_recharge")
    msg_cache['mbudget_plan'] = Cache(cur_min, 1, "mbudget_plan")
    msg_cache['mbudget_user'] = Cache(cur_min, 1, "mbudget_user")
    cnt = 0
    while True:
        try:
            if is_quit():
                logger.info("thread quit: [%d]" % os.getpid())
                return True
            #start=time.time()*1000
            message = message_queue.get() 
            #logger.info("prepare process offset=%d, processid=%d, topic=%s, group=%s" % \
            #           (message.offset, idx, g_conf["topic_name"], g_conf["group_name"]))
            if save_mc_msg(message, idx, db_cli, msg_cache) == False:
                logger.warning("save msg error, msg is [%s]" % str(message))
            if cnt%10000 == 0:
                logger.info("msg_work[%d] cnt:%u"% (idx, cnt))
            cnt += 1
            #end = int(time.time()*1000 - start)
            #logger.info("save_mc_msg process idx:%u cost:%u" % (idx, end))
        except Exception, e:
            logger.error("work error, exception is [%s], traceback is [%s]" % (e, traceback.format_exc()))
            time.sleep(5)
            continue

    return ret


def create_table(date, db_cli):
    global g_conf
    global sql_handler
    global logger

    #click
    sql = "create table if not exists `click_%s`(\
	`id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
	`userid`                                bigint(20) NOT NULL,\
	`planid`                                int(10) unsigned NOT NULL,\
	`query`					varchar(512),\
	`src`					varchar(128),\
	`keyword`				varchar(256),\
	`clickprice`			        float(10,1),\
	`matchtype`				varchar(32),\
	`chargetime`                            bigint(20) ,\
	`lsid`					int(10) unsigned,\
	`clicktime`				int(10) unsigned,\
	`dealtime`				int(10) unsigned,\
	`gspprice`				float(10,1),\
	`bucket_id`				int(10) unsigned,\
	`bidprice`				float(10,1),\
         index clicktime(clicktime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date
    
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table click_%s failed", date)
       return False

    #antispam user
    sql = "create table if not exists `antispam_user_%s`(\
	`id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
	`userid`				bigint(20) NOT NULL,\
	`userbalance`			    	float(10,1) unsigned NOT NULL,\
	`userbudget`				float(10,1),\
	`usercost`				float(10,1),\
	`lsid`					varchar(32) ,\
	`chargetime`				bigint(20) unsigned,\
	`dealtime`				int(10) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table antispam_%s failed", date)
       return False

    #antispam plan
    sql = "create table if not exists `antispam_plan_%s`(\
	`id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
	`userid`				bigint(20) NOT NULL,\
	`planid`			    	int(10) unsigned NOT NULL,\
	`planbudget`				float(10,1),\
	`plancost`				float(10,1),\
	`clickprice`				float(10,1),\
	`lsid`					int(10) unsigned,\
	`chargetime`				bigint(20) unsigned,\
	`dealtime`				int(10) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table antispam_%s failed", date)
       return False

    #set user cost 
    sql = "create table if not exists `user_cost_%s`(\
        `id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
        `userid`				bigint(20) NOT NULL,\
        `userbalance`				float(10,1),\
        `userbudget`				float(10,1),\
        `usercost`				float(10,1),\
        `chargetime`				bigint(15) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table user_info_%s failed", date)
       return False

    #set plan cost
    sql = "create table if not exists `plan_cost_%s`(\
        `id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
        `userid`				bigint(20) NOT NULL,\
        `planid`				int(10) unsigned NOT NULL,\
        `planbudget`				float(10,1),\
        `plancost`				float(10,1),\
        `chargetime`				bigint(15) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table user_info_%s failed", date)
       return False
    #set recharge
    sql = "create table if not exists `user_recharge_%s`(\
        `id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
        `userid`				bigint(20) NOT NULL,\
        `userbalance`				float(10,1),\
        `chargetime`				bigint(15) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table user_info_%s failed", date)
       return False

    #set user budget
    sql = "create table if not exists `mbudget_user_%s`(\
        `id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
        `userid`				bigint(20) NOT NULL,\
        `userbalance`				float(10,1),\
        `userbudget`				float(10,1),\
        `chargetime`				bigint(15) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table user_info_%s failed", date)
       return False
    #set plan budget
    sql = "create table if not exists `mbudget_plan_%s`(\
        `id` 					int(10) unsigned NOT NULL AUTO_INCREMENT,\
        `userid`				bigint(20) NOT NULL,\
        `planid`			        int(10) unsigned NOT NULL,\
        `userbalance`				float(10,1),\
        `userbudget`				float(10,1),\
        `usercost`				float(10,1),\
        `planbudget`				float(10,1),\
        `chargetime`				bigint(15) unsigned,\
         index chargetime(chargetime),\
	PRIMARY KEY(`id`)\
	)ENGINE=InnoDB DEFAULT CHARSET=utf8;" % date 
    ret = db_cli.mysql_create(sql)
    if ret == False:
       logger.error("create table user_info_%s failed", date)
       return False
    return True
def check_pkg(message):
    global g_update_info
    global g_cur_day
    global g_master_logger

    cur_day = time.strftime("%Y%m%d", time.localtime(time.time()))
    if int(g_cur_day) < int(cur_day):
        g_update_info.clear()
        g_cur_day = cur_day

    pb_data = msg_pb2.AdBudgetMsgReq()
    pb_data.ParseFromString(message)
    
    msg_key = 0
    if pb_data.budgetmsg.HasField('planid') and pb_data.budgetmsg.planid != 0:
        msg_key = pb_data.budgetmsg.planid << 32 | pb_data.budgetmsg.budgettype        
    elif pb_data.budgetmsg.HasField('userid') and pb_data.budgetmsg.userid != 0:
        msg_key = pb_data.budgetmsg.userid
    else:
        g_master_logger.warning("budgetmsg has not planid or userid")
        return False
        
    ret = g_update_info.has_key(msg_key)
    if ret == False:
        g_update_info[msg_key] = pb_data.budgetmsg.chargetime
        return True
    if g_update_info[msg_key] >= pb_data.budgetmsg.chargetime:
        g_master_logger.warning("update type:%u the newest chargetime:%u but pkg chargetime:%u"%(pb_data.budgetmsg.budgettype, g_update_info[msg_key], pb_data.budgetmsg.chargetime))
        return False 
    g_update_info[msg_key] = pb_data.budgetmsg.chargetime
    return True


def kafka_pull(message_queue):
    global g_conf
    global g_master_logger
    ret = True
    while True:
        try:
            if is_quit():
                g_master_logger.info("thread quit: [%d]" % os.getpid())
                return True

            random_v = random.randint(0, len(g_conf["broker_list"])-1)
            broker = g_conf["broker_list"][random_v]
            g_master_logger.info("use broker is [%s]" % broker)
            partition_set = set([0])

            # client
            client = KafkaClient(broker)
            consumer = SimpleConsumer( client, g_conf["msg_group_name"],
                    g_conf["msg_topic_name"], partitions=partition_set,
                    auto_commit_every_n=g_conf["auto_commit_every_n"],
                    auto_commit_every_t=g_conf["auto_commit_every_t"],
                    fetch_size_bytes=g_conf["fetch_size_bytes"],
                    buffer_size=g_conf["buffer_size"],
                    max_buffer_size=g_conf["max_buffer_size"]
                    )

            cnt = 0
            for message in consumer:
                cnt += 1
                if cnt % 10000 == 0:
                    g_master_logger.info("msg consumer cnt is [%d] queue:%u" % (cnt, message_queue.qsize()))
                if is_quit():
                    consumer.stop()
                    g_master_logger.info("thread fetch msg quit: [%d]" % os.getpid())
                    break

                value = message.message.value
                if value == None:
                    g_master_logger.warning("value is none, msg is [%s]" % str(message))
                    continue
                if len(value) == 0:
                    g_master_logger.warning("value len is 0, msg is [%s]" % str(message))
                    continue
                if check_pkg(value) == False:
                    continue
                message_queue.put(message)
    
        except Exception, e:
            g_master_logger.error("work error, exception is [%s], traceback is [%s]" % (e, traceback.format_exc()))
            time.sleep(5)
            continue

    return ret

def run():
    ret = True
    global g_conf
    global sql_handler
    global MAX_NODE
    global g_cur_day
    global g_master_logger

    # init
    ret = load_conf(CONF_ROOT_PATH + CONSUMER_CONF_FILE, g_conf)
    if ret != True:
        g_master_logger.error("load conf error.")
        return ret

    clear_signal();

    parser = argparse.ArgumentParser()
    parser = argparse.ArgumentParser(description='Consumer budget server kafka message.')
    parser.add_argument('--begin_stamp', action="store", default=0, type=int)
    results = parser.parse_args()
    g_conf['begin_stamp'] = results.begin_stamp
    g_conf['table_suffix'] = 0
    g_cur_day = time.strftime("%Y%m%d", time.localtime(time.time()))

    g_master_logger.info("begin_stamp is [%u]" % g_conf['begin_stamp'])
    g_master_logger.info("table_suffix:%s" % g_conf['table_suffix'])
    queue = Queue(MAX_NODE)

    jobs = []

    #consumer insert process
    for idx in range(process_num):
        p = multiprocessing.Process(
                target=msg_work,
                args=(queue, idx)
                )
        jobs.append(p)
        g_master_logger.info("partition-[%d] begin work." % idx)
        p.start()

    #producer pull process
    producer = multiprocessing.Process(target=kafka_pull, args=(queue,))
    producer.start()

    for j in jobs:
        j.join()
        if j.exitcode != 0:
            g_master_logger.error('process error, exitcode [%d] [%d].' % (j.pid, j.exitcode))
            ret = False
    producer.join() 
    return ret


def main():
    global g_master_logger
    try:
        if run() == False:
            g_master_logger.error("consumer error!")
            return False
    except Exception, e:
        g_master_logger.error("build_idx error, exception is [%s], traceback is [%s]" % (e, traceback.format_exc()))
        return False

    logger.info("--------end--------")
    return True


if __name__ == "__main__":
    main()

