const { expect } = require("chai");
const { ethers } = require("hardhat");

describe("Voting", function () {
  let voting;
  let owner;
  let addr1;

  beforeEach(async function () {
    [owner, addr1] = await ethers.getSigners();
    const Voting = await ethers.getContractFactory("Voting");
    voting = await Voting.deploy();
    await voting.waitForDeployment();
  });

  it("Should initialize with 3 candidates", async function () {
    expect(await voting.candidatesCount()).to.equal(3);
  });

  it("Should allow voting", async function () {
    await voting.connect(addr1).vote(1);
    const candidate = await voting.getCandidate(1);
    expect(candidate[2]).to.equal(1); // vote count
  });

  it("Should prevent double voting", async function () {
    await voting.connect(addr1).vote(1);
    await expect(voting.connect(addr1).vote(2)).to.be.revertedWith("You have already voted");
  });
});