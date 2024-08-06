// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "src/contracts/VideoNFT.sol";

contract VideoNFTTest is Test {
    VideoNFT videoNFT;

    function setUp() public {
        address deployer = address(this);
        videoNFT = new VideoNFT(deployer);
    }

    function testMint() public {
        uint256 tokenId = videoNFT.createNFT("ipfs://test");
        assertEq(tokenId, 0);
        assertEq(videoNFT.tokenCounter(), 1);
    }
}
