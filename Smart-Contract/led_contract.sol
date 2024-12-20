// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LedControl {
    int8 private ledStatus; // 1 = LED an, 0 = LED aus
    address public owner;
    uint256 public fee; // Fee for setting the LED

    // Konstruktor, um den Besitzer des Contracts zu setzen
    constructor(uint256 _fee) payable {
        owner = msg.sender;
        fee = _fee; // Set the fee for setting the LED
    }

    // Funktion zum Ein- und Ausschalten der LED
    // Erwartet: 1 für an, 0 für aus
    
    function setLed(int8 newOn) public payable {
    require(msg.value >= fee, "Insufficient fee sent for setting LED");
        require(newOn == 0 || newOn == 1, "Ungueltiger Wert fuer LED");
        ledStatus = newOn;
    }

    // Funktion zum Lesen des LED-Zustands
    function readLed() public view returns (int8) {
        return ledStatus;
    }

    // Funktion, um Ether durch den Besitzer zu extrahieren
    function retrieveEther() public payable onlyOwner {
        payable(owner).transfer(address(this).balance);
    }

    // Funktion zum "Entfernen" des Smart Contracts aus der Blockchain
    function kill() public onlyOwner {
        selfdestruct(payable(owner));
    }

    // Modifier, um sicherzustellen, dass nur der Besitzer Funktionen aufrufen kann
    modifier onlyOwner() {
        require(msg.sender == owner, "Nur der Besitzer kann diese Funktion aufrufen.");
        _;
    }

    // Fallback-Funktion, um Ether zu empfangen
    receive() external payable {}
}
