"""
@Time           :2022/6/7
@author         :XDS
@Description    :
"""
import datetime
import os
from loguru import logger

# 服务启动配置
start_run = dict(
    app="main:app",
    host='0.0.0.0',
    port=8081,
    reload=False,
    debug=False
)

# 记录日志
logger.add(f'./log/{datetime.datetime.now().strftime("%Y%m")}.log', level='INFO', rotation='100MB', enqueue=True)

# mysql数据库链接地址
mysql_url = 'mysql+pymysql://root:mysql@192.168.0.224:3306/my_db?charset=utf8'

# 阿里云配置
alioss = dict(
    get_params_url='https://api.taoic.com/oss/policyToken',  # 获取上传参数
    upload_url='https://taoic.oss-cn-hangzhou.aliyuncs.com',  # 上传地址
    image_prefix='sku/image',  # 图片存储路径
    pdf_prefix='sku/pdf'  # pdf存储路径
)

pdfs_dir = './resource/pdfs/'  # 本地pdf存储路径
images_dir = './resource/images/'  # 本图片存储路径

if not os.path.exists(pdfs_dir):
    os.makedirs(pdfs_dir)

if not os.path.exists(images_dir):
    os.makedirs(images_dir)

auth = [
    'eBb5M2IDXhSJIj17EYVdr2cf5YifImKT1'
]

doc = {
    "title": "TAOIC数据匹配系统"
}

try:
    # 导入测试配置
    from settings_test import *
except Exception as e:
    pass
