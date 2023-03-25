from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from models.querier import StorageLayoutAdd
from utils.utils_slither import (
    getStorageLayout,
    getVariableInfo,
    getStorageSlot,
    getSlotValue,
)

router = APIRouter()

# Pydantic typing is left for routes


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


@router.post("/getVariable")
async def getVariable(
    contractAddress: str = Body(...),
    variableName: str = Body(...),
):
    try:
        # get storage layout for contract
        storageLayout = getStorageLayout(contractAddress)

        # get storage slot
        name, slot, size, offset, typeStr = getStorageSlot(
            contractAddress, variableName
        )

        # get slot value
        slotValue = getSlotValue(
            contractAddress=contractAddress,
            slot=slot,
            offset=offset,
            size=size,
            typeStr=typeStr,
        )

        return {
            "message": "Variable value fetched!",
            "variableName": variableName,
            "variableValue": slotValue,
            "variableType": typeStr,
        }
    except Exception as e:
        raise e
        return {"message": "Error: " + str(e)}


@router.post("/getSlot")
async def getSlot(
    contractAddress: str = Body(...),
    variableName: str = Body(...),
):

    # Directly fetch slot value from storage slot and return

    return  # TODO
