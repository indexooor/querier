import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from utils.elementary_type_slither import ElementaryTypeName


def getStorageLayout(contractAddress: str) -> dict:
    # read  storage layout example as json
    with open("./files/" + contractAddress + ".json") as json_file:
        storageLayout = json.load(json_file)

        return storageLayout


def getTopLevelType(type_to: str) -> str:

    return type_to.split("_")[1].split("(")[0]


def getVariableInfo(
    storageLayout: dict, var_log_name: str
) -> Tuple[int, int, int, str]:
    for h, i in storageLayout["contracts"].items():
        layout = i["storage-layout"]["storage"]

        for var in layout:
            if var["label"] == var_log_name:
                int_slot = int(var["slot"])
                offset = int(var["offset"]) * 8
                type_to = var["type"]
                size = i["storage-layout"]["types"][type_to]["size"] * 8
                className = h.split(":")[1]
                return int_slot, size, offset, type_to, className

    return 0, 0, 0, "", ""


def findArraySlot(
    storageLayout: dict,
    typeName: str,
    key: int,
    deep_key: int = None,
    struct_var: str = None,
) -> Tuple[int, int, int, str]:
    offset = 0
    size = 256

    arrayType = ""
    typeStrInternal = typeName.split("(")[1].split(")")[0].split("_")[1]

    if typeStrInternal in ElementaryTypeName:
        arrayType = "elementary"
    if "array" in typeStrInternal:
        arrayType = "array"
    if "struct" in typeStrInternal:
        arrayType = "struct"

    if arrayType == "array":
        typeStrInternalInternal = (
            typeStrInternal.split("(")[1]
            .split(")")[0]
            .split("_")[1]
            .split("(")[1]
            .split(")")[0]
            .split("_")[1]
        )

        assert typeStrInternalInternal in ElementaryTypeName

        raise NotImplemented


def getStorageSlot(contractAddress: str, targetVariable: str, **kwargs: Any):

    storageLayout = getStorageLayout(contractAddress)

    key: Optional[int] = kwargs.get("key", None)
    deep_key: Optional[int] = kwargs.get("deep_key", None)
    struct_var: Optional[str] = kwargs.get("struct_var", None)

    var_log_name: str = targetVariable

    int_slot, size, offset, type_to, className = getVariableInfo(
        storageLayout, var_log_name
    )

    if type_to == "" and className == "":
        raise "Error"

    typeType = ""

    slot = int.to_bytes(int_slot, 32, byteorder="big")

    # find topLevel type
    if type_to.split("_")[1] in ElementaryTypeName:
        typeType = "elementary"
    elif "array" in type_to.split("_")[1]:
        typeType = "array"
    elif "struct" in type_to.split("_")[1]:
        typeType = "struct"
    elif "mapping" in type_to.split("_")[1]:
        typeType = "mapping"
    else:
        typeType = "unknown"


if __name__ == "__main__":
    # read  storage layout example as json
    with open("./files/0x1234567890123456789012345678901234567890.json") as json_file:
        storageLayout = json.load(json_file)

        print(storageLayout["primaryClass"])

    print("Hello World!")
