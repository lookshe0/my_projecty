from django.shortcuts import render
from django.views.generic import View
import re
import json
import requests
from bs4 import BeautifulSoup
from django.utils.safestring import mark_safe
# Create your views here.
import search_zb
from django.shortcuts import render
from django.views.generic import View
import re
import json
import requests
from bs4 import BeautifulSoup
import re
from .models import  bidding
from requests import get
from lxml import etree

from django.utils import timezone
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.core.paginator import Paginator
'''

'''
#创建类视图
class Index(View):

    def get(self,request):
        zb_info=[]
        infos=[]
        '''if request.GET.get('q'):
            user_input=request.GET.get('q')
            if user_input=="上海大学" :
                for i in self.search_zb1():  # 获取所有页面中对应文章的urls的列表
                    for j in self.zb1(i, zb_info):  # 编历urls的列表，获取各url对应的标题正文等内容加入字典，并循环输入而组成的这个新列表
                        infos = j
            elif user_input=="北京交通大学":
                for i in self.search_zb2():  # 获取所有页面中对应文章的urls的列表
                    for j in self.zb2(i, zb_info):  # 编历urls的列表，获取各url对应的标题正文等内容加入字典，并循环输入而组成的这个新列表
                        infos = j
            return render(request, 'index.html',{'page_obj': infos})
        return render(request, 'index.html')'''
        if request.GET.get('q'):
            user_input = request.GET.get('q')
            entries = bidding.objects.filter(Q(bid_title__icontains=user_input))
            if entries.exists():
                for h in entries:
                    ins = {
                        'id': h.id,
                        'time': h.bid_time,
                        'name': h.bid_name,
                        'title': h.bid_title,
                    }
                    infos.append(ins)
                return render(request, 'index.html', {'page_obj': infos})
                # return render(request, 'index.html',{'infos':infos})
            else:
                ins = {
                    'name': "未找到相关信息",
                }
                infos.append(ins)
                return render(request, 'index.html', {'page_obj': infos})
        return render(request, 'index.html')

    def get_html1(self, url):
        headers = {
            'usr_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers).text
        return response

    def get_html2(self, url):
        headers = {
            'usr_Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.encoding = "gbk"
        return response

    def search_zb1(self):
    #一共79页
        for index in range(1,80):
            url='https://bidding.shu.edu.cn/sy/xtgg_list.jsp?gglx2bh=KCGG_A&page={}&searchText='.format(index)
            print('正在访问：第%s页' % index)
            html = self.get_html1(url)
            soup = BeautifulSoup(html, 'lxml')
            uls=soup.findAll('ul',class_="listPageList")
            # 选择所有的 < ul > 元素
            links=[]
            ulElement = soup.select("ul.listPageList")
            for liElement in ulElement:
                liElement = liElement.select("li")
                #print(liElement)
                for aElement in liElement:
                    Element = aElement.select("a")
                    for e in Element:
                        links.append([e.get("title"),e.get("href")])
            for i in links:
                i[1] = "https://bidding.shu.edu.cn/sy/"+i[1]
                print(i,end="\n")
            yield links
    def zb1(self,links,zb_info):
        for i in links:
            url=i[1]
            html=self.get_html1(url)
            soup = BeautifulSoup(html, 'lxml')
            zbname = soup.find('div', class_="artical_tit").text
            print(zbname)
            zbtexts = soup.find('div', class_="artical_text")
            results = zbtexts.select('p')
            zbtext = ''
            for tr in results:
                text = tr.get_text()
                zbtext += text + '\n'
            print(zbtext)
            timelist = soup.findAll('div', class_="text_right")
            zbtime = []
            for time in timelist:
                zbtime.append(time.get_text())


            #'''
            bid_title = zbname  # 从爬虫获取的标题数据
            bid_time = zbtime[1]  # 从爬虫获取的时间数据
            bid_text = zbtext  # 从爬虫获取的文本数据
            bid_web = i[1]  # 从爬虫获取的网址数据
            bid_name="上海大学"
            bid = bidding(bid_title=bid_title, bid_time=bid_time, bid_text=bid_text, bid_web=bid_web,bid_name=bid_name)
            bid.save()
            #'''

            info = dict()
            info['title'] = zbname
            info['time'] = zbtime[1]
            info['text'] = zbtext
            info['web'] = i[1]
            info['school']="上海大学"

            item = {
                'title': info.get('title'),
                'time': info.get('time'),
                'text': info.get('text'),
                'web': info.get('web'),
                'school':info.get('school')
            }
            zb_info.append(item)
        yield zb_info

    def search_zb2(self):
        url = 'https://gzc.bjtu.edu.cn/zb/zbcggs/index.htm'
        html = self.get_html2(url).text
        soup = BeautifulSoup(html, 'lxml')
        divs = soup.find("div", class_="list_content")
        lis = divs.findAll("li")
        link0 = []
        times = []
        for x in lis:
            a = x.select("a")
            span = x.select("span")
            for e in a:
                for i in span:
                    link0.append([e.get("title"), e.get("href"), i])
        for i in link0:
            i[1] = "https://gzc.bjtu.edu.cn/zb/zbcggs/" + i[1]
        yield link0
        for index in range(1, 76):#34数据太长了爬了一半(1,34)34(35,75)
            url = 'https://gzc.bjtu.edu.cn/zb/zbcggs/index{}.htm'.format(index)
            print('正在访问：第%s页' % index)
            html = self.get_html2(url).text
            soup = BeautifulSoup(html, 'lxml')
            divs=soup.find("div",class_="list_content")
            lis=divs.findAll("li")
            links=[]
            times=[]
            for x in lis:
                a=x.select("a")
                span = x.select("span")
                for e in a:
                    for i in span:
                        links.append([e.get("title"), e.get("href"),i])
            for i in links:
                i[1] = "https://gzc.bjtu.edu.cn/zb/zbcggs/" + i[1]
            yield links


    def zb2(self,links,zb_info):
        for i in links:
            url = i[1]
            html = self.get_html2(url)
            soup = BeautifulSoup(html.text, 'lxml')
            zbp=soup.findAll("p")
            zbtext=" "
            for x in zbp:
                text=x.get_text()
                zbtext += text + '\n'

            i[2]=i[2].text
            #'''
            bid_title = i[0]  # 从爬虫获取的标题数据
            bid_time = i[2]  # 从爬虫获取的时间数据
            bid_text = zbtext  # 从爬虫获取的文本数据
            bid_web = i[1]  # 从爬虫获取的网址数据
            bid_name="北京交通大学"
            bid = bidding(bid_title=bid_title, bid_time=bid_time, bid_text=bid_text, bid_web=bid_web,bid_name=bid_name)
            bid.save()
            #'''

            info = {}
            info['title'] = i[0]
            info['time'] = i[2]
            info['text'] = zbtext
            info['web'] = i[1]
            info['school']="北京交通大学"
            item = {
                'title': info.get('title'),
                'time': info.get('time'),
                'text': info.get('text'),
                'web': info.get('web'),
                'school':info.get('school')
            }
            zb_info.append(item)
        yield zb_info

def article_detail(request,id):
    articles=bidding.objects.filter(id=id)
    article=[]
    for h in articles:
        ins = {
            'title' : h.bid_title,
            'text' : h.bid_text,
            'web' : h.bid_web,
        }
        article.append(ins)
    return render(request, 'article.html', {'article': article})
def sh(request):
    datas = bidding.objects.filter(bid_name="上海大学")
    if request.GET.get('q') is None:
        infos = []
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title': h.bid_title,
                'text': h.bid_text,
                'web': h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos=[]
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
            # return render(request, 'index.html',{'infos':infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})


def bj(request):
    datas = bidding.objects.filter(bid_name="北京交通大学")
    if request.GET.get('q') is None:
        infos = []
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title': h.bid_title,
                'text': h.bid_text,
                'web': h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos=[]
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
            # return render(request, 'index.html',{'infos':infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
def oneweek(request):
    '''d = timezone.now()
    date=d.strftime("%Y-%m-%d")
    print(date)'''
    # 获取当前时间
    current_time = datetime.now()
    date = current_time.date()  # 将datetime对象转换为date对象
    # 计算一周前的时间
    one_week_ago = date - timedelta(days=7)
    # 从数据库中筛选近一周的数据记录
    datas = bidding.objects.filter(bid_time__gte=one_week_ago)
    if request.GET.get('q') is None:
        # 获取当前时间
        infos=[]
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title' : h.bid_title,
                'text' : h.bid_text,
                'web' : h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos=[]
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
            # return render(request, 'index.html',{'infos':infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})

def onemonth(request):
    # 获取当前时间
    current_time = datetime.now()
    date = current_time.date()  # 将datetime对象转换为date对象
    # 计算一周前的时间
    one_month_ago = date - timedelta(days=30)
    # 从数据库中筛选近一个月的数据记录
    datas = bidding.objects.filter(bid_time__gte=one_month_ago)
    if request.GET.get('q') is None:
        # 获取当前时间
        infos = []
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title': h.bid_title,
                'text': h.bid_text,
                'web': h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos = []
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
            # return render(request, 'index.html',{'infos':infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
def threemonths(request):
    current_time = datetime.now()
    date = current_time.date()
    three_months_ago = date - timedelta(days=90)
    # 从数据库中筛选近一个月的数据记录
    datas = bidding.objects.filter(bid_time__gte=three_months_ago)
    if request.GET.get('q') is None:
        # 获取当前时间
        infos = []
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title': h.bid_title,
                'text': h.bid_text,
                'web': h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos = []
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
            # return render(request, 'index.html',{'infos':infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
def halfyear(request):
    # 获取当前时间
    current_time = datetime.now()
    date = current_time.date()  # 将datetime对象转换为date对象
    #half_year_ago = date3 - timedelta(days=180)
    half_year_ago = date - relativedelta(months=6)
    datas = bidding.objects.filter(bid_time__gte=half_year_ago)
    if request.GET.get('q') is None:
        # 获取当前时间
        infos = []
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title': h.bid_title,
                'text': h.bid_text,
                'web': h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos = []
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
            # return render(request, 'index.html',{'infos':infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
def oneyear(request):
    current_time = datetime.now()
    date = current_time.date()
    one_year_ago = date - timedelta(days=365)
    #one_year_ago = date4 -relativedelta(months=12)
    datas = bidding.objects.filter(bid_time__gte=one_year_ago)
    if request.GET.get('q') is None:
        # 获取当前时间
        infos = []
        for h in datas:
            ins = {
                'id': h.id,
                'time': h.bid_time,
                'name': h.bid_name,
                'title': h.bid_title,
                'text': h.bid_text,
                'web': h.bid_web,
            }
            infos.append(ins)
        paginator = Paginator(infos, 10)  # 每页显示的数量
        page_number = request.GET.get('page')  # 从URL参数中获取页码
        page_obj = paginator.get_page(page_number)  # 根据页码获取对应的Page对象
        return render(request, 'index.html', {'page_obj': page_obj})
    else:
        infos = []
        user_input = request.GET.get('q')
        entries = datas.filter(Q(bid_title__icontains=user_input))
        if entries.exists():
            for h in entries:
                ins = {
                    'id': h.id,
                    'time': h.bid_time,
                    'name': h.bid_name,
                    'title': h.bid_title,
                }
                infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})
        else:
            ins = {
                'name': "未找到相关信息",
            }
            infos.append(ins)
            return render(request, 'index.html', {'page_obj': infos})