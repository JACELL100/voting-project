import json
import os
from web3 import Web3
from django.conf import settings

class BlockchainService:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(settings.WEB3_PROVIDER_URL))
        
        # Load contract data
        contract_path = os.path.join(os.path.dirname(__file__), '../contract.json')
        with open(contract_path, 'r') as f:
            contract_data = json.load(f)
            
        self.contract_address = contract_data['address']
        self.contract_abi = contract_data['abi']
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=self.contract_abi
        )
        
        # Get default account for transactions
        self.accounts = self.w3.eth.accounts
        self.default_account = self.accounts[0] if self.accounts else None
        
    def get_candidates(self):
        """Get all candidates from blockchain"""
        candidates = []
        candidates_count = self.contract.functions.candidatesCount().call()
        
        for i in range(1, candidates_count + 1):
            candidate_data = self.contract.functions.getCandidate(i).call()
            candidates.append({
                'id': candidate_data[0],
                'name': candidate_data[1],
                'vote_count': candidate_data[2]
            })
        return candidates
    
    def vote(self, candidate_id, voter_address=None):
        """Cast a vote for a candidate"""
        if not voter_address:
            voter_address = self.default_account
            
        try:
            # Build transaction
            transaction = self.contract.functions.vote(candidate_id).build_transaction({
                'from': voter_address,
                'gas': 100000,
                'gasPrice': self.w3.to_wei('20', 'gwei'),
                'nonce': self.w3.eth.get_transaction_count(voter_address),
            })
            
            # Sign and send transaction (for demo - in production use proper key management)
            # This assumes you have access to private keys for testing
            signed_txn = self.w3.eth.account.sign_transaction(transaction, private_key='0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80')  # Hardhat account #0
            tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
            
            # Wait for confirmation
            tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return {
                'success': True,
                'tx_hash': tx_hash.hex(),
                'block_number': tx_receipt.blockNumber
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def has_voted(self, address):
        """Check if address has already voted"""
        return self.contract.functions.hasVoted(address).call()

# Global instance
blockchain_service = BlockchainService()