#----------------urllib库发送请求----------------

# from urllib import request
# 这种方法，有反扒技术的网站中不适用
# url = "http://www.dianping.com/"
# res = request.urlopen(url)  # 访问url并获得响应
# print(res.geturl())  # 返回相应地址
# print(res.getcode())  # 获取请求状态码 2XX 正常，3XX, 4XX 访问页面有问题。。。
# print(res.info())  # 获取响应头
# html = res.read()  # 获取的是字节形式的内容
#
# html.decode('utf-8')  # 解码
# print(html)

# 这种方法，有反扒技术的网站中适用

# from urllib import request
# url = "http://www.dianping.com/"
# # header字典类型，这就伪装成了浏览器去访问网站
# header = {"User-Agent":\
#               "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
# # 不直接传url对象，使用request来封装一个url对象
# req = request.Request(url, headers=header)
# res = request.urlopen(req)
# print(res.geturl())
# print(res.getcode())
# print(res.info())
# html = res.read()
# html.decode('utf-8')
# print(html)


# ---------------------requests库发送请求————————————————————


# import requests
# url ="http://www.dainping.com/"
# res = requests.get(url)
# print(res.encoding)
# print(res.status_code)
# res.encoding = 'utf-8'
# html = res.text
# print(html)

# import requests
# url = "http://www.dianping.com"
# header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
# res = requests.get(url, headers=header)
# print(res.encoding)
# print(res.headers)  # 'Content-Type': 'text/html;charset=UTF-8'，代表这个网页的编码格式就是chaeset的值；若是没有这个key，就是默认utf-8
# print(res.status_code)
# res.encoding = 'utf-8'
# html = res.text
# print(html)




# -------------------解析响应里面我们感兴趣的内容---------------------
# re正则（解析速度最快，但对正则表达式的掌握要求很高）/Beautiful soup（第三方解析模块，较简单，把复杂的html
# 文档封装成python的树形结构，每一个节点都是python对象/Pyquery/lxml




# # -----beautifulsoup4解析内容
# # BeautifulSoup(html)
# #   获取节点：find（）
# #   获取属性：attrs
# #   获取文本：text
# from bs4 import BeautifulSoup
# import requests
# url = "http://wsjkw.sc.gov.cn/scwsjkw/gzbd/fyzt.shtml"
# header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
# res = requests.get(url, headers=header)
# res.encoding = 'utf-8'
# html = res.text
# soup = BeautifulSoup(html, features="html.parser")
#
# a = soup.find("a")
# # print(a)
# # print(a.attrs) # 拿到标签里的属性
# # print(a.attrs["href"]) # 属性值是字典类型
#
# url_new = "http://wsjkw.sc.gov.cn" + a.attrs["href"]
# # 利用这个新地址我们就可以开始新一轮的爬取了
# res_new = requests.get(url_new, headers=header)
# res_new.encoding = 'utf-8'
# html_new = res_new.text
# soup_new = BeautifulSoup(html_new, features="html.parser")
# p = soup_new.find("p")
# print(p)


# # -------re解析内容，re是Python自带的正则表达式模块
# # re.search(regex,str)
# #   1、在str中查找满足条件的字符串，regex处填写正则表达式，匹配上了就会返回match后面的值，匹配不上返回None
# #   2、对返回结果可以分组，可在字符串内添加小括号分离数据：
# #       groups()
# #       group(index):返回指定分组结果
#
# # 在BeautifulSoup 通过网页标签粗略匹配的基础上用re来做精确匹配
# import re
# from bs4 import BeautifulSoup
# import requests
# url = "http://wsjkw.sc.gov.cn/scwsjkw/gzbd/fyzt.shtml"
# header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
# res = requests.get(url, headers=header)
# res.encoding = 'utf-8'
# html = res.text
# soup = BeautifulSoup(html, features="html.parser")
#
# a = soup.find("a")
#
# url_new = "http://wsjkw.sc.gov.cn" + a.attrs["href"]
# # 利用这个新地址我们就可以开始新一轮的爬取了
# res_new = requests.get(url_new, headers=header)
# res_new.encoding = 'utf-8'
# html_new = res_new.text
# soup_new = BeautifulSoup(html_new, features="html.parser")
# p = soup_new.find("p")
#
# text = p.text
# # print(p)
# # print(text)
#
# # 正则表达式
# pattern = "(\d+)名确诊患者.*?住院隔离治疗(\d+)人.*?危重(\d+)人.*?治愈出院(\d+)人.*?死亡(\d+)人"   # .*?，加上？为非贪心匹配
# result = re.search(pattern, text)
# print(result)
#
# print(result.groups())  # 元组类型，拿到小括号里面匹配到的所有的值
# print(result.group(0))  # 拿到字符串本身
# print(result.group(1), result.group(2), result.group(3))  # 拿到第一个参数值


