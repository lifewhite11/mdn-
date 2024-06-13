#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
1. 导入模块
'''

import stylecloud
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Grid
from pyecharts.charts import Pie
from pyecharts.charts import PictorialBar
from pyecharts import options as opts
from pyecharts.globals import ThemeType

'''
2.Pandas数据处理
'''
# 2.1 读取数据
df = pd.read_csv('autohome.csv', encoding='gbk', low_memory=False)
df.head(5)

# 2.2 数据大小
print(df.shape)

# 2.3 查看索引、数据类型和内存信息
df.info()

# 2.4 筛选部分列数据
df1 = df.loc[:,['full_name', 'name',
       'brand_name', 'group_name', 'series_name', 'price', 'year', 'carType',
       'displacement', 'month', 'chexi', 'oil', 'chargetime', 'color']]
df1.head(5)

# 2.5 查看所有汽车品牌
df1['brand_name'].unique()


'''
3. Pyecharts数据可视化
'''
# 3.1 汽车售价区间占比饼图
df_tmp = df1.copy()
df_tmp = df_tmp[(df_tmp['price']>0)]
df_tmp['price'] /= 10000
price_bin = pd.cut(df_tmp['price'],bins=[0,10,30,50,70,100,500,7000],include_lowest=True,right=False,
                    labels=['<10万', '10-30万', '30-50万', '50-70万', '70-100万', '100-500万', '>500万'])
df_price = pd.Series(price_bin).value_counts()

data_pair = [list(z) for z in zip(df_price.index.tolist(), df_price.values.tolist())]
p1 = (
    Pie(init_opts=opts.InitOpts(theme=ThemeType.DARK,width='1000px',height='600px',bg_color='#0d0735'))

    .add(
        '售价', data_pair, radius=['40%', '70%'],
        label_opts=opts.LabelOpts(
                position="outside",
                formatter="{a|{a}}{abg|}\n{hr|}\n {b|{b}: }{c|{c}}  {d|{d}%}  ",
                background_color="#eee",
                border_color="#aaa",
                border_width=1,
                border_radius=4,
                rich={
                    "a": {"color": "#c92a2a", "lineHeight": 20, "align": "center"},
                    "abg": {
                        "backgroundColor": "#00aee6",
                        "width": "100%",
                        "align": "right",
                        "height": 22,
                        "borderRadius": [4, 4, 0, 0],
                    },
                    "hr": {
                        "borderColor": "#00d1b2",
                        "width": "100%",
                        "borderWidth": 0.5,
                        "height": 0,
                    },
                    "b": {"color": "#bc0024","fontSize": 16, "lineHeight": 33},
                    "c": {"color": "#4c6ef5","fontSize": 16, "lineHeight": 33},
                    "d": {"color": "#bc0024","fontSize": 20, "lineHeight": 33},
                },
            ),
         itemstyle_opts={
            'normal': {
                'shadowColor': 'rgba(0, 0, 0, .5)',
                'shadowBlur': 5,
                'shadowOffsetY': 2,
                'shadowOffsetX': 2,
                'borderColor': '#fff'
            }
        }
    )

    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="汽车售价区间占比",
            pos_left='center',
            pos_top='center',
            title_textstyle_opts=opts.TextStyleOpts(
                color='#ea1d5d',
                font_size=26,
                font_weight='bold'
            ),

        ),
        visualmap_opts=opts.VisualMapOpts(
            is_show=False,
            min_=0,
            max_=20000,
            is_piecewise=False,
            dimension=0,
            range_color=['#e7e1ef','#d4b9da','#c994c7','#df65b0','#e7298a','#ce1256','#91003f']
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )

)
p1.render("1-汽车售价区间占比饼图.html")

# 3.2 xx品牌汽车百公里油耗/排量/价格
colors = ["#ea1d5d", "#00ad45", "#0061d5"]
width = 3
car_brand_name = '凯迪拉克'
# car_brand_name = '玛莎拉蒂'
data_tmp = df1[(df1.brand_name == car_brand_name)]
data = data_tmp.copy()
data = data.dropna(subset=['price', 'displacement', 'oil'])
data = data[(data['price'] > 0) & (data['displacement'] > 0) & (data['oil'] > 0)]
data['price'] = data['price'] / 10000
price = data.price.values.tolist()
displacement = data.displacement.values.tolist()
oil = data.oil.tolist()
region = [i for i in range(len(price))]
line2 = (
    Line()
        .add_xaxis(region)
        .add_yaxis(
        series_name='百公里油耗',
        y_axis=oil,
        yaxis_index=1,
        color=colors[0],
        z=10,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts={
            'normal': {
                'width': width,
                'shadowColor': 'rgba(94, 204, 98, .3)',
                'shadowBlur': 10,
                'shadowOffsetY': 10,
                'shadowOffsetX': 10,
            }
        },
    )
        .add_yaxis(
        series_name="排量",
        y_axis=displacement,
        yaxis_index=2,
        color=colors[1],
        z=10,
        label_opts=opts.LabelOpts(is_show=False),
        linestyle_opts={
            'normal': {
                'width': width,
                'shadowColor': 'rgba(155, 18, 184, .3)',
                'shadowBlur': 10,
                'shadowOffsetY': 10,
                'shadowOffsetX': 10,
            }
        },
    )
        .extend_axis(
        yaxis=opts.AxisOpts(
            name='百公里油耗',
            type_="value",
            min_=0,
            max_=12,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=2, color=colors[0])
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} L"),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(type_='dashed', opacity=0.3)
            ),
        )
    )
        .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="排量",
            min_=0,
            max_=5,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=2, color=colors[1])
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} L"),

        )
    )
        .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
            ]
        ),
    )
        .set_global_opts(
        title_opts=opts.TitleOpts(
            title=f'{car_brand_name}--百公里油耗/排量/价格',
            pos_left='center',
            pos_top='2%',
            title_textstyle_opts=opts.TextStyleOpts(color='#ffb900', font_size=18)
        ),
        legend_opts=opts.LegendOpts(pos_left="center", pos_top='12%'),
        tooltip_opts=opts.TooltipOpts(
            is_show=True, trigger='axis', axis_pointer_type='cross'),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(font_size=14, color='#fff200'),
                                 axisline_opts=opts.AxisLineOpts(is_show=False,
                                                                 linestyle_opts=opts.LineStyleOpts(width=2,
                                                                                                   color='#DB7093'))),
        yaxis_opts=opts.AxisOpts(
            name='价格',
            position="right",
            offset=60,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=2, color=colors[2])
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} 万"),
        )
    )
)

bar1 = (
    Bar()
        .add_xaxis(xaxis_data=region)
        .add_yaxis(
        series_name="价格",
        yaxis_index=0,
        y_axis=price,
        label_opts=opts.LabelOpts(is_show=False),
        color=colors[2],
        itemstyle_opts=opts.ItemStyleOpts(color=colors[2]),
    )
        .set_series_opts(
        label_opts=opts.LabelOpts(is_show=False),
        markpoint_opts=opts.MarkPointOpts(
            data=[
                opts.MarkPointItem(type_="max", name="最大值"),
                opts.MarkPointItem(type_="min", name="最小值"),
            ]
        ),
    )
)

line2.overlap(bar1)
grid2 = Grid(init_opts=opts.InitOpts(width='1400px', height='600px', bg_color='#0d0735'))
grid2.add(line2, opts.GridOpts(pos_top="20%", pos_left="5%", pos_right="15%"), is_control_axis_index=True)
grid2.render("2-xx品牌汽车百公里油耗-排量-价格.html")

# 3.3 在售汽车品牌数量TOP15象形图
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
df_brand_name_tmp = df1.groupby(['brand_name'])['name'].count().to_frame('数量').reset_index().sort_values(by=['数量'],ascending=False)
df_brand_name = df_brand_name_tmp[:15]
x_data = df_brand_name['brand_name'].values.tolist()[::-1]
y_data = df_brand_name['数量'].values.tolist()[::-1]
for idx,sch in enumerate(x_data):
    icons.append(dict(name=sch, value=y_data[idx], symbol=sch_icons[sch]))
p1 = (
        PictorialBar(init_opts=opts.InitOpts(theme='light', width='1000px', height='700px'))
        .add_xaxis(x_data)
        .add_yaxis('',
            icons,
            label_opts=opts.LabelOpts(is_show=False),
            category_gap='40%',
            symbol_repeat='fixed',
            symbol_margin='30%!',
            symbol_size=40,
            is_symbol_clip=True,
            itemstyle_opts={"normal": {
                'shadowBlur': 10,
                'shadowColor': 'rgba(0, 0, 200, 0.3)',
                'shadowOffsetX': 10,
                'shadowOffsetY': 10,}
            }
          )
        .set_global_opts(
            title_opts=opts.TitleOpts(title='在售汽车品牌数量TOP15',pos_top='2%',pos_left = 'center',
                                   title_textstyle_opts=opts.TextStyleOpts(color="blue",font_size=30)),
            xaxis_opts=opts.AxisOpts(
                position='top',
                is_show=True,
                axistick_opts=opts.AxisTickOpts(is_show=True),
                axislabel_opts=opts.LabelOpts(font_size=20,color='#ed1941',font_weight=700,margin=12),
                splitline_opts=opts.SplitLineOpts(is_show=True,
                                                  linestyle_opts=opts.LineStyleOpts(type_='dashed')),
                axisline_opts=opts.AxisLineOpts(is_show=False,
                                        linestyle_opts=opts.LineStyleOpts(width=2, color='#DB7093'))
            ),
            yaxis_opts=opts.AxisOpts(
                is_show=True,
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(font_size=20,color='#ed1941',font_weight=700,margin=20),
                axisline_opts=opts.AxisLineOpts(is_show=False,
                                        linestyle_opts=opts.LineStyleOpts(width=2, color='#DB7093'))
            ),
        )
       .reversal_axis()
    )
grid0 = Grid(init_opts=opts.InitOpts(theme='light', width='1000px', height='800px'))
grid0.add(p1, is_control_axis_index=False, grid_opts=opts.GridOpts(pos_left='15%', pos_right='15%', pos_top='15%'))
grid0.render("3-在售汽车品牌数量TOP15象形图.html")

# 3.4 在售汽车品牌数量TOP15堆叠图
p2 = (
        PictorialBar()
        .add_xaxis(x_data)
        .add_yaxis("",
            icons,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_pos='start',
            symbol_size=40,
            is_symbol_clip=False,
            itemstyle_opts={"normal": {
                'shadowBlur': 10,
                'shadowColor': 'rgba(0, 0, 255, 0.5)',
                'shadowOffsetX': 10,
                'shadowOffsetY': 10,}
            }
         )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                is_show=True,
                is_scale=True,
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(font_size=20,color='#ed1941',font_weight=700,margin=20),
                splitline_opts=opts.SplitLineOpts(is_show=False,
                                                  linestyle_opts=opts.LineStyleOpts(type_='dashed')),
                axisline_opts=opts.AxisLineOpts(is_show=False,
                                        linestyle_opts=opts.LineStyleOpts(width=2, color='#DB7093'))
            ),
        )
       .reversal_axis()
    )

b1 = (
     Bar()
     .add_xaxis(x_data)
     .add_yaxis('', y_data, category_gap='40%')
     .set_series_opts(
         label_opts=opts.LabelOpts(
            position='insideLeft',
            vertical_align='middle',
            horizontal_align='top',
            font_size=18,
            font_weight='bold',
            formatter=' {c} '),
            itemstyle_opts={
                'opacity': 0.9,
                'shadowBlur': 10,
                'shadowOffsetX': 10,
                'shadowOffsetY': 10,
                'shadowColor': 'rgba(0,0, 255, 0.5)',
                'barBorderRadius': [30, 15, 30, 15],
                'color':'red'
            }
      )
      .set_global_opts(
            yaxis_opts=opts.AxisOpts(is_show=False),
            xaxis_opts=opts.AxisOpts(
                is_scale=True,
                type_='value',
                name_location='middle',
                position='top',
                name_textstyle_opts=opts.TextStyleOpts(font_size=14, font_weight='bold',),
                axisline_opts=opts.AxisLineOpts(is_show=False),
                axislabel_opts=opts.LabelOpts(is_show=False),
                splitline_opts=opts.SplitLineOpts(is_show=False),
                axistick_opts=opts.AxisTickOpts(is_show=False),),
          title_opts=opts.TitleOpts(title='在售汽车品牌数量TOP15',pos_top='2%',pos_left = 'center',
                                   title_textstyle_opts=opts.TextStyleOpts(color="blue",font_size=30)),
      )
      .reversal_axis()
     )

grid1 = Grid(init_opts=opts.InitOpts(theme='light', width='1000px', height='800px'))
grid1.add(p2, is_control_axis_index=False, grid_opts=opts.GridOpts(pos_left='15%', pos_right='80%', pos_top='10%'))
grid1.add(b1, is_control_axis_index=False, grid_opts=opts.GridOpts(pos_left='21%', pos_right='10%', pos_top='10%'))
grid1.render("4-在售汽车品牌数量TOP15堆叠图.html")

# 3.5 汽车品牌词云
brand_name_list = []
for idx, value in enumerate(df_brand_name_tmp.brand_name.values.tolist()):
    brand_name_list += [value] * (df_brand_name_tmp.数量.values.tolist())[idx]
pic_name = '5-词云.png'
stylecloud.gen_stylecloud(
    text=' '.join(brand_name_list),
    font_path=r'STXINWEI.TTF',
    palette='cartocolors.qualitative.Bold_5',
    max_font_size=100,
    icon_name='fas fa-car-side',
    background_color='#0d0735',
    output_name=pic_name,
    )