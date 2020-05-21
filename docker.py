# -*- coding: UTF-8 -*-

"""
   Docker 命令操作
"""

import os


class Docker():
    path = os.path.dirname(__file__)

    def shell(self, cmd):
        try:
            res = os.popen(cmd)
            return [x.replace("\n", "") for x in res.readlines()]
        except Exception as e:
            print("运行命令失败: ", e)
        finally:
            pass
        return []

    def version(self):
        return self.shell("docker -v")[0]

    def running(self):
        running = self.shell("docker ps")
        if len(running) > 1:
            running_list = [x for x in running[1:]]
            running_dict = []
            for i in running_list:
                tmp = [x for x in i.split() if x]
                running_dict.append({"name": tmp[1], "id": tmp[0]})
            return running_dict
        return []

    def images(self):
        images = self.shell("docker images")
        if len(images) > 1:
            images_list = [x for x in images[1:]]
            images_dict = []
            for i in images_list:
                tmp = [x for x in i.split() if x]
                images_dict.append({"name": tmp[0], "version": tmp[1],
                                    "id": tmp[2], "size": tmp[-1]})
            return images_dict
        return []

    def remove(self, id=None):
        for i in self.images():
            if id is None:
                if i["name"] == "<none>" and i["version"] == "<none>":
                    os.popen("docker rmi -f {}".format(i["id"]))
            else:
                if i["id"] == id:
                    os.popen("docker rmi -f {}".format(i["id"]))

    def stop(self, name, version, max=None):
        running = self.running()
        count = 0
        for i in running:
            if i["name"] == name + ":" + version:
                os.popen("docker stop {}".format(i["id"]))
                count += 1
            if max is None or max == count:
                break

    def run(self, name, version, path=None, env=None, port=None):
        """
        :param name: 镜像名称
        :param version: 镜像版本
        :param path: 路径挂载[元组和元组列表] (宿主机目录,镜像内目录)
                                           (".../ultimate/Resources","/var/www/ultimate/Resources")
        :param env:  镜像环境变量设置
        :param port: 端口映射[同path]
        """
        images = self.images()
        status = False
        for i in images:
            if i["name"] == name and i["version"] == version:
                status = True
        if status:
            command = "docker run -d"
            if isinstance(path, tuple):
                command += " -v {}:{}".format(path[0], path[1])
            if isinstance(path, list):
                for i in path:
                    command += " -v {}:{}".format(i[0], i[1])
            if env:
                command += " -e {}".format(env)
            if isinstance(port, tuple):
                command += " -p {}:{}".format(port[0], port[1])
            if isinstance(port, list):
                for i in port:
                    command += " -p {}:{}".format(i[0], i[1])
            command += " {}:{}".format(name, version)
            os.popen(command)
        return status

    def save(self, path=None):
        """
        @param path:  镜像存储路径,未输入使用当前文件所在路径
        @return:  None | 备份当前所有镜像
        """
        if path is None: path = self.path
        images = self.images()
        for i in images:
            self.shell("docker -o {target} {source}".format(
                target=os.path.join(path, str(i["name"]) + "_" + str(i["version"]) + ".tgz"),
                source=str(i["name"]) + ":" + str(i["version"])))

    def load(self, path=None):
        """
        @param path:  镜像文件路径,未输入使用当前文件所在路径
        @return:  None | 加载镜像
        """
        if path is None: path = self.path
        os.chdir(path)
        print("当前路径: ", path)
        for i in os.listdir("."):
            if str(i).endswith("tgz") and "_" in str(i):
                self.shell("docker load < {}".format(os.path.join(path, i)))


if __name__ == "__main__":
    Docker().load()
