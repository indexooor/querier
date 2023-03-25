import re
import json


class TypeParser:
    def __init__(self, type_string):
        self.type_string = type_string

        self.type_re = re.compile(r"^t_(\w+)")
        self.array_re = re.compile(r"^t_array\((.+)\)(\d*_storage)?")
        self.mapping_re = re.compile(r"^t_mapping\((.+?),(.+)\)$")
        self.struct_re = re.compile(r"^t_struct\((\w+)\)(\d*_storage)?")
        self.storage_re = re.compile(r".*_(storage)")

        self.parse_type()

    def parse_type(self):
        match = self.type_re.match(self.type_string)
        self.size = None
        if match:
            self.type = match.group(1)
        else:
            raise ValueError(f"Invalid type string: {self.type_string}")

        match = self.storage_re.match(self.type_string)
        if match:
            self.storage = match.group(1)
        else:
            self.storage = "Dynamic"

        match = self.array_re.match(self.type_string)
        if match:
            self.type = "Array"
            self.internal_type = match.group(1)

            self.storage = match.group(2) or "Dynamic"

            if self.storage == "Dynamic":
                self.size = None
            else:
                self.size = int(match.group(2).split("_")[0])

            self.internal_type = TypeParser(self.internal_type)
        else:
            match = self.mapping_re.match(self.type_string)
            if match:
                self.type = "Mapping"
                self.key_type = match.group(1)
                self.key_type = TypeParser(self.key_type)
                self.internal_type = match.group(2)
                print("Internal type", self.internal_type)
                self.internal_type = TypeParser(self.internal_type)
            else:
                match = self.struct_re.match(self.type_string)
                if match:
                    self.type = "Struct"
                    self.name = match.group(1)
                    self.storage = match.group(2) or "Dynamic"
                    if self.storage == "Dynamic":
                        self.size = None
                    else:
                        self.size = int(match.group(2).split("_")[0])
                else:
                    self.internal_type = None
                    self.storage = None
                    self.size = None

    def __repr__(self):
        if self.type == "Array":
            if self.size:
                return f"{self.type}({self.internal_type}){self.size}_{self.storage}"
            else:
                return f"{self.type}({self.internal_type}){self.storage}"
        elif self.type == "Mapping":
            return f"{self.type}({self.key_type},{self.internal_type})"
        elif self.type == "Struct":
            if self.size:
                return f"{self.type}({self.name}){self.size}_{self.storage}"
            else:
                return f"{self.type}({self.name}){self.storage}"
        else:
            return self.type


if __name__ == "__main__":

    # read storage layout file
    # with open("storageLayout.Example.json") as f:
    #     storageLayout = json.load(f)
    #     for key, value in storageLayout["contracts"].items():
    #         try:
    #             for k, v in value["storage-layout"]["types"].items():
    #                 print(k)

    #                 t = TypeParser(k)
    #                 print(t)

    #                 print(t.storage)
    #                 print(t.size)
    #         except Exception as e:
    #             print(e)

    # t = TypeParser("t_mapping(t_string_memory_ptr,t_uint256)")

    # print(t)
    # print(t.internal_type)
    # print(t.storage)
    # print(t.key_type)

    t = TypeParser("t_mapping(t_address,t_mapping(t_address,t_uint256))")

    print(t)
    print(t.internal_type)
    print(t.storage)
    print(t.size)


# Prompt

# build a parse that can parse type of a variable, refer to this look up table
# t_address : (Type : address)
# t_array(t_address)10_storage: (Type: Array, Size: 10, Storage: Fixed, Internal Type: address)
# t_array(t_address)dyn_storage: (Type: Array, Storage: Dynamic, Internal Type: address)
# t_array(t_array(t_address)dyn_storage)dyn_storage: (Type: Array, Storage: Dynamic, Internal Type: (Type: Array, Storage: Dynamic, Internal Type: address))
# t_array(t_array(t_string_storage)dyn_storage)dyn_storage: (Type: Array, Storage Dynamic, Internal Type:(Type: Array, Storage: Dyanmic, Internal Type: string))
# t_array(t_array(t_struct(Hello)13_storage)dyn_storage)dyn_storage: (Type: Array, Storage: Dyanmic, Internal Type:(Type: Array, Storage:Dynamic, Internal Type: (Type: Struct, Storage: Fixes, Size: 13)))
# t_mapping(t_address,t_mapping(t_address,t_uint256)): (Type: Mapping, Key: address, Internal Type: (Type: Mapping, Key: address, Internal Type: uint256))
# t_mapping(t_address,t_uint256): (Type: Mapping, Key: address, Internal Type: uint256)
# t_mapping(t_uint256,t_struct(Hello)13_storage): (Type: Mapping, Key: uint256, Internal Type: (Type: Struct, Storage: Fixed, Size: 13))
# t_string_storage: (Type: String, Storage: Dyamic)
# t_struct(Hello)13_storage: (Type: Struct, Storage: Fixed, Size: 13)
# t_uint256: (Type: uint156)
# t_address: (Type: address)
# t_address: (Type: uint256)


# do not use a look up table as the look up table only has example create a generalized parser
