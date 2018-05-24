# -*- coding: utf-8 -*-
from mysql.connector import connect
from mysql.connector import errorcode
from mysql.connector import Error
from dataProcess.dap.confs import db_config
from dataProcess.dap.modules.log_initiate import initiate_log
from dataProcess.dap.modules.dp_exception import DpException
from dataProcess.dap.modules.constants import ErrorConstants

class MySQLConnector:

    cnx = None
    cursor = None

    def __init__(self):
        """
        初始化 MySQL 连接参数
        """
        logger = initiate_log(__name__)
        try:
            self.config = {
                'host': db_config.host,
                'database': db_config.db,
                'user': db_config.user,
                'password': db_config.passwd,
                'raise_on_warnings': False,
                'charset': 'utf8',
            }
            self.cnx = connect(**self.config)
        except Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                err_msg = "Something is wrong with your user name or password"
                logger.error(err_msg)
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                err_msg = "Database does not exist"
                logger.error(err_msg)
            else:
                err_msg = err.msg
                logger.error(err_msg)
            raise DpException(ErrorConstants.ec_sys_error,
                              ErrorConstants.error_code_message
                              .get(ErrorConstants.ec_sys_error) + err_msg)
        finally:
            self.cursor = self.cnx.cursor(dictionary=True)
            logger.info("database connect success.")

    def query_data(self, sql):
        """
        MySQL 查询语句
        :return:
        """
        self.cursor.execute(sql)
        data = self.cursor.fetchall()

        self.cursor.close()
        self.cnx.close()
        return data

    def manipulate_data(self, sql):
        """
        执行 MySQL insert、update、delete 语句
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        self.cnx.commit()

        self.cursor.close()
        self.cnx.close()

    def call_stored_procedure(self, name, *args):
        """
        调用存储过程
        :param name:
        :return:
        """
        self.cursor.callproc(name, args)
        stored_results = self.cursor.stored_results()
        self.cnx.commit()

        self.cursor.close()
        self.cnx.close()
        return stored_results




