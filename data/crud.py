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


def get_product_details(
        model: str = Query(description="型号"),
        brand: str = Query(description="品牌")
):
    result = Digikey().get_details(model, brand)
    if not result or not result.pdfpath:
        MouserData = Mouser().get_details(model, brand)
        if MouserData and MouserData.pdfpath:
            result = MouserData
        else:
            raise HTTPException(status_code=201, detail="product not find")

    # 获取图片
    if result and result.pdfpath:
        pdfname = result.pdfpath.split('.')[0]
        result.pdf_image = tools.pdf_image(result.pdfpath, pdfname)
        result.pdf_raw = f"{settings.alioss['upload_url']}/{settings.alioss['image_prefix']}/{result.pdfpath}"
    else:
        result.pdfimage = list()
        result.pdf_raw = ''

    return result


class Digikey:
    def get_details(self, model: str, brand: str):
        return Db.query(digikeydetails.Details).filter(digikeydetails.Details.model == model).filter(digikeydetails.Details.brand == brand).first()


class Mouser:
    def get_details(self, model: str, brand: str):
        return Db.query(mouserdetails.Details).filter(mouserdetails.Details.model == model).filter(mouserdetails.Details.brand == brand).first()
