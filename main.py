import uvicorn
from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)

from routers import product
from settings import start_run
from tools import res_data
from settings import doc

from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

app = FastAPI(title=doc['title'], docs_url=None, redoc_url=None)

app.include_router(product.router)

app.mount('/static', StaticFiles(directory='static'), name='static')


# 自定义httpException错误
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(res_data(None, exc.status_code, str(exc.detail)), status_code=exc.status_code)


@app.get("/", include_in_schema=False)
async def root():
    return "TAOIC API 1.0"


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        # title=app.title + " - Swagger UI",
        title=doc['title'],
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


# @app.get("/showImage/{path}", response_class=FileResponse)
# def show_image(path: str):
#     return config.images_dir + path


if __name__ == "__main__":
    uvicorn.run(app=start_run['app'], host=start_run['host'], port=start_run['port'], reload=start_run['reload'], debug=start_run['debug'])
