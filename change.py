# coding = utf-8
# @Version : 1.0
# @Author : zwj
# @File : change.py
# @Time : 2024-6-8 17:43
# 检测文件的编码格式
import csv
import re
import chardet
import pandas as pd
def detect_encoding(file_path):
    with open(file_path, 'rb') as f:
        result = chardet.detect(f.read())
    return result['encoding']


# 转换文件编码格式
def convert_file_encoding(input_file, output_file, output_encoding='utf-8'):
    # 检测输入文件的编码格式
    input_encoding = detect_encoding(input_file)

    # 读取CSV文件
    df = pd.read_csv(input_file, encoding="gbk")

    # 将数据写入新的CSV文件，使用指定的编码格式
    df.to_csv(output_file, encoding=output_encoding, index=False)
    print(f"文件已成功转换为 {output_encoding} 编码并保存为 {output_file}")




# 转换文件编码格式
# convert_file_encoding(input_file, output_file, output_encoding='utf-8')
pattern_oil = r'\d+\.\d+L'
pattern_max = r'\d+'
with open("汽车之家.csv",newline='',encoding="utf_8") as infile,open("汽车之家_modified.csv", mode ='w', newline ='', encoding ='utf-8') as outfile:
    reader = csv.DictReader(infile)

    filenames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=filenames)
    writer.writeheader()
    for row in reader:
        #writer.writerow(row['year'].split('.'[0]),"year")
        if re.match( pattern_oil,row['oil']) and re.match(pattern_max,row['max_speed']) and re.match(pattern_max,row['max_load']) and re.match(pattern_max,row['max_power']):
            if row['month'].startswith('0'):
                row['month'] =row['month'][1]





            writer.writerow(row)