# ---------疫情数据来源：
# 1、全国各地的卫健委网站上爬取数据；
# 2、直接去大平台上爬取最终数据，如腾讯、百度

#-----因为腾讯直接有全部的数据，所以我们直接用腾讯
import requests
# import json
# url = "https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5"
# header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
# res = requests.get(url, headers=header)
# print(res.headers)
# print(res.text)
# # 由于拿到的是JSON格式，JSON字符串，我们可以用JSON模块把他转成字典格式
# d = json.loads(res.text)
# # print(d["data"])
# type(d["data"])
# data_all = json.loads(d["data"])
# print(data_all.keys())
# print(data_all["lastUpdateTime"])  # 上次数据更新时间
# print(data_all["chinaTotal"])  # 当前汇总数据
# print(data_all["chinaAdd"])  # 新增的数据
# print(data_all["chinaDayList"])  # 全部数据
# print(data_all["areaTree"])
# print(len(data_all["areaTree"]))
# print(data_all["areaTree"][0].keys())



import requests
import json
url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
res = requests.get(url, headers=header)
d = json.loads(res.text)
data_foreign = json.loads(d['data'])
# print(data_foreign['foreignList'])#{'name': '美国', 'continent': '北美洲', 'date': '03.28', 'isUpdated': True, 'confirmAdd': 15681, 'confirmAddCut': 0, 'confirm': 101724, 'suspect': 0, 'dead': 1586, 'heal': 869, 'nowConfirm': 99269, 'confirmCompare': 15681, 'nowConfirmCompare': 15283, 'healCompare': 116, 'deadCompare': 282, 'children': [{'name': '纽约',
# print(data_foreign['globalDailyHistory'])  # 全球总共的数据，每天全球确诊多少。。。{'date': '01.28', 'all': {'confirm': 57, 'dead': 0, 'heal': 3, 'newAddConfirm': 19, 'deadRate': '0.00', 'healRate': '5.26'}}, {'date': '01.29', 'all': {'confirm': 74, 'dead': 0, 'heal': 3, 'newAddConfirm': 12, 'deadRate': '0.00', 'healRate': '4.05'}}
# print(data_foreign['continentStatis'])  # 各个州的数据。{'date': '02/23', 'statis': {'亚洲': 960, '其他': 691, '北美洲': 42, '大洋洲': 17, '欧洲': 174}, 'nowConfirm': 1716, 'rate': 188, 'range': '02/17-02/23'}
#------开始--------------------------------------

world_List = {}
world_confirm = {}  # 把各个国家总共确诊人数也做一个字典，以便后边做图
def world_data(data_foreign):
    for i in data_foreign['foreignList']:
        country_name = i['name']
        country_date = i['date']
        country_confirmAdd = i['confirmAdd']  # 今日新增确诊
        country_totalconfirm = i['confirm']  # 累计有多少确诊过
        country_nowConfirm = i['nowConfirm']  # 目前仍有多少确诊
        country_dead = i['dead']
        country_heal = i['heal']

        world_confirm[country_name] = country_totalconfirm

        world_List[country_name] = {'country_date': country_date, 'country_confirmAdd':country_confirmAdd, 'country_totalconfirm':country_totalconfirm, 'country_nowConfirm':country_nowConfirm, 'country_dead':country_dead, 'country_heal':country_heal}
        world_confirm_List = list(world_confirm.items())
    return world_List, world_confirm_List

from pyecharts.charts import *
from pyecharts import options


