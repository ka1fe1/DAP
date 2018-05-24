# -*- coding: utf-8 -*-
from dataProcess.dap.confs.env import env

host = ""
user = ""
passwd = ""
db = ""
port = 3306

if env == 'local':
    # host = "127.0.0.1"
    # db_user = 'root'
    # db_password = 'admino0o0oo0'
    # database = 'original_data'
    host = "127.0.0.1"
    user = 'root'
    passwd = 'mysql'
    db = 'original_data'
elif env == 'dev':
    host = ''
    user = ''
    passwd = ''
    db = ''
elif env == 'beta':
    host = ''
    user = ''
    passwd = ''
    db = ''
elif env == 'pro':
    host = ''
    user = ''
    passwd = ''
    db = ''