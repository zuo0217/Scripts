#!/usr/bin/env python
# -*- coding: utf-8 -*-


import psutil
from mysql.connector import connect
import sys


class SystemInfo():
    """
       获取 CPU / MEMORY / STORAGE 使用率
    """

    def __init__(self):
        self.config = {}

    def configFilter(self, config):
        """host/port=3306/database/charset=utf8/user/password"""
        self.config["port"] = "3306"
        self.config["charset"] = "utf8"
        if config is not None:
            if "@@" in str(config):
                for i in str(config).split("@@"):
                    if "=" in str(i):
                        tmp = str(i).split("=")
                        self.config[tmp[0]] = tmp[1]

    def cpu(self):
        tmp = psutil.cpu_percent(1)
        return tmp

    def memory(self):
        return psutil.virtual_memory().percent

    def storage(self):
        return psutil.disk_usage('/').percent

    def db(self):
        for i in ["host", "port", "database", "charset", "user", "password"]:
            if str(i) not in self.config.keys():
                print("--config=参数缺失或者异常.")
                sys.exit(1)
        try:
            return connect(**self.config)
        except Exception as e:
            print("数据库连接失败: ".e)
            sys.exit(1)

    def getData(self):
        return {"cpu": self.cpu(), "memory": self.memory(), "storage": self.storage()}

    def printInfo(self):
        print("CPU:     ", self.cpu())
        print("MEMORY:  ", self.memory())
        print("STORAGE: ", self.storage())

    def mysql(self, table):
        if table is None:
            print("--table=参数缺失或者异常.")
            sys.exit(1)

        con = self.db()
        cursor = con.cursor()
        info = self.getData()
        print(info)

        sql = "INSERT INTO {} ({}) values{}".format(table, ",".join(["`{}`".format(x) for x in info.keys()]),
                                                    tuple(info.values()))

        try:
            cursor.execute(sql, ())
            con.commit()
            con.close()
            sys.exit(0)
        except Exception as e:
            print("SQL:{0} \nERROR:{1}".format(sql, e))
            con.close()
            sys.exit(1)


def main(*args):
    """
        parameters: mysql --config=[username=**@@password=**] || print
    """
    t = SystemInfo()

    config = False
    mysql = False
    table = None

    for i in args:
        if str(i) == "print" or "-print" == str(i):
            t.printInfo()
        if str(i) == "mysql" or "-mysql" == str(i):
            mysql = True
        if "--config=" in str(i) and "@" in str(i) and "=" in str(i):
            config = str(i).replace("--config=", "")
        if "--table=" in str(i):
            table = str(i).replace("--table=", "")
        if "-h" == str(i):
            print(
                """Usage:\n\tmysql --config=username=host/port=3306/database/charset=utf8/user/password --table=**\n\tprint""")

    if mysql and config:
        t.configFilter(config)
        t.mysql(table)


if __name__ == "__main__":
    main(*sys.argv[1:])
