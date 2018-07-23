# Clipboard.WEB
一个简单的网络剪贴板。
## 依赖
* Flask>=0.12.2
* pymongo>=3.7.1
* Jinjia2>=2.9.6
## config.py文件内容
请在根目录下添加`config.py`文件用作配置信息。
```python
host = '0.0.0.0'  # 监听的IP。可设置为None。
port = 5000  # 监听的端口。设置为None表示不设置此项。

debug = True  # 是否使用debug。
secret_key = ''  # 密钥。


mongodb = {  # mongodb的各项配置
    'host': 'localhost',
    'port': '27017',
    'name': 'clipboard_web'
}

file_uploads = {  # 文件上传的相关配置
    'max_size': 1024 * 1024 * 16,  # 16mb,  # 最大文件大小
    'path': 'uploads/'  # 上传放置目录。以/开头会放在根目录。
}
```