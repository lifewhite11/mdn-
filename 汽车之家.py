# coding = utf-8
# @Version : 1.1
# @Author : zwj
# @File : 汽车之家.py
# @Time : 2024-6-6 16:35
import os.path
import time

import pandas as pd
from selenium.common import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
import requests
import parsel
import csv
import json
import re
from bs4 import BeautifulSoup
from _cffi_backend import string
from selenium import webdriver
import chardet
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

'''
定义表头
id表示每辆车的唯一编号
brand_id表示每个品牌对应的编号
group_id表示每一个厂商对应的编号
series_id表示每一个车系对应的编号
full_name表示车的名字
brand_name表示品牌的名字
group_name表示厂商的名字
series_name表示车系的名字
price表示车的价格
year表示车的年份
displacement表示排量
month表示上市月份
oil表示百公里油耗
max_power表示最大功率
max_speed表示最高车速
max_load表示最大满载
max_horsepower表示最大马力
'''



#获取已经爬取到的车款的数量


headers = ["id", "brand_id",
           "group_id", "series_id",
           "full_name",
           "brand_name", "group_name",
           "series_name", "price", "year",
           "displacement", "month", "oil", "max_power", "max_speed", "max_load", "max_horsepower"]

brand_name = ""
group_name = ""
series_name = ""
brand_dict = {}  # 创建一个空字典，存储品牌名称和品牌id的映射关系。
group_dict = {}  # 创建一个空字典，存储厂商名称和厂商id的映射关系。
series_dict = {}  # 创建一个空字典，存储车系名称和车系id的映射关系。

driver = webdriver.Chrome()
#获取每个品牌或厂商或车系对应的id，如果不存在就加上

#获取已经爬取的存在csv文件中name与id的映射关系，并存储到字典里
def get_dict(brand_dict,group_dict,series_dict):
    with open ("汽车之家.csv",mode='r',encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile,fieldnames=headers)
        #跳过第一行
        next(csvreader)
        # 将所有行读入列表中
        rows = list(csvreader)
        for row in rows:
            for header in ["brand","group","series"]:
                id_field = f"{header}_id"
                name_field = f"{header}_name"
                if id_field in row and name_field in row:
                    match header:
                        case "brand":
                            brand_dict[row[name_field]] = row[id_field]
                        case "group":
                            group_dict[row[name_field]] = row[id_field]
                        case "series":
                            series_dict[row[name_field]] = row[id_field]
    print (brand_dict)


def get_id(name, dict):
    if name in dict:
        return dict[name]
    else:
        id = len(dict)+1
        dict[name] = id
        return id

#获取每款车系所在主页的链接
def get_car_home_links():
    url = "https://www.autohome.com.cn/price/fueltypedetail_1"
    driver.get(url)

    # 执行JavaScript来模拟滚动
    i = 300

    while i > 0:
        driver.execute_script("window.scrollTo(0, window.scrollY + 300);")
        i -= 1

    time.sleep(1)
    html_data = driver.page_source
    select = parsel.Selector(text=html_data)

    # 获取所有的li标签，li标签里包含每款车的链接
    lis = select.xpath(
        '//ul [@class = "tw-grid tw-h-full tw-grid-cols-4 tw-gap-4 tw-pb-8 max-lg:tw-gap-2 xl:tw-grid-cols-5 2xl:tw-grid-cols-6"]/li')

    car_home_links=[]

    for li in lis[len(series_dict)+1:]:
        car_home_link = li.xpath('.//div [@class="tw-mt-1 tw-px-4"]/a/@href').extract_first().strip()
        car_home_links.append(car_home_link)

    return  car_home_links

