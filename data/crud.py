"""
@Time           :2022/6/7
@author         :XDS
@Description    :
"""
import datetime

from fastapi import HTTPException
from sqlalchemy import text

import settings
import tools
from data.database import Db
import data.digikey.details as digikeydetails
import data.mouser.details as mouserdetails
from fastapi import Query
from typing import Union
from loguru import logger


def get_product_details(
        model: str = Query(description="型号", min_length=2),
        brand: Union[str, None] = Query(None, description="型号"),
        page: Union[int, None] = Query(1, description="分页"),
        limit: Union[int, None] = Query(10, description="数量")
):
    start_time = datetime.datetime.now()
    try:
        result = get_details(model, brand, page, limit)
        if not result:
            result = get_details_fulltest(model, brand, page, limit)
            if not result:
                raise Exception('产品查询失败')

        for value in result:
            # 获取图片
            if value.pdfpath:
                pdfname = value.pdfpath.split('.')[0]
                value.pdf_image = tools.pdf_image(value.pdfpath, pdfname)
                value.pdf_raw = f"{settings.alioss['upload_url']}/{settings.alioss['pdf_prefix']}/{value.pdfpath}"
            else:
                value.pdfimage = list()
                value.pdf_raw = ''

            if value.attributes and type(value.attributes) == str:
                value.attributes = eval(value.attributes)


    except Exception as e:
        end_time = datetime.datetime.now()
        logger.error(str(e) + ' [model]==>>' + model + ' [execute] ==>> ' + str(end_time - start_time))
        raise HTTPException(status_code=201, detail="product not find")

    return result


def get_details_fulltest(
        model: str,
        brand: Union[str, None] = None,
        page: int = 1,
        limit: int = 10
):
    try:
        digikeyres = Db().query(digikeydetails.Details).filter(text(f" match(`model`) against('\"{model}\"' IN BOOLEAN MODE)"))
        mouserres = Db().query(mouserdetails.Details).filter(text(f" match(`model`) against('\"{model}\"' IN BOOLEAN MODE)"))
        if brand:
            digikeyres = digikeyres.filter(digikeydetails.Details.brand == brand)
            mouserres = mouserres.filter(mouserdetails.Details.brand == brand)

        res = digikeyres.union(mouserres)

        # logger.info(f"sql:{digikeyIs}")
        # logger.info(Db().query(res.exists()))
        return res.offset((page - 1) * limit).limit(limit).all()
    except Exception as e:
        logger.warning('model全文索引查询失败：' + str(e))
        return None


def get_details(
        model: str,
        brand: Union[str, None] = None,
        page: int = 1,
        limit: int = 10
):
    digikeyres = Db().query(digikeydetails.Details).filter(digikeydetails.Details.model == model)
    mouserres = Db().query(mouserdetails.Details).filter(mouserdetails.Details.model == model)
    if brand:
        digikeyres = digikeyres.filter(digikeydetails.Details.brand == brand)
        mouserres = mouserres.filter(mouserdetails.Details.brand == brand)

    return digikeyres.union(mouserres).offset((page - 1) * limit).limit(limit).all()
