import time
import json
import requests
import xlsxwriter


# ----------请求数据
def ask_for_data_all1():
    # 为了获得chinaDayList中国每天累计数据(拿到日期1.13开始、每天的确诊人数、疑似人数、死亡人数、治愈人数），做成横轴为日期的四条折线图
    # chinaDayAddList中国每天更新数据（拿到日期1.20开始，每天的确诊人数、疑似人数、死亡人数、治愈人数）做成横轴为日期的四条折线图，找各种拐点
    url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
    header = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    res1 = requests.get(url1, headers=header)  # 访问url并获得响应
    context1 = res1.text  # 获取响应内容
    text = json.loads(context1)  # 第一次解析json格式
    data1 = text['data']
    data_all1 = json.loads(data1)  # 再次解析json格式
    return data_all1


def ask_for_data_all2():
    url2 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'  # areaTree各国、各省、各市数据做（世界地图、中国地图、湖北省地图）
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
    res2 = requests.get(url2, headers=header)
    context2 = res2.text
    text2 = json.loads(context2)
    data2 = text2['data']
    data_all2 = json.loads(data2)
    return data_all2


def ask_for_data_foreign():
    url = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_foreign'
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36"}
    res = requests.get(url, headers=header)
    d = json.loads(res.text)
    data_foreign = json.loads(d['data'])
    return data_foreign

# ----------筛选、加工数据
# 1、加工chinaDayList。日期：01.13--》2020.01.13
# 2、加工chinaDayAddList。日期：01.20---》2020.01.20
# 3、整理foreignList数据，各个国家的疫情数据
# 4、整理areaTree数据，整理好中国的各省以及下面各市的数据树


def polise_chinaDayList_data(data_all1):  # 利用ask_for_data_all1（）传参
    # 1、chinaDayList
    date_list = []  # 时间列表
    confirm_list = []  # 确诊列表
    suspect_list = []  # 疑似列表
    dead_list = []  # 死亡列表
    heal_list = []  # 治愈列表
    num = 0

    history = {}  # 历史数据
    # history = {'2020-1-20':{'confirm':41, 'suspect':0, 'dead':1, 'heal':0}}
    # history['2020-1-20'] = {'confirm':41, 'suspect':0, 'dead':1, 'heal':0}
    for i in data_all1['chinaDayList']:
        date = '2020.' + i['date']
        tup = time.strptime(date, '%Y.%m.%d')
        date = time.strftime('%Y-%m-%d', tup)  # 如果要插入数据库，就要改变时间格式，不然插入数据库时会报错，数据库是datetime格式
        confirm = i['confirm']
        suspect = i['suspect']
        dead = i['dead']
        heal = i['heal']

        history[date] = {'confirm': confirm, 'suspect': suspect, 'dead': dead, 'heal': heal}

        # 以下存储为列表主要是要做折线图
        num += 1
        if num % 2 == 0:  # 隔天统计，不然数据量太大
            date_list.append(i['date'])  # 将没处理的时间先装入一个列表
            confirm_list.append(confirm)  # 将每日的确诊人数先装入一个列表
            suspect_list.append(suspect)  # 将每日的疑似人数先装入列表
            dead_list.append(dead)  # 将每日的死亡人数先装入列表
            heal_list.append(heal)  # 将每日的治愈人数先装入列表

    # 返回多个参数，到时候用元组的方式去接这些返回值
    # （history, date_list, confirm_list, suspect_list, dead_list, heal_list） = polise_chinaDayList_data(data_all1)
    return history, date_list, confirm_list, suspect_list, dead_list, heal_list