def pye_world_map(world_confirm_List):
    # 创建World_Map
    World_Map = Map()
    # 添加数据  name_map把世界地图国家名称中英文对照起来
    World_Map.add("新冠肺炎全球累计确诊数", world_confirm_List, maptype="world",
                  name_map={'Singapore Rep.': '新加坡',
                            'Dominican Rep.': '多米尼加',
                            'Palestine': '巴勒斯坦',
                            'Bahamas': '巴哈马',
                            'Timor-Leste': '东帝汶',
                            'Afghanistan': '阿富汗',
                            'Guinea-Bissau': '几内亚比绍',
                            "Côte d'Ivoire": '科特迪瓦',
                            'Siachen Glacier': '锡亚琴冰川',
                            "Br. Indian Ocean Ter.": '英属印度洋领土',
                            'Angola': '安哥拉',
                            'Albania': '阿尔巴尼亚',
                            'United Arab Emirates': '阿联酋',
                            'Argentina': '阿根廷',
                            'Armenia': '亚美尼亚',
                            'French Southern and Antarctic Lands': '法属南半球和南极领地',
                            'Australia': '澳大利亚',
                            'Austria': '奥地利',
                            'Azerbaijan': '阿塞拜疆',
                            'Burundi': '布隆迪',
                            'Belgium': '比利时',
                            'Benin': '贝宁',
                            'Burkina Faso': '布基纳法索',
                            'Bangladesh': '孟加拉国',
                            'Bulgaria': '保加利亚',
                            'The Bahamas': '巴哈马',
                            'Bosnia and Herz.': '波斯尼亚和黑塞哥维那',
                            'Belarus': '白俄罗斯',
                            'Belize': '伯利兹',
                            'Bermuda': '百慕大',
                            'Bolivia': '玻利维亚',
                            'Brazil': '巴西',
                            'Brunei': '文莱',
                            'Bhutan': '不丹',
                            'Botswana': '博茨瓦纳',
                            'Central African Rep.': '中非',
                            'Canada': '加拿大',
                            'Switzerland': '瑞士',
                            'Chile': '智利',
                            'China': '中国',
                            'Ivory Coast': '象牙海岸',
                            'Cameroon': '喀麦隆',
                            'Dem. Rep. Congo': '刚果民主共和国',
                            'Congo': '刚果',
                            'Colombia': '哥伦比亚',
                            'Costa Rica': '哥斯达黎加',
                            'Cuba': '古巴',
                            'N. Cyprus': '北塞浦路斯',
                            'Cyprus': '塞浦路斯',
                            'Czech Rep.': '捷克',
                            'Germany': '德国',
                            'Djibouti': '吉布提',
                            'Denmark': '丹麦',
                            'Algeria': '阿尔及利亚',
                            'Ecuador': '厄瓜多尔',
                            'Egypt': '埃及',
                            'Eritrea': '厄立特里亚',
                            'Spain': '西班牙',
                            'Estonia': '爱沙尼亚',
                            'Ethiopia': '埃塞俄比亚',
                            'Finland': '芬兰',
                            'Fiji': '斐',
                            'Falkland Islands': '福克兰群岛',
                            'France': '法国',
                            'Gabon': '加蓬',
                            'United Kingdom': '英国',
                            'Georgia': '格鲁吉亚',
                            'Ghana': '加纳',
                            'Guinea': '几内亚',
                            'Gambia': '冈比亚',
                            'Guinea Bissau': '几内亚比绍',
                            'Eq. Guinea': '赤道几内亚',
                            'Greece': '希腊',
                            'Greenland': '格陵兰',
                            'Guatemala': '危地马拉',
                            'French Guiana': '法属圭亚那',
                            'Guyana': '圭亚那',
                            'Honduras': '洪都拉斯',
                            'Croatia': '克罗地亚',
                            'Haiti': '海地',
                            'Hungary': '匈牙利',
                            'Indonesia': '印度尼西亚',
                            'India': '印度',
                            'Ireland': '爱尔兰',
                            'Iran': '伊朗',
                            'Iraq': '伊拉克',
                            'Iceland': '冰岛',
                            'Israel': '以色列',
                            'Italy': '意大利',
                            'Jamaica': '牙买加',
                            'Jordan': '约旦',
                            'Japan': '日本',
                            'Kazakhstan': '哈萨克斯坦',
                            'Kenya': '肯尼亚',
                            'Kyrgyzstan': '吉尔吉斯斯坦',
                            'Cambodia': '柬埔寨',
                            'Korea': '韩国',
                            'Kosovo': '科索沃',
                            'Kuwait': '科威特',
                            'Lao PDR': '老挝',
                            'Lebanon': '黎巴嫩',
                            'Liberia': '利比里亚',
                            'Libya': '利比亚',
                            'Sri Lanka': '斯里兰卡',
                            'Lesotho': '莱索托',
                            'Lithuania': '立陶宛',
                            'Luxembourg': '卢森堡',
                            'Latvia': '拉脱维亚',
                            'Morocco': '摩洛哥',
                            'Moldova': '摩尔多瓦',
                            'Madagascar': '马达加斯加',
                            'Mexico': '墨西哥',
                            'Macedonia': '马其顿',
                            'Mali': '马里',
                            'Myanmar': '缅甸',
                            'Montenegro': '黑山',
                            'Mongolia': '蒙古',
                            'Mozambique': '莫桑比克',
                            'Mauritania': '毛里塔尼亚',
                            'Malawi': '马拉维',
                            'Malaysia': '马来西亚',
                            'Namibia': '纳米比亚',
                            'New Caledonia': '新喀里多尼亚',
                            'Niger': '尼日尔',
                            'Nigeria': '尼日利亚',
                            'Nicaragua': '尼加拉瓜',
                            'Netherlands': '荷兰',
                            'Norway': '挪威',
                            'Nepal': '尼泊尔',
                            'New Zealand': '新西兰',
                            'Oman': '阿曼',
                            'Pakistan': '巴基斯坦',
                            'Panama': '巴拿马',
                            'Peru': '秘鲁',
                            'Philippines': '菲律宾',
                            'Papua New Guinea': '巴布亚新几内亚',
                            'Poland': '波兰',
                            'Puerto Rico': '波多黎各',
                            'Dem. Rep. Korea': '朝鲜',
                            'Portugal': '葡萄牙',
                            'Paraguay': '巴拉圭',
                            'Qatar': '卡塔尔',
                            'Romania': '罗马尼亚',
                            'Russia': '俄罗斯',
                            'Rwanda': '卢旺达',
                            'W. Sahara': '西撒哈拉',
                            'Saudi Arabia': '沙特阿拉伯',
                            'Sudan': '苏丹',
                            'S. Sudan': '南苏丹',
                            'Senegal': '塞内加尔',
                            'Solomon Is.': '所罗门群岛',
                            'Sierra Leone': '塞拉利昂',
                            'El Salvador': '萨尔瓦多',
                            'Somaliland': '索马里兰',
                            'Somalia': '索马里',
                            'Serbia': '塞尔维亚',
                            'Suriname': '苏里南',
                            'Slovakia': '斯洛伐克',
                            'Slovenia': '斯洛文尼亚',
                            'Sweden': '瑞典',
                            'Swaziland': '斯威士兰',
                            'Syria': '叙利亚',
                            'Chad': '乍得',
                            'Togo': '多哥',
                            'Thailand': '泰国',
                            'Tajikistan': '塔吉克斯坦',
                            'Turkmenistan': '土库曼斯坦',
                            'East Timor': '东帝汶',
                            'Trinidad and Tobago': '特里尼达和多巴哥',
                            'Tunisia': '突尼斯',
                            'Turkey': '土耳其',
                            'Tanzania': '坦桑尼亚',
                            'Uganda': '乌干达',
                            'Ukraine': '乌克兰',
                            'Uruguay': '乌拉圭',
                            'United States': '美国',
                            'Uzbekistan': '乌兹别克斯坦',
                            'Venezuela': '委内瑞拉',
                            'Vietnam': '越南',
                            'Vanuatu': '瓦努阿图',
                            'West Bank': '西岸',
                            'Yemen': '也门',
                            'South Africa': '南非',
                            'Zambia': '赞比亚',
                            'Zimbabwe': '津巴布韦'})
    # 不显示地图各国标签
    World_Map.set_series_opts(label_opts=options.LabelOpts(is_show=False), )
    # 设置数据与颜色的一个映射
    World_Map.set_global_opts(visualmap_opts=options.VisualMapOpts( is_piecewise=True,
     pieces=[
        {"min": 1, "max": 19, "color": "#ffefd7"},
        {"min": 20, "max": 99, "color": "#ffd2a0"},
        {"min": 100, "max": 199, "color": "#fe8664"},
        {"min": 200, "max": 799, "color": "#e64b47"},
        {"min": 800, "max": 4999, "color": "#c91014"},
        {"min": 5000, "max": 15999, "color": "#9c0a0d"},
        {"min": 16000,"max": 59999, "color": "#800000"},
        {"min": 60000, "max": 199999, "color": "#FF0000"}
    ]))
    # 显示或者渲染地图
    World_Map.render('world_3.28.html')




