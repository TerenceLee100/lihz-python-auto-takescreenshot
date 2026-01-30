import urllib, urllib3, sys, uuid
import ssl
import base64
import json
import pandas as pd
import os
import glob

# pip install urllib3 pandas 

host = 'https://sdwordocr.market.alicloudapi.com'
path = '/general/ocr'
method = 'POST'
appcode = '' # 去阿里云市场获取
querys = ''
bodys = {}
url = host + path

http = urllib3.PoolManager()
headers = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Authorization': 'APPCODE ' + appcode
}
# 遍历指定目录下所有png图片
image_dir = '116-122'
png_files = glob.glob(os.path.join(image_dir, '*.png'))

all_rows = []

for png_path in png_files:
    # 构造对应的json文件名
    json_path = os.path.splitext(png_path)[0] + '.json'

    # 如果同名json文件已存在，直接读取缓存
    if os.path.exists(json_path):
        print(f"识别结果文件已存在，直接读取结果缓存文件: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as jf:
            parsed_data = json.load(jf)
    else:
        print(f"识别结果文件不存在，调用OCR接口识别: {png_path}")
        # 否则调用OCR接口
        with open(png_path, 'rb') as f:
            image_data = f.read()
            base64_data = base64.b64encode(image_data).decode('utf-8')
            bodys['image'] = base64_data

        bodys['url'] = '''url'''
        post_data = urllib.parse.urlencode(bodys).encode('utf-8')
        response = http.request('POST', url, body=post_data, headers=headers)
        content = response.data.decode('utf-8')
        if content:
            print(f"处理文件: {png_path}")
            parsed_data = json.loads(content)
            # 缓存识别结果到同名json文件
            with open(json_path, 'w', encoding='utf-8') as jf:
                json.dump(parsed_data, jf, ensure_ascii=False, indent=2)
        else:
            print(response.status, response.reason)
            continue   # 跳过当前文件

    # 提取data.info
    info_list = parsed_data['data']['info']

    # 收集当前图片的识别结果
    for item in info_list:
        all_rows.append({
            'file': os.path.basename(png_path),
            'confidence': item['confidence'],
            'line_no': item['line_no'],
            'line_content': item['line_content']
        })
    # with open(png_path, 'rb') as f:
    #     image_data = f.read()
    #     base64_data = base64.b64encode(image_data).decode('utf-8')
    #     bodys['image'] = base64_data

    # bodys['url'] = '''url'''
    # post_data = urllib.parse.urlencode(bodys).encode('utf-8')
    # response = http.request('POST', url, body=post_data, headers=headers)
    # content = response.data.decode('utf-8')
    # if content:
    #     print(f"处理文件: {png_path}")
    #     # print(content)
    #     # 解析JSON
    #     parsed_data = json.loads(content)

    #     # 缓存识别结果到同名json文件
    #     json_path = os.path.splitext(png_path)[0] + '.json'
    #     with open(json_path, 'w', encoding='utf-8') as jf:
    #         json.dump(parsed_data, jf, ensure_ascii=False, indent=2)

    #     # 提取data.info
    #     info_list = parsed_data['data']['info']

    #     # 收集当前图片的识别结果
    #     for item in info_list:
    #         all_rows.append({
    #             'file': os.path.basename(png_path),
    #             'confidence': item['confidence'],
    #             'line_no': item['line_no'],
    #             'line_content': item['line_content']
    #         })
    # else:
    #     print(response.status, response.reason)

# 创建总DataFrame
df = pd.DataFrame(all_rows)

# 打印总表格
print("===== 词汇表格 ======")
print(df.to_string(index=False))

# 保存为CSV文件
csv_file = 'vocabulary_table.csv'
df.to_csv(csv_file, index=False, encoding='utf-8-sig')
print(f"\n表格已保存到: {csv_file}")