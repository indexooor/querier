import json
from utils.db_connector import db_connector
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
from utils.elementary_type import ElementaryTypeName, ElementaryType
from utils.typeParser import TypeParser
from eth_utils import keccak
from eth_utils import to_checksum_address, to_int, to_text, to_bytes
from eth_abi import decode, encode


class FetchObj:
    def __init__(self, contractAddress: str):
        self.contractAddress = contractAddress

    def getSlotData(self, slot: str) -> bytes:
        connection = db_connector()

        # pad enough 0s to hex slot to make an eth address

        hexString = hex(slot)[2:]
        hexString = "0" * (64 - len(hexString)) + hexString

        slot = "0x" + hexString

        cursor = connection.cursor()
        cursor.execute(
            "select * from indexooor where slot='{}' and contract='{}'".format(
                slot, self.contractAddress
            )
        )
        data = cursor.fetchall()

        if len(data) == 0:
            return None

        return bytes.fromhex(data[0][2].split("x")[1])

    def getDirectSlotData(self, slot: str) -> bytes:
        connection = db_connector()

        cursor = connection.cursor()
        cursor.execute(
            "select * from indexooor where slot='{}' and contract='{}'".format(
                slot, self.contractAddress
            )
        )
        data = cursor.fetchall()

        if len(data) == 0:
            return None

        return data[0][2].split("x")[1]


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
                size = int(i["storage-layout"]["types"][type_to]["numberOfBytes"]) * 8
                className = h.split(":")[1]

                return int_slot, size, offset, type_to, className


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
        internalSlitherType = ElementaryType(targetVariableType.internal_type.type)
        name = targetVariableType.internal_type.type.split("_")[0]
        size = internalSlitherType.size

    slot = int.to_bytes(slotInt, 32, byteorder="big")

    return (info, name, slot, size, offset, name)


def findMappingSlot(
    targetVariableType: TypeParser,
    slot: bytes,
    key: Union[int, str],
    deepKey: Union[int, str] = None,
    structVar: str = None,
):
    info = f"\nKey: {key}"
    offset = 0

    if key:
        info += f"\nKey: {key}"
    if deepKey:
        info += f"\nDeep Key: {deepKey}"

    assert targetVariableType.key_type.type in ElementaryTypeName

    key_type = targetVariableType.key_type.type.split("_")[0]

    if "int" in key_type:
        key = int(key)

    key = coerce_type(key_type, key)

    slot = keccak(encode([key_type, "uint256"], [key, decode(("uint256",), slot)[0]]))

    if targetVariableType.internal_type.type == "Struct":
        raise NotImplementedError

    elif targetVariableType.internal_type.type == "Mapping":

        assert deepKey

        assert targetVariableType.internal_type.key_type.type in ElementaryTypeName

        key_type = targetVariableType.internal_type.key_type.type.split("_")[0]

        if "int" in key_type:
            deepKey = int(deepKey)

        deepKey = coerce_type(key_type, deepKey)

        slot = keccak(encode([key_type, "bytes32"], [deepKey, slot]))

        typeTo = targetVariableType.internal_type.internal_type.type.split("_")[0]

        size = ElementaryType(typeTo).size

        offset = 0

        if targetVariableType.internal_type.internal_type.type == "Struct":
            raise NotImplementedError
        elif targetVariableType.internal_type.internal_type.type in ElementaryTypeName:
            pass
        else:
            raise NotImplementedError

        return info, typeTo, slot, size, offset, typeTo

    typeTo = targetVariableType.internal_type.type.split("_")[0]

    size = ElementaryType(typeTo).size

    offset = 0

    return info, typeTo, slot, size, offset, typeTo