if __name__ == '__main__':
    (world_List, world_confirm_List) = world_data(data_foreign)
    print(world_confirm_List)
    pye_world_map(world_confirm_List)




# print(world_data(data_foreign))
# 分析与处理
# lastUpdateTime:最后更新时间
# chinaTotal：总数
# chinaDayList：历史记录
# chinaDayAddList：历史新增记录
# areaTree：name      #areaTree[0],中国数据
#           today
#           total
#           children: name   #省级数据，列表
#                     today
#                     total
#                     children: name  #市级数据，列表
#                               today
# # #                               total
# import time
# import json
#
#
# import requests
#
# url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
# header = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                         '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
# res1 = requests.get(url1, headers=header)  #
# context1 = res1.text
# print(context1)
#
#


#
# text = json.loads(res1.text)
# data1 = text['data']
# data_all1 = json.loads(data1)
# print(data_all1.keys())
# # print('chinaDayList', data_all1['chinaDayList'])
# # print('chinaDayAddList', data_all1['chinaDayAddList'])
#
# url2 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
# res2 = requests.get(url2, headers=header)
# context2 = res2.text
# text2 = json.loads(context2)
# data2 = text2['data']
# data_all2 = json.loads(data2)



#----测试
# print(data_all2.keys())
# print('lastUpdateTime', data_all2['lastUpdateTime'])
# print('chinaTotal', data_all2['chinaTotal'])
# print('chinaAdd', data_all2['chinaAdd'])
# print('areaTree', data_all2['areaTree'])  # areaTree是个树形结构，包含着各地的疫情信息
# print(len(data_all2['areaTree']))  # areaTree里面有多少元素
# print(type(data_all2['areaTree'][0]))
# print('中国各地的疫情数据：', data_all2['areaTree'][0])
# print('chinaDayList', data_all1['chinaDayList'])
# print(type(data_all1['chinaDayList']))