# 2、chinaDayAddList
# history = {'2020-1-20':{'confirm':41, 'suspect':0, 'dead':1, 'heal':0,
#                           'confirm_add':3, 'suspect_add':4, 'dead_add':0, 'heal_add':2}}
def polise_chinaDayAddList_data(data_all1, history):  # data_all1利用ask_for_data_all1（）传参，history利用polise_chinaDayList_data(data_all1)的返回值拿到
    date_add_list = []
    confirm_add_list = []
    dead_add_list = []
    heal_add_list = []
    for i in data_all1['chinaDayAddList']:
        date = '2020.' + i['date']
        tup = time.strptime(date, '%Y.%m.%d')
        date = time.strftime('%Y-%m-%d', tup)
        confirm_add = i['confirm']
        suspect_add = i['suspect']
        dead_add = i['dead']
        heal_add = i['heal']

        history[date].update({'confirm_add': confirm_add, 'suspect_add': suspect_add,
                              'dead_add': dead_add, 'heal_add': heal_add})
        # Python 字典 update() 方法用于更新字典中的键值对可以修改存在的键值对应的值，也可以添加新的键值对到字典中

        date_add_list.append(i['date'])  # 装入时间列表，为后面作图用
        confirm_add_list.append(confirm_add)  # 装入每天新增确诊人数列表，为后面作图用
        dead_add_list.append(dead_add)
        heal_add_list.append(heal_add)

    return history, date_add_list, confirm_add_list, dead_add_list, heal_add_list


# 3、foreignList
def world_data(data_foreign, data_all2):  # 利用 ask_for_data_all2()传参
    # 1）世界地区图，各个国家
    # world = {'中国'：{'country_date': 03.28, 'country_confirmAdd':222, 'country_totalconfirm':12222,
    #                                'country_nowConfirm':2221, 'country_dead':12, 'country_heal':33, 'isUpdated': True}}
    world = {}
    world_confirm = {}  # 只拿到世界各国累计确诊人数，为后面做世界地图需要
    for i in data_foreign['foreignList']:
        country_name = i['name']
        country_date = i['date']
        country_confirmAdd = i['confirmAdd']  # 今日新增确诊
        country_totalconfirm = i['confirm']  # 累计有多少确诊过
        country_nowConfirm = i['nowConfirm']  # 目前仍有多少确诊
        country_dead = i['dead']
        country_heal = i['heal']
        isUpdated = i['isUpdated']
        world[country_name] = {'country_date': country_date, 'country_confirmAdd':country_confirmAdd, 'country_totalconfirm':country_totalconfirm,
                               'country_nowConfirm':country_nowConfirm, 'country_dead':country_dead, 'country_heal':country_heal, 'isUpdated': isUpdated}

        world_confirm[country_name] = country_totalconfirm

    #  以上数据中没有中国的数据，所以要单独加进去,从data_all2中的chinaTotal
    country_date = '0' + data_all2['lastUpdateTime'][6] + '.' + data_all2['lastUpdateTime'][8] \
                                                + data_all2['lastUpdateTime'][9] # date是2020/3/15 14:47，所以要转一下
    country_totalconfirm = data_all2['chinaTotal']['confirm']
    country_nowConfirm = data_all2['chinaTotal']['nowConfirm']
    country_dead = data_all2['chinaTotal']['dead']
    country_heal = data_all2['chinaTotal']['heal']
    # 今日新增确诊要去areaTree中找
    country_confirmAdd = data_all2['areaTree'][0]['today']['confirm']
    isUpdated = data_all2['areaTree'][0]['today']['isUpdated']

    world['中国'] = {'country_date': country_date, 'country_confirmAdd':country_confirmAdd, 'country_totalconfirm':country_totalconfirm,
                               'country_nowConfirm':country_nowConfirm, 'country_dead':country_dead, 'country_heal':country_heal, 'isUpdated': isUpdated}

    world_confirm['中国'] = country_totalconfirm
    # 把字典转成元组对的列表，为之后做世界地图需要
    world_confirm_list = list(world_confirm.items())

    return world, world_confirm, world_confirm_list


# areaTree：name      #areaTree[0],中国数据
#           today
#           total
#           children: name   #省级数据，列表
#                     today
#                     total
#                     children: name  #市级数据，列表
#                               today
# #                               total

