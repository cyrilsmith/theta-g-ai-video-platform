// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "forge-std/Test.sol";
import "../src/VideoNFT.sol";

contract VideoNFTTest is Test {
    VideoNFT public videoNFT;

    function setUp() public {
        videoNFT = new VideoNFT();
    }

    function testMint() public {
        videoNFT.createNFT("ipfs://example-uri");
        assertEq(videoNFT.tokenCounter(), 1);
    }
}
