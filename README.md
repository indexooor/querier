# querier

querier service to query contract data indexed by indexooor core 😄


Setup

```
virtualenv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

run command

```

source venv/Scripts/activate
uvicorn main:app --reload --workers 1 --host 0.0.0.0 --port 5010

```


How to find storageLayout json for your contracts

```
solc contracts/Mocks/MockERC20.sol --base-path=/ --include-path=node_modules/ --combined-json storage-layout > storageLayout.json
```

## Querioor Features

| Features | Supported |
| --- | --- |
| Elementary Solidity Types | :heavy_check_mark: |
| Mappings with Elementary Types as Values | :heavy_check_mark: |
| Nested Mapping with Elementary Types as Final Key (up to 2 levels) | :heavy_check_mark: |
| Single Dimension Array of Elementary Types | :heavy_check_mark: |
| Complex Types (Structs) | :x: |
| Complex Types Inside Mappings and Arrays | :x: |
| Multidimensional Arrays | :x: |
| Other Types | :x: |

👍 Queriooor currently supports querying data with elementary Solidity types, mappings with elementary types as values, and nested mappings with elementary types as the final key (up to two levels). Additionally, it supports single dimension arrays of elementary types.

👎 However, Queriooor currently does not support complex types such as structs, complex types inside mappings and arrays, multidimensional arrays, and other types.
