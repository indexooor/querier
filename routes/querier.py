from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from models.querier import StorageLayoutAdd

router = APIRouter()


@router.get("/test")
async def test():
    return {"message": "Welcome to Indexooor Querier Rest API!"}


# setStoageLayout end takes storage layout json as param and saves it as json on filesystem
@router.post("/setStorageLayout")
async def setStorageLayout(
    storageLayout: StorageLayoutAdd = Body(...),
):
    # save dictionary as json file with name contractAddress
    with open("./files/" + storageLayout.contractAddress + ".json", "w") as outfile:
        storageLayout.storageLayout["primaryClass"] = storageLayout.primaryClass
        json.dump(storageLayout.storageLayout, outfile)

    return {"message": "Storage layout saved!"}
