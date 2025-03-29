from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from .models import Sentence

# ---------- Authentication Views ----------
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect logged-in users
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect("login")

def signup_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Prevent signed-in users from signing up again

    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password1 = request.POST["password1"]
        password2 = request.POST["password2"]

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return render(request, "signup.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")

        User.objects.create_user(username=username, email=email, password=password1)
        messages.success(request, "Account created successfully. Please log in.")
        return redirect("login")

    return render(request, "signup.html")

@login_required
def home(request):
    sentences = Sentence.objects.all().order_by('-created_at')

    if request.method == 'POST':
        text = request.POST.get('text', '').strip()
        if text:
            sentiment = analyze_sentiment(text)  # Call your sentiment analysis function
            Sentence.objects.create(user=request.user, text=text, sentiment=sentiment, created_at=now())
        return redirect('home')

    return render(request, 'home.html', {'sentences': sentences})

def analyze_sentiment(text):
    """ Replace with actual sentiment analysis logic. """
    negative_words = ['angry', 'upset', 'bad', 'sad']
    positive_words = ['happy', 'good', 'great', 'joy']
    
    text_lower = text.lower()

    if any(word in text_lower.split() for word in negative_words):  # Ensuring exact word match
        return 'negative'
    elif any(word in text_lower.split() for word in positive_words):
        return 'positive'
    return 'neutral'
 