# 这是UpdaterLite的函数版，如果你在找独立版，转到main.py文件

import json
import urllib.request
import os
from ul_lib.utils import ul_reporthook  # 导入工具函数

with open('ul_config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
# 加载配置文件

ul_url = config["ul_url"]
ul_name = config["ul_name"]
ul_save_path = config["ul_save_path"]

# 设置配置

if ul_url is None:
    print("检查你的config.json文件，ul_url不能为空")
if ul_name is None:
    print("检查你的config.json文件，ul_name不能为空")
if ul_save_path is None:
    print("检查你的config.json文件，ul_save_path不能为空")
else:
    if not os.path.exists(ul_save_path):
        os.makedirs(ul_save_path) # 创建保存目录（如果不存在）

def ul_download(ul_url, ul_name, ul_save_path):
    urllib.request.urlretrieve(ul_url, os.path.join(ul_save_path, ul_name), reporthook=ul_reporthook)
    print("下载完成!")
    # 下载