# # -----------为之后数据可视化准备数据列表
# date_list = []  #时间列表
# confirm_list = []  #确诊列表
# suspect_list = []  #疑似列表
# dead_list = []  #死亡列表
# heal_list = []  #治愈列表
#
# history = {}  # 历史数据
# num = 0
# # history = {'2020-1-20':{'confirm':41, 'suspect':0, 'dead':1, 'heal':0, 'confirm_add':3, 'suspect_add':4, 'dead_add':0, 'heal_add':2}}
# # history['2020-1-20'] = {'confirm':41, 'suspect':0, 'dead':1, 'heal':0}
# for i in data_all1['chinaDayList']:
#
#
#
#
#     date = '2020.' + i['date']
#     tup = time.strptime(date, '%Y.%m.%d')
#     date = time.strftime('%Y-%m-%d', tup)  # 改变时间格式，不然插入数据库时会报错，数据库是datetime格式
#
#     # date_list.append(i['date'])  # 将处理后的时间先装入一个列表
#
#     confirm = i['confirm']
#     suspect = i['suspect']
#     dead = i['dead']
#     heal = i['heal']
#
#     num += 1
#     if num % 2 == 0:  # 隔天统计
#         date_list.append(i['date'])  # 将没处理的时间先装入一个列表
#         confirm_list.append(confirm)  # 将每日的确诊人数先装入一个列表
#         suspect_list.append(suspect)  # 将每日的疑似人数先装入列表
#         dead_list.append(dead)  # 将每日的死亡人数先装入列表
#         heal_list.append(heal)  # 将每日的治愈人数先装入列表
#
#
#     history[date] = {'confirm': confirm, 'suspect': suspect, 'dead': dead, 'heal': heal}
# print(history)
# print()

