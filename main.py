import uvicorn
from fastapi import FastAPI
from routers import product
from settings import start_run

app = FastAPI()

app.include_router(product.router)


@app.get("/")
async def root():
    return "TAOIC API 1.0"


# @app.get("/showImage/{path}", response_class=FileResponse)
# def show_image(path: str):
#     return config.images_dir + path


if __name__ == "__main__":
    uvicorn.run(app=start_run['app'], host=start_run['host'], port=start_run['port'], reload=start_run['reload'], debug=start_run['debug'])