def china_data(data_all2):
    # 2）中国行政地区图，省、市每天更新的数据
    china = {}  # china = {'湖北': {'pro_total_confirm’：20222, 'pro_total_dead': 222, 'pro_deadRate':4.86 ,'children':[{'city_name':'武汉' ,'city_total_confirm':1222,'city_total_dead':222, 'city_deadRate':1.2}]}
    china_pro_total_confirm = {}
    for i in data_all2['areaTree'][0]['children']:  # 拿到中国各省的数据
        pro_name = i['name']
        pro_total_confirm = i['total']['confirm']  # 各省累计确诊人数
        pro_total_dead = i['total']['dead']
        pro_deadRate = i['total']['deadRate']

        pro_children = []  # 每次都要拿一个空列表来装每个省份的 地级市信息
        for j in i['children']:
            city_name = j['name']
            city_total_confirm = j['total']['confirm']
            city_total_dead = j['total']['dead']
            city_deadRate = j['total']['deadRate']
            new_pro_children = {'city_name': city_name, 'city_total_confirm': city_total_confirm,
                                'city_total_dead': city_total_dead, 'city_deadRate': city_deadRate}

            pro_children.append(new_pro_children)  # 这个省份的一个地级市信息，添加入列表

        china[pro_name] = {'pro_total_confirm': pro_total_confirm,'pro_total_dead': pro_total_dead,
                           'pro_deadRate': pro_deadRate, 'pro_children': pro_children}

        china_pro_total_confirm[pro_name] = pro_total_confirm  # 为了拿到中国每个省的每天确诊人数，为之后做地图用

    china_pro_total_confirm_list = list(china_pro_total_confirm.items())  # 将字典转成元组对的列表，为作图用

    return china, china_pro_total_confirm, china_pro_total_confirm_list


# ----------存储数据到Excel,   history、world、china
# history = {'2020-1-20':{'confirm':41, 'suspect':0, 'dead':1, 'heal':0, 'confirm_add':3,
#                                          'suspect_add':4, 'dead_add':0, 'heal_add':2}}
# world = {'中国'：{'confirm':10000, 'suspect': 1002, 'dead': 2333, 'heal': 787,
#                                          'confirm_add': 122, 'isUpdated': True}}
# china = {'湖北': {'Total_confirm’：20222, 'Total_isUpdated': True,
#          'children':[{'city_name':'武汉' ,'city_confirm':1222,'city_isUpdated':True},
#                       {'city_name':‘孝感’，‘city_confirm':222,'city_isUpdated':True}]}

