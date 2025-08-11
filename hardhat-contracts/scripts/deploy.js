const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  // Deploy the contract
  const Voting = await hre.ethers.getContractFactory("Voting");
  const voting = await Voting.deploy();
  
  await voting.waitForDeployment();
  
  const votingAddress = await voting.getAddress();
  console.log("Voting contract deployed to:", votingAddress);
  
  // Save contract address and ABI to file for Django
  const contractData = {
    address: votingAddress,
    abi: JSON.parse(voting.interface.formatJson())
  };
  
  const djangoDir = path.join(__dirname, "../../django-app");
  if (!fs.existsSync(djangoDir)) {
    fs.mkdirSync(djangoDir, { recursive: true });
  }
  
  fs.writeFileSync(
    path.join(djangoDir, "contract.json"),
    JSON.stringify(contractData, null, 2)
  );
  
  console.log("Contract data saved to django-app/contract.json");
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });