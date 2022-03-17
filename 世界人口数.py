import requests
from bs4 import BeautifulSoup
import re
import json

# url = "https://www.kylc.com/stats/global/yearly_overview/g_population_total.html"
# res = requests.get(url)
# html = res.text
# soup = BeautifulSoup(html, features="html.parser")
# table = soup.find('tbody')
# print(table.text)
#
# # 用正则来匹配出各国人口数
# pattern = "2018.*?(\d+)亿"   # .*?，加上？为非贪心匹配
# result = re.findall(pattern, table.text, flags=0)
# print(result)




url1 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_other'
res1 = requests.get(url1)
html1 = res1.text
text1 = json.loads(html1)
content1 = json.loads(text1['data'])
# # print(text1)
# print(content1.keys())
# print(content1['dailyHistory'])
# print()
# # # {'date': '01.20', 'hubei': {'dead': 6, 'heal': 25, 'nowConfirm': 239, 'deadRate': '2.22', 'healRate': '9.26'}, 'notHubei': {'dead': 0, 'heal': 0, 'nowConfirm': 52, 'deadRate': '0.00', 'healRate': '0.00'}, 'country': {'dead': 6, 'heal': 25, 'nowConfirm': 291, 'deadRate': '2.06', 'healRate': '8.59'}}
# # print()
# # print(content1['provinceCompare'])
# # # {'上海': {'nowConfirm': 3, 'confirmAdd': 3, 'dead': 0, 'heal': 0}, '云南': {'nowConfirm': -2, 'confirmAdd': 0, 'dead': 0, 'heal': 2}
# # print()
# # print(content1['foreignList'])
# # print()
# # # {'name': '意大利', 'date': '03.15', 'isUpdated': True, 'confirmAdd': 3497, 'confirmAddCut': 0, 'confirm': 21157, 'suspect': 0, 'dead': 1441, 'heal': 1966, 'nowConfirm': 17750, 'confirmCompare': 3497, 'nowConfirmCompare': 2795, 'healCompare': 527, 'deadCompare': 175, 'children': [{'name': '伦巴第', 'date': '03.15', 'nameMap': 'Lombardy', 'isUpdated': True, 'confirmAdd': 1865, 'confirmAddCut': 0, 'confirm': 11685, 'suspect': 0, 'dead': 966, 'heal': 1660},
# print(content1['globalStatis'])
# print()
# # # {'nowConfirm': 63509, 'confirm': 75131, 'heal': 9003, 'dead': 2619, 'nowConfirmAdd': 6831, 'confirmAdd': 9060, 'healAdd': 1866, 'deadAdd': 363}
# # print()
# print(content1['globalDailyHistory'])
# print()
# {'date': '01.28', 'all': {'confirm': 57, 'dead': 0, 'heal': 3, 'newAddConfirm': 19, 'deadRate': '0.00', 'healRate': '5.26'}}
# print()
print(content1['chinaDayList'])
print()
print(content1['chinaDayAddList'])

#
url2 = 'https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'
header = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'}
res2 = requests.get(url2, headers=header)
html2 = res2.text
text2 = json.loads(html2)
content2 = json.loads(text2['data'])
print(content2.keys())

print(content2['lastUpdateTime'])
print(content2['chinaTotal'])
print(content2['areaTree'])


