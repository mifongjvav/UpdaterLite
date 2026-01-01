# 这是修改后的 ul_lib/utils.py 文件
import sys
import time
import logging
import coloredlogs

logging.basicConfig(level=logging.INFO)
coloredlogs.install(level="INFO", fmt="%(asctime)s - %(funcName)s: %(message)s")  # noqa: F821

# ANSI 颜色代码
COLOR_RED = '\033[31m'
COLOR_GREEN = '\033[32m'
COLOR_YELLOW = '\033[33m'
COLOR_BLUE = '\033[34m'
COLOR_PURPLE = '\033[35m'
COLOR_CYAN = '\033[36m'
COLOR_WHITE = '\033[37m'
COLOR_RESET = '\033[0m'

# 进度报告函数
def ul_reporthook(count, block_size, total_size):
    """显示下载进度"""
    if count == 0:
        # 计算文件大小显示单位
        units = ['B', 'KB', 'MB', 'GB']
        size = total_size
        unit_index = 0
        while size >= 1024 and unit_index < 3:
            size /= 1024
            unit_index += 1
        logging.info(f"文件大小: {COLOR_CYAN}{size:.2f} {units[unit_index]}{COLOR_RESET}")
        return
    
    # 计算已下载大小和百分比
    downloaded = count * block_size
    percent = min(int(downloaded * 100 / total_size), 100)
    
    # 显示进度条
    bar_length = 50
    filled_length = int(bar_length * percent / 100)
    
    # 为进度条添加颜色
    bar = f"{COLOR_GREEN}{'#' * filled_length}{COLOR_RESET}{'-' * (bar_length - filled_length)}"
    
    # 显示下载速度（简单估算）
    if hasattr(ul_reporthook, 'start_time'):
        elapsed = time.time() - ul_reporthook.start_time
        if elapsed > 0:
            speed = downloaded / elapsed / 1024  # KB/s
            speed_unit = 'KB/s'
            if speed >= 1024:
                speed /= 1024
                speed_unit = 'MB/s'
            # 为百分比和速度添加颜色
            sys.stdout.write(f"\r[{bar}] {COLOR_BLUE}{percent}%{COLOR_RESET} - {COLOR_PURPLE}{speed:.2f} {speed_unit}{COLOR_RESET}")
    else:
        ul_reporthook.start_time = time.time()
        # 为百分比添加颜色
        sys.stdout.write(f"\r[{bar}] {COLOR_BLUE}{percent}%{COLOR_RESET}")
    
    sys.stdout.flush()
    
    # 下载完成时换行
    if percent == 100:
        sys.stdout.write("\n")