# 这是UpdaterLite的函数版，如果你在找独立版，转到main.py文件

import urllib.request
import os
import threading
import requests
import logging
import coloredlogs
from urllib.parse import urlparse
from ul_lib.utils import ul_reporthook  # 导入工具函数
import ssl
# 修复InsecureRequestWarning导入路径
import urllib3
# 直接禁用所有警告
urllib3.disable_warnings()

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(funcName)s: %(message)s")  # noqa: F821

def ul_download(ul_url, ul_name, ul_save_path, num_threads=4, ul_autorename=True, disable_ssl_verify=None):
    """
    多线程下载文件
    
    参数:
    ul_url: 下载链接
    ul_name: 保存的文件名（如果从URL无法识别则使用此名）
    ul_save_path: 保存路径
    num_threads: 线程数量，默认4
    ul_autorename: 是否允许自动重命名，默认True
    disable_ssl_verify: 是否禁用SSL验证（None表示询问用户）
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
    
    # 询问用户是否禁用SSL验证
    if disable_ssl_verify is None:
        logging.warning("警告：禁用SSL验证可能会导致安全风险，如中间人攻击和恶意文件下载。")
        user_input = input("是否禁用SSL证书验证？(y/n，默认n): ").lower().strip()
        disable_ssl_verify = user_input == 'y'
    
    try:
        # 获取文件大小
        # 当disable_ssl_verify为True时，verify参数应为False
        response = requests.head(ul_url, verify=not disable_ssl_verify, timeout=10)
        response.raise_for_status()  # 检查请求是否成功
        file_size = int(response.headers.get('Content-Length', 0))
    except requests.exceptions.SSLError as e:
        # 如果SSL验证失败，再次询问用户是否禁用
        logging.error(f"SSL证书验证失败: {e}")
        # 如果用户还没有明确选择是否禁用，才询问
        if disable_ssl_verify is None:
            user_input = input("SSL验证失败，是否禁用SSL证书验证？(y/n): ").lower().strip()
            disable_ssl_verify = user_input == 'y'
            
            if disable_ssl_verify:
                # 重新尝试获取文件大小
                try:
                    response = requests.head(ul_url, verify=False, timeout=10)
                    response.raise_for_status()
                    file_size = int(response.headers.get('Content-Length', 0))
                except Exception as e:
                    logging.error(f"即使禁用SSL验证，获取文件信息仍然失败: {e}")
                    return
            else:
                logging.error("SSL验证失败，下载已取消。")
                return
        elif not disable_ssl_verify:
            # 如果用户之前选择不禁用，现在SSL验证失败，再次询问
            user_input = input("SSL验证失败，是否禁用SSL证书验证？(y/n): ").lower().strip()
            disable_ssl_verify = user_input == 'y'
            
            if disable_ssl_verify:
                # 重新尝试获取文件大小
                try:
                    response = requests.head(ul_url, verify=False, timeout=10)
                    response.raise_for_status()
                    file_size = int(response.headers.get('Content-Length', 0))
                except Exception as e:
                    logging.error(f"即使禁用SSL验证，获取文件信息仍然失败: {e}")
                    return
            else:
                logging.error("SSL验证失败，下载已取消。")
                return
        else:
            # 用户已经选择禁用SSL验证，但仍然失败，这可能是其他网络问题
            logging.error(f"即使禁用SSL验证，请求仍然失败: {e}")
            logging.error("可能是网络连接问题或服务器不可访问。")
            return
    except requests.exceptions.RequestException as e:
        logging.error(f"获取文件信息失败: {e}")
        return
    
    if file_size == 0:
        # 如果无法获取文件大小，使用单线程下载
        try:
            if disable_ssl_verify:
                # 创建不验证SSL证书的上下文
                ssl_context = ssl._create_unverified_context()
                # 使用urlopen替代urlretrieve，因为urlretrieve可能不支持context参数
                with urllib.request.urlopen(ul_url, context=ssl_context) as response, open(save_file, 'wb') as out_file:
                    # 处理进度报告
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    block_size = 8192
                    count = 0  # 已下载的块数
                    
                    while True:
                        chunk = response.read(block_size)
                        if not chunk:
                            break
                        downloaded += len(chunk)
                        out_file.write(chunk)
                        count += 1  # 增加已下载块数
                        # 调用进度报告函数，传递正确的count参数
                        ul_reporthook(count, block_size, total_size)
            else:
                # 使用urlopen替代urlretrieve，保持一致性
                with urllib.request.urlopen(ul_url) as response, open(save_file, 'wb') as out_file:
                    # 处理进度报告
                    total_size = int(response.headers.get('Content-Length', 0))
                    downloaded = 0
                    block_size = 8192
                    count = 0  # 已下载的块数
                    
                    while True:
                        chunk = response.read(block_size)
                        if not chunk:
                            break
                        downloaded += len(chunk)
                        out_file.write(chunk)
                        count += 1  # 增加已下载块数
                        # 调用进度报告函数，传递正确的count参数
                        ul_reporthook(count, block_size, total_size)
            
            logging.info("下载完成!")
            return
        except urllib.error.URLError as e:
            logging.error(f"单线程下载失败: {e}")
            return
        except Exception as e:
            logging.error(f"单线程下载失败: {e}")
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
        
        try:
            with requests.get(ul_url, headers=headers, stream=True, verify=not disable_ssl_verify, timeout=10) as r:
                r.raise_for_status()
                with open(temp_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        if chunk:
                            f.write(chunk)
        except Exception as e:
            logging.error(f"线程{thread_id}下载失败: {e}")
            # 如果下载失败，清理临时文件
            for tf in temp_files:
                if os.path.exists(tf):
                    os.remove(tf)
            raise
    
    try:
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
    except Exception as e:
        logging.error(f"多线程下载失败: {e}")
        return

# 单线程下载函数保持不变，以确保向后兼容
def ul_download_single(ul_url, ul_name, ul_save_path, ul_autorename=True, disable_ssl_verify=None):
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
    
    # 询问用户是否禁用SSL验证
    if disable_ssl_verify is None:
        logging.warning("警告：禁用SSL验证可能会导致安全风险，如中间人攻击和恶意文件下载。")
        user_input = input("是否禁用SSL证书验证？(y/n，默认n): ").lower().strip()
        disable_ssl_verify = user_input == 'y'
    
    try:
        if disable_ssl_verify:
            # 创建不验证SSL证书的上下文
            ssl_context = ssl._create_unverified_context()
            # 使用urlopen替代urlretrieve，因为urlretrieve可能不支持context参数
            with urllib.request.urlopen(ul_url, context=ssl_context) as response, open(save_file, 'wb') as out_file:
                # 处理进度报告
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                block_size = 8192
                count = 0  # 已下载的块数
                
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    downloaded += len(chunk)
                    out_file.write(chunk)
                    count += 1  # 增加已下载块数
                    # 调用进度报告函数，传递正确的count参数
                    ul_reporthook(count, block_size, total_size)
        else:
            # 使用urlopen替代urlretrieve，保持一致性
            with urllib.request.urlopen(ul_url) as response, open(save_file, 'wb') as out_file:
                # 处理进度报告
                total_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                block_size = 8192
                count = 0  # 已下载的块数
                
                while True:
                    chunk = response.read(block_size)
                    if not chunk:
                        break
                    downloaded += len(chunk)
                    out_file.write(chunk)
                    count += 1  # 增加已下载块数
                    # 调用进度报告函数，传递正确的count参数
                    ul_reporthook(count, block_size, total_size)
        
        logging.info("下载完成!")
    except urllib.error.URLError as e:
        # 检查是否是SSL验证错误
        if hasattr(e.reason, 'verify_code') or 'SSL' in str(e).upper():
            logging.error(f"SSL证书验证失败: {e}")
            # 如果用户还没有明确选择是否禁用，才询问
            if disable_ssl_verify is None or not disable_ssl_verify:
                user_input = input("SSL验证失败，是否禁用SSL证书验证？(y/n): ").lower().strip()
                disable_ssl_verify = user_input == 'y'
                
                if disable_ssl_verify:
                    # 创建不验证SSL证书的上下文
                    ssl_context = ssl._create_unverified_context()
                    # 使用urlopen替代urlretrieve
                    with urllib.request.urlopen(ul_url, context=ssl_context) as response, open(save_file, 'wb') as out_file:
                        # 处理进度报告
                        total_size = int(response.headers.get('Content-Length', 0))
                        downloaded = 0
                        block_size = 8192
                        count = 0  # 已下载的块数
                        
                        while True:
                            chunk = response.read(block_size)
                            if not chunk:
                                break
                            downloaded += len(chunk)
                            out_file.write(chunk)
                            count += 1  # 增加已下载块数
                            # 调用进度报告函数，传递正确的count参数
                            ul_reporthook(count, block_size, total_size)
                    logging.info("下载完成!")
                else:
                    logging.error("SSL验证失败，下载已取消。")
            else:
                logging.error("即使禁用SSL验证，下载仍然失败。")
        else:
            logging.error(f"下载失败: {e}")
    except Exception as e:
        logging.error(f"下载失败: {e}")