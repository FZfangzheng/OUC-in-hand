from functions import User
from functions import Functions
import urllib


if __name__ == "__main__":
    userName = input("请输入你的学号")
    pwd = input("请输入你的密码")
    user = User.Student(userName, pwd)
    if user.loginext():
        if userName == "16020031016":
            function = Functions.Function(userName, user.url, user.sessionid, user.deskey, user.nowtime)
            function.changTime()
            while True:
                print("1.查询成绩 2.查询排名情况 3.查询选课(按选课号) 4.查询选课(按学号) 5.查询课程给分情况 6.查看照片(按学号) 7.重置选课查询时间 8.退出")
                choice = input("请选择你要进行的操作")
                try:
                    if choice == "1":
                        xh = input("输入你要选择的学号：")
                        timeId = input("输入你要选择的时间序号：\n0.入学以来\n1.2018秋季学期\n2.2018夏季学期\n3.2018春季学期\n"
                                       "4.2017秋季学期\n5.2017夏季学期\n6.2017春季学期\n"
                                       "7.2016秋季学期\n")
                        if timeId == "0":
                            xn = "0000"
                            xq = "0"
                        elif timeId == "1":
                            xn = "2018"
                            xq = "1"
                        elif timeId == "2":
                            xn = "2018"
                            xq = "0"
                        elif timeId == "3":
                            xn = "2017"
                            xq = "2"
                        elif timeId == "4":
                            xn = "2017"
                            xq = "1"
                        elif timeId == "5":
                            xn = "2017"
                            xq = "0"
                        elif timeId == "6":
                            xn = "2016"
                            xq = "2"
                        elif timeId == "7":
                            xn = "2016"
                            xq = "1"
                        else:
                            print("输入错误")
                            break
                        informationlist = function.InquiryGrades(xn, xq, xh, xn+"-"+xq)
                        print("{:^10}\t{:^10}\t{:^10}\t{:^10}".format("课程名称", "课程学分", "初修|重修", "分数"))
                        for i in range(len(informationlist)):
                            information = informationlist[i]
                            print(
                                "{:^10}\t{:^10}\t{:^10}\t{:^10}".format(information[0], information[1], information[2],
                                                                        information[3]))
                    if choice == "2":
                        function.getAllStudentGrade()
                    if choice == "3":
                        function.SelectClassByClass()
                    if choice == "4":
                        function.SelectClassByNumber()
                    if choice == "5":
                        function.getClassGrade()
                    if choice == "6":
                        function.acquirePhoto()
                    if choice == "7":
                        function.changTime()
                    if choice == "8":
                        break
                except urllib.request.HTTPError as e:
                    print(e.code)
                    print(e.reason)
        else:
            print("登陆失败！退出程序")
    else:
        print("登陆失败！退出程序")