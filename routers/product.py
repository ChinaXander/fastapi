"""
@Time           :2022/6/8
@author         :XDS
@Description    :
"""
from fastapi import APIRouter, Depends
import tools
from data import crud

router = APIRouter(prefix="/product")


@router.get("/details/{model}")
def get_details(details: dict = Depends(crud.get_product_details)):
    return tools.res_data(details)
