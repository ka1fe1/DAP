# -*- coding: utf-8 -*-
import os
import logging.config
import pureyaml
from dataProcess.dap import path


def initiate_log(conf_path='', default_level=logging.DEBUG, logger_name=""):
    conf_path = conf_path if conf_path else os.path.abspath(path.conf_director + 'log.yaml')
    if os.path.exists(conf_path):
        with open(conf_path, 'rt') as f:
            config = pureyaml.load(f.read())
        config['handlers']['info_file_handler']['filename'] = path.log_director + config['handlers']['info_file_handler']['filename']
        config['handlers']['error_file_handler']['filename'] = path.log_director + config['handlers']['error_file_handler']['filename']
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)
    return logging.getLogger(logger_name)

if __name__ == '__main__':
    logger = initiate_log(logger_name=__name__)
    logger.debug('this is message')