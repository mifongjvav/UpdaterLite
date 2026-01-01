# 这是UpdaterLite的独立版，如果你在找函数版，转到ul.py文件

import json
import os
import logging
import coloredlogs
from ul import ul_download  # 导入下载函数

# 配置文件路径
CONFIG_FILE = 'ul_config.json'

# 配置文件默认内容
DEFAULT_CONFIG = {
    "ul_url": "",
    "ul_name": "",
    "ul_save_path": "./downloads",
    "num_threads": 4,
    "ul_autorename": True
}

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(funcName)s: %(message)s")  # noqa: F821

# 检查配置文件是否存在，如果不存在则创建
if not os.path.exists(CONFIG_FILE):
    logging.info(f"配置文件 {CONFIG_FILE} 不存在，正在创建默认配置...")
    with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
        json.dump(DEFAULT_CONFIG, file, ensure_ascii=False, indent=4)
    logging.info(f"默认配置文件已创建：{CONFIG_FILE}")

# 加载配置文件
with open(CONFIG_FILE, 'r', encoding='utf-8') as file:
    config = json.load(file)

# 确保配置文件包含所有必要的键
for key, value in DEFAULT_CONFIG.items():
    if key not in config:
        config[key] = value

# 更新配置文件
with open(CONFIG_FILE, 'w', encoding='utf-8') as file:
    json.dump(config, file, ensure_ascii=False, indent=4)

# 提取配置
ul_url = config["ul_url"]
ul_name = config["ul_name"]
ul_save_path = config["ul_save_path"]
num_threads = config["num_threads"]
ul_autorename = config.get("ul_autorename", True)

logging.info("欢迎使用UpdaterLite")

def main_menu():
    global num_threads, ul_url, ul_name, ul_save_path
    
    logging.info("菜单：")
    logging.info("1. 按配置进行下载操作")
    logging.info("2. 按配置进行下载操作（多线程）")
    logging.info("3. 不使用配置进行操作")
    logging.info("4. 不使用配置进行操作（多线程）")
    logging.info("5. 退出")
    choice = input()

    # 主菜单
    if choice == "1":
        # 设置配置
        if ul_url is None or ul_url == "":
            logging.info("配置文件中 ul_url 为空，请先编辑配置文件或使用选项3/4手动输入")
        elif ul_name is None or ul_name == "":
            logging.info("配置文件中 ul_name 为空，请先编辑配置文件或使用选项3/4手动输入")
        elif ul_save_path is None or ul_save_path == "":
            logging.info("配置文件中 ul_save_path 为空，请先编辑配置文件或使用选项3/4手动输入")
        else:
            if not os.path.exists(ul_save_path):
                os.makedirs(ul_save_path)  # 创建保存目录（如果不存在）
            ul_download(ul_url, ul_name, ul_save_path, num_threads=1, ul_autorename=ul_autorename)
            # 下载
    elif choice == "2":
        if ul_url is None or ul_url == "":
            logging.info("配置文件中 ul_url 为空，请先编辑配置文件或使用选项3/4手动输入")
        elif ul_name is None or ul_name == "":
            logging.info("配置文件中 ul_name 为空，请先编辑配置文件或使用选项3/4手动输入")
        elif ul_save_path is None or ul_save_path == "":
            logging.info("配置文件中 ul_save_path 为空，请先编辑配置文件或使用选项3/4手动输入")
        else:
            if not os.path.exists(ul_save_path):
                os.makedirs(ul_save_path)  # 创建保存目录（如果不存在）
            ul_download(ul_url, ul_name, ul_save_path, num_threads=num_threads, ul_autorename=ul_autorename)
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
        ul_download(ul_url, ul_name, ul_save_path, num_threads=num_threads, ul_autorename=ul_autorename)
        # 多线程下载
    elif choice == "5":
        os._exit(0)
    else:
        logging.info("输入错误，请重新输入")

while True:
    main_menu()