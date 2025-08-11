from django.db import models

class Vote(models.Model):
    voter_address = models.CharField(max_length=42)
    candidate_id = models.IntegerField()
    transaction_hash = models.CharField(max_length=66)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Vote for candidate {self.candidate_id} by {self.voter_address[:8]}..."

class Candidate(models.Model):
    blockchain_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name