#
# # print(data_all1['chinaDayAddList'])
#
#
# for i in data_all1['chinaDayAddList']:
#     date = '2020.' + i['date']
#     tup = time.strptime(date, '%Y.%m.%d')
#     date = time.strftime('%Y-%m-%d', tup)
#     confirm_Add = i['confirm']
#     suspect_Add = i['suspect']
#     dead_Add = i['dead']
#     heal_Add = i['heal']
#     history[date].update({'confirm_Add': confirm_Add, 'suspect_Add': suspect_Add, 'dead_Add': dead_Add, 'heal_Add': heal_Add})
#     # Python 字典 update() 方法用于更新字典中的键值对可以修改存在的键值对应的值，也可以添加新的键值对到字典中
# # print(history)
#
# #
# print(data_all2['areaTree'])
# print(len(data_all2['areaTree']))
# #
#
# 世界地区图，各个国家
# world = {'中国'：{'confirm':10000, 'suspect': 1002, 'dead': 2333, 'heal': 787, 'confirm_Add': 122, 'isUpdated': True}}
# world = {}
# world_confirm = {}
# for i in data_all2['areaTree']:
#     country_name = i['name']
#     confirm = i['total']['confirm']
#     suspect = i['total']['suspect']
#     dead = i['total']['dead']
#     heal = i['total']['heal']
#     confirm_Add = i['today']['confirm']
#     isUpdated = i['today']['isUpdated']
#     world[country_name] = {'confirm': confirm, 'suspect': suspect, 'dead': dead, 'heal': heal, 'confirm_Add': confirm_Add, 'isUpdated': isUpdated}
#
#     world_confirm[country_name] = confirm
#     world_confirm_list = list(world_confirm.items())
#
# print(world_confirm_list)
#
#
# # 中国行政地区图，省、市每天更新的数据
# china = {}   #china = {'湖北': {'Total_confirm’：20222, 'Total_isUpdated': True, 'children':[{'city_name':'武汉' ,'city_confirm':1222,'city_isUpdated':True},{'city_name':‘孝感’，‘city_confirm':222,'city_isUpdated':True}}
# china_pro_today = {}
# pro = {}
# for i in data_all2['areaTree'][0]['children']:
#     pro_name = i['name']
#     Total_today_confirm = i['today']['confirm']
#     Total_today_isUpdated = i['today']['isUpdated']
#
#     Total_confirm = i['total']['confirm']  # 各省累计确诊人数
#     pro[pro_name] = Total_confirm
#     children = []  # 每次都要拿一个空列表来装每个省份的地级市信息
#
#     for j in i['children']:
#         city_name = j['name']
#         city_today_confirm = j['today']['confirm']
#         city_today_isUpdated = j['today']['isUpdated']
#         new_pro_children = {'city_name': city_name, 'city_today_confirm': city_today_confirm, 'city_today_isUpdated': city_today_isUpdated}
#         children.append(new_pro_children)  # 这个省份的一个地级市信息，添加入列表
#     china_pro_today[pro_name] = Total_today_confirm
#     china[pro_name] = {'Total_today_confirm': Total_today_confirm, 'Total_today_isUpdated': Total_today_isUpdated, 'children': children}
# china_pro_today_list = list(china_pro_today.items())
#
# pro_list = list(pro.items())
# # print(china_pro_today_list)
# print(pro_list)

#
# #------------数据可视化测试
# import numpy as np
# import matplotlib
# import matplotlib.figure
# import matplotlib.pyplot as plt
# from matplotlib.font_manager import FontProperties
# from mpl_toolkits.basemap import Basemap
# from matplotlib.backends.backend_agg import FigureCanvasAgg
# from matplotlib.patches import Polygon
# from matplotlib.collections import PatchCollection

#
# plt.rcParams['font.sans-serif'] = ['FangSong']  #设置默认字体
# plt.rcParams['axes.unicode_minus'] = 'False'  # 解决保存图像时，’-‘显示为方块的问题
#
#
# def plot_china_everyday():
#     # 根据日期，绘制中国每日确诊、疑似、死亡、治愈数据
#     plt.figure('2019-nCoV中国每日疫情统计图表', facecolor='#f4f4f4', figsize=(200, 100))
#     plt.title('2019-nCoV中国每日疫情曲线', fontsize=20)
#
#
#     plt.plot(date_list, confirm_list, label='确诊')
#     plt.plot(date_list, suspect_list, label='疑似')
#     plt.plot(date_list, dead_list, label='死亡')
#     plt.plot(date_list, heal_list, label='治愈')
#     plt.grid(linestyle=':')  # 显示网格
#     plt.legend(loc='best')  # 显示图例
#     # plt.savefig('2019-nCoV中国每日疫情统计图表.png')  # 保存为文件
#     plt.show()
#
#
# def plot_distribution():
#     # 绘制行政区域确诊分布数据
#     font = FontProperties(fname = 'STKAITI.TTF', size = 14)
#     lat_min = 0
#     lat_max = 60
#     lon_min = 70
#     lon_max = 140
#
#     handles = [
#         matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
#         matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
#         matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
#         matplotlib.patches.Patch(color='#ffaa85', alpha=1, linewidth=0),
#     ]
#     labels = ['0人', '1-5人', '5-10人', '>10人']
#
#     fig = matplotlib.figure.Figurre()
#     fig.set_sizeinches(10, 8)  # 设置绘图板尺寸
#     axes = fig.add_axes((0.1, 0.12, 0.8, 0.8)) # rect = l,b,w,h
#
#     m = Basemap(llcrnrlon=lon_min, )
# #
#
#
#
# if __name__ == '__main__':
#     # plot_china_everyday()
# #
#





