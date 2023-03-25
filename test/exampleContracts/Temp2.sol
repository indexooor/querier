// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract Temp2 {
    uint256 public val1;
    bool public bool1; 
    string public str1;

    mapping(address => uint256) public balances;

    struct Temp {
        string name;
        uint256 val;
    }
    Temp public temp;

    function set() public {
        val1 = 5;
        bool1 = true;
        str1 = "Indexooor rocks";
        balances[msg.sender] = val1;
        Temp memory _temp = Temp(str1, val1);
        temp = _temp;
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