# -*- coding: utf-8 -*-

from kazoo.client import KazooClient
from dataProcess.dap.modules.log_initiate import initiate_log
from kazoo.client import KazooState
from kazoo.protocol.states import WatchedEvent
from kazoo.handlers.threading import KazooTimeoutError
import unittest
import json

logger = initiate_log()

hosts = "192.168.150.250:2181"
node = "dcm/beta"
nodeMysql = node + "/mysql"


def connection_listener(state):
    if state == KazooState.SUSPENDED:
        # handle being disconnected from zookeeper
        logger.error("disconnect from zookeeper")

def watcher_default(event: WatchedEvent):
    """
    default watcher: A watch function passed to get() or exists()
    will be called when the data on the node changes
    or the node itself is deleted.
    and it is one-time watch events
    :param event:
    :return:
    """
    logger.debug("path is : %s\n type is : %s\n stat is %s\n",
          event.path, event.type, event.state)
    pass


class ZookeeperTutorial(unittest.TestCase):

    def setUp(self):
        self.zk = KazooClient(hosts=hosts)
        try:
            self.zk.start()
        except KazooTimeoutError as e:
            exit(e.args)
        finally:
            self.zk.add_listener(connection_listener)

    def test_node_exists(self):
        stat = self.zk.exists(nodeMysql, watch=watcher_default)
        if stat is None:
            logger.error("%s node not exists.", nodeMysql)
        else:
            logger.info("node exists.")

        while True:
            pass

    def test_watch_children(self):

        @self.zk.ChildrenWatch(nodeMysql)
        def watch_children(children):
            logger.warning("Children are now: %s\n", children)

        @self.zk.DataWatch(nodeMysql)
        def watch_node(data, stat, event: WatchedEvent):
            logger.warning("Version: %s, data: %s, event is %s\n",
                           stat.version, data.decode("utf-8"), event)

        data = self.zk.get(nodeMysql)
        conf_data = str(data[0].decode("utf-8"))
        try:
            conf_dict = json.loads(conf_data)
        except:
            err_msg = "can't convert conf data to dict, conf_data is %s".format(conf_data)
            logger.error(err_msg)
        else:
            print(conf_dict)




        while True:
            pass


if __name__ == "__main__":
    pass