# #-----Pyecharts画地图
#
# from pyecharts.charts import *
# from pyecharts import options
#
# # 创建World_Map
# World_Map = Map()
# # 添加数据  name_map把世界地图国家名称中英文对照起来
# World_Map.add("新冠肺炎全球累计确诊数", world_confirm_list, maptype="world",
#  name_map={'Singapore Rep.':'新加坡',
#             'Dominican Rep.':'多米尼加',
#             'Palestine':'巴勒斯坦',
#             'Bahamas':'巴哈马',
#             'Timor-Leste':'东帝汶',
#            'Afghanistan':'阿富汗',
#            'Guinea-Bissau':'几内亚比绍',
#            "Côte d'Ivoire":'科特迪瓦',
#            'Siachen Glacier':'锡亚琴冰川',
#            "Br. Indian Ocean Ter.":'英属印度洋领土',
#            'Angola':'安哥拉',
#            'Albania':'阿尔巴尼亚',
#            'United Arab Emirates':'阿联酋',
#            'Argentina':'阿根廷',
#            'Armenia':'亚美尼亚',
#            'French Southern and Antarctic Lands':'法属南半球和南极领地',
#            'Australia':'澳大利亚',
#            'Austria':'奥地利',
#            'Azerbaijan':'阿塞拜疆',
#            'Burundi':'布隆迪',
#            'Belgium':'比利时',
#            'Benin':'贝宁',
#            'Burkina Faso':'布基纳法索',
#            'Bangladesh':'孟加拉国',
#            'Bulgaria':'保加利亚',
#            'The Bahamas':'巴哈马',
#            'Bosnia and Herz.':'波斯尼亚和黑塞哥维那',
#            'Belarus':'白俄罗斯',
#            'Belize':'伯利兹',
#            'Bermuda':'百慕大',
#            'Bolivia':'玻利维亚',
#            'Brazil':'巴西',
#            'Brunei':'文莱',
#            'Bhutan':'不丹',
#            'Botswana':'博茨瓦纳',
#            'Central African Rep.':'中非',
#            'Canada':'加拿大',
#            'Switzerland':'瑞士',
#            'Chile':'智利',
#            'China':'中国',
#            'Ivory Coast':'象牙海岸',
#            'Cameroon':'喀麦隆',
#            'Dem. Rep. Congo':'刚果民主共和国',
#            'Congo':'刚果',
#            'Colombia':'哥伦比亚',
#            'Costa Rica':'哥斯达黎加',
#            'Cuba':'古巴',
#            'N. Cyprus':'北塞浦路斯',
#            'Cyprus':'塞浦路斯',
#            'Czech Rep.':'捷克',
#            'Germany':'德国',
#            'Djibouti':'吉布提',
#            'Denmark':'丹麦',
#            'Algeria':'阿尔及利亚',
#            'Ecuador':'厄瓜多尔',
#            'Egypt':'埃及',
#            'Eritrea':'厄立特里亚',
#            'Spain':'西班牙',
#            'Estonia':'爱沙尼亚',
#            'Ethiopia':'埃塞俄比亚',
#            'Finland':'芬兰',
#            'Fiji':'斐',
#            'Falkland Islands':'福克兰群岛',
#            'France':'法国',
#            'Gabon':'加蓬',
#            'United Kingdom':'英国',
#            'Georgia':'格鲁吉亚',
#            'Ghana':'加纳',
#            'Guinea':'几内亚',
#            'Gambia':'冈比亚',
#            'Guinea Bissau':'几内亚比绍',
#            'Eq. Guinea':'赤道几内亚',
#            'Greece':'希腊',
#            'Greenland':'格陵兰',
#            'Guatemala':'危地马拉',
#            'French Guiana':'法属圭亚那',
#            'Guyana':'圭亚那',
#            'Honduras':'洪都拉斯',
#            'Croatia':'克罗地亚',
#            'Haiti':'海地',
#            'Hungary':'匈牙利',
#            'Indonesia':'印度尼西亚',
#            'India':'印度',
#            'Ireland':'爱尔兰',
#            'Iran':'伊朗',
#            'Iraq':'伊拉克',
#            'Iceland':'冰岛',
#            'Israel':'以色列',
#            'Italy':'意大利',
#            'Jamaica':'牙买加',
#            'Jordan':'约旦',
#            'Japan':'日本',
#            'Kazakhstan':'哈萨克斯坦',
#            'Kenya':'肯尼亚',
#            'Kyrgyzstan':'吉尔吉斯斯坦',
#            'Cambodia':'柬埔寨',
#            'Korea':'韩国',
#            'Kosovo':'科索沃',
#            'Kuwait':'科威特',
#            'Lao PDR':'老挝',
#            'Lebanon':'黎巴嫩',
#            'Liberia':'利比里亚',
#            'Libya':'利比亚',
#            'Sri Lanka':'斯里兰卡',
#            'Lesotho':'莱索托',
#            'Lithuania':'立陶宛',
#            'Luxembourg':'卢森堡',
#            'Latvia':'拉脱维亚',
#            'Morocco':'摩洛哥',
#            'Moldova':'摩尔多瓦',
#            'Madagascar':'马达加斯加',
#            'Mexico':'墨西哥',
#            'Macedonia':'马其顿',
#            'Mali':'马里',
#            'Myanmar':'缅甸',
#            'Montenegro':'黑山',
#            'Mongolia':'蒙古',
#            'Mozambique':'莫桑比克',
#            'Mauritania':'毛里塔尼亚',
#            'Malawi':'马拉维',
#            'Malaysia':'马来西亚',
#            'Namibia':'纳米比亚',
#            'New Caledonia':'新喀里多尼亚',
#            'Niger':'尼日尔',
#            'Nigeria':'尼日利亚',
#            'Nicaragua':'尼加拉瓜',
#            'Netherlands':'荷兰',
#            'Norway':'挪威',
#            'Nepal':'尼泊尔',
#            'New Zealand':'新西兰',
#            'Oman':'阿曼',
#            'Pakistan':'巴基斯坦',
#            'Panama':'巴拿马',
#            'Peru':'秘鲁',
#            'Philippines':'菲律宾',
#            'Papua New Guinea':'巴布亚新几内亚',
#            'Poland':'波兰',
#            'Puerto Rico':'波多黎各',
#            'Dem. Rep. Korea':'朝鲜',
#            'Portugal':'葡萄牙',
#            'Paraguay':'巴拉圭',
#            'Qatar':'卡塔尔',
#            'Romania':'罗马尼亚',
#            'Russia':'俄罗斯',
#            'Rwanda':'卢旺达',
#            'W. Sahara':'西撒哈拉',
#            'Saudi Arabia':'沙特阿拉伯',
#            'Sudan':'苏丹',
#            'S. Sudan':'南苏丹',
#            'Senegal':'塞内加尔',
#            'Solomon Is.':'所罗门群岛',
#            'Sierra Leone':'塞拉利昂',
#            'El Salvador':'萨尔瓦多',
#            'Somaliland':'索马里兰',
#            'Somalia':'索马里',
#            'Serbia':'塞尔维亚',
#            'Suriname':'苏里南',
#            'Slovakia':'斯洛伐克',
#            'Slovenia':'斯洛文尼亚',
#            'Sweden':'瑞典',
#            'Swaziland':'斯威士兰',
#            'Syria':'叙利亚',
#            'Chad':'乍得',
#            'Togo':'多哥',
#            'Thailand':'泰国',
#            'Tajikistan':'塔吉克斯坦',
#            'Turkmenistan':'土库曼斯坦',
#            'East Timor':'东帝汶',
#            'Trinidad and Tobago':'特里尼达和多巴哥',
#            'Tunisia':'突尼斯',
#            'Turkey':'土耳其',
#            'Tanzania':'坦桑尼亚',
#            'Uganda':'乌干达',
#            'Ukraine':'乌克兰',
#            'Uruguay':'乌拉圭',
#            'United States':'美国',
#            'Uzbekistan':'乌兹别克斯坦',
#            'Venezuela':'委内瑞拉',
#            'Vietnam':'越南',
#            'Vanuatu':'瓦努阿图',
#            'West Bank':'西岸',
#            'Yemen':'也门',
#            'South Africa':'南非',
#            'Zambia':'赞比亚',
#            'Zimbabwe':'津巴布韦'})
# # 不显示地图各国标签
# World_Map.set_series_opts(label_opts=options.LabelOpts(is_show=False),)
# # 设置数据与颜色的一个映射
# World_Map.set_global_opts(visualmap_opts=options.VisualMapOpts(max_=60000, is_piecewise=True, pieces=[
#     {"min":1, "max":19, "color":"#ffefd7"},
#     {"min":20, "max":99, "color":"#ffd2a0"},
#     {"min":100, "max":199, "color":"#fe8664"},
#     {"min":200, "max":279, "color":"#e64b47"},
#     {"min":280, "max":999, "color":"#c91014"},
#     {"min":1000, "max":9999, "color":"#9c0a0d"},
#     {"min":10000, "max":99999, "color": "red"}
# ]))
# # 显示或者渲染地图
# World_Map.render()