def save_data_to_excel(history, world, china):

    # 打开工作簿，创建工作表
    workbook = xlsxwriter.Workbook('2020疫情实时数据new.xlsx')
    worksheet1 = workbook.add_worksheet('中国历史疫情数据')
    worksheet2 = workbook.add_worksheet('世界爆发疫情数据')
    worksheet3 = workbook.add_worksheet('中国地区疫情数据')


    # ----worksheet1

    #set_column(first_col, last_col, width, cell_format, options)方法，用于设置一列或多列单元格的属性
    # first_col：整型，指定开始列位置，起始下标为0；
    # last_col：整型，指定结束列位置，起始下标为0；
    # width：float类型，设置列宽；
    # cell_format：format类型，指定格式对象；
    # options：dict类型，设置hidden（隐藏）、level（组合分级）、collpsed（折叠）；
    worksheet1.set_column(0, 8, 17)

    # 第0行设置各列名称
    worksheet1.write(0, 0, '日期')
    worksheet1.write(0, 1, '累计确诊人数')
    worksheet1.write(0, 2, '累计疑似人数')
    worksheet1.write(0, 3, '累计死亡人数')
    worksheet1.write(0, 4, '累计治愈人数')
    worksheet1.write(0, 5, '今日新增确诊人数')
    worksheet1.write(0, 6, '今日新增疑似人数')
    worksheet1.write(0, 7, '今日新增死亡人数')
    worksheet1.write(0, 8, '今日新增治愈人数')

    count = 1  # 控制现在写入的是第几行

    for key in history.keys():
        date = key
        confirm = history[key]['confirm']
        suspect = history[key]['suspect']
        dead = history[key]['dead']
        heal = history[key]['heal']
        if len(history[key].keys()) > 5:
            confirm_add = history[key]['confirm_add']
            suspect_add = history[key]['suspect_add']
            dead_add = history[key]['dead_add']
            heal_add = history[key]['heal_add']

        # 边从history字典中取数据，边写入EXCEL
        # worksheet.write(行，列，数据）

        worksheet1.write(count, 0, date)
        worksheet1.write(count, 1, confirm)
        worksheet1.write(count, 2, suspect)
        worksheet1.write(count, 3, dead)
        worksheet1.write(count, 4, heal)
        if len(history[key].keys()) > 5:
            worksheet1.write(count, 5, confirm_add)
            worksheet1.write(count, 6, suspect_add)
            worksheet1.write(count, 7, dead_add)
            worksheet1.write(count, 8, heal_add)

        count += 1  # 此处写入行数累加，换下一行

    # world = {'中国'：{'country_date': 03.28, 'country_confirmAdd':222, 'country_totalconfirm':12222,
    #                                'country_nowConfirm':2221, 'country_dead':12, 'country_heal':33, 'isUpdated': True}}
    # ---worksheet2

    # set_column(first_col, last_col, width, cell_format, options)方法，用于设置一列或多列单元格的属性
    # first_col：整型，指定开始列位置，起始下标为0；
    # last_col：整型，指定结束列位置，起始下标为0；
    # width：float类型，设置列宽；
    # cell_format：format类型，指定格式对象；
    # options：dict类型，设置hidden（隐藏）、level（组合分级）、collpsed（折叠）；
    worksheet2.set_column(0, 7, 17)

    # 第0行设置各列名称
    worksheet2.write(0, 0, '国家')
    worksheet2.write(0, 1, '时间')
    worksheet2.write(0, 2, '今日新增确诊人数')
    worksheet2.write(0, 3, '累计确诊人数')
    worksheet2.write(0, 4, '现有确诊人数')
    worksheet2.write(0, 5, '累计死亡人数')
    worksheet2.write(0, 6, '累计治愈人数')
    worksheet2.write(0, 7, '今日确诊人数是否新增')

    count = 1  # 控制现在写入的是第几行

    for key in world.keys():

        country_name = key
        country_date = world[key]['country_date']
        country_confirmAdd = world[key]['country_confirmAdd']
        country_totalconfirm = world[key]['country_totalconfirm']
        country_nowConfirm = world[key]['country_nowConfirm']
        country_dead = world[key]['country_dead']
        country_heal = world[key]['country_heal']
        isUpdated = world[key]['isUpdated']


        # 边从history字典中取数据，边写入EXCEL
        # worksheet.write(行，列，数据）

        worksheet2.write(count, 0, country_name)
        worksheet2.write(count, 1, country_date)
        worksheet2.write(count, 2, country_confirmAdd)
        worksheet2.write(count, 3, country_totalconfirm)
        worksheet2.write(count, 4, country_nowConfirm)
        worksheet2.write(count, 5, country_dead)
        worksheet2.write(count, 6, country_heal)
        worksheet2.write(count, 7, isUpdated)


        count += 1  # 此处写入行数累加，换下一行

    # china = {'湖北': {'pro_total_confirm’：20222, 'pro_total_dead': 222, 'pro_deadRate':4.86 ,
    #                   'children':[{'city_name':'武汉' ,'city_total_confirm':1222,'city_total_dead':222, 'city_deadRate':1.2}]}
    # ---worksheet3

    worksheet3.set_column(0, 4, 17)

    # 第0行设置各列名称
    worksheet3.write(0, 0, '省份')
    worksheet3.write(0, 1, '地级市')
    worksheet3.write(0, 2, '累计确诊人数')
    worksheet3.write(0, 3, '累计死亡人数')
    worksheet3.write(0, 4, '死亡率')

    count = 1  # 控制现在写入的是第几行

    for key in china.keys():  # 各省份数据

        pro_name = key
        pro_total_confirm = china[key]['pro_total_confirm']
        pro_total_dead = china[key]['pro_total_dead']
        pro_deadRate = china[key]['pro_deadRate']

        # 边从history字典中取数据，边写入EXCEL
        # worksheet.write(行，列，数据）

        worksheet3.write(count, 0, pro_name)
        worksheet3.write(count, 2, pro_total_confirm)
        worksheet3.write(count, 3, pro_total_dead)
        worksheet3.write(count, 4, pro_deadRate)

        count += 1  # 此处写入行数累加，换下一行，将城市数据存储在下一行

        for city in china[key]['pro_children']:  # 各省下面的地级市
            city_name = city['city_name']
            city_total_confirm = city['city_total_confirm']
            city_total_dead = city['city_total_dead']
            city_deadRate = city['city_deadRate']

            worksheet3.write(count, 1, city_name)
            worksheet3.write(count, 2, city_total_confirm)
            worksheet3.write(count, 3, city_total_dead)
            worksheet3.write(count, 4, city_deadRate)

            count += 1  # 此处写入行数累加，换下一行

    workbook.close()



