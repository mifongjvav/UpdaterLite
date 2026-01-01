# 这是UpdaterLite的函数版，如果你在找独立版，转到main.py文件

import urllib.request
import os
import threading
import requests
import logging
import coloredlogs
from urllib.parse import urlparse
from ul_lib.utils import ul_reporthook  # 导入工具函数

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(funcName)s: %(message)s")  # noqa: F821

def ul_download(ul_url, ul_name, ul_save_path, num_threads=4, ul_autorename=True):
    """
    多线程下载文件
    
    参数:
    ul_url: 下载链接
    ul_name: 保存的文件名（如果从URL无法识别则使用此名）
    ul_save_path: 保存路径
    num_threads: 线程数量，默认4
    ul_autorename: 是否允许自动重命名，默认True
    """
    # 检查保存路径是否存在
    if not os.path.exists(ul_save_path):
        os.makedirs(ul_save_path)
    
    # 尝试从URL中提取文件名
    parsed_url = urlparse(ul_url)
    url_filename = os.path.basename(parsed_url.path)
    
    # 如果URL中提取的文件名有效，则使用它，否则使用传入的文件名
    if url_filename and not url_filename.endswith('.'):
        # 移除可能的查询参数
        url_filename = url_filename.split('?')[0].split('#')[0]
        final_filename = url_filename
    else:
        final_filename = ul_name
    
    # 检查文件是否存在，如果存在且允许自动重命名，则自动重命名
    save_file = os.path.join(ul_save_path, final_filename)
    if ul_autorename:
        base, ext = os.path.splitext(final_filename)
        counter = 1
        
        while os.path.exists(save_file):
            final_filename = f"{base} ({counter}){ext}"
            save_file = os.path.join(ul_save_path, final_filename)
            counter += 1
    
    logging.info(f"将下载文件保存为: {final_filename}")
    
    # 获取文件大小
    response = requests.head(ul_url)
    file_size = int(response.headers.get('Content-Length', 0))
    
    if file_size == 0:
        # 如果无法获取文件大小，使用单线程下载
        urllib.request.urlretrieve(ul_url, save_file, reporthook=ul_reporthook)
        logging.info("下载完成!")
        return
    
    # 计算每个线程下载的块大小
    block_size = file_size // num_threads
    
    # 创建临时文件列表
    temp_files = []
    
    def download_part(start, end, thread_id):
        """下载文件的一部分"""
        headers = {'Range': f'bytes={start}-{end}'}
        temp_file = f"{save_file}.part{thread_id}"
        temp_files.append(temp_file)
        
        with requests.get(ul_url, headers=headers, stream=True) as r:
            r.raise_for_status()
            with open(temp_file, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
    
    # 创建并启动线程
    threads = []
    for i in range(num_threads):
        start = i * block_size
        # 最后一个线程下载剩余的所有内容
        end = file_size - 1 if i == num_threads - 1 else (i + 1) * block_size - 1
        
        thread = threading.Thread(target=download_part, args=(start, end, i))
        threads.append(thread)
        thread.start()
    
    # 等待所有线程完成
    for thread in threads:
        thread.join()
    
    # 合并所有临时文件
    with open(save_file, 'wb') as f:
        for temp_file in temp_files:
            with open(temp_file, 'rb') as tf:
                f.write(tf.read())
            # 删除临时文件
            os.remove(temp_file)
    
    logging.info("下载完成!")

# 单线程下载函数保持不变，以确保向后兼容
def ul_download_single(ul_url, ul_name, ul_save_path, ul_autorename=True):
    # 检查保存路径是否存在
    if not os.path.exists(ul_save_path):
        os.makedirs(ul_save_path)
    
    # 尝试从URL中提取文件名
    parsed_url = urlparse(ul_url)
    url_filename = os.path.basename(parsed_url.path)
    
    # 如果URL中提取的文件名有效，则使用它，否则使用传入的文件名
    if url_filename and not url_filename.endswith('.'):
        # 移除可能的查询参数
        url_filename = url_filename.split('?')[0].split('#')[0]
        final_filename = url_filename
    else:
        final_filename = ul_name
    
    # 检查文件是否存在，如果存在且允许自动重命名，则自动重命名
    save_file = os.path.join(ul_save_path, final_filename)
    if ul_autorename:
        base, ext = os.path.splitext(final_filename)
        counter = 1
        
        while os.path.exists(save_file):
            final_filename = f"{base} ({counter}){ext}"
            save_file = os.path.join(ul_save_path, final_filename)
            counter += 1
    
    logging.info(f"将下载文件保存为: {final_filename}")
    urllib.request.urlretrieve(ul_url, save_file, reporthook=ul_reporthook)
    logging.info("下载完成!")