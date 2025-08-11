// SPDX-License-Identifier: MIT
pragma solidity ^0.8.19;

contract Voting {
    struct Candidate {
        uint id;
        string name;
        uint voteCount;
    }
    
    mapping(uint => Candidate) public candidates;
    mapping(address => bool) public voters;
    
    uint public candidatesCount;
    
    event VotedEvent(uint indexed candidateId);
    
    constructor() {
        addCandidate("Alice Johnson");
        addCandidate("Bob Smith");
        addCandidate("Carol Davis");
    }
    
    function addCandidate(string memory name) private {
        candidatesCount++;
        candidates[candidatesCount] = Candidate(candidatesCount, name, 0);
    }
    
    function vote(uint candidateId) public {
        require(!voters[msg.sender], "You have already voted");
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate");
        
        voters[msg.sender] = true;
        candidates[candidateId].voteCount++;
        
        emit VotedEvent(candidateId);
    }
    
    function getCandidate(uint candidateId) public view returns (uint, string memory, uint) {
        require(candidateId > 0 && candidateId <= candidatesCount, "Invalid candidate");
        Candidate memory candidate = candidates[candidateId];
        return (candidate.id, candidate.name, candidate.voteCount);
    }
    
    function hasVoted(address voter) public view returns (bool) {
        return voters[voter];
    }
}