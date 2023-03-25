import json
import db_connector 
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from elementary_type_slither import ElementaryTypeName, ElementaryType
from typeParser import TypeParser
from eth_utils import keccak


class FetchObj:
    def getSlotData() -> bytes:
        pass


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
    typeTo: TypeParser,
    slot: bytes,
    key: int,
    deepKey: int = None,
    structVar: str = None,
) -> Tuple[int, int, int, str]:
    info = f"\nKey: {key}"
    offset = 0
    size = 256

    targetVariableType = typeTo

    if targetVariableType.internal_type.type == "Array":
        raise NotImplementedError
    elif targetVariableType.size != None:
        # Is a fixed size array
        slotInt = int.from_bytes(slot, byteorder="big") + int(key)

        if (
            targetVariableType.internal_type.type == "Struct"
            or targetVariableType.internal_type.type == "Array"
        ):
            raise NotImplementedError
        else:
            internalType = targetVariableType.internal_type.type
            internalSlitherType = ElementaryType(internalType)
            name = internalSlitherType.name
            size = internalSlitherType.size

    elif targetVariableType.internal_type.type == "Struct":
        raise NotImplementedError
    else:
        # is a dynamic array of elementary type
        assert targetVariableType.internal_type.type in ElementaryTypeName

        slot = keccak(slot)
        slotInt = int.from_bytes(slot, byteorder="big") + int(key)
        internalSlitherType = ElementaryType(targetVariableType.type)
        name = targetVariableType.type
        size = internalSlitherType.size

    slot = int.to_bytes(slotInt, 32, byteorder="big")

    return info, name, slot, size, offset


def getStorageSlot(contractAddress: str, targetVariable: str, **kwargs: Any):

    storageLayout = getStorageLayout(contractAddress)

    key: Optional[int] = kwargs.get("key", None)
    deepKey: Optional[int] = kwargs.get("deep_key", None)
    structVar: Optional[str] = kwargs.get("struct_var", None)

    varLogName: str = targetVariable

    intSlot, size, offset, typeStr, className = getVariableInfo(
        storageLayout, varLogName
    )

    if typeStr == "" and className == "":
        raise "Error"

    typeTo = TypeParser(typeStr)

    slot = int.to_bytes(intSlot, 32, byteorder="big")

    if typeTo.type.split("_")[0] in ElementaryTypeName:
        pass

    elif typeTo.type.split("_")[0] == "Array":
        info, name, slot, size, offset = findArraySlot(
            typeTo, slot, key, deepKey, structVar
        )

    elif typeTo.type.split("_")[0] == "Struct":
        raise NotImplementedError

    elif typeTo.type.split("_")[0] == "Mapping":
        raise NotImplementedError

    else:
        raise NotImplementedError

    intSlot = int.from_bytes(slot, byteorder="big")

    return name, intSlot, size, offset


# def getSlotValue(
#     fetchObj: FetchObj,
#     name: str,
#     slot: int,
#     size: int,
#     offset: int,
#     value: Optional[Union[int, bool, str, ChecksumAddress]] = None,
# ):

#     # cursor.execute("select * from ")
#     # get bytes at a slot
#     hex_bytes = fetchObj.getSlotData(slot)

def temp():
    connection = db_connector.db_connector()
    print(connection)
    cursor = connection.cursor()
    cursor.execute("select * from indexooor where slot=%s;",("0xc0de027a52efca8d625712b39f648cf86940d46898ac8d8a2d323408c2b4cc51",))
    data = cursor.fetchall()
    print(data)


    
if __name__ == "__main__":
    # read  storage layout example as json
    with open("./files/0x1234567890123456789012345678901234567890.json") as json_file:
        storageLayout = json.load(json_file)

        print(storageLayout["primaryClass"])
    temp()
    print("Hello World!")
