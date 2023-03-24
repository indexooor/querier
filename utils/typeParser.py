import re


class TypeParser:
    def __init__(self, type_string):
        self.type_string = type_string

        self.type_re = re.compile(r"^t_(\w+)")
        self.array_re = re.compile(r"^t_array\((.+)\)(\d*_storage)?")
        self.mapping_re = re.compile(r"^t_mapping\((.+),(.+)\)")
        self.struct_re = re.compile(r"^t_struct\((\w+)\)(\d*_storage)?")
        self.storage_re = re.compile(r".*_(storage)")

        self.parse_type()

    def parse_type(self):
        match = self.type_re.match(self.type_string)
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
            self.internal_type = TypeParser(self.internal_type)
            self.storage = match.group(2) or "Dynamic"
            if self.storage:
                self.size = None
            else:
                self.size = int(match.group(2).split("_")[0])
        else:
            match = self.mapping_re.match(self.type_string)
            if match:
                self.type = "Mapping"
                self.key_type = match.group(1)
                self.key_type = TypeParser(self.key_type)
                self.internal_type = match.group(2)
                self.internal_type = TypeParser(self.internal_type)
            else:
                match = self.struct_re.match(self.type_string)
                if match:
                    self.type = "Struct"
                    self.name = match.group(1)
                    self.storage = match.group(2) or "Dynamic"
                    if self.storage:
                        self.size = None
                    else:
                        self.size = int(match.group(2).split("_")[0])
                else:
                    self.internal_type = None

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
