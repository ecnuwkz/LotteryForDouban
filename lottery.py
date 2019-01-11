# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:05:54 2019

@author: Jorah Wu
"""


from bs4 import BeautifulSoup
import requests
import time,random
import wx
import wx.adv
#import wx.richtext

class UserInfo:
    def __init__(self, user_id, user_link,user_comment,user_time):
        self.__id__ = user_id
        self.__link__ = user_link
        self.__comment__ = user_comment
        self.__time__ = user_time
 
    def get_id(self):
        return self.__id__
 
    def get_link(self):
        return self.__link__
    
    def get_comment(self):
        return self.__comment__
    
    def get_time(self):
        return self.__time__
 
    def __str__(self):
        return str("用户名:{}\n主页地址:{}\n转发内容:{}\n转发时间:{}\n"
                   .format(self.__id__, self.__link__,self.__comment__,self.__time__))
    def __eq__(self, other):
        if isinstance(other, UserInfo):
            return (self.__link__ == other.__link__)
        else:
            return False
 
    def __ne__(self, other):
        return (not self.__eq__(other))
 
    def __hash__(self):
        return hash(self.__link__)

class Lottery(wx.Frame):
    def __init__(self, title):
        global s_link,m_area_cookie,m_area_info,share_list,share_count,lottery_num
        share_list=[]#存放所有转发内容
        lottery_num=1#默认中奖人数
        
        wx.Frame.__init__(self, None, title=title)
        panel = wx.Panel(self,wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)

        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        label_link=wx.StaticText(panel, label="抽奖广播地址:", 
                           size=wx.DefaultSize, style=0)
        s_link=wx.TextCtrl(panel,size=(600,25))
        
        hbox1.Add(label_link, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 5)
        hbox1.Add(s_link, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 3)      
        
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)    
        label_cookie=wx.StaticText(panel, label="cookie:", style=0)
        hbox2.Add(label_cookie, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 5)
        
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        m_area_cookie = wx.TextCtrl(panel,size=(700,100), 
                               style=wx.TE_MULTILINE)
        hbox3.Add(m_area_cookie, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 5)
                         
        hbox5=wx.BoxSizer(wx.HORIZONTAL)
        statictext=wx.StaticText(panel,label='请选择中奖人数：',style=0,size=(100,25))
        list1=[]
        for i in range(1,20):
            list1.append(str(i))
        ch1=wx.ComboBox(panel,-1,value='1',choices=list1,style=0,size=(100,25))
        self.Bind(wx.EVT_COMBOBOX,self.on_combobox,ch1)
        m_lottery = wx.Button(panel,label="抽奖")
        m_lottery.Bind(wx.EVT_BUTTON, self.OnLottery)
        hbox5.Add(statictext,1,flag = wx.EXPAND|wx.ALL,border=5)
        hbox5.Add(ch1,1,flag = wx.EXPAND|wx.ALL,border=5)
        hbox5.Add(m_lottery,1,flag = wx.EXPAND|wx.ALL, border = 5)
        
        hbox4 = wx.BoxSizer(wx.HORIZONTAL)    
        label_info=wx.StaticText(panel, label="中奖用户信息:", style=0)
        hbox4.Add(label_info, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 5)
        
        hbox6 = wx.BoxSizer(wx.HORIZONTAL)
        m_area_info = wx.TextCtrl(panel,size=(700,400), 
                               style=wx.TE_MULTILINE)
        hbox6.Add(m_area_info, proportion = 0, flag = wx.EXPAND|wx.ALL, border = 5)
        
        vbox.Add(hbox1, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox2, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox3, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox5, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox4, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        vbox.Add(hbox6, proportion=0, flag=wx.EXPAND | wx.ALL, border=5)
        panel.SetSizer(vbox)

        self.SetSize((700,650))
        self.Center()
        self.Show()
        self.Fit()      
     
    def on_combobox(self,event):
        global lottery_num
        lottery_num=int(event.GetString())
        
    def OnLottery(self, event):
        global share_count,share_list,lottery_num
        #print(lottery_num)
        url=s_link.GetValue()
        if '?tab=reshare#reshare' not in url:
            url=url+'?tab=reshare#reshare'
        cookies={'cookie':m_area_cookie.GetValue()}
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'
        }
        share_count=0
        while 1: 
            #print(url)
            url_info = requests.get(url, cookies=cookies, headers=headers)
            next_page = self.get_comment_info(url_info.text)
            time.sleep(3)
            if next_page=='':
                break
            url = 'https://www.douban.com'+next_page   
        share_list=list(set(share_list))
        m_area_info.WriteText('一共有'+str(share_count)+'人次转发,'
                              +'其中有效转发为'+str(len(share_list))+'人次,共'
                              +str(lottery_num)+'人中奖,获奖名单如下：\n')
        resultList=random.sample(range(0,len(share_list)),lottery_num)
        for i in resultList:
            m_area_info.WriteText(str(share_list[int(i)])+'\n')
        
    def get_comment_info(self,html):
        global share_count
        soup = BeautifulSoup(html, 'html.parser')
        share= soup.find('div',class_='status-reshare-list')    
        for content in share.findAll('div',class_='content'):
            share_count=share_count+1
            #print(content)
            share_ID=content.find('a', class_='')
            #print('用户名'+share_ID.string)
            #print('用户主页地址'+share_ID['href'])
            share_content=content.find('p')
            #print('转发内容'+share_content.string)
            share_time=content.find('span',class_='pubtime')
            #print('转发时间'+share_time.string)
            share_list.append(UserInfo(share_ID.string,share_ID['href'],
                                       share_content.string.strip(),share_time.string))        
        #print(share_list[random.randint(0, 19)])
        share_next = soup.find('span',class_='next')
        share_page=share_next.find('a', class_='')
        if share_page:#说明有下一页
            n_page=share_page['href']
        else:
            n_page=''
        return n_page


if __name__ == "__main__":   
    app = wx.App(redirect=True)
    top = Lottery("豆瓣广播转发抽奖")
    top.Show()
    app.MainLoop()