#进入车系首页，获取参数配置的链接
def get_car_detail_url_and_data(car_home_link,car_data):
    # 进入车系首页
    response = requests.get(car_home_link)
    car_html_data = response.text

    select = parsel.Selector(car_html_data)

    # 获取品牌名称brand_name
    brand_name = select.xpath('.//div [@class="container athm-crumb"]/a[2]/text()').extract_first().strip()

    # 获取厂商名称group_name与group_id
    group_name = select.xpath('.//div [@class="athm-sub-nav__car__name"]/a/text()').extract_first().strip().rstrip('-')

    # 获取参数配置的链接

    car_detail_url = "https:" + select.xpath('.//div [@id="navTop"]/ul/li[2]/a/@href').extract_first().strip()
    detail_html_data = requests.get(car_detail_url).text
    select = parsel.Selector(detail_html_data)
    series_name = select.xpath('//div [@class = "subnav-title-name"]/a/text()').extract_first().strip().rstrip(
        brand_name + '-')

    car_data["series_name"] = series_name
    car_data["series_id"] = get_id(series_name, series_dict)
    car_data["brand_name"] = brand_name
    car_data["brand_id"] = get_id(brand_name, brand_dict)
    car_data["group_name"] = group_name
    car_data["group_id"] = get_id(group_name, group_dict)
    return car_detail_url,detail_html_data

#递归处理异常
def get_full_name(links, link, car_data_list, car_detail_url):

    try:
        url = link.get_attribute("href")
        # isin用来判断url中包含的车id是否在car_data_list中
        isin = False
        specid = url.split(r'https://www.autohome.com.cn/spec/')[1].split('/')[0]

        for car in car_data_list:
            if url and eval(specid) == car["id"]:
                # 访问链接
                driver.get(url)
                #element = driver.find_element(By.CSS_SELECTOR,'#PL41 input[value = "汽油"').click()

                # 等待页面加载完成
                WebDriverWait(driver, 10).until(EC.url_contains(url))

                # 将网页源代码传递给Beautiful Soup对象
                soup = BeautifulSoup(driver.page_source, 'html.parser')

                # 使用Beautiful Soup对象的方法查找页面标题标签，并提取其内容
                title_tag = soup.find('title')
                if title_tag:
                    title = title_tag.text.strip()
                    full_name = title.split("【图】")[1].split("报价")[0]
                    car["full_name"] = full_name
                else:
                    print("未找到页面标题")
                break
    except StaleElementReferenceException:
        # 如果发生StaleElementReferenceException异常，则重新获取链接元素
        driver.get(car_detail_url)
        links_parent = driver.find_element(By.XPATH, '//*[@id="config_nav"]')
        links_ = links_parent.find_elements(By.XPATH, './/div[@class="carbox"]/div/a')
        link = links_[links.index(link)]
        get_full_name(links,link, car_data_list,car_detail_url)
def get_full_names(car_detail_url,car_data_list):
    # 打开网页
    driver.get(car_detail_url)
    WebDriverWait(driver, 10).until(EC.url_contains(car_detail_url))

    # 找到父元素
    links_parent = driver.find_element(By.XPATH, r'//*[@id="config_nav"]')

    # 找到所有链接
    links = links_parent.find_elements(By.XPATH, r'//*[@class = "carbox"]/div/a')

    for link in links:
              get_full_name(links,link,car_data_list,car_detail_url)

