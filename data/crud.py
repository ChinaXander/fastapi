"""
@Time           :2022/6/7
@author         :XDS
@Description    :
"""
import settings
import tools
from data.database import Db
import data.digikey.details as digikeydetails
import data.mouser.details as mouserdetails


def get_product_details(model: str):
    result = Digikey().get_details(model)
    print(result)
    if not result or not result.pdfpath:
        MouserData = Mouser().get_details(model)
        if MouserData.pdfpath:
            result = MouserData

    # 获取图片
    if result and result.pdfpath:
        pdfname = result.pdfpath.split('.')[0]
        result.pdf_image = tools.pdf_image(result.pdfpath, pdfname)
        result.pdf_raw = f"{settings.alioss['upload_url']}/{settings.alioss['image_prefix']}/{result.pdfpath}"
    else:
        result.pdfimage = list()

    return result


class Digikey:
    def get_details(self, model: str):
        return Db.query(digikeydetails.Details).filter(digikeydetails.Details.model == model).first()


class Mouser:
    def get_details(self, model: str):
        return Db.query(mouserdetails.Details).filter(mouserdetails.Details.model == model).first()