# ----------数据可视化1matplotlab（主要是做折线图、饼图）
# 1）全国每天累计治愈死亡走势折线图。数据：时间、china的dead、china的heal


import matplotlib.pyplot as plt


plt.rcParams['font.sans-serif'] = ['FangSong']  # 设置默认字体
plt.rcParams['axes.unicode_minus'] = 'False'  # 解决保存图像时，’-‘显示为方块的问题

# figure(num=None, figsize=None, dpi=None, facecolor=None, edgecolor=None, frameon=True)
# 如果num的值是字符串，则将窗口标题设置为此字符串。
# figsize:指定figure的宽和高，单位为英寸。facecolor:背景颜色
def plot_china_dead_heal_everyday(date_list, heal_list, dead_list):
    plt.figure('2020疫情中国每日治愈与死亡走势', facecolor='#f4f4f4', figsize=(100, 50))
    plt.title('全国治愈与死亡走势', fontsize=25)

    plt.plot(date_list, heal_list, label='治愈')
    plt.plot(date_list, dead_list, label='死亡')

    plt.tick_params(labelsize=8)  # 设置坐标刻度值的大小以及刻度值的字体
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.gcf().autofmt_xdate()  # 自动适应刻度线密度，包括x轴，y轴
    plt.show()


def plot_china_confirm_add_everyday(date_add_list, confirm_add_list):
    plt.figure('2020疫情中国每日确诊增加走势', facecolor='#f4f4f4', figsize=(100, 50))
    plt.title('全国每日确诊走势', fontsize=25)

    plt.plot(date_add_list, confirm_add_list, 'c*-', label='新增确诊')

    plt.tick_params(labelsize=8)  # 设置坐标刻度值的大小以及刻度值的字体
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.gcf().autofmt_xdate()  # 自动适应刻度线密度，包括x轴，y轴
    plt.show()


def plot_china_confirm_dead_heal_compare_everyday(date_add_list, confirm_add_list, heal_add_list, dead_add_list):
    fig, ax1 = plt.subplots(facecolor='#f4f4f4', figsize=(100, 50))  # 使用subplots（）创建窗口
    # 同一个x轴，左右两个y轴
    ax1.plot(date_add_list, confirm_add_list, 'c*-', label='新增确诊')  # 绘制折线图1
    ax2 = ax1.twinx()  # 两个纵坐标，做镜像处理
    ax2.bar(date_add_list, heal_add_list, label='新增治愈')
    ax2.bar(date_add_list, dead_add_list, label='新增死亡')

    ax1.set_xlabel('日期')  # 设置x轴标题
    ax1.set_ylabel('治愈/死亡人数新增', color='b')  # 设置Y1轴标题
    ax2.set_ylabel('确诊人数新增', color='g')  # 设置Y2轴标题

    ax1.tick_params(labelsize=8)

    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.gcf().autofmt_xdate()  # 自动适应刻度线密度，包括x轴，y轴
    plt.title('全国每日确诊/治愈/死亡对比', fontsize=25)
    plt.show()


def plot_china_everyday(date_list, confirm_list, suspect_list, dead_list, heal_list):
    # 根据日期，绘制中国每日确诊、疑似、死亡、治愈数据
    plt.figure('2020疫情中国每日疫情统计图表', facecolor='#f4f4f4', figsize=(100, 50))
    plt.title('2020疫情中国每日疫情曲线', fontsize=20)

    plt.plot(date_list, confirm_list, label='确诊')
    plt.plot(date_list, suspect_list, label='疑似')
    plt.plot(date_list, dead_list, label='死亡')
    plt.plot(date_list, heal_list, label='治愈')
    plt.grid(linestyle=':')  # 显示网格
    plt.legend(loc='best')  # 显示图例
    plt.gcf().autofmt_xdate()  # 自动适应刻度线密度，包括x轴，y轴
    plt.show()


