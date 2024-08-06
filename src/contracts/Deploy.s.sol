// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./VideoNFT.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        new VideoNFT();
        vm.stopBroadcast();
    }
}
