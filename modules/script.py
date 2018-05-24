# -*- coding: utf-8 -*-

import subprocess
import os
from dataProcess.dap.confs import db_config
from dataProcess.dap import path


class Script:
    """
    调用mysql客户端执行sql脚本文件
    """
    def execute_sql_script(self, filename, config_db=None):
        if config_db is None:
            config_db = (db_config.host, db_config.db, db_config.user, db_config.passwd)
        host, database, db_user, db_password = config_db
        file_path = path.sql_director + filename
        file_path_sql_abspath = os.path.abspath(file_path).encode()
        process = subprocess.Popen('mysql -h %s -u %s -p%s -D%s --default-character-set=utf8' % (host, db_user, db_password, database),
                                   stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        output = process.communicate(b'source ' + file_path_sql_abspath)
        if output and output[1]:
            execute_result = output[1].decode().lower()
            if execute_result.find('error') != -1:
                raise SystemExit(execute_result)
        return output