def getStorageSlot(contractAddress: str, targetVariable: str, **kwargs: Any):

    storageLayout = getStorageLayout(contractAddress)

    key: Optional[int] = kwargs.get("key", None)
    deepKey: Optional[int] = kwargs.get("deepKey", None)
    structVar: Optional[str] = kwargs.get("structVar", None)

    varLogName: str = targetVariable

    finalType = None

    try:
        intSlot, size, offset, typeStr, className = getVariableInfo(
            storageLayout, varLogName
        )
    except Exception as e:
        raise ValueError("Variable not found")

    typeTo = TypeParser(typeStr)

    slot = int.to_bytes(intSlot, 32, byteorder="big")

    if typeTo.type.split("_")[0] in ElementaryTypeName:
        finalType = typeTo.type.split("_")[0]

    elif typeTo.type.split("_")[0] == "Array":
        _, _, slot, size, offset, finalType = findArraySlot(
            typeTo, slot, key, deepKey, structVar
        )

    elif typeTo.type.split("_")[0] == "Struct":
        raise NotImplementedError

    elif typeTo.type.split("_")[0] == "Mapping":
        _, _, slot, size, offset, finalType = findMappingSlot(
            typeTo, slot, key, deepKey, structVar
        )

    else:
        raise NotImplementedError

    intSlot = int.from_bytes(slot, byteorder="big")

    return varLogName, intSlot, size, offset, finalType


def getSlotValue(
    contractAddress: str,
    typeStr: str,
    slot: int,
    size: int,
    offset: int,
    value: Optional[Union[int, bool, str]] = None,
):
    fetchObj = FetchObj(contractAddress)
    #     # get bytes at a slot
    hex_bytes = fetchObj.getSlotData(slot)

    data = convertValueToType(hex_bytes, size, offset, typeStr)

    return data


def temp():
    connection = db_connector()

    cursor = connection.cursor()
    cursor.execute(
        "select * from indexooor where slot=%s && contract=%s",
        (
            "0xc0de027a52efca8d625712b39f648cf86940d46898ac8d8a2d323408c2b4cc51",
            "0x5f4eC3Df9cbd43714FE2740f5E3616155c5b8419",
        ),
    )
    data = cursor.fetchall()


def convertValueToType(hexBytes: bytes, size: int, offset: int, typeStr: str):

    offsetHexBytes = getOffsetValue(hexBytes, offset, size)

    try:
        value = coerce_type(typeStr, offsetHexBytes)
    except ValueError:
        return coerce_type("int256", offsetHexBytes)

    return value


def getOffsetValue(hex_bytes: bytes, offset: int, size: int) -> bytes:
    """
    Trims slot data to only contain the target variable's.
    Args:
        hex_bytes (HexBytes): String representation of type
        offset (int): The size (in bits) of other variables that share the same slot.
        size (int): The size (in bits) of the target variable.
    Returns:
        (bytes): The target variable's trimmed data.
    """
    size = int(size / 8)
    offset = int(offset / 8)
    if offset == 0:
        value = hex_bytes[-size:]
    else:
        start = size + offset
        value = hex_bytes[-start:-offset]
    return value


def coerce_type(
    solidity_type: str, value: Union[int, str, bytes]
) -> Union[int, bool, str]:
    """
    Converts input to the indicated type.
    Args:
        solidity_type (str): String representation of type.
        value (bytes): The value to be converted.
    Returns:
        (Union[int, bool, str, ChecksumAddress, hex]): The type representation of the value.
    """

    if "int" in solidity_type:
        return to_int(value)
    if "bool" in solidity_type:
        return bool(to_int(value))
    if "string" in solidity_type and isinstance(value, bytes):
        # length * 2 is stored in lower end bits
        # TODO handle bytes and strings greater than 32 bytes
        length = int(int.from_bytes(value[-2:], "big") / 2)
        return to_text(value[:length])

    if "address" in solidity_type:
        if not isinstance(value, (str, bytes)):
            raise TypeError
        return to_checksum_address(value)

    if not isinstance(value, bytes):
        raise TypeError
    return value.hex()


if __name__ == "__main__":
    # read  storage layout example as json
    with open("./files/0x1234567890123456789012345678901234567890.json") as json_file:
        storageLayout = json.load(json_file)

        print(storageLayout["primaryClass"])
    temp()
    print("Hello World!")
