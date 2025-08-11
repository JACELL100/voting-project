from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Vote, Candidate
from .blockchain import blockchain_service

def index(request):
    """Main voting page"""
    candidates = blockchain_service.get_candidates()
    
    # Sync with local database
    for candidate_data in candidates:
        Candidate.objects.get_or_create(
            blockchain_id=candidate_data['id'],
            defaults={'name': candidate_data['name']}
        )
    
    # Calculate progress width for progress bars
    max_votes = max([c['vote_count'] for c in candidates]) if candidates else 1
    for candidate in candidates:
        if max_votes == 0:
            candidate['progress_width'] = 0
        else:
            candidate['progress_width'] = (candidate['vote_count'] / max_votes) * 100
    
    context = {
        'candidates': candidates,
        'accounts': blockchain_service.accounts[:5],  # Show first 5 accounts for demo
    }
    return render(request, 'voting/index.html', context)

def vote(request):
    """Handle vote submission"""
    if request.method == 'POST':
        candidate_id = int(request.POST.get('candidate_id'))
        voter_address = request.POST.get('voter_address', blockchain_service.default_account)
        
        # Check if already voted
        if blockchain_service.has_voted(voter_address):
            messages.error(request, 'This address has already voted!')
            return redirect('index')
        
        # Cast vote
        result = blockchain_service.vote(candidate_id, voter_address)
        
        if result['success']:
            # Save to local database
            Vote.objects.create(
                voter_address=voter_address,
                candidate_id=candidate_id,
                transaction_hash=result['tx_hash']
            )
            messages.success(request, f'Vote cast successfully! Transaction: {result["tx_hash"][:10]}...')
        else:
            messages.error(request, f'Vote failed: {result["error"]}')
    
    return redirect('index')

def results(request):
    """Show voting results"""
    candidates = blockchain_service.get_candidates()
    return JsonResponse({'candidates': candidates})