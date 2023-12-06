import pathlib
import os
import json

import httpx
from openapi_python_client.config import Config
from openapi_python_client import (
    update_existing_client,
    create_new_client,
    MetaType,
)


def generate_client(
    url="http://localhost:8080/openapi.json", config="scripts/client-config.yml"
):
    print("OpenAPI Client Generator")

    openapi_json = "openapi.json"
    res = httpx.get(url)
    data = res.json()
    data["openapi"] = "3.0.3"
    # data["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"][
    #     "password"
    # ].pop("tokenUrl")
    for component in data["components"]["schemas"]:
        properties = data["components"]["schemas"][component]["properties"]
        if "total" in properties:
            properties["total"] = {"type": "integer", "minimum": 0.0}

        if "page" in properties:
            properties["page"] = {"type": "integer", "minimum": 1.0}

        if "size" in properties:
            properties["size"] = {"type": "integer", "minimum": 1.0}

        if "pages" in properties:
            properties["pages"] = {"type": "integer", "minimum": 0.0}

    with open(openapi_json, "w") as f:
        json.dump(data, f)

    path = pathlib.Path("api-client")
    if not path.exists():
        print("Generate Clinet")
        errors = create_new_client(
            url=None,
            path=pathlib.Path(openapi_json),
            # url=url,
            # path=None,
            meta=MetaType.POETRY,
            config=Config.load_from_path(pathlib.Path(config)),
        )

    else:
        print("Update Clinet")
        errors = update_existing_client(
            url=None,
            path=pathlib.Path(openapi_json),
            # url=url,
            # path=None,
            meta=MetaType.POETRY,
            config=Config.load_from_path(pathlib.Path(config)),
        )

    for error in errors:
        print(error.detail)

    openapi_json_path = pathlib.Path(openapi_json)
    openapi_json_path.unlink(missing_ok=False)


if __name__ == "__main__":
    generate_client()
