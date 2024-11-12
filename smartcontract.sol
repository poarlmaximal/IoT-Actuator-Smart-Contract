// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LedControl {
    int8 private ledStatus; // 1 = LED on, 0 = LED off
    address public owner;
    uint256 public fee; // Fee for setting the LED

/// here die constructo

  owner = msg.sender; // Set the deployer as the owner
        fee = _fee; // Set the fee for setting the LED

         // Function to set the LED status (write operation)
    function setLed(int8 newOn) public payable {
        require(msg.value >= fee, "Insufficient fee sent for setting LED");
        require(newOn == 0 || newOn == 1, "Invalid value for LED");
        ledStatus = newOn;
    }

    // Function to read the LED status (view operation)
    function readLed() public view returns (int8) {
        return ledStatus;
    }

    // Function to retrieve Ether by the owner
    function retrieveEther() public {
        require(msg.sender == owner, "Only the owner can call this function.");
        payable(owner).transfer(address(this).balance);
    }

    // Fallback function to receive Ether
    receive() external payable {}
}
    
