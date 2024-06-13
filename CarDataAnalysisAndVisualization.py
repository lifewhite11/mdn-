#!/usr/bin/env python
# -*- coding: utf-8 -*-


# 1. 导入模块

import pandas as pd

from GenerateCharts.CarPricePieChart import car_price_pie_chart
from GenerateCharts.CarOilConsumptionPer100km import car_oil_consumption_per100km
from GenerateCharts import OnSaleCarAmountTop15 as oscat


# 2.Pandas数据处理

# 2.1 读取数据
from GenerateCharts.HeatMap import CarDataHeatMap

df = pd.read_csv('汽车之家.csv', encoding='gbk', low_memory=False)
df.head(5)

# 2.2 筛选部分列数据
df1 = df.loc[:, ['full_name', 'brand_name', 'group_name', 'series_name', 'price', 'year',
                 'displacement', 'month', 'oil', 'max_power', 'max_speed', 'max_load', 'max_horsepower']]
df1.head(5)

# 2.3提取数据中的数字并转为float类型
df1['price'] = df1['price'].str.extract('(\d+\.?\d*)').astype(float)
df1['displacement'] = df1['displacement'].str.extract('(\d+\.?\d*)').astype(float)
df1['oil'] = df1['oil'].str.extract('(\d+\.?\d*)').astype(float)
df1['max_power'] = df1['max_power'].str.extract('(\d+\.?\d*)').astype(float)
df1['max_speed'] = df1['max_speed'].str.extract('(\d+\.?\d*)').astype(float)
df1['max_load'] = df1['max_load'].str.extract('(\d+\.?\d*)').astype(float)

# 因最大马力中包含排量数据，去除最大马力中的前五个字符
df1['max_horsepower'] = df1['max_horsepower'].map(lambda x: str(x)[5:])

# 继续提取数字并转化类型
df1['max_horsepower'] = df1['max_horsepower'].str.extract('(\d+\.?\d*)').astype(float)

# 2.4 查看索引、数据类型和内存信息
df1.info()

# 2.5 数据大小
print(df1.shape)

# 2.6 查看所有汽车品牌
df1['brand_name'].unique()

# '''
# 3. Pyecharts数据可视化
# '''
# 3.1 汽车售价区间占比饼图

car_price_pie_chart(df1)

# 3.2 xx品牌汽车百公里油耗/排量/价格

car_oil_consumption_per100km(df1)

# 3.3 在售汽车品牌数量TOP15象形图
# 3.4 在售汽车品牌数量TOP15堆叠图
# 3.5 汽车品牌词云

sch_icons = {
        '大众': 'image://https://car2.autoimg.cn/cardfs/series/g24/M07/57/D8/autohomecar__ChsEeV26zOKAATwCAAAMlhPv54M195.png',
        '奔驰': 'image://https://car3.autoimg.cn/cardfs/series/g26/M00/AF/E7/autohomecar__wKgHHVs9u6mAaY6mAAA2M840O5c440.png',
        '宝马': 'image://https://car2.autoimg.cn/cardfs/series/g1/M08/18/4F/autohomecar__ChsEmV5fMd6AZK-bAAAg8taR7xI407.png',
        '丰田': 'image://https://car2.autoimg.cn/cardfs/series/g28/M04/C5/46/autohomecar__ChwFkmGgkM-ADLF_AAA7SzrQUQw971.png',
        '奥迪': 'image://https://car2.autoimg.cn/cardfs/series/g26/M0B/AE/B3/autohomecar__wKgHEVs9u5WAV441AAAKdxZGE4U148.png',
        '吉利汽车': 'image://https://car3.autoimg.cn/cardfs/series/g15/M06/A0/71/autohomecar__ChwEoWDylfGAOuKfAAA5bSitpkk273.png',
        '江淮': 'image://https://car3.autoimg.cn/cardfs/series/g27/M01/B0/3D/autohomecar__ChcCQFs9touAZxvgAAAcEM6h5fk288.png',
        '福特': 'image://https://car2.autoimg.cn/cardfs/series/g27/M01/E7/3D/autohomecar__ChwFkWGVuYCAWgzzAAA86IJMQok255.png',
        '上汽大通': 'image://https://car2.autoimg.cn/cardfs/series/g25/M08/5B/0F/autohomecar__ChwFj18eQ3CABqIiAAAPb9iBKuM681.png',
        '奇瑞': 'image://https://car2.autoimg.cn/cardfs/series/g29/M09/AF/7F/autohomecar__wKgHJFs9s2qAawQfAAAnXgLikoM954.png',
        '福田': 'image://https://car3.autoimg.cn/cardfs/series/g1/M02/22/4C/autohomecar__ChcCQ1z0hJyAKjxnAABAVJ0IgBo091.png',
        '现代': 'image://https://car3.autoimg.cn/cardfs/series/g2/M06/77/58/autohomecar__ChsEml2DT3iAZXJtAAB5yfqMJ50322.png',
        '起亚': 'image://https://car3.autoimg.cn/cardfs/series/g3/M03/C3/04/autohomecar__ChwFlV_1kBmAFRXxAAAn-KcSG8Q668.png',
        '日产': 'image://https://car2.autoimg.cn/cardfs/series/g16/M14/7B/F8/autohomecar__ChsEzWDylM6AejvfAABHS68N4Ic340.png',
        '长安': 'image://https://car3.autoimg.cn/cardfs/series/g28/M06/44/F5/autohomecar__ChwFkl9y_JqAVybMAAAUINDQ2uo180.png'
    }
icons = []
oscat.on_sale_car_amount_top15(df1, sch_icons, icons)

#热力图
CarDataHeatMap(df1)