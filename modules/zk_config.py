# -*- coding: utf-8 -*-
from kazoo.client import KazooClient
from kazoo.client import KazooState
from kazoo.protocol.states import WatchedEvent
from kazoo.handlers.threading import KazooTimeoutError
from dataProcess.dap.confs.zk import zk_hosts
from dataProcess.dap.modules.log_initiate import initiate_log
from dataProcess.dap.modules.dp_exception import DpException
from dataProcess.dap.modules.constants import ErrorConstants, Constants
import json
import dataProcess.dap.confs.db_config as db_config


logger = initiate_log(__name__)


def connection_listener(state):
    if state == KazooState.SUSPENDED:
        # handle being disconnected from zookeeper
        err_msg = "disconnect from zookeeper"
        logger.error(err_msg)
        raise DpException(ErrorConstants.ec_sys_error,
                          ErrorConstants.error_code_message
                          .get(ErrorConstants.ec_sys_error) + err_msg)


class ZkConfig:

    def __init__(self):
        self.zk = KazooClient(hosts=zk_hosts)
        try:
            self.zk.start()
        except KazooTimeoutError as e:
            exit(e.args)
        finally:
            self.zk.add_listener(connection_listener)

    def _get_config(func):

        def wrapper(self, node_path_env: str, node_path_conf: str, conf_dict: dict = {}):
            stat = self.zk.exists(node_path_conf)
            if stat is None:
                err_msg = "%s is not exists".format(node_path_conf)
                logger.error(err_msg)
                raise DpException(ErrorConstants.ec_sys_error,
                                  ErrorConstants.error_code_message
                                  .get(ErrorConstants.ec_sys_error) + err_msg)

            @self.zk.ChildrenWatch(node_path_env)
            def watch_children(children):
                logger.warning("Children of %s are now: %s\n", node_path_env, children)

            @self.zk.DataWatch(node_path_conf)
            def watch_node(data, stat, event: WatchedEvent):
                logger.warning("Version: %s, data: %s, event is %s\n",
                               stat.version, data.decode("utf-8"), event)

            data = self.zk.get(node_path_conf)
            conf_data = data[0].decode("utf-8")
            try:
                conf_dict = json.loads(conf_data)
            except:
                err_msg = "can't convert conf data to dict, conf_data is %s".format(conf_data)
                logger.error(err_msg)
                raise DpException(ErrorConstants.ec_sys_error,
                                  ErrorConstants.error_code_message
                                  .get(ErrorConstants.ec_sys_error) + err_msg)

            func(self, node_path_conf, node_path_env, conf_dict)

        return wrapper

    @_get_config
    def get_db_config(self, node_path_env: str, node_path_conf: str, conf_dict: dict =  {}):
        test_dict = {}
        test_dict["host"] = "a"
        test_dict.get("host")
        try:
            db_config.host = conf_dict.get("host")
            db_config.user = conf_dict.get("user")
            db_config.passwd = conf_dict.get("passwd")
            db_config.db = conf_dict.get("db")
            db_config.port = conf_dict.get("port")
        except:
            err_msg = "param of mysql config is deficiency: %s".format(conf_dict)
            logger.error(err_msg)
            raise DpException(ErrorConstants.ec_sys_error,
                              ErrorConstants.error_code_message
                              .get(ErrorConstants.ec_sys_error) + err_msg)
        else:
            logger.debug(db_config)


if __name__ == '__main__':
    zk = ZkConfig()
    zk.get_db_config('/dcm/beta', '/dcm/beta/mysql', None)
