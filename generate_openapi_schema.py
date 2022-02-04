from fastapi.openapi.utils import get_openapi
from app.main import app
import json

file_path: str = "./swagger-ui/public/openapi.json"
with open(file_path, "w") as f:
    json.dump(
        get_openapi(
            title=app.title,
            version=app.version,
            openapi_version=app.openapi_version,
            routes=app.routes,
        ),
        f,
    )