#获取车系的细节，包含每款车的数据
def get_car_detail(car_data,detail_html_data,car_detail_url,car_data_list):
    # 获取参数配置的数据
    pattern = re.compile(r'var config = ({.*?});', re.DOTALL)
    result = pattern.search(detail_html_data)
    if result:
        # 获取嵌入的JSON数据
        json_data = result.group(1)

        # 将JSON数据转换为字典
        config_data = json.loads(json_data)
        # print(json.dumps(config_data, indent=4, ensure_ascii=False))  # 打印字典
        for paramtypeitem in config_data["result"]["paramtypeitems"]:
            if paramtypeitem["name"] == "基本参数":
                for car_driver in paramtypeitem["paramitems"][4]["valueitems"]:
                    # 获取油车,记录每辆油车对应的id，用于后续的数据处理
                    if car_driver["value"] == "汽油":
                        car_data_list.append(car_data.copy())
                        # 记录油车的id
                        car_data_list[len(car_data_list) - 1]["id"] = car_driver["specid"]


                for i in range(0, len(paramtypeitem["paramitems"])):
                    for car_perdata in paramtypeitem["paramitems"][i]["valueitems"]:
                        specid = car_perdata["specid"]
                        for car in car_data_list:
                            # 如果车辆id已经被记录，是油车
                            if car["id"] == specid:
                                str = paramtypeitem["paramitems"][i]["name"]
                                match str:
                                    case "最大功率(kW)":
                                        car["max_power"] = car_perdata["value"] + "kw"
                                    case "最高车速(km/h)":
                                        car["max_speed"] = car_perdata["value"] + "km/h"
                                    case "最大满载<span class='hs_kw29_configKC'></span>(kg)":
                                        car["max_load"] = car_perdata["value"] + "kg"
                                    case "发动机":
                                        car["max_horsepower"] = car_perdata["value"]

                                if str.startswith("WLTC"):
                                    car["oil"] = car_perdata["value"] + "L"

                                if str.startswith("厂") and str.endswith(")"):
                                    price = car_perdata["value"]
                                    pattern = r'^[+-]?\d+(\.\d+)?'
                                    match = re.match(pattern, price)
                                    if match:
                                        price = match.group(0)
                                        car["price"] = price + "万元"

                                if str.startswith("最大满载"):
                                    car["max_load"] = car_perdata["value"] + "kg"

                                if str.startswith("上市"):
                                    #  非空
                                    if len(car_perdata["value"]) == 7:
                                        car["year"] = car_perdata["value"]
                                        car["month"] = car_perdata["value"].split(".")[1]


            elif paramtypeitem["name"] == "发动机":
                for i in range(0, len(paramtypeitem["paramitems"])):
                    for car_perdata in paramtypeitem["paramitems"][i]["valueitems"]:
                        specid = car_perdata["specid"]
                        for car in car_data_list:
                            # 如果车辆id已经被记录，是油车
                            if car["id"] == specid:
                                str = paramtypeitem["paramitems"][i]["name"]
                                if str.endswith("(L)"):
                                    car["displacement"] = car_perdata["value"] + "L"

        get_full_names(car_detail_url, car_data_list)
    else:
        print("未找到嵌入的JSON数据")
    return car_data_list

#打开csv文件
def create_csv():
    with open("汽车之家.csv", "w", newline="") as file:
        # 创建一个csv文件的写入对象
        csv_writer = csv.writer(file)
        if not os.path.isfile("汽车之家.csv"):
            # 文件不存在，新建写入表头
            csv_writer.writerow(headers)

#存储数据到csv文件
def save_csv(count,file_name,car_data_list):
    with open(file_name, "a",encoding='utf-8',newline="") as file:
        csv_writer = csv.writer(file)
        for car in car_data_list:

            csv_writer.writerow([
                car["id"], car["brand_id"], car["group_id"], car["series_id"], car["full_name"],
                car["brand_name"], car["group_name"], car["series_name"], car["price"], car["year"],
                car["displacement"], car["month"], car["oil"],
                car["max_power"], car["max_speed"], car["max_load"],
                car["max_horsepower"]
            ])
            print(car["series_id"],count,car["full_name"])
            count+=1
    return count
def main():


    #获取已经存储了的品牌，厂商，车系的字典
    get_dict(brand_dict, group_dict, series_dict)
    # 使用Chrome浏览器驱动
    car_home_links = get_car_home_links()
    df = pd.read_csv("汽车之家.csv",encoding="utf-8")

    #获取当前已经得到的车的数量count
    count = len(df)-1
    print(count)
    for car_home_link in car_home_links:
        #初始化car_data的值未None
        car_data = {
            "id": None,
            "brand_id": None,
            "group_id": None,
            "series_id": None,
            "full_name": None,
            "brand_name": None,
            "group_name": None,
            "series_name": None,
            "price": None,
            "year": None,
            "displacement": None,
            "month": None,
            "oil": None,
            "max_power": None,
            "max_speed": None,
            "max_load": None,
            "max_horsepower": None

        }

        # 创建每款车不同型号的列表
        car_data_list = []
        car_detail_url,detail_html_data = get_car_detail_url_and_data(car_home_link,car_data)
        car_data_list = get_car_detail(car_data,detail_html_data,car_detail_url,car_data_list)
        count = save_csv(count,"汽车之家.csv",car_data_list)

if __name__ == "__main__":
    main()