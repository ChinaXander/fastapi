"""
@Time           :2022/6/7
@author         :XDS
@Description    :
"""
import json
import queue
import threading
from time import sleep
from typing import Union

import fitz
import os
import requests
import settings

from fastapi import Header, HTTPException
from loguru import logger


def pdf_image(pdf_url: str, imagename: str, start: int = 0, num: int = 5):
    """
    pdf转images
    :param pdf_url:
    :param imagename:
    :param start:
    :param num:
    :return:
    """
    image_list = list()

    pdf_file = f"{settings.pdfs_dir}{pdf_url}"  # pdf文件路径

    images_dir = settings.images_dir + imagename  # images保存目录
    if not os.path.exists(images_dir):
        os.mkdir(images_dir)

    # 下载pdf
    if not os.path.isfile(pdf_file):
        response = requests.get(f"{settings.alioss['upload_url']}/{settings.alioss['pdf_prefix']}/{pdf_url}")
        if response.status_code == 200:
            f = open(pdf_file, 'wb')
            f.write(response.content)
            f.close()
        else:
            logger.error(f"pdf下载失败 ===>>> [url]{settings.alioss['upload_url']}/{settings.alioss['pdf_prefix']}/{pdf_url}")
            return image_list

    # 打开pdf
    doc = fitz.open(pdf_file)
    # 计算转换页数
    if num > 0:
        end = min(len(doc), num + start)
    else:
        end = len(doc)

    # 保存图片
    oss_setting = None
    for pg in range(start, end):
        image_list.append(f"{settings.alioss['upload_url']}/{settings.alioss['image_prefix']}/{imagename}-{str(pg)}.jpg")

        if not os.path.isfile(f"{images_dir}/{imagename}-{str(pg)}.jpg"):
            pm = doc[pg].get_pixmap(alpha=False)
            pm.save(f"{images_dir}/{imagename}-{str(pg)}.jpg")

            # 获取oss上传参数
            if not oss_setting:
                response = requests.get(settings.alioss['get_params_url'])
                if response.status_code == 200:
                    oss_setting = json.loads(response.text)

            # 上传oss
            q.put({
                "files": {'file': ('product/image', open(f"{settings.images_dir}{imagename}/{imagename}-{str(pg)}.jpg", 'rb'), 'image/jpeg')},
                "file_names": f"{imagename}-{str(pg)}.jpg",
                "oss_setting": oss_setting
            })
            # q.put({"files": imagename, "file_names": pg, "oss_setting": oss_setting})
            # upload_oss({'file': ('product/image', open(f"{settings.images_dir}{imagename}/{imagename}-{str(pg)}.jpg", 'rb'), 'image/jpeg')}, f"{imagename}-{str(pg)}.jpg")

    doc.close()

    logger.debug(f"线程数：{len(threading.enumerate())}")
    if not upload_oss_thread.is_alive() and oss_setting:
        logger.debug(f"线程开始===>>>{upload_oss_thread.name}")
        upload_oss_thread.start()

    return image_list


def upload_oss(files, file_name, oss_setting):
    """
    上传图片到oss 图片只能上传jpg
    :param oss_setting:
    :param files: 格式
    {'file': ('product/image', open('./download/image/test.jpg', 'rb'), 'image/jpeg')}
    {'file': ('product/pdf', open('./download/pdf/test.pdf', 'rb'), 'application/pdf')}
    :param file_name: 文件名称
    :return: 返回oss文件地址 form_data['key']
    """
    # if requests.get(f"{config.alioss['upload_url']}/{config.alioss['image_prefix']}/{file_name}").status_code == 200:
    #     return True

    # sleep(1)
    # logger.debug(f"上传oss成功 ===>>> {files}-{file_name}")
    # return False

    if not oss_setting:
        return False

    form_data = {
        'key': f'{settings.alioss["image_prefix"]}/{file_name}',
        'policy': oss_setting['policy'],
        'OSSAccessKeyID': oss_setting['accessid'],
        'sucess_action_status': 200,
        'Signature': oss_setting['signature']
    }

    # 上传
    try:
        oss_response = requests.post(url=settings.alioss['upload_url'], data=form_data, files=files, timeout=60)
        if oss_response.status_code != 204:
            raise Exception(oss_response.status_code)
    except Exception as e:
        logger.error(f"上传oss失败 ===>>> [error]{e} [data]{form_data}")
        return False

    logger.debug(f"上传oss成功 ===>>> {form_data['key']}")
    return True


async def token_verify(Authorization_token: Union[str, None] = Header(None, description="token")):
    try:
        settings.auth.index(Authorization_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail="authentication failed")


def res_data(data, code: int = 200, msg: str = 'success'):
    return {'code': code, 'msg': msg, 'data': data}


class UploadOssTask(threading.Thread):
    def run(self):
        while not q.empty():
            re = q.get()
            upload_oss(re['files'], re['file_names'], re['oss_setting'])
        else:
            logger.debug(f"线程结束===>>>{self.name}")
            self.__init__(name='aliyun_oss')


upload_oss_thread = UploadOssTask(name='aliyun_oss')
q = queue.Queue()
