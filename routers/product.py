"""
@Time           :2022/6/8
@author         :XDS
@Description    :
"""
from fastapi import APIRouter, Depends

import tools
from data import crud

router = APIRouter(
    prefix="/product",
    dependencies=[Depends(tools.token_verify)],
    responses={400: {"description": "authentication failed"}}
)


@router.get("/details", responses={201: {"description": "product not find"}}, description='元器件匹配')
def get_details(details: dict = Depends(crud.get_product_details)):
    return tools.res_data(details)