# ----------数据可视化2Pyecharts（主要用来做地图）
# 1)世界地图

from pyecharts.charts import *
from pyecharts import options


def pye_world_map(world_confirm_list):
    # 创建World_Map
    World_Map = Map()
    # 添加数据  name_map把世界地图国家名称中英文对照起来
    World_Map.add("新冠肺炎全球累计确诊数", world_confirm_list, maptype="world",
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
    World_Map.set_global_opts(visualmap_opts=options.VisualMapOpts(is_piecewise=True,
     pieces=[
        {"min": 1, "max": 19, "color": "#FFFFCC"},
        {"min": 20, "max": 99, "color": "#FFCC66"},
        {"min": 100, "max": 199, "color": "#FFCC00"},
        {"min": 200, "max": 799, "color": "#FF9900"},
        {"min": 800, "max": 4999, "color": "#CC6600"},
        {"min": 5000, "max": 15999, "color": "#CC3300"},
        {"min": 16000,"max": 59999, "color": "#993300"},
        {"min": 60000, "max": 89999, "color": "#990033"},
        {"min": 89999, "max": 199999, "color": "#660000"}
    ]))
    # 显示或者渲染地图
    World_Map.render('world_new_map.html')


# 2）中国行政区地图
def pye_china_map(pro_list):

    china_Map = Map()
    # 添加数据
    china_Map.add("新冠肺炎中国累计确诊数", pro_list, maptype="china",)
    # 显示各省标签
    china_Map.set_series_opts(label_opts=options.LabelOpts(is_show=True), )
    # 设置数据与颜色的一个映射
    china_Map.set_global_opts(visualmap_opts=options.VisualMapOpts(max_=100000, is_piecewise=True,
      pieces=[
        {"min": 1, "max": 19, "color": "#ffefd7"},
        {"min": 20, "max": 99, "color": "#ffd2a0"},
        {"min": 100, "max": 199, "color": "#fe8664"},
        {"min": 200, "max": 279, "color": "#e64b47"},
        {"min": 280, "max": 999, "color": "#c91014"},
        {"min": 1000, "max": 9999, "color": "#9c0a0d"},
        {"min": 10000, "max": 99999, "color": "red"}
    ]))
    # 显示或者渲染地图
    china_Map.render('china_map.html')


if __name__ == '__main__':  # 可自行调控哪几个函数运行
# ----------请求数据
    data_all1 = ask_for_data_all1()
    # data_all2 = ask_for_data_all2()
    # data_foreign = ask_for_data_foreign()
#
# ----------筛选、加工数据
#     # 1、加工chinaDayList。
    (history, date_list, confirm_list, suspect_list, dead_list, heal_list) = polise_chinaDayList_data(data_all1)

#     # 2、加工chinaDayAddList。
    (history, date_add_list, confirm_add_list, dead_add_list, heal_add_list) = polise_chinaDayAddList_data(data_all1, history)

    # 3、整理areaTree数据。1）各个国家的总体四个数据图
    # (world, world_confirm, world_confirm_list) = world_data(data_foreign, data_all2)

    # 2）整理好中国的各省以及下面各市的数据树
    # (china, china_pro_total_confirm, china_pro_total_confirm_list) = china_data(data_all2)

# ----------数据存储到EXCEL
#     save_data_to_excel(history, world, china)

# ----------数据可视化1matplotlab
#     plot_china_dead_heal_everyday(date_list, heal_list, dead_list)  # 中国肺炎死亡/治愈对比图
#     plot_china_confirm_add_everyday(date_add_list, confirm_add_list)  # 中国每日新增确诊图
#     plot_china_confirm_dead_heal_compare_everyday(date_add_list, confirm_add_list, heal_add_list, dead_add_list)  # 中国每日新增确诊/死亡/治愈人数对比图
    plot_china_everyday(date_list, confirm_list, suspect_list, dead_list, heal_list)  # 中国每日确诊/疑似/死亡/治愈折线图

    # ----------数据可视化2Pyecharts
    # pye_world_map(world_confirm_list)   # 世界累计确诊疫情图（地图）
    # pye_china_map(china_pro_total_confirm_list)   # 中国各省累计确诊疫情图（地图）



