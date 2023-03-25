from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
import json
from models.querier import StorageLayoutAdd, Querier
from models.api import ResponseModel, ErrorResponseModel
from utils.utils_slither import (
    getStorageLayout,
    getStorageSlot,
    getSlotValue,
)

router = APIRouter()

# Pydantic typing is left for routes


@router.get("/test", response_description="test route for querioor")
async def test():
    return {"message": "Welcome to Indexooor Querier Rest API!"}


# setStoageLayout end takes storage layout json as param and saves it as json on filesystem
@router.post(
    "/setStorageLayout",
    response_description="Set storage layout for contract address for which querier will fetch and decode data",
)
async def setStorageLayout(
    storageLayout: StorageLayoutAdd = Body(...),
):
    # save dictionary as json file with name contractAddress
    with open("./files/" + storageLayout.contractAddress + ".json", "w") as outfile:
        storageLayout.storageLayout["primaryClass"] = storageLayout.primaryClass
        json.dump(storageLayout.storageLayout, outfile)

    return ResponseModel(
        data=storageLayout.storageLayout,
        message="Storage layout added successfully!",
    )


@router.post(
    "/getVariable",
    response_description="Get variable value from indexed slot database (decoding it using type from storage layout)",
)
async def getVariable(
    data: Querier = Body(...),
):
    try:
        # get storage slot
        name, slot, size, offset, typeStr = getStorageSlot(
            data.contractAddress,
            data.targetVariable,
            key=data.key,
            deepKey=data.deepKey,
            structVar=data.structVar,
        )

        # get slot value
        slotValue = getSlotValue(
            contractAddress=data.contractAddress,
            slot=slot,
            offset=offset,
            size=size,
            typeStr=typeStr,
        )

        return ResponseModel(
            data={
                "variableName": data.targetVariable,
                "variableValue": slotValue,
                "variableType": typeStr,
            },
            message="Variable fetched successfully!",
        )
    except Exception as e:
        raise e

        return ErrorResponseModel(
            error=str(e),
            code=500,
            message="An error occurred",
        )


@router.post(
    "/getSlot", response_description="Get slot value from indexed slot database"
)
async def getSlot(
    contractAddress: str = Body(...),
    variableName: str = Body(...),
):

    # Directly fetch slot value from storage slot and return

    return  # TODO
