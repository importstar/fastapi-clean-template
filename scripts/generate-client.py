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

    # openapi_json = "openapi.json"
    # res = httpx.get(url)
    # data = res.json()
    # data["components"]["securitySchemes"]["OAuth2PasswordBearer"]["flows"][
    #     "password"
    # ].pop("tokenUrl")

    # with open(openapi_json, "w") as f:
    #     json.dump(data, f)

    path = pathlib.Path("api-client")
    if not path.exists():
        print("Generate Clinet")
        create_new_client(
            # url=None,
            # path=pathlib.Path(openapi_json),
            url=url,
            path=None,
            meta=MetaType.POETRY,
            config=Config.load_from_path(pathlib.Path(config)),
        )
    else:
        print("Update Clinet")
        update_existing_client(
            # url=None,
            # path=pathlib.Path(openapi_json),
            url=url,
            path=None,
            meta=MetaType.POETRY,
            config=Config.load_from_path(pathlib.Path(config)),
        )

    # openapi_json_path = pathlib.Path(openapi_json)
    # openapi_json_path.unlink(missing_ok=False)


if __name__ == "__main__":
    generate_client()
