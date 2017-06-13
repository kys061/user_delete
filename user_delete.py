#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
# Copyright (C) 2016 Saisei Networks Inc. All rights reserved.

import logging
import requests
import time

################################################################
# config
################################################################
REST_SERVER = 'localhost'
REST_PORT = '5000'
REST_PROTO = 'http'
REST_SYS_NAME = 'stm' #change you hostname
REST_BASIC_PATH = r'/rest/'+REST_SYS_NAME+'/configurations/running/'
REST_USER_PATH = r'users/?level=full&format=human'
# if your group is bigger than 100,
#please change limit=100 to your number of your group
REST_USERGRP_PATH = r'user_groups/?token=1&order=%3Ename&start=0&limit=100&select=name%2Cnested_groups&format=human'
USER = 'admin'
PASS = 'admin'
################################################################



# recorder logger setting
SCRIPT_MON_LOG_FILE = r'/var/log/user_delete.log'

logger = logging.getLogger('saisei.user_delete')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(SCRIPT_MON_LOG_FILE)
handler.setLevel(logging.INFO)
filter = logging.Filter('saisei.user_delete')
formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
handler.addFilter(filter)

logger.addHandler(handler)
logger.addFilter(filter)

def query(url, user, password):
    try:
        resp = requests.get(url, auth=(user, password))
    except Exception as err:
        resp = None
        logger.error("### Got exception from requsts.get : {} ###".format(err))

    if resp:
        data = resp.json()
        return data['collection']
    else:
        logger.error("### requests.get returned None ###")
        logger.error("### requests.get retry interval 1 second (1st) ###")
        logger.error("### url: '{}' ###".format(url))
        time.sleep(1)
        resp = requests.get(url, auth=(user, password))

        if resp:
            data = resp.json()
            return data['collection']
        else:
            logger.error("### requests.get returned None ###")
            logger.error("### requests.get retry interval 1 second (1st) ###")
            logger.error("### url: '{}' ###".format(url))
            time.sleep(1)
            resp = requests.get(url, auth=(user, password))

            if resp:
                data = resp.json()
                return data['collection']
            else:
                logger.error("### requests.get returned None script exit ###")
                logger.error("### url: '{}' ###".format(url))
                return None


def rest_delete(url, user, password):
    try:
        resp = requests.delete(url, auth=(user, password))
    except Exception as err:
        resp = None
        logger.error("### Got exception from requsts.delete : {} ###".format(err))

    if resp:
        status_code= resp.status_code
        return status_code
    else:
        logger.error("### requests.delete returned None ###")
        logger.error("### requests.delete retry interval 1 second (1st) ###")
        logger.error("### url: '{}' ###".format(url))
        time.sleep(1)
        resp = requests.delete(url, auth=(user, password))

        if resp:
            status_code= resp.status_code
            return status_code
        else:
            logger.error("### requests.delete returned None ###")
            logger.error("### requests.delete retry interval 1 second (1st) ###")
            logger.error("### url: '{}' ###".format(url))
            time.sleep(1)
            resp = requests.delete(url, auth=(user, password))

            if resp:
                status_code= resp.status_code
                return status_code
            else:
                logger.error("### requests.delete returned None script exit ###")
                logger.error("### url: '{}' ###".format(url))
                return None


def get_user_url():
    return REST_PROTO+r'://'+REST_SERVER+r':'+REST_PORT+REST_BASIC_PATH+REST_USER_PATH

def get_user_delete_url(_user):
    return REST_PROTO+r'://'+REST_SERVER+r':'+REST_PORT+REST_BASIC_PATH+r'users/'+_user

def get_group_url():
    return REST_PROTO+r'://'+REST_SERVER+r':'+REST_PORT+REST_BASIC_PATH+REST_USERGRP_PATH

def get_group_delete_url(_group):
    return REST_PROTO+r'://'+REST_SERVER+r':'+REST_PORT+REST_BASIC_PATH+r'user_groups/'+_group

def main():
    # get user
    try:
        user_url = get_user_url()
    except Exception as err:
        logger.error("### Got exception from requsts.delete : {} ###".format(err))

    users = query(user_url, USER, PASS)

    # delete users
    if users:
        for user in users:
            print('{} : {}'.format(user['name'], user['groups']))
            status = rest_delete(get_user_delete_url(user['name']), USER, PASS)
            if status == 200:
                print('{} is deleted successfully'.format(user['name']))
            else:
                print('status : {}, {} is not deleted...check if user is already deleted or not..'.format(status, user['name']))

    # get and delete groups
    _users = query(user_url, USER, PASS)
    if len(_users) == 0:
        _groups = query(get_group_url(), USER, PASS)
        for _group in _groups:
            print(_group['name'])
            status = rest_delete(get_group_delete_url(_group['name']), USER, PASS)
            if status == 200:
                print('{} is deleted successfully'.format(_group['name']))
            else:
                print('status : {}, {} is not deleted...check if user is exist or not..'.format(sataus, _group['name']))

if __name__ == '__main__' :
    main()
