import sys
import time

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
        print(f"文件大小: {size:.2f} {units[unit_index]}")
        return
    
    # 计算已下载大小和百分比
    downloaded = count * block_size
    percent = min(int(downloaded * 100 / total_size), 100)
    
    # 显示进度条
    bar_length = 50
    filled_length = int(bar_length * percent / 100)
    bar = '#' * filled_length + '-' * (bar_length - filled_length)
    
    # 显示下载速度（简单估算）
    if hasattr(ul_reporthook, 'start_time'):
        elapsed = time.time() - ul_reporthook.start_time
        if elapsed > 0:
            speed = downloaded / elapsed / 1024  # KB/s
            speed_unit = 'KB/s'
            if speed >= 1024:
                speed /= 1024
                speed_unit = 'MB/s'
            sys.stdout.write(f"\r[{bar}] {percent}% - {speed:.2f} {speed_unit}")
    else:
        ul_reporthook.start_time = time.time()
        sys.stdout.write(f"\r[{bar}] {percent}%")
    
    sys.stdout.flush()
    
    # 下载完成时换行
    if percent == 100:
        print()