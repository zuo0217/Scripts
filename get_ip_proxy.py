# _*_ coding:utf-8 _*_
# Create by Saseny on 2019-06-01


import requests
import re
import time
import mysql.connector


class IP_Proxy(object):
    url_special = 'https://www.kuaidaili.com/free/inha/{}/'
    url_normal = 'https://www.kuaidaili.com/free/intr/{}/'
    create_table_sql = 'CREATE TABLE `proxy` (' \
                       + '`ip` varchar(255) NOT NULL,' \
                       + '`port` varchar(255) NOT NULL,' \
                       + '`conceal` varchar(255) NOT NULL,' \
                       + '`type` varchar(255) DEFAULT NULL,' \
                       + '`location` varchar(255) DEFAULT NULL,' \
                       + '`speed` varchar(255) DEFAULT NULL,' \
                       + '`last-verify` varchar(255) DEFAULT NULL,' \
                       + '`status` varchar(255) DEFAULT NULL,' \
                       + 'PRIMARY KEY (`ip`)' \
                       + ') ENGINE=InnoDB DEFAULT CHARSET=utf8;'

    def __init__(self, **kwargs):
        self.store = kwargs.get("store", False)
        self.host = kwargs.get("host", None)
        self.port = kwargs.get("port", None)
        self.database = kwargs.get("database", None)
        self.username = kwargs.get("username", None)
        self.password = kwargs.get("password", None)
        self.table = kwargs.get("table", None)
        self.config = {}
        self.connect = None
        self.configInit()

    def page(self, url, verify=True):
        """
        :param url: url for ip proxy search
        :return: "IP", "PORT", "匿名度", "类型", "位置", "响应速度", "最后验证时间"
        """
        dataInfoList = []
        try:
            response = requests.get(url)
            data = re.findall(r'<td data-title=".*?">(.*?)</td>', response.text)

            for i in range(0, len(data), 7):
                info = {
                    "ip": data[i],
                    "port": data[i + 1],
                    "conceal": data[i + 2],
                    "type": data[i + 3],
                    "location": data[i + 4],
                    "speed": data[i + 5],
                    "last-verify": data[i + 6],
                    "status": str(self.verify(data[i], data[i + 1]) if verify is True else None)
                }

                self.insertSql(info)

                dataInfoList.append(info)

        except Exception as e:
            pass

        return dataInfoList

    @classmethod
    def verify(self, ip, port):
        """
        :param ip: ip address
        :param port: proxy port
        :return: whether for use
        """
        server = 'http://' + ip + ':' + port
        head = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'
        }

        try:
            p = requests.get(url='http://icanhazip.com', headers=head, proxies={"http": server}, timeout=3)

            findOut = re.findall(r'\d+\.\d+\.\d+.\d+', str(p.text))

            if str(ip) in findOut:
                return True
            if len(findOut) > 0:
                return True

        except Exception as e:
            pass

        return False

    def run(self, default="special", page=100, verify=False, timeSeconds=3):
        """
        :param default: url for ip proxy get
        :param page: search how many page
        :param verify: whether verify ip proxy
        :param timeSeconds: time sleep after one page
        :return: data
        """
        total = []
        if default == "special":
            for i in range(1, int(page), 1):
                tmp = self.page(url=self.url_special.format(i), verify=verify)
                total.extend(tmp)
                time.sleep(0 if verify is True else timeSeconds)

        elif default == "normal":
            for i in range(1, int(page), 1):
                tmp = self.page(url=self.url_normal.format(i), verify=verify)
                total.extend(tmp)
                time.sleep(0 if verify is True else timeSeconds)
        else:
            print("Error Default Value.")

        try:
            self.connect.close()
        except:
            pass

        return total

    def configInit(self):
        self.config["host"] = self.host
        self.config["port"] = self.port
        self.config["database"] = self.database
        self.config["charset"] = "utf8"
        self.config["user"] = self.username
        self.config["password"] = self.password
        if None not in self.config.values() and self.table is not None:
            try:
                self.connect = mysql.connector.connect(**self.config)
                self.store = True
            except:
                self.store = False
            finally:
                pass
        else:
            self.store = False

    def insertSql(self, dictInfo):
        if self.store:
            try:
                cursor = self.connect.cursor()
                sql_insert = "INSERT INTO {} ({}) values{}".format(self.table,
                                                                   ",".join(
                                                                       ["`{}`".format(x) for x in dictInfo.keys()]),
                                                                   tuple(dictInfo.values()))
                cursor.execute(sql_insert, ())
                self.connect.commit()
            except Exception as e:
                print("ERROR: {}".format(e))
            finally:
                pass


if __name__ == "__main__":
    t = IP_Proxy(store=True, host="******", port="3306",
                 username="root", password="******",
                 database="Data", table="proxy")
    # t.run(default="normal", page=5, verify=True)