// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Script.sol";
import "../src/VideoNFT.sol";

contract Deploy is Script {
    function run() external {
        vm.startBroadcast();
        new VideoNFT();
        vm.stopBroadcast();
    }
}
