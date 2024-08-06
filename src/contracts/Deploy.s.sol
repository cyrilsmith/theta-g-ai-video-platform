// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "src/contracts/VideoNFT.sol";
import "forge-std/Script.sol";

contract Deploy is Script {
    function run() external {
        address deployer = msg.sender;
        vm.startBroadcast();
        new VideoNFT(deployer);
        vm.stopBroadcast();
    }
}
