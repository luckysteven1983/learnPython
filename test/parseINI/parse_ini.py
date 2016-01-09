# -*- coding:utf-8 -*-

import sys,os
import ConfigParser

class Db_Connector:
    def __init__(self, config_file_path):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        
        s = cf.sections()
        print 'section:', s
        
        o = cf.options("baseconf")
        print 'options:', o
        
        v = cf.items("baseconf")
        print 'db:', v
        
        db_host = cf.get("baseconf", "host")
        db_port = cf.getint("baseconf", "port")
        db_user = cf.get("baseconf", "user")
        db_pwd = cf.get("baseconf", "password")
        
        print db_host, db_port, db_user, db_pwd
        
        cf.set("baseconf", "db_pass", "123456")
        cf.write(open("config_file_path", "w"))
if __name__ == "__main__":
    f = Db_Connector("./db_config.ini")