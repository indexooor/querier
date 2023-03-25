// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Temp3 {
    uint256 public val1;
    bool public bool1;
    string public str1;
    address addr1;

    mapping(address => uint256) public balances;
    mapping(address => mapping(address => uint256)) public balances2;

    uint256[] public arr;

    struct Temp {
        string name;
        uint256 val;
    }
    Temp public temp;

    function set() public {
        val1 = 5;
        bool1 = true;
        str1 = "Indexooor rocks";
        balances[0x0f3aac271357DdE397c6a59204Cf5FD2Ac7f78ea] = val1;
        balances2[0x0f3aac271357DdE397c6a59204Cf5FD2Ac7f78ea][
            0x0f3aac271357DdE397c6a59204Cf5FD2Ac7f78ea
        ] = val1;
        arr.push(1);
        arr.push(2);
        arr.push(3);
        arr.push(4);
        arr.push(5);
        Temp memory _temp = Temp(str1, val1);
        temp = _temp;

        addr1 = 0x0f3aac271357DdE397c6a59204Cf5FD2Ac7f78ea;
    }

    function set2() public {
        val1 = 10;
        bool1 = false;
        str1 = "Hello world";
        balances[msg.sender] = val1;
        Temp memory _temp = Temp(str1, val1);
        temp = _temp;
    }
}
