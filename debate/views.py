from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse, HttpResponse
from .models import Debate, Participant, Argument
from .forms import DebateForm
import google.generativeai as genai
from django.conf import settings
from django.db.models import Sum
from .decorators import custom_login_required  # Import the custom decorator

genai.configure(api_key=settings.GOOGLE_API_KEY)

def home(request):
    debates = Debate.objects.filter(is_active=True)
    return render(request, 'debate/home.html', {'debates': debates})

@custom_login_required
def create_debate(request):
    if request.method == 'POST':
        form = DebateForm(request.POST)
        if form.is_valid():
            debate = form.save(commit=False)
            debate.host = request.user
            debate.save()
            Participant.objects.create(user=request.user, debate=debate)
            return render(request, 'debate/debate_created.html', {'debate': debate})
    else:
        form = DebateForm()
    return render(request, 'debate/create_debate.html', {'form': form})

def join_debate(request, debate_id=None):
    if request.method == 'POST':
        print(f"POST data: {request.POST}")  # Debug
        code = request.POST.get('code')
        if code:
            try:
                debate = get_object_or_404(Debate, code=code, is_active=True)
                print(f"Found debate with code {code}: {debate.topic}")  # Debug
                # Store the debate ID in session and render name entry
                request.session['join_debate_id'] = debate.id
                return render(request, 'debate/join_debate.html', {'debate': debate})
            except Http404:
                return render(request, 'debate/join_debate.html', {'error': 'Invalid or inactive debate code.'})
        else:
            # Handle name and stance submission
            debate_id = request.session.get('join_debate_id')
            if debate_id:
                debate = get_object_or_404(Debate, id=debate_id, is_active=True)
                if request.user.is_authenticated:
                    participant, created = Participant.objects.get_or_create(user=request.user, debate=debate)
                    print(f"Authenticated user {request.user} joined as participant: {participant}")  # Debug
                else:
                    guest_name = request.POST.get('guest_name')
                    if not guest_name:
                        return render(request, 'debate/join_debate.html', {'debate': debate, 'error': 'Please enter a unique guest name.'})
                    # Check if guest_name already exists for this debate to avoid duplicates
                    participant, created = Participant.objects.get_or_create(debate=debate, guest_name=guest_name)
                    if not created:
                        return render(request, 'debate/join_debate.html', {'debate': debate, 'error': 'This guest name is already taken. Please choose another.'})
                    stance = request.POST.get('stance', 'for')
                    participant.stance = stance
                    participant.save()
                    # Store guest_name in session
                    request.session['guest_name'] = guest_name
                    print(f"Guest {guest_name} joined with stance {stance} as participant: {participant}")  # Debug
                # Clear join_debate_id from session
                if 'join_debate_id' in request.session:
                    del request.session['join_debate_id']
                return redirect('debate_room', debate_id=debate.id)
            else:
                return render(request, 'debate/join_debate.html', {'error': 'No debate session found.'})
    elif debate_id:
        debate = get_object_or_404(Debate, id=debate_id, is_active=True)
        return render(request, 'debate/join_debate.html', {'debate': debate})
    return render(request, 'debate/join_debate.html', {'error': 'Please enter a debate code.'})

def debate_room(request, debate_id):
    debate = get_object_or_404(Debate, id=debate_id, is_active=True)
    participant = None
    if request.user.is_authenticated:
        participant = Participant.objects.filter(user=request.user, debate=debate).first()
        print(f"Authenticated user {request.user} identified as participant: {participant}")  # Debug
    else:
        # Use the guest_name from session
        guest_name = request.session.get('guest_name')
        if guest_name:
            participant = Participant.objects.filter(guest_name=guest_name, debate=debate).first()
            print(f"Guest with name {guest_name} identified as participant: {participant}")  # Debug
        else:
            print("No guest_name found in session")  # Debug

    if not participant:
        print(f"No participant found for user or guest, redirecting to join debate_id={debate.id}")  # Debug
        return redirect('join_debate', debate_id=debate.id)

    arguments = Argument.objects.filter(participant__debate=debate).order_by('submitted_at')
    for_participants = debate.participants.filter(stance='for')
    against_participants = debate.participants.filter(stance='against')
    for_total = for_participants.aggregate(total=Sum('total_score'))['total'] or 0
    against_total = against_participants.aggregate(total=Sum('total_score'))['total'] or 0

    return render(request, 'debate/debate_room.html', {
        'debate': debate,
        'participant': participant,
        'arguments': arguments,
        'for_participants': for_participants,
        'against_participants': against_participants,
        'for_total': for_total,
        'against_total': against_total,
    })

@login_required
def debate_history(request):
    debates = Debate.objects.filter(host=request.user).order_by('-created_at')
    return render(request, 'debate/history.html', {'debates': debates})

@login_required
def close_debate(request, debate_id):
    debate = get_object_or_404(Debate, id=debate_id, host=request.user)
    if request.method == 'POST':
        debate.is_active = False
        # Calculate difference table
        for_team = debate.participants.filter(stance='for').aggregate(total=Sum('total_score'))['total'] or 0
        against_team = debate.participants.filter(stance='against').aggregate(total=Sum('total_score'))['total'] or 0
        debate.difference_table = {
            'for_total': for_team,
            'against_total': against_team,
            'difference': for_team - against_team
        }
        debate.save()
        winner = debate.participants.order_by('-total_score').first()
        return render(request, 'debate/results.html', {'debate': debate, 'winner': winner})
    return redirect('debate_room', debate_id=debate.id)

def submit_argument(request, debate_id):
    if request.method == 'POST':
        debate = get_object_or_404(Debate, id=debate_id, is_active=True)
        participant = None
        if request.user.is_authenticated:
            participant = Participant.objects.filter(user=request.user, debate=debate).first()
        else:
            guest_name = request.session.get('guest_name')
            if guest_name:
                participant = Participant.objects.filter(guest_name=guest_name, debate=debate).first()
        
        if not participant:
            return JsonResponse({'error': 'Not a participant'}, status=403)

        content = request.POST.get('content')
        if content:
            argument = Argument.objects.create(participant=participant, content=content)
            # Score with Google Generative AI
            model = genai.GenerativeModel('gemini-1.5-flash')
            prompt = f"Score this debate argument out of 100 based on clarity, relevance, and persuasiveness(Only give the integer 0-100 and nothing more.): '{content}'"
            response = model.generate_content(prompt)
            print(response)
            score = int(response.text.strip()) if response.text.strip().isdigit() else 50.0  # Fallback
            argument.score = min(max(score, 0), 100)  # Ensure score is 0-100
            print(argument.score)
            argument.save()
            participant.total_score += argument.score
            participant.save()
            return JsonResponse({'success': True, 'score': argument.score})
        return JsonResponse({'error': 'No content provided'}, status=400)
    return JsonResponse({'error': 'Invalid request'}, status=400)

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'debate/signup.html', {'form': form})

def clear_session(request):
    if request.method == 'POST':
        key = request.POST.get('key')
        if key in request.session:
            del request.session[key]
        return JsonResponse({'success': True})
    return JsonResponse({'error': 'Invalid request'}, status=400)
