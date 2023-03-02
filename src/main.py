import os
import subprocess
import re
from git import Repo
from fastapi import FastAPI ,HTTPException
from fastapi.openapi.utils import get_openapi

rw_dir = os.getcwd()
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
    proj_name = re.search("[^\/]+(?=\.git$)", url)[0]
    dest_dir = f"repo/{proj_name}"

    if not os.path.exists(dest_dir):
        try:
            repo = Repo.clone_from(url, dest_dir)
            subprocess.run(["docker", "build", "-t", proj_name, "."], cwd=os.path.join(rw_dir,dest_dir))
        except:
            raise HTTPException(status_code=400, detail="Error during cloning repository or starting container.")
    try:
        subprocess.run(["docker", "run", "-d", "-p", "5000:5000", proj_name], cwd=os.path.join(rw_dir,dest_dir))
        return {"message": "Successfully started container."}
    except:
        raise HTTPException(status_code=400, detail="Error during starting container.")