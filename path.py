# -*- coding: utf-8 -*-
import os

root_director = os.path.dirname(__file__)
sql_director = root_director + '/sql/'
conf_director = root_director + '/confs/'
log_director = root_director + "/logs/"

if __name__ == '__main__':
    print(root_director)
    print(sql_director)
    print(conf_director)
