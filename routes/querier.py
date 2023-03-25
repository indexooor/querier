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

        # get variable info from storage layout
        int_slot, size, offset, type_to, className = getVariableInfo(
            storageLayout, variableName
        )

        # get storage slot
        slot = getStorageSlot(contractAddress, int_slot)

        # get slot value
        slotValue = getSlotValue(slot, offset, size)

        return {
            "message": "Variable value fetched!",
            "variableName": variableName,
            "variableValue": slotValue,
            "variableType": type_to,
            "className": className,
        }
    except Exception as e:
        return {"message": "Error: " + str(e)}


@router.post("/getSlot")
async def getSlot(
    contractAddress: str = Body(...),
    variableName: str = Body(...),
):

    # Directly fetch slot value from storage slot and return

    return  # TODO
