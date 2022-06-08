"""
@Time           :2022/6/7
@author         :XDS
@Description    :
"""
from fastapi import HTTPException

import settings
import tools
from data.database import Db
import data.digikey.details as digikeydetails
import data.mouser.details as mouserdetails
from fastapi import Query
from typing import Union


def get_product_details(
        model: str = Query(description="型号"),
        brand: Union[str, None] = Query(None, description="型号")
):
    DigikeyData = Digikey().get_details(model, brand)
    MouserData = Mouser().get_details(model, brand)

    if DigikeyData and MouserData:
        result = DigikeyData + MouserData
    elif DigikeyData:
        result = DigikeyData
    elif MouserData:
        result = MouserData
    else:
        raise HTTPException(status_code=201, detail="product not find")

    for value in result:
        # 获取图片
        if value.pdfpath:
            pdfname = value.pdfpath.split('.')[0]
            value.pdf_image = tools.pdf_image(value.pdfpath, pdfname)
            value.pdf_raw = f"{settings.alioss['upload_url']}/{settings.alioss['image_prefix']}/{value.pdfpath}"
        else:
            value.pdfimage = list()
            value.pdf_raw = ''

    return result


class Digikey:
    def get_details(self, model: str, brand: Union[str, None] = None):
        # res = None
        res = Db.query(digikeydetails.Details).filter(digikeydetails.Details.model == model)
        if brand:
            res = res.filter(digikeydetails.Details.brand == brand)
        return res.all()


class Mouser:
    def get_details(self, model: str, brand: Union[str, None] = None):
        # res = None
        res = Db.query(mouserdetails.Details).filter(mouserdetails.Details.model == model)
        if brand:
            res = res.filter(mouserdetails.Details.brand == brand)
        return res.all()
