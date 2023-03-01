from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

app = FastAPI()


def custom_openapi():
    # cache the generated schema
    if app.openapi_schema:
        return app.openapi_schema

    # custom settings
    openapi_schema = get_openapi(
        title="Zlab-Interview",
        version="0.1.1",
        description="This is a Simple API for Zlab bakend's interview",
        routes=app.routes,
    )
    # setting new logo to docs
    openapi_schema["info"]["x-logo"] = {
        "url": "https://dev.z-lab.ir/wp-content/themes/site/assets/build/src/img/zlab-logo.png"
    }

    app.openapi_schema = openapi_schema

    return app.openapi_schema


# assign the customized OpenAPI schema
app.openapi = custom_openapi


@app.get(
    "/",
    responses={
        200: {
            "content": {"image/png": {}},
            "description": "Return the JSON of greeting",
        }
    },
)
async def root():
    """
    This function only used to welcome users who use this api.
    """

    return {"message": "This is from Zlab"}


@app.get('/api/clone-repo/{url:path}')
async def cloneapi(url:str):
    return {'git repo':url}