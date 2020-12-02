#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import threading
from threading import Thread
import time

"""
线程锁：
thread1: 同步锁
thread2: 互斥锁
thread3: 重用锁
thread4: 信号量
"""


def J(cond, list):
    for i in list:
        with cond:
            print(i)
            cond.notify()
            cond.wait()


def Y(cond, list):
    for i in list:
        with cond:
            cond.wait()
            print(i)
            cond.notify()


def thread1():
    """同步锁"""
    Jlist = ["在吗", "干啥呢", "去玩儿不", "好吧"]
    Ylist = ["在呀", "玩儿手机", "不去", "哦"]
    cond = threading.Condition()
    t1 = Thread(target=J, args=(cond, Jlist))
    t2 = Thread(target=Y, args=(cond, Ylist))
    t2.start()
    t1.start()  # 一定保证t1启动在t2之后,因为notify发送的信号要被t2接受到，如果t1先启动，会发生阻塞。


def a(lock):
    global num
    for _ in range(1000000):
        with lock:
            num += 1


def b(lock):
    global num
    for _ in range(1000000):
        with lock:
            num += 1


def thread2():
    """互斥锁"""
    global num
    num = 0
    lock = threading.Lock()
    t1 = Thread(target=a, args=(lock,))
    t1.start()
    t2 = Thread(target=b, args=(lock,))
    t2.start()
    t1.join()
    t2.join()
    print(num)  # 永远会输出20000000


def c(lock):
    with lock:
        print("我是A")
        b(lock)


def d(lock):
    with lock:
        print("我是b")


def thread3():
    """重用锁"""
    global num
    num = 0
    lock = threading.RLock()
    t1 = Thread(target=c, args=(lock,))
    t1.start()  # 会发生死锁，因为在第一次还没释放锁后，b就准备上锁，并阻止a释放锁


class B(threading.Thread):
    def __init__(self, name, sem):
        super(B, self).__init__()
        self.name = name
        self.sem = sem

    def run(self):
        time.sleep(1)
        print(self.name)
        self.sem.release()


class A(threading.Thread):
    def __init__(self, sem):
        super(A, self).__init__()
        self.sem = sem

    def run(self):
        for i in range(100):
            self.sem.acquire()
            b = B(str(i), self.sem)
            b.start()


def thread4():
    """信号量"""
    sem = threading.Semaphore(value=3)
    a = A(sem)
    a.start()  # 通过执行上面的代码，我们发现一次只能输出三个数字，sem控制访问并发量


if __name__ == '__main__':
    thread4()
