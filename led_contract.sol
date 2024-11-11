// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract LedControl {
    int8 private ledStatus; // 1 = LED an, 0 = LED aus
    address public owner;

    // Konstruktor, um den Besitzer des Contracts zu setzen
    constructor() payable {
        owner = msg.sender;
    }

    // Funktion zum Ein- und Ausschalten der LED
    // Erwartet: 1 für an, 0 für aus
    function setLed(int8 newOn) public payable {
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
