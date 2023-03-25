from pydantic import BaseModel, Field
from typing import Union, Optional


class Querier(BaseModel):
    contractAddress: str = Field(...)
    targetVariable: str = Field(...)
    key: Optional[Union[int, str]]
    deepKey: Optional[Union[int, str]] = None
    structVar: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "contractAddress": "0x1234567890123456789012345678901234567890",
                "targetVariable": "_balances",
                "key": "0x1234567890123456789012345678901234567890",
                "deepKey": "0x1234567890123456789012345678901234567890",
                "structVar": "c",
            }
        }


class QuerySlot(BaseModel):
    contractAddress: str = Field(...)
    slot: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "contractAddress": "0xB0F3056D4f6F55cAA65610CF522DD3516E7D72BC",
                "slot": "0x0000000000000000000000000000000000000000000000000000000000000003",
            }
        }


class StorageLayoutAdd(BaseModel):
    contractAddress: str = Field(...)
    primaryClass: str = Field(...)
    storageLayout: dict = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "contractAddress": "0x1234567890123456789012345678901234567890",
                "primaryClass": "MockERC20",
                "storageLayout": {
                    "contracts": {
                        "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20": {
                            "storage-layout": {
                                "storage": [
                                    {
                                        "astId": 182,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_balances",
                                        "offset": 0,
                                        "slot": "0",
                                        "type": "t_mapping(t_address,t_uint256)",
                                    },
                                    {
                                        "astId": 188,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_allowances",
                                        "offset": 0,
                                        "slot": "1",
                                        "type": "t_mapping(t_address,t_mapping(t_address,t_uint256))",
                                    },
                                    {
                                        "astId": 190,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_totalSupply",
                                        "offset": 0,
                                        "slot": "2",
                                        "type": "t_uint256",
                                    },
                                    {
                                        "astId": 192,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_name",
                                        "offset": 0,
                                        "slot": "3",
                                        "type": "t_string_storage",
                                    },
                                    {
                                        "astId": 194,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_symbol",
                                        "offset": 0,
                                        "slot": "4",
                                        "type": "t_string_storage",
                                    },
                                    {
                                        "astId": 61,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_owner",
                                        "offset": 0,
                                        "slot": "5",
                                        "type": "t_address",
                                    },
                                    {
                                        "astId": 9,
                                        "contract": "/Users/kaush/AurtusCodes/pedalsup/Game-Planet/contracts/Mocks/MockERC20.sol:MockERC20",
                                        "label": "_owner",
                                        "offset": 0,
                                        "slot": "6",
                                        "type": "t_address",
                                    },
                                ],
                                "types": {
                                    "t_address": {
                                        "encoding": "inplace",
                                        "label": "address",
                                        "numberOfBytes": "20",
                                    },
                                    "t_mapping(t_address,t_mapping(t_address,t_uint256))": {
                                        "encoding": "mapping",
                                        "key": "t_address",
                                        "label": "mapping(address => mapping(address => uint256))",
                                        "numberOfBytes": "32",
                                        "value": "t_mapping(t_address,t_uint256)",
                                    },
                                    "t_mapping(t_address,t_uint256)": {
                                        "encoding": "mapping",
                                        "key": "t_address",
                                        "label": "mapping(address => uint256)",
                                        "numberOfBytes": "32",
                                        "value": "t_uint256",
                                    },
                                    "t_string_storage": {
                                        "encoding": "bytes",
                                        "label": "string",
                                        "numberOfBytes": "32",
                                    },
                                    "t_uint256": {
                                        "encoding": "inplace",
                                        "label": "uint256",
                                        "numberOfBytes": "32",
                                    },
                                },
                            }
                        },
                        "@openzeppelin/contracts/access/Ownable.sol:Ownable": {
                            "storage-layout": {
                                "storage": [
                                    {
                                        "astId": 61,
                                        "contract": "@openzeppelin/contracts/access/Ownable.sol:Ownable",
                                        "label": "_owner",
                                        "offset": 0,
                                        "slot": "0",
                                        "type": "t_address",
                                    }
                                ],
                                "types": {
                                    "t_address": {
                                        "encoding": "inplace",
                                        "label": "address",
                                        "numberOfBytes": "20",
                                    }
                                },
                            }
                        },
                        "@openzeppelin/contracts/token/ERC20/ERC20.sol:ERC20": {
                            "storage-layout": {
                                "storage": [
                                    {
                                        "astId": 182,
                                        "contract": "@openzeppelin/contracts/token/ERC20/ERC20.sol:ERC20",
                                        "label": "_balances",
                                        "offset": 0,
                                        "slot": "0",
                                        "type": "t_mapping(t_address,t_uint256)",
                                    },
                                    {
                                        "astId": 188,
                                        "contract": "@openzeppelin/contracts/token/ERC20/ERC20.sol:ERC20",
                                        "label": "_allowances",
                                        "offset": 0,
                                        "slot": "1",
                                        "type": "t_mapping(t_address,t_mapping(t_address,t_uint256))",
                                    },
                                    {
                                        "astId": 190,
                                        "contract": "@openzeppelin/contracts/token/ERC20/ERC20.sol:ERC20",
                                        "label": "_totalSupply",
                                        "offset": 0,
                                        "slot": "2",
                                        "type": "t_uint256",
                                    },
                                    {
                                        "astId": 192,
                                        "contract": "@openzeppelin/contracts/token/ERC20/ERC20.sol:ERC20",
                                        "label": "_name",
                                        "offset": 0,
                                        "slot": "3",
                                        "type": "t_string_storage",
                                    },
                                    {
                                        "astId": 194,
                                        "contract": "@openzeppelin/contracts/token/ERC20/ERC20.sol:ERC20",
                                        "label": "_symbol",
                                        "offset": 0,
                                        "slot": "4",
                                        "type": "t_string_storage",
                                    },
                                ],
                                "types": {
                                    "t_address": {
                                        "encoding": "inplace",
                                        "label": "address",
                                        "numberOfBytes": "20",
                                    },
                                    "t_mapping(t_address,t_mapping(t_address,t_uint256))": {
                                        "encoding": "mapping",
                                        "key": "t_address",
                                        "label": "mapping(address => mapping(address => uint256))",
                                        "numberOfBytes": "32",
                                        "value": "t_mapping(t_address,t_uint256)",
                                    },
                                    "t_mapping(t_address,t_uint256)": {
                                        "encoding": "mapping",
                                        "key": "t_address",
                                        "label": "mapping(address => uint256)",
                                        "numberOfBytes": "32",
                                        "value": "t_uint256",
                                    },
                                    "t_string_storage": {
                                        "encoding": "bytes",
                                        "label": "string",
                                        "numberOfBytes": "32",
                                    },
                                    "t_uint256": {
                                        "encoding": "inplace",
                                        "label": "uint256",
                                        "numberOfBytes": "32",
                                    },
                                },
                            }
                        },
                        "@openzeppelin/contracts/token/ERC20/IERC20.sol:IERC20": {
                            "storage-layout": {"storage": []}
                        },
                        "@openzeppelin/contracts/token/ERC20/extensions/IERC20Metadata.sol:IERC20Metadata": {
                            "storage-layout": {"storage": []}
                        },
                        "@openzeppelin/contracts/utils/Context.sol:Context": {
                            "storage-layout": {"storage": []}
                        },
                    },
                    "version": "0.8.17+commit.8df45f5f.Windows.msvc",
                },
            }
        }
