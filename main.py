# 这是UpdaterLite的独立版，如果你在找函数版，转到ul.py文件

import json
import os
import logging
import coloredlogs
from ul import ul_download  # 导入下载函数

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(funcName)s: %(message)s")  # noqa: F821

with open('ul_config.json', 'r', encoding='utf-8') as file:
    config = json.load(file)
# 加载配置文件

ul_url = config["ul_url"]
ul_name = config["ul_name"]
ul_save_path = config["ul_save_path"]
num_threads = config["num_threads"]
ul_autorename = config["ul_autorename"]


logging.info("欢迎使用UpdaterLite")

def main_menu():
    logging.info("菜单：")
    logging.info("1. 按配置进行下载操作")
    logging.info("2. 按配置进行下载操作（多线程）")
    logging.info("3. 不使用配置进行操作")
    logging.info("4. 不使用配置进行操作（多线程）")
    logging.info("5. 退出")
    choice = input()

    # 主菜单
    # 修复：将所有条件判断语句移到while循环体内
    if choice == "1":
        # 设置配置
        if ul_url is None:
            logging.info("检查你的config.json文件，ul_url不能为空")
        if ul_name is None:
            logging.info("检查你的config.json文件，ul_name不能为空")
        if ul_save_path is None:
            logging.info("检查你的config.json文件，ul_save_path不能为空")
        if num_threads is None:
            num_threads = 4
        else:
            if not os.path.exists(ul_save_path):
                os.makedirs(ul_save_path) # 创建保存目录（如果不存在）
        ul_download(ul_url, ul_name, ul_save_path, num_threads=1, ul_autorename=ul_autorename)
            # 下载
    elif choice == "2":
        if ul_url is None:
            logging.info("检查你的config.json文件，ul_url不能为空")
        if ul_name is None:
            logging.info("检查你的config.json文件，ul_name不能为空")
        if ul_save_path is None:
            logging.info("检查你的config.json文件，ul_save_path不能为空")
        if num_threads is None:
            num_threads = 4
        else:
            if not os.path.exists(ul_save_path):
                os.makedirs(ul_save_path) # 创建保存目录（如果不存在）
        ul_download(ul_url, ul_name, ul_save_path, num_threads, ul_autorename)
        # 多线程下载
    elif choice == "3":
        logging.info("url：")
        ul_url = input()
        logging.info("保存文件名：")
        ul_name = input()
        logging.info("保存目录：")
        ul_save_path = input()
        ul_download(ul_url, ul_name, ul_save_path, num_threads=1, ul_autorename=ul_autorename)
        # 下载
    elif choice == "4":
        logging.info("url：")
        ul_url = input()
        logging.info("保存文件名：")
        ul_name = input()
        logging.info("保存目录：")
        ul_save_path = input()
        logging.info("线程数：")
        num_threads = int(input())
        ul_download(ul_url, ul_name, ul_save_path, num_threads, ul_autorename)
        # 多线程下载
    elif choice == "5":
        os._exit(0)
    else:
        logging.info("输入错误，请重新输入")

while True:
    main_menu()