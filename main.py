# 这是UpdaterLite的独立版，如果你在找函数版，转到ul.py文件

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

while True:
    print("欢迎使用UpdaterLite")
    print("菜单：")
    print("1. 按配置进行下载操作")
    print("2. 退出")
    choice = input()

    # 主菜单

    if choice == "1":
        urllib.request.urlretrieve(ul_url, os.path.join(ul_save_path, ul_name), reporthook=ul_reporthook)
        print("下载完成!")
        # 下载
    elif choice == "2":
        os._exit(0)
    else:
        print("输入错误，请重新输入")
