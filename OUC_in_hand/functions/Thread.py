import threading
from queue import Queue
from functions import Functions
import datetime
import time

# 多进程查询
def processSelect(xn, xq, nowUrl, sessionid, informationlist, sel_skbjdm, times):
    threads = []
    q = Queue()
    count = len(informationlist)
    # 每份进程多少个爬取任务
    if times > count:
        times = count
    piece = int(count / times)
    # 多余部分
    extra = count - times * piece
    # 划分数组
    newinformationlist = []
    information = []
    for i in range(count):
        information.append(informationlist[i])
        if (i + 1) % piece == 0:
            newinformationlist.append(information)
            information = []
    if extra != 0:
        # 如果有多余的，则这个时候append
        newinformationlist.append(information)
    for i in range(len(newinformationlist)):
        t = threading.Thread(target=select, args=(xn, xq, nowUrl, sessionid, newinformationlist, i, sel_skbjdm, q))
        threads.append(t)
    t1 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    for t in threads:
        # t.setDaemon(True)
        t.start()
    for t in threads:
        # t.setDaemon(True)
        t.join()
    t2 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(t1)
    print(t2)
    return q
    # for i in range(count):
    #     information.append(informationlist[i])
    #     if i % piece == 0:
    #         newinformationlist.append(information)
    #         information = []
    # if extra != 0:
    #     # 如果有多余的，则这个时候append
    #     newinformationlist.append(information)
    # p = Pool(times)
    # for i in range(times):
    #     p.apply_async(select, args=(xn, xq, nowUrl, sessionid, newinformationlist, i, sel_skbjdm, q))
    #
    # p.close()
    # p.join()
    # print('All subprocesses done.')
    # return q


def select(xn, xq, nowUrl, sessionid, newinformationlist, number, sel_skbjdm, q):
    for i in range(len(newinformationlist[number])):
        information = newinformationlist[number][i]
        moneyOfClass, ifReStudy = Functions.Function.SelectClassByClass_UseNumber(xn, xq, nowUrl, sessionid, information[0], sel_skbjdm)
        powerOfCoin = moneyOfClass
        print(int(str(information[0])))
        if(int(str(information[0])) >= 18000000000 and int(str(information[0])) < 19000000000):
            powerOfCoin = int(str(moneyOfClass))*1
        if (int(str(information[0])) >= 17000000000 and int(str(information[0])) < 18000000000):
            powerOfCoin = int(str(moneyOfClass))*1.1
        if (int(str(information[0])) >= 16000000000 and int(str(information[0])) < 17000000000):
            powerOfCoin = int(str(moneyOfClass))*1.2
        if (int(str(information[0])) >= 15000000000 and int(str(information[0])) < 16000000000):
            powerOfCoin = int(str(moneyOfClass))*1.3
        else :
            powerOfCoin = int(str(moneyOfClass))*1.2
        # informationAboutClass.append([powerOfCoin, moneyOfClass, ifReStudy, information[0], information[1], information[2]])
        # q.put("test")
        q.put([round(powerOfCoin, 2), moneyOfClass, ifReStudy, information[0], information[1], information[2]])