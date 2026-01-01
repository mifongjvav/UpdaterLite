# UpdaterLite

> 一个简单的文件下载器，虽然名字里有Updater，但是目前并不能批量更新文件

## 功能

- 下载单个文件
- 多线程下载
- 支持在脚本中调用下载功能

## 安装

1. 下载最新版本的UpdaterLite
2. 解压到任意目录
3. 运行main.py 或在自己的脚本中调用UpdaterLite（`from ul import ul_download`）

## 使用方法

### 作为独立程序使用

1. 运行main.py
2. 在ul_config.json中配置要下载的文件的URL，保存的文件名，保存目录
3. 等待下载完成

### 在脚本中使用UpdaterLite

1. 在自己的脚本中导入UpdaterLite（`from ul import ul_download`）
2. 调用`ul_download(ul_url, ul_name, ul_save_path, num_threads=4, ul_autorename=True)`函数，其中`ul_url`是要下载的文件的URL，`ul_name`是要保存的文件名，`ul_save_path`是要保存的目录，`num_threads`是要使用的线程数，`ul_autorename`是是否自动重命名文件（如果文件已存在）
3. 等待下载完成

示例代码

```python
from ul import ul_download

ul_url = "https://example.com/file.txt"
ul_name = "file.txt"
ul_save_path = "C:/Users/Administrator/Desktop"
num_threads = 4
ul_autorename = True

ul_download(ul_url, ul_name, ul_save_path, num_threads, ul_autorename)
```

> UpdaterLite默认导入了json库，这意味着你可以通过修改ul_config.json来配置要下载的文件的URL，保存的文件名，保存目录。

## 编译成exe

1. 确保你已经安装了PyInstaller（`pip install pyinstaller`）
2. 在命令行中cd到UpdaterLite的目录
3. 运行以下命令将main.py编译成exe：

   ```bash
   pyinstaller --onefile --name UpdaterLite --add-data "ul_lib;ul_lib" main.py
   ```

## 许可证

本项目采用MIT许可证，详情请参阅LICENSE文件。[tl;dr](https://tldrlegal.com/license/mit-license) 只要在任何作品/源代码的副本中包含原始版权和许可证声明，你可以做任何你想做的事情。
