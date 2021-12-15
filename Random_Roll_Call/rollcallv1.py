# -*- coding: utf-8 -*-
"""
Created on Sat May 30 12:29:03 2020

@author: Amber
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Apr 24 13:06:50 2020

@author: Amber
利用Python：GUI实现课堂点名器:https://www.jianshu.com/p/64d1cb4a8b28
"""

import tkinter as tk

import xlrd

import time

import random

import datetime

import numpy as np


class LoveYou():

    # 初始化
    def __init__(self):
        # 第1步，建立窗口window
        self.window = tk.Tk()

        # 第2步，给窗口的可视化起名字
        self.window.title('随机点名小程序')

        # 第3步，设定窗口的大小(长＊宽)
        self.window.geometry('1000x800')

        self.text = tk.StringVar()  # 创建str类型
        self.roll = tk.StringVar()
        

        self.name,self.stu_id = self.read_data()

        # 获取星期几
        d = datetime.datetime.now()
        self.day = d.weekday() + 1

    def read_data(self):
        '''
        数据读取
        :return:
        '''
        workbook = xlrd.open_workbook('name.xlsx')

        sheet1 = workbook.sheet_by_index(0)  # sheet索引从0开始
        name = list(sheet1.col_values(0))  # 读取第一列内容
        name.pop(0)  # 把姓名 去掉
        stu_id = list(sheet1.col_values(1))#读取第二列学号
        stu_id.pop(0)  #把学号 去掉
        stu_id = [int(s) for s in stu_id]
        
        

        return name,stu_id
    
    def namecall(self):
        '''随机产生本次课的点名名单'''
        roll_desc = ''
        call_num = 1            #每次只点一个名字
        call_index = np.random.randint(0,len(self.name),size=call_num) 
        roll_name = np.array(self.name)[call_index]
        roll_id = np.array(self.stu_id)[call_index]
        self.pickname = roll_name[0]
        self.pickid = roll_id[0]
        roll_desc += '点名：%s :  %s \n'%(self.pickid ,self.pickname)
        
        self.roll.set(roll_desc)  # 设置内容
        self.window.update()  # 屏幕更新
        self.savecount(roll_desc)  # 写入日志
        
    def absence(self):
        
        abs_desc = '缺勤：'
        abs_desc+= "学号-%s-姓名-%s\n"%(self.pickid,self.pickname)
        self.savedesc(abs_desc) 
    
    def absence2(self):
        
        abs2_desc = '回答缺勤：'
        abs2_desc+= "学号-%s-姓名-%s\n"%(self.take_id,self.take_name)
        self.savedesc(abs2_desc) 
    
    def good(self):
        
        good_desc = '回答认真：'
        good_desc+= "学号-%s-姓名-%s\n"%(self.take_id,self.take_name)
        self.savedesc(good_desc) 
    
    def take(self):
        '''
        负责随机抽取同学提问
        :return:
        '''

        for s in range(15):
            '''
            后几秒有所停顿点，制造紧张气氛
            '''
            desc = ''
            if s == 12:
                time.sleep(0.5)
            elif s == 13:
                time.sleep(0.5)
            elif s == 14:
                time.sleep(0.5)
            else:
                time.sleep(0.1)
            
            index = np.random.randint(0,len(self.name),size=1)
            self.take_name = np.array(self.name)[index][0]
            self.take_id = np.array(self.stu_id)[index][0]

            desc += "\n恭喜:%s - 学号：%s 喜提回答问题的机会!\n" % (self.take_name,self.take_id)
    

            self.text.set(desc)  # 设置内容
            self.window.update()  # 屏幕更新


    def gettime(self):
        '''
        格式化时间
        :return:
        '''
        return time.strftime('\n%Y-%m-%d', time.localtime(time.time())) + "  星期" + str(self.day)


    def savedesc(self, desc):
        '''
        负责把选中的人写入到log里面
        :param desc:
        :return:
        '''
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write('*********************************\n')
            f.write(desc)

    def savecount(self, count):
        '''
        负责把被罚写的遍数写入到log里面
        :param count:
        :return:
        '''
        with open('log.txt', 'a', encoding='utf-8') as f:
            f.write(str(count) + '\n')
            

    def main(self):
        '''
        主函数负责绘制
        :return:
        '''
        
        # 绘制日期、班级总人数等
        now = time.strftime('%Y-%m-%d', time.localtime(time.time())) + "  星期" + str(self.day)
        now += "\n班级总人数:%s人" % str(len(self.name))
        now += "\n上课啦\n"
        self.savedesc(self.gettime()+"\n班级总人数:%s人\n" % str(len(self.name)))
        
        l1 = tk.Label(self.window, fg='red', text=now, width=500, height=5)
        l1.config(font='Helvetica -%d bold' % 25)
        l1.pack()  # 安置标签

        #绘制点名按钮
        btntake = tk.Button(self.window, text="随机点名", width=15, height=2, command=self.namecall)
        btntake.pack()
        
        # 绘制回答问题按钮
        btntake = tk.Button(self.window, text="回答问题", width=15, height=2, command=self.take)
        btntake.pack()

       #绘制缺勤按钮
        l5 = tk.Button(self.window, text="缺勤", width=15, height=2, command=self.absence,bg='red').place(x=600, y=155)
        #l5.pack()
        
        #绘制回答问题缺勤和认真按钮
        l7 = tk.Button(self.window, text="认真", width=7, height=2, command=self.good,bg='green').place(x=600, y=215)
        l6 = tk.Button(self.window, text="缺勤", width=7, height=2, command=self.absence2,bg='red').place(x=680, y=215)
        
        

        #绘制点名名单信息
        l4 = tk.Label(self.window, fg='black', textvariable=self.roll, width=500, height=10)
        l4.config(font='Helvetica -%d bold' % 20)
        l4.pack()
        
        # 绘制回答问题信息
        l2 = tk.Label(self.window, fg='red', textvariable=self.text, width=500, height=3)
        l2.config(font='Helvetica -%d bold' % 20)
        l2.pack()
        
        
        
        # 进入循环
        self.window.mainloop()


if __name__ == '__main__':
    loveyou = LoveYou()
    loveyou.